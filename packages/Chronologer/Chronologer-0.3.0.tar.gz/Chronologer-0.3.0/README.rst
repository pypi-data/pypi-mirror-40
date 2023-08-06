.. image:: https://img.shields.io/badge/dynamic/json.svg?url=https://api.bitbucket.org/2.0/repositories/saaj/chronologer/pipelines/?page=1%26pagelen=1%26sort=-created_on%26target.ref_name=backend&label=build&query=$.values[0].state.result.name&colorB=blue
   :target: https://bitbucket.org/saaj/chronologer/addon/pipelines/home
.. image:: https://codecov.io/bitbucket/saaj/chronologer/branch/backend/graph/badge.svg
   :target: https://codecov.io/bitbucket/saaj/chronologer/branch/backend
.. image:: https://badge.fury.io/py/Chronologer.svg
   :target: https://pypi.org/project/Chronologer/
.. image:: https://images.microbadger.com/badges/image/saaj/chronologer.svg
   :target: https://microbadger.com/images/saaj/chronologer

===========
Chronologer
===========

.. figure:: https://bitbucket.org/saaj/chronologer/raw/8b437413ac3ecf50a5f422394332b7d921ce6804/chronologer/static/resource/clui/image/logo/logo-alt240.png
   :alt: Chronologer

Chronologer is a counterpart of Python stdlib's logging ``HTTPHandler`` [1]_ and more.
It provides RESTful API for accepting Python logging HTTP POST requests and optional
UI for browsing and searching the logs. The idea is the same as for database backends
of logging software, like ``rsyslog-mysql`` [2]_.

UI features are described in the `frontend`_ branch and released as
``ChronologerUI`` [17]_ package.

.. contents::

Scope
=====
Chronologer is meant for small- and medium-sized logging workloads and audit logging.
Practically it's limited by its backend's write throughput and capacity. In case of
MySQL backend vertical scaling can suffice many types of applications.

Especially it's useful for microservice architecture where file logging is no longer
practical.

Installation
============
Chronologer is available as a Python package [3]_ and as a Docker image [4]_ (includes UI).
The former can be installed like ``pip install chronologer[server,mysql,ui]``. The latter
can be used like in the following ``docker-compose.yml`` for deployment with MySQL database.

::

    version: '2.1'
    services:
      web:
        image: saaj/chronologer
        environment:
          CHRONOLOGER_STORAGE_DSN: mysql://chronologer:pass@mysql/chronologer
        depends_on:
          mysql:
            condition: service_healthy
        ports:
          - 8080:8080

      mysql:
        image: mysql:5.7
        environment:
          MYSQL_DATABASE: chronologer
          MYSQL_USER: chronologer
          MYSQL_PASSWORD: pass
          MYSQL_ROOT_PASSWORD: pass
        healthcheck:
          test: mysqladmin ping --protocol=tcp --password=pass --silent
          interval: 5s
          retries: 4

It can be run like the following. The second line applies database migrations.

::

    docker-compose up -d
    docker-compose run --rm web python -m chronologer -e production migrate

Chronologer's configuration can be fine-tuned with several environment variables
defined in ``envconf`` [5]_. Default ``envconf`` can be overridden completely, see
``python -m chronologer --help``.

Logging handler
===============
The naive imperative logging configuration looks like:

.. sourcecode:: python

    import logging.handlers

    chrono = logging.handlers.HTTPHandler(
      'localhost:8080', '/api/v1/record', 'POST', credentials = ('logger', ''))
    handlers = [logging.StreamHandler(), chrono]
    logging.basicConfig(level = logging.DEBUG, handlers = handlers)

The same can be expressed declaratively:

.. sourcecode:: python

    import logging.config

    conf = {
      'version'                  : 1,
      'disable_existing_loggers' : False,
      'handlers'                 : {
        'console' : {
          'class' : 'logging.StreamHandler',
        },
        'http' : {
          'class'       : 'logging.handlers.HTTPHandler',
          'host'        : 'localhost:8080',
          'url'         : '/api/v1/record',
          'method'      : 'POST',
          'credentials' : ('logger', ''),
          'secure'      : False
        },
      },
      'root' : {
        'handlers' : ['console', 'http'],
        'level'    : 'DEBUG'
      }
    }
    logging.config.dictConfig(conf)

