# Gnar Gear: Gnarly Python Apps

[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gl/gnaar/gear/branch/master/graph/badge.svg?token=MRowdXaujg)](https://codecov.io/gl/gnaar/gear)
[![pipeline status](https://gitlab.com/gnaar/gear/badges/master/pipeline.svg)](https://gitlab.com/gnaar/gear/commits/master)
[![Python versions](https://img.shields.io/pypi/pyversions/gnar-gear.svg)](https://pypi.python.org/pypi/gnar-gear)
[![PyPI version](https://badge.fury.io/py/gnar-gear.svg)](https://badge.fury.io/py/gnar-gear)

**Part of Project Gnar:** &nbsp;[base](https://hub.docker.com/r/gnar/base) &nbsp;•&nbsp; [gear](https://pypi.org/project/gnar-gear) &nbsp;•&nbsp; [piste](https://gitlab.com/gnaar/piste) &nbsp;•&nbsp; [off-piste](https://gitlab.com/gnaar/off-piste) &nbsp;•&nbsp; [edge](https://www.npmjs.com/package/gnar-edge) &nbsp;•&nbsp; [powder](https://gitlab.com/gnaar/powder) &nbsp;•&nbsp; [genesis](https://gitlab.com/gnaar/genesis) &nbsp;•&nbsp; [patrol](https://gitlab.com/gnaar/patrol)

**Get started with Project Gnar on** &nbsp;[![Project Gnar on Medium](https://s3-us-west-2.amazonaws.com/project-gnar/medium-68x20.png)](https://medium.com/@ic3b3rg/project-gnar-d274165793b6)

**Join Project Gnar on** &nbsp;[![Project Gnar on Slack](https://s3-us-west-2.amazonaws.com/project-gnar/slack-69x20.png)](https://join.slack.com/t/project-gnar/shared_invite/enQtNDM1NzExNjY0NjkzLWQ3ZTQyYjgwMjkzNWYxNDJiNTQzODY0ODRiMmZiZjVkYzYyZWRkOWQzNjA0OTk3NWViNWM5YTZkMGJlOGIzOWE)

**Support Project Gnar on** &nbsp;[![Project Gnar on Patreon](https://s3-us-west-2.amazonaws.com/project-gnar/patreon-85x12.png)](https://patreon.com/project_gnar)

Gnar Gear sets up a powerful Flask-based Python service with two lines of code:

```python
from gnar_gear import GnarApp

...

GnarApp('my_gnarly_app', production=True, port=80).run()
```

## Installation

```bash
pip3 install gnar-gear
```

## Feature List

- Flask app with auto blueprint registration
- [Flask WSGI Development Server](http://flask.pocoo.org/docs/1.0/server)
- [Bjoern WSGI Production Server](https://github.com/jonashaag/bjoern)
  - Why Bjoern? Check out [these benchmarks!](https://blog.appdynamics.com/engineering/a-performance-analysis-of-python-wsgi-servers-part-2/)
  - And also [these benchmarks](https://github.com/kubeup/python-wsgi-benchmark)
- Postgres database connection via [Postgres.py](https://postgres-py.readthedocs.io/en/latest/#tutorial)
- SES client connection via [Boto 3](https://boto3.readthedocs.io/en/latest/)
- JWT configuration via [Flask-JWT-Extended](http://flask-jwt-extended.readthedocs.io/en/latest/)
- Peer requests - HTTP requests to other microservices in the app
- External requests - Convenience wrapper around [requests](http://docs.python-requests.org)
- SQS Message Polling and Sending
- [argon2_cffi.PasswordHasher](https://argon2-cffi.readthedocs.io) instance
  - `Argon2` was the winner of the [2015 Password Hashing Competition](https://password-hashing.net)
- Logger configuration
- Error handler with traceback
- Overridable and extendable class-based design

#### Development Mode

- Flask WSGI server in fault-tolerant debug (watch & reload) mode
  - The module loader logs the stack trace of any modules that fail to load
  - If a module fails to load, the app continues to watch for file changes
- CORS "disabled" (`Access-Control` response headers set), so you don't need to use other means to circumvent CORS

#### Production Mode

- Bjoern WSGI server
- CORS "enabled" (`Access-Control` response headers are not set)

## Requirements

### Bjoern

`Bjoern` requires `libev` (high performance event loop)
- Install `libev` with `brew install libev` on Mac, or find your platform-specific installation command [here](https://github.com/jonashaag/bjoern/wiki/Installation#libev)

### Application Structure

`GnarApp` expects to be instantiated in `main.py` at `<top-level-module>/app`, i.e. the minimum app folder structure is

```
+ <top-level-module>
    + app
        main.py
    __init__.py
```
It is recommended (not required) to place your apis in segregated folders under `app` and the tests in a `test` folder under the `<top-level-module>`, e.g.

```
+ <top-level-module>
    + app
        + admin
            apis.py
            constants.py
            services.py
        + user
            apis.py
            constants.py
            services.py
        __init__.py
        main.py
    + test
        constants.py
        test_app.py
    __init__.py
```

### Blueprints

Each [Flask `Blueprint`](http://flask.pocoo.org/docs/1.0/blueprints/) must be assigned to a global-level `blueprint` variable in its module, e.g.

```python
from flask import Blueprint, jsonify


api_name = 'user'
url_prefix = '/{}'.format(api_name)

blueprint = Blueprint(api_name, __name__, url_prefix=url_prefix)
^^^^^^^^^

@blueprint.route('/get', methods=['GET'])
def user_get():
    return jsonify({'status': 'ok'})
```

By default, the `GnarApp` picks up every `blueprint` in an auto-scan of the application code.

## Overview

The `GnarApp` class provides a highly configurable, feature-rich, production-ready Flask-based app.

### Parameters

#### Args (required)

- **name**: The name of the application's top-level module
- **production**: Boolean flag indicating whether or not the build is in production mode
- **port**: The port to bind to the WSGI server

#### Kwargs (optional)

- **env_prefix**: Environment variable prefix (defaults to `GNAR`)
- **log_level**: Log level override
  - see [configure_logger](#configure_logger) for log level overview
- **blueprint_modules**: List of modules to find Flask blueprints (default is auto-scan)
  - see [configure_blueprints](#configure_blueprints) for blueprints overview
- **sqs**: List (or single dict) of SQS queues to poll
  - see [configure_sqs_polls](#configure_sqs_polls) for SQS polling overview
- **no_db**: Boolean flag - specify `True` if the app does not need a Postgres connection
- **no_jwt**: Boolean flag - specify `True` if the app does not use JWT headers (i.e. non-api services)

### Overridable Behavior

`GnarApp.run` simply calls a set of steps in the class. Here is an example of how to override any of the steps:

```python
def postconfig():
    log.info('My Postconfig Step!')

ga = GnarApp('my_gnarly_app', production=True, port=80)
ga.postconfig = postconfig
ga.run()
```

### Run Steps
The run steps rely on a set of [environment variables](#environment-variables) which use a configurable prefix
(i.e. the `env_prefix` parameter). The default `env_prefix` is `GNAR`. An example of a Gnar environment variable
using a custom prefix is `GnarApp( ..., env_prefix='MY_APP')` and then instead of reading `GNAR_LOG_LEVEL`, the
`configure_logger` step will read `MY_APP_LOG_LEVEL`.

#### preconfig

- No default behavior - provided as an optional initial step in the app configuration.

#### configure_flask

- Attaches a `Flask` instance to the Gnar app.

#### configure_logger

- Attaches the root logger to `sys.stdout`.
- Sets the logging level to the first defined:
  - `log_level` parameter
  - `GNAR_<app name>_LOG_LEVEL` environment variable, e.g. `GNAR_MY_GNARLY_APP_LOG_LEVEL`
  - `GNAR_LOG_LEVEL` environment variable
  - `INFO`
  - Reminder: [Valid settings](https://docs.python.org/2/library/logging.html#logging-levels) (in increasing order of severity) are `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- Sets the log format to the first defined:
  - `GNAR_LOG_FORMAT`
  - `'%(asctime)s %(levelname)-8s %(name)s:%(lineno)d   %(message)s'`, e.g.:
  <pre>
  2018-07-09 15:41:46.420 INFO     gear.gnar_app:75   Logging at INFO
  </pre>
- Sets the log format `default_msec_format` to the first defined:
  - `GNAR_LOG_FORMAT_MSEC`
  - `'%s.%03d'` (e.g. `.001`)

#### configure_argon2

- Attaches an `argon2_cffi.PasswordHasher` instance to the Gnar app.
- Reads the following environment variables `[TYPE: DEFAULT]` to [pass into the Argon2 instance](https://argon2-cffi.readthedocs.io/en/stable/api.html):
  - `GNAR_ARGON2_TIME_COST`: `[INT: 2]` Number of iterations to perform
  - `GNAR_ARGON2_MEMORY_COST`: `[INT: 512]` Amount of memory (in KB) to use
  - `GNAR_ARGON2_PARALLELISM`: `[INT: 2]` Number of parallel threads (changes the resulting hash value)
  - `GNAR_ARGON2_HASH_LEN`: `[INT: 16]` Length of the hash in bytes
  - `GNAR_ARGON2_SALT_LEN`: `[INT: 16]` Length of random salt to be generated for each password in bytes
  - `GNAR_ARGON2_ENCODING`: `[STR: 'utf-8']` Encoding to use when a string is passed into `hash` or `verify`
- Note [from the docs](https://argon2-cffi.readthedocs.io/en/stable/parameters.html):
  > Only tweak these if you’ve determined using CLI that these defaults are too slow or too fast for your use case.
- To hash a password using `Argon2`:

  ```python
  from <top-level-module>.main import app
  hash = app.generate_password_hash(<plain text password>)
  # OR
  hash = app.argon2.hash(<plain text password>)
  ```

  Note that this creates a [randomly salted, memory-hard hash using the Argon2i algorithm](https://argon2-cffi.readthedocs.io/en/stable/parameters.html).
- To validate a password with `Argon2`:

  ```python
  from <top-level-module>.main import app
  is_valid = app.check_password_hash(<password hash from database>, <plain text password>)
  # OR
  is_valid = app.argon2.verify(<password hash from database>, <plain text password>)
  ```

  Note that `app.argon2.verify` [raises an exception](https://argon2-cffi.readthedocs.io/en/stable/faq.html) if the password is invalid whereas `app.check_password_hash` does not.

#### configure_database

- Creates a Postgres database connection and attaches it to the Gnar app
- Reads the following environment variables to set the `host`, `dbname`, `user`, `password` connection string parameters, respectively:
  - `GNAR_PG_ENDPOINT`
  - `GNAR_PG_DATABASE`
  - `GNAR_PG_USERNAME`
  - `GNAR_PG_PASSWORD`
- Note: The [Postgres API](https://postgres-py.readthedocs.io/en/latest/#tutorial) primarily consists of `run`, `one`, and `all`

#### attach_instance

- Attaches the `GnarApp` instance to the `app.main` module. This enables easy access to the Gnar app from anywhere in the application using

  ```python
  from <top-level-module>.main import app
  ```
- The `GnarApp`'s runtime assets are `db`, `argon2`, `flask`, `check_password_hash`, `generate_password_hash`, and `get_ses_client`
- For example, to fetch one result (or `None`) from the database:

  ```python
  app.db.one("SELECT * FROM foo WHERE bar='buz'")
  ```

#### configure_blueprints

- By default, `GnarApp` [auto-scans every Python module](#blueprints) under the `app` folder for blueprints.
- Each [Flask `Blueprint`](http://flask.pocoo.org/docs/1.0/blueprints/) must be assigned to a global-level `blueprint` variable in its module.
- If you prefer to skip the auto-scan, you can provide a list (or single string) of blueprint modules.
  - Each item in the list of module names may use one of two formats:
    - Without a `.` in the module name: `GnarApp` will look for the module in `<top-level-module>.app.<module name>.apis`
    - With a `.` in the module: `GnarApp` will look for the module in `<top-level-module>.app.<module name>`

#### configure_errorhandler

- Defines a generic (Exception-level) Flask error handler which:
  - Logs the error message and its `traceback` (format_exec)
  - Returns a 200-level json response containing `{"error": <error message>, "traceback": <traceback>}`

#### configure_jwt

- Sets the Flask `JWT_SECRET_KEY` variable to the value of the `GNAR_JWT_SECRET_KEY` environment variable.
- Sets the Flask `JWT_ACCESS_TOKEN_EXPIRES` variable to the value of the `GNAR_JWT_ACCESS_TOKEN_EXPIRES_MINUTES` environment variable (default 15 mins).
- Attaches a [JWTManager](http://flask-jwt-extended.readthedocs.io/en/latest/_modules/flask_jwt_extended/jwt_manager.html#JWTManager) instance to the `GnarApp`.
- Defines functions for `expired_token_loader`, `invalid_token_loader`, and `unauthorized_loader` which return meaningful error messages as 200-level json responses containing `{"error": <error message>}`.

#### configure_sqs_polls

- Configures a set of polls to run at specified intervals to receive messages from SQS queues.
- Specified via the `sqs` kwarg as a list of dicts (or a single dict) with a set of required (\*) and optional properties. See the [AWS ReceiveMessage docs](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_ReceiveMessage.html) for more details on the optional properties:
  - \* **queue_name**: The name of the SQS queue - the queue URL is retrieved from AWS with this name
  - \* **callback**: The function to call with each received message. The message will be deleted from the queue unless the callback function returns `False`.
  - **interval_seconds**: The interval (in seconds) between receive message requests - default 60
  - **attribute_names**: A list of attributes to return with each message
  - **max_number_of_messages**: The maximum number of messages to return with each request - 1 to 10, default 1
  - **message_attribute_names**: Metadata to include with the message - [more details](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-message-attributes.html)
  - **receive_request_attempt_id**: The token used for deduplication of ReceiveMessage calls (FIFO queues only)
  - **visibility_timeout**: The duration (in seconds) that the received messages are hidden from subsequent retrieve requests
  - **wait_time_seconds**: The duration (in seconds) for which the call waits for a message to arrive in the queue before returning
- Each message received by the callback includes the following properties. See the [AWS Message docs](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_Message.html) for more details on these properties:
    - **Body**: Message contents
    - **Attributes**: Map of requested attributes
    - **MD5OfBody**: MD5 Digest of the message body
    - **MD5OfMessageAttributes**: MD5 digest of the message attribute string
    - **MessageAttributes**: Map of custom message metadata
- Notes:
  - Messages are processed sequentially in the order they are received
  - The `callback` blocks message processing until it's complete
  - After all received messages are processed, the queue is immediately checked for new messages
  - Once the `receive_message` call returns no messages, a [`Timer`](https://docs.python.org/3.7/library/threading.html#timer-objects) with the specified `interval_seconds` starts the next loop
- Reads the following environment variables to set the `region_name`, `aws_access_key_id`, and `aws_secret_access_key` parameters of the `boto3.client` call, respectively:
  - `GNAR_SQS_REGION_NAME`
  - `GNAR_SQS_ACCESS_KEY_ID`
  - `GNAR_SQS_SECRET_ACCESS_KEY`
- Example:

  ```python
  def receive_sqs_message(message):
    redis_connection.set(message['MessageId'], message['Body'], 3600)

  sqs = {'queue_name': 'gnar-queue', 'callback': receive_sqs_message}
  GnarApp('piste', production, port, sqs=sqs).run()
  ```

#### configure_after_request

- Adds a JWT Authorization header (Bearer token) to responses which received a valid JWT token in the request.
- In development mode, adds CORS headers to the response (so that you don't need to bother circumventing CORS).

#### postconfig

- No default behavior - provided as an optional initial step in the app configuration.

### Runtime Functionality

#### peer

- Handles requests to other microservices in a Kubernetes app.
- Usage:

  ```python
  from <top-level-module>.main import app
  peer = app.peer(<< service name >>)
  ```

- Requires environment variables in the form:
  - production: `<< SERVICE >>_SERVICE_PORT`, e.g. `PISTE_SERVICE_PORT`
  - development: `GNAR_<< SERVICE >>_SERVICE_PORT`, e.g. `GNAR_PISTE_SERVICE_PORT`
- In production, the environment variable is automatically set by Kubernetes
- In development, the environment variable should point to another Gnar Gear app on localhost on a separate port
- The environment variable value must be in the form `<< ip address >>:<< port >>`, e.g.

  ```bash
  export GNAR_PISTE_SERVICE_PORT='127.0.0.1:9401'
  ```

##### peer Methods

- Each peer method accepts all the `kwargs` of the underlying `requests` method in addition to an `auto_auth` property.
  - If `auto_auth` is `True` and the current route is protected, an Authorization header is added to the request.
  - Both microservices must use the same `GNAR_JWT_SECRET_KEY` for the authorization to work.
- Uses [requests](http://docs.python-requests.org/en/master/api/#main-interface) under the hood:
  - [**request**](http://docs.python-requests.org/en/master/api/#requests.request)(method, path, \*\*kwargs): Constructs and sends a request
  - [**head**](http://docs.python-requests.org/en/master/api/#requests.head)(path, \*\*kwargs): Sends a HEAD request
  - [**get**](http://docs.python-requests.org/en/master/api/#requests.get)(path, params=None, \*\*kwargs): Sends a GET request
  - [**post**](http://docs.python-requests.org/en/master/api/#requests.post)(path, data=None, json=None, \*\*kwargs): Sends a POST request
  - [**put**](http://docs.python-requests.org/en/master/api/#requests.put)(path, data=None, \*\*kwargs): Sends a PUT request
  - [**patch**](http://docs.python-requests.org/en/master/api/#requests.patch)(path, data=None, \*\*kwargs): Sends a PATCH request
  - [**delete**](http://docs.python-requests.org/en/master/api/#requests.delete)(path, \*\*kwargs): Sends a DELETE request
- Example:

  ```python
  from <top-level-module>.main import app
  response = app.peer('piste').post('login', {'email': 'ic3b3rg@gmail.com'})
  ```

#### external

- Convenience wrapper around [requests](http://docs.python-requests.org)
- Example:

  ```python
  from <top-level-module>.main import app
  response = app.external.get('https://api.pwnedpasswords.com/range/5ce7d')
  ```

#### generate_password_hash / check_password_hash

- Convenience wrappers for `app.argon2.hash` and `app.argon2.verify`
- Usage:

  ```python
  from <top-level-module>.main import app
  hash = app.generate_password_hash(<plain text password>)
  is_valid = app.check_password_hash(<password hash from database>, <plain text password>)
  ```

#### get_ses_client

- Exposed as runtime functionality (as opposed to creating the client at initialization) because AWS will close the client after a short period of time
- Returns an SES connection (using boto3)
- Reads the following environment variables to set the `region_name`, `aws_access_key_id`, and `aws_secret_access_key` parameters of the `boto3.client` call, respectively:
  - `GNAR_SES_REGION_NAME`
  - `GNAR_SES_ACCESS_KEY_ID`
  - `GNAR_SES_SECRET_ACCESS_KEY`
- Usage:

  ```python
  from <top-level-module>.main import app
  app.get_ses_client().send_email( ... )
  ```
- See the [`Boto 3 Docs`](https://boto3.readthedocs.io/en/latest/reference/services/ses.html#SES.Client.send_email) for the `send_email` request syntax.

#### send_sqs_message

- Sends a message to an SQS queue.
- Args (required):
  - **queue_name**: The name of the SQS queue - the queue URL is retrieved from AWS with this name
  - **message_body**: Message contents
- Kwargs (optional) - See the [AWS SendMessage docs](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SendMessage.html) for more details on these properties:
  - **delay_seconds**: The length of time, in seconds, for which to delay a specific message
  - **message_attributes**: Metadata to include with the message
  - **message_deduplication_id**: The token used for deduplication of sent messages (FIFO queues only)
  - **message_group_id**: The tag that specifies that a message belongs to a specific message group (FIFO queues only)
- Returns a dict with the following attributes:
  - **MessageId**: Unique message identifier
  - **MD5OfMessageAttributes**: MD5 digest of the message attribute string
  - **MD5OfMessageBody**: MD5 digest of the message body
  - **SequenceNumber**: Unique, non-consecutive, 128 bit string (FIFO queues only)
- Reads the following environment variables to set the `region_name`, `aws_access_key_id`, and `aws_secret_access_key` parameters of the `boto3.client` call, respectively:
  - `GNAR_SQS_REGION_NAME`
  - `GNAR_SQS_ACCESS_KEY_ID`
  - `GNAR_SQS_SECRET_ACCESS_KEY`
- Example:

  ```python
  from <top-level-module>.main import app
  message = app.send_sqs_message('gnar-queue', 'The gnarliest gear in the world 🤙')
  ```

### Environment Variables

- The environment variables (with configurable prefix) used by `GnarApp` are:
  - `GNAR_ARGON2_ENCODING`
  - `GNAR_ARGON2_HASH_LEN`
  - `GNAR_ARGON2_MEMORY_COST`
  - `GNAR_ARGON2_PARALLELISM`
  - `GNAR_ARGON2_SALT_LEN`
  - `GNAR_ARGON2_TIME_COST`
  - `GNAR_JWT_SECRET_KEY`
  - `GNAR_LOG_LEVEL`
  - `GNAR_PG_DATABASE`
  - `GNAR_PG_ENDPOINT`
  - `GNAR_PG_PASSWORD`
  - `GNAR_PG_USERNAME`
  - `GNAR_SES_ACCESS_KEY_ID`
  - `GNAR_SES_REGION_NAME`
  - `GNAR_SES_SECRET_ACCESS_KEY`
  - `GNAR_SQS_REGION_NAME`
  - `GNAR_SQS_ACCESS_KEY_ID`
  - `GNAR_SQS_SECRET_ACCESS_KEY`
- See the relevant sections above for details

---

<p><div align="center">Made with <img alt='Love' width='32' height='27' src='https://s3-us-west-2.amazonaws.com/project-gnar/heart-32x27.png'> by <a href='https://www.linkedin.com/in/briengivens'>Brien Givens</a></div></p>