This configuration is called naive because the handler is blocking. It may work
in simple cases but generally it's discouraged because the network is not reliable [6]_.
Instead Python provides logging queueing in stdlib [7]_:

    Along with the ``QueueHandler`` class, ``QueueListener`` can be used to let handlers
    do their work on a separate thread from the one which does the logging. This is
    important in Web applications and also other service applications where threads
    servicing clients need to respond as quickly as possible, while any potentially
    slow operations (such as sending an email via ``SMTPHandler``) are done on a
    separate thread.

Here follows imperative configuration with memory queueing.

.. sourcecode:: python

    chrono = logging.handlers.HTTPHandler(
      'localhost:8080', '/api/v1/record', 'POST', credentials = ('logger', ''))
    q = queue.Queue(maxsize = 4096)
    qh = logging.handlers.QueueHandler(q)
    ql = logging.handlers.QueueListener(q, chrono)
    ql.start()
    handlers = [logging.StreamHandler(),  qh]
    logging.basicConfig(level = logging.DEBUG, handlers = handlers)

    # somewhere on shutdown
    ql.stop()

Because the queue listener's shutdown procedure is inconvenient this way and it's
hard to express declaratively, ``QueueProxyHandler`` is suggested.

.. sourcecode:: python

    import logging.handlers
    import logging.config


    class QueueProxyHandler(logging.handlers.QueueHandler):
      '''Queue handler which creates its own ``QueueListener`` to
      proxy log records via provided ``queue`` to ``target`` handler.'''

      _listener = None
      '''Queue listener'''


      def __init__(self, queue, target = logging.handlers.HTTPHandler, **kwargs):
        # user-supplied factory is not converted by default
        if isinstance(queue, logging.config.ConvertingDict):
          queue = queue.configurator.configure_custom(queue)

        super().__init__(queue)
        self._listener = logging.handlers.QueueListener(queue, target(**kwargs))
        self._listener.start()

      def close(self):
        super().close()
        self._listener.stop()

    conf = {
      'version'                  : 1,
      'disable_existing_loggers' : False,
      'handlers'                 : {
        'console' : {
          'class' : 'logging.StreamHandler',
        },
        'http' : {
          'class'       : 'somemodule.QueueProxyHandler',
          'queue'       : {'()': 'queue.Queue', 'maxsize': 4096},
          'host'        : 'localhost:8080',
          'url'         : '/api/v1/record',
          'method'      : 'POST',
          'credentials' : ('logger', ''),
          'secure'      : False
        },
      },
      'root' : {
        'handlers' : ['console', 'http'],
        'level'    : 'DEBUG'
      }
    }
    logging.config.dictConfig(conf)

.. warning::
   Always set reasonable ``maxsize`` for the underlying queue to avoid
   unbound memory growth. ``logging.handlers.QueueHandler`` uses
   non-blocking ``put_nowait`` to enqueue records and in case the queue
   is full, it raises and the exception is handled by
   ``logging.Handler.handleError``. Alternatively a file-based queue, for
   instance, ``pqueue`` [8]_, can used to allow more capacity in
   memory-restricted environments.

Client
======
For convenience reasons, the above is available as
``chronologer.client.QueueProxyHandler``.

In addition it has logger name prefixing and suffixing capability. ``prefix``
is passed to ``QueueProxyHandler`` on creation. It allows many applications
logging into the same Chronologer instance to have separate logger namespaces
(e.g. including ``aiohttp`` logging whose namespace is fixed).
``suffix`` is an extra attribute of ``LogRecord`` which allows to fine-tune
the logger namespace for easier search of the records.

.. sourcecode:: python

    import logging.config


    conf = {
      'version'                  : 1,
      'disable_existing_loggers' : False,
      'handlers'                 : {
        'console' : {
          'class' : 'logging.StreamHandler',
        },
        'http' : {
          'class'       : 'chronologer.client.QueueProxyHandler',
          'queue'       : {'()': 'queue.Queue', 'maxsize': 4096},
          'prefix'      : 'appname',
          'host'        : 'localhost:8080',
          'url'         : '/api/v1/record',
          'method'      : 'POST',
          'credentials' : ('logger', ''),
          'secure'      : False
        },
      },
      'root' : {
        'handlers' : ['console', 'http'],
        'level'    : 'DEBUG'
      }
    }
    logging.config.dictConfig(conf)

    logging.getLogger('some').info(
      'Chronologer!', extra = {'suffix': 'important.transfer'})

The ``LogRecord`` corresponding to the last line will have ``name`` equal to
``'appname.some.important.transfer'``. If ``name`` is modified the original is
saved as ``origname``.

JSON input support
==================
Besides ``application/x-www-form-urlencoded`` of  ``HTTPHandler`` Chronologer
supports ``application/json`` of the same structure. It also supports
``application/x-ndjson`` [19]_ for bulk ingestion.

JSON of arbitrary structure can ingested in the *raw mode*. In the mode
Chronologer will not classify input on logging ``meta``, ``data`` and ``error``
and will not insist on presence of Python ``logging``-specific keys.
For example, a file containing newline separated JSON entries can be sent to
Chronologer like::

  curl -H "content-type: application/x-ndjson" --user logger: \
    --data-binary @/path/to/some/file.ndjson localhost:8080/api/v1/record?raw=1

Record retention
================
When ``CHRONOLOGER_RETENTION_DAYS`` is set, daily, around midnight a background
thread will purge records older than given number of days.

Authentication
==============
Chronologer does not provide (neither intends to) a user management. The intent
is to delegate authentication. The credentials and roles used by the server can
be provided by the following environment variables:

* ``CHRONOLOGER_USERNAME``
* ``CHRONOLOGER_PASSWORD``
* ``CHRONOLOGER_ROLES`` ­– space separated role list (see below)

Alternatively a JSON file located by ``CHRONOLOGER_AUTHFILE`` of the following
structure can be used to authenticate multiple users::

    [
      {
        "username": "bob",
        "pbkdf2": "f57ef1e3e8f90cb367dedd44091f251b5b15c9c36ddd7923731fa7ee41cbaa82",
        "hashname": "sha256",
        "salt": "c0139cff",
        "iterations": 32,
        "roles": ["writer"]
      }, {
        "username": "obo",
        "pbkdf2": "ff680a9237549f698da5345119dec1ed314eb4fdefe59837d0724d747c3169089ae45...",
        "hashname": "sha384",
        "salt": "9230dbdd5a13f009",
        "iterations": 4096,
        "roles": ["basic-reader", "query-reader"]
      }
    ]

The value of ``pbkdf2`` and keys ``hashname``, ``salt``, ``iterations`` correspond to
Python ``hashlib.pbkdf2_hmac`` [21]_.

Authorisation
=============
Chronologer defines the following roles:

* ``basic-reader`` allows ``HEAD`` and ``GET`` to ``/api/v1/record``
* ``query-reader`` in combination with ``basic-reader`` allows the use
  ``query``, SQL expression, to (further) filter the records
* ``writer`` allows ``POST`` to ``/api/v1/record``

The UI (in case ``chronologerui`` is installed) is available to every
authenticated user.

API
===
By default Chronologer listens port 8080 and is protected by HTTP Basic
Authentication, username "logger" without password (see environment
variables to override these).

Chronologer provides *Record* resource.

Create record
-------------
======================== ===============================================
URL                      ``/api/v1/record``
------------------------ -----------------------------------------------
Method                   ``POST``
------------------------ -----------------------------------------------
Request content-type     ``application/x-www-form-urlencoded``,
                         ``application/json``, ``application/x-ndjson``
------------------------ -----------------------------------------------
Request body             Representation of ``logging.LogRecord``
------------------------ -----------------------------------------------
Response content-type    ``application/json``
------------------------ -----------------------------------------------
Response body            Representation of created ``model.Record``,
                         except for ``application/x-ndjson`` input
                         where only a list of insert record identifiers
                         is returned
------------------------ -----------------------------------------------
Successful response code ``201 Created``
======================== ===============================================

Optional *raw* mode, accepting arbitrary JSON documents, is supported by
passing ``raw=1`` into the query string.

``application/x-ndjson`` request body can produce ``207 Multi-Status``
response when a successful chunk is followed by a failed chunk,
say that contained malformed a JSON line. Multi-status body looks like:

::

  {
    "multistatus": [
      {"status": 201, "body": [1, 2, ...]},
      {"status": 400, "body": "Invalid JSON document on line 2012"},
    ]
  }

Retrieve record count
---------------------
======================== ===============================================
URL                      ``/api/v1/record``
------------------------ -----------------------------------------------
Method                   ``HEAD``
------------------------ -----------------------------------------------
Query string             Optional filtering fields (see details below):

                         * ``after`` – ISO8601 timestamp
                         * ``before`` – ISO8601 timestamp
                         * ``level`` – integer logging level
                         * ``name`` – logging record prefix(es)
                         * ``query`` – storage-specific expression
------------------------ -----------------------------------------------
Response headers         * ``X-Record-Count: 42``
------------------------ -----------------------------------------------
Successful response code ``200 OK``
======================== ===============================================

Retrieve record timeline
------------------------
======================== ===============================================
URL                      ``/api/v1/record``
------------------------ -----------------------------------------------
Method                   ``HEAD``
------------------------ -----------------------------------------------
Query string             Required fields:

                         * ``group`` – "day" or "hour"
                         * ``timezone`` – ``pytz``-compatible one

                         Optional filtering fields (see details below):

                         * ``after`` – ISO8601 timestamp
                         * ``before`` – ISO8601 timestamp
                         * ``level`` – integer logging level
                         * ``name`` – logging record prefix(es)
                         * ``query`` – storage-specific expression
------------------------ -----------------------------------------------
Response headers         * ``X-Record-Count: 90,236``
                         * ``X-Record-Group: 1360450800,1360537200``
------------------------ -----------------------------------------------
Successful response code ``200 OK``
======================== ===============================================

Retrieve record range
---------------------
======================== ===============================================
URL                      ``/api/v1/record``
------------------------ -----------------------------------------------
Method                   ``GET``
------------------------ -----------------------------------------------
Query string             Required fields:

                         * ``left`` – left offset in the result set
                         * ``right`` – right offset in the result set

                         Optional filtering fields (see details below):

                         * ``after`` – ISO8601 timestamp
                         * ``before`` – ISO8601 timestamp
                         * ``level`` – integer logging level
                         * ``name`` – logging record prefix(es)
                         * ``query`` – storage-specific expression
------------------------ -----------------------------------------------
Response content-type    ``application/json``
------------------------ -----------------------------------------------
Response body            ::

                           [
                             {
                               "name": "some.module",
                               "ts": "2018-05-10 16:36:53.377493+00:00",
                               "message": "Et quoniam eadem...",
                               "id": 177260,
                               "level": 20
                             },
                             ...
                           ]
------------------------ -----------------------------------------------
Successful response code ``200 OK``
======================== ===============================================

Retrieve record
---------------
======================== ===============================================
URL                      ``/api/v1/record/{id}``
------------------------ -----------------------------------------------
Method                   ``GET``
------------------------ -----------------------------------------------
Response content-type    ``application/json``
------------------------ -----------------------------------------------
Response body            ::

                           {
                             "name": "some.module",
                             "logrec": {
                               "data": {
                                 "foo": 387
                               },
                               "meta": {
                                 "process": 29406,
                                 "module": "some.module",
                                 "relativeCreated": 103.23762893676758,
                                 "msecs": 376.4379024505615,
                                 "pathname": "logtest.py",
                                 "msg": "Et quoniam eadem...",
                                 "stack_info": null,
                                 "processName": "MainProcess",
                                 "filename": "logtest.py",
                                 "thread": 140312867051264,
                                 "threadName": "MainThread",
                                 "lineno": 20,
                                 "funcName": "main",
                                 "args": null
                               }
                             },
                             "id": 177260,
                             "level": 20,
                             "message": "Et quoniam eadem...",
                             "ts": "2018-05-10 16:36:53.377493+00:00"
                           }

                         ``logrec`` has two nested dictionaries.
                         ``data`` has what was passed to ``extra`` [16]_
                         and ``meta`` has internal fields of
                         ``logging.LogRecord``.
------------------------ -----------------------------------------------
Successful response code ``200 OK``
======================== ===============================================

Error representation
--------------------
Errors for HTTP method requests that allow a response body are represented like::

  {
    "error" : {
      "type"    : "HTTPError",
      "message" : "Nothing matches the given URI"
    }
  }

Errors for HTTP method requests that don't allow a response body are represented in the headers:

* ``X-Error-Type: StorageQueryError``
* ``X-Error-Message: Make sure the query filter is a valid WHERE expression``

Filtering
=========
Filter fields have the following semantics:

* ``after`` – ISO8601 timestamp.
  The predicate is true for a record which was created after given timestamp.
* ``before`` – ISO8601 timestamp.
  The predicate is true for a record which was created before given timestamp.
* ``level`` – integer logging level.
  The predicate is true for a record whose severity level is greater or equal to given level.
* ``name`` – logging record prefix. Optionally can be a comma-separated list of prefixes.
  The predicate is true for a record whose logger name starts with any of given prefixes.
* ``query`` – storage-specific expression.
  See JSON path description below.

.. warning::
   Each user who has access to Chronologer with ``query-reader`` role effectively
   has full access to its database, because ``query`` expressions are put into the
   SQL queries directly as there's no intent to abstract native database query
   features.

MySQL
=====
Chronologer relies on a compressed InnoDB table which provides good compromise
between reliability, data modelling, search features, performance and size of
logging data. The data of logging records are written into ``logrec`` JSON
field (see the initial migration [9]_ and examples above).

Because currently there's immediate write to the table, it's recommended to
allow MySQL to batch writes by setting ``innodb_flush_log_at_trx_commit = 0``
[10]_. Disabling performance schema [11]_ by setting ``performance_schema = 0``
is also recommended, because it has significant overhead. Basic InnoDB settings
should be reasonably configured:

* ``innodb_buffer_pool_size`` [12]_
* ``innodb_log_buffer_size`` [13]_
* ``innodb_log_file_size`` [14]_

It is a good idea to have dedicated MySQL instance for Chronologer.

JSON path query
---------------
``query`` passes a storage-specific expression. Particularly, it's useful
to write post-filtering conditions for ``logrec`` JSON field using
JSONPath expressions and ``->`` operator [15]_. It may look like the following,
though arbitrary ``WHERE`` clause expressions are possible.

* ``"logrec->'$.data.foo' = 387 AND logrec->'$.meta.lineno' = 20"``
* ``"logrec->'$.meta.threadName' != 'MainThread'"``

Note that connection to MySQL works in ``ANSI_QUOTES`` mode [18]_, so ``"``
cannot be used to form string literals. ``'`` must be used instead.

SQLite
======
SQLite is supported for very simple, one-off or evaluation cases. Also it doesn't
support compression. ``JSON1`` extension [20]_ is required for JSON Path queries.

* ``"json_extract(logrec, '$.data.foo') = 387 AND json_extract(logrec, '$.meta.lineno') = 20"``
* ``"json_extract(logrec, '$.meta.threadName') = 'MainThread'"``

A one-off Chronologer container with SQLite storage can be run on port 8080 like::

  docker run -d -p 8080:8080 --name chronologer -v /tmp \
    -e CHRONOLOGER_STORAGE_DSN=sqlite:////tmp/db.sqlite  saaj/chronologer
  docker exec chronologer python -m chronologer -e production migrate
  docker exec chronologer chown www-data:www-data /tmp/db.sqlite

Later, when the task is done, the container can be cleaned up like::

  docker rm -fv chronologer

R&D roadmap
===========
See the `roadmap`_ issue.

Credits
=======
Logo is contributed by `lightypaints`_.

____

.. _frontend: https://bitbucket.org/saaj/chronologer/src/frontend
.. _roadmap: https://bitbucket.org/saaj/chronologer/issues/1
.. _lightypaints: https://www.behance.net/lightypaints
.. [1]  https://docs.python.org/3/library/logging.handlers.html#httphandler
.. [2]  https://packages.debian.org/sid/rsyslog-mysql
.. [3]  https://pypi.org/project/Chronologer/
.. [4]  https://hub.docker.com/r/saaj/chronologer/
.. [5]  https://bitbucket.org/saaj/chronologer/src/backend/chronologer/envconf.py
.. [6]  https://en.wikipedia.org/wiki/Fallacies_of_distributed_computing
.. [7]  https://docs.python.org/3/library/logging.handlers.html#queuelistener
.. [8]  https://pypi.org/project/pqueue/
.. [9]  https://bitbucket.org/saaj/chronologer/src/backend/chronologer/migration/20171026T1428_initial.py
.. [10] https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_flush_log_at_trx_commit
.. [11] https://dev.mysql.com/doc/refman/5.7/en/performance-schema.html
.. [12] https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_buffer_pool_size
.. [13] https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_log_buffer_size
.. [14] https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_log_file_size
.. [15] https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-column-path
.. [16] https://docs.python.org/3/library/logging.html#logging.debug
.. [17] https://pypi.org/project/ChronologerUI/
.. [18] https://dev.mysql.com/doc/refman/5.7/en/sql-mode.html#sqlmode_ansi_quotes
.. [19] https://github.com/ndjson/ndjson-spec
.. [20] https://www.sqlite.org/json1.html
.. [21] https://docs.python.org/3/library/hashlib.html#hashlib.pbkdf2_hmac
