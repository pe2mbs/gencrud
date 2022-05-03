# Running an Angular application from Python and Flask

This is an example how to setup and run an Angular application from Python and Flask.


# General
This repository should be used as follows:

    # git init
    # git submodule add https://gitlab.pe2mbs.nl/python/webapp.git
    
    # ng new frontend
    # touch version.py

Contents of the `version.py`
```python    
version = '1.0.0'
author = 'Marc Bertens-Nguyen'
copyright = '2020 Copyright'
```

This project was based on many internet sources. Many thanks to all those authors that 
showed how to solve parts of the problem.

# Licence
Python and Flask serving Angular application.
Copyright (C) 2018-2021 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>

This library is free software; you can redistribute it and/or modify
it under the terms of the GNU Library General Public License GPL-2.0-only
as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


# Structure.
```
<project-root-folder>
+-  webapp2              this repro
    ...
    requirements.txt
    +-- requirements
        dev.txt
        prod.txt
+-- <application-api>
    __init__.py
    ...
+-- frontend
    (the angular source tree)
        (the angular project files)      

```


## Python.
Tested on the following versions on Linux: 
* Python 3.5.2 
* Python 3.6.9
* Python 3.8.0

Tested on the following versions on Version:
* Python 3.6.6


## Flask.
``` 
Flask==1.0.2              
Flask-Bcrypt==0.7.1                
Flask-Builder==0.9                   
Flask-Caching==1.4.0               
Flask-Cors==3.0.6                 
Flask-JWT-Extended==3.13.1                 
Flask-Migrate==2.2.1                 
Flask-CLI==0.4.05      
Click==7.0 
Flask-SQLAlchemy==2.3.2 
alembic==0.8.4
PyJWT==1.6.4
PyYAML==3.13
Werkzeug==0.14.1
pyyaml==5.3.1
```   

  
# Starting the web service. 
## Standard development modes.
```bash
# export FLASK_APP=webapp/autoapp.py
# export FLASK_DEBUG=1
# export FLASK_ENV=DEVELOPMENT 
# flask run
```


### Enhanched development modes.
```bash
# export FLASK_APP=webapp/autoapp.py
# export FLASK_APP_CONFIG=devconfig.yaml
# export FLASK_DEBUG=1
# export FLASK_ENV=DEVELOPMENT 
# flask serve dev
```


## Standard test modes.
```bash 
# export FLASK_APP=webapp/autoapp.py
# export FLASK_ENV=STAGING 
# flask run --no-reload --with-threads 
```


## Standard production modes.
```bash 
# export FLASK_APP=webapp/autoapp.py
# export FLASK_ENV=PRODUCTION 
# flask run --no-reload --with-threads 
```


## Enhanched production modes.
```bash 
# export FLASK_APP=webapp/autoapp.py
# export FLASK_APP_CONFIG=prodconfig.yaml
# export FLASK_ENV=PRODUCTION 
# flask serve prod 
```

# Flask CLI commands

**cli**                     Management script for the webapp application.

**cli clean**               Remove *.pyc and *.pyo files recursively starting at current...

**cli lint**                Lint and check code style with flake8 and isort.

**cli test**                Run the tests.

**cli urls**                Display all of the url matching routes for the project.

**cli db**                  Perform database migrations.

**cli db branches**         Show current branch points

**cli db current**          Display the current revision for each database.

**cli db downgrade**        Revert to a previous version

**cli db edit**             Edit a revision file

**cli db heads**            Show current available heads in the script directory

**cli db history**          List changeset scripts in chronological order.

**cli db init**             Creates a new migration repository.

**cli db merge**            Merge two revisions together, creating a new revision file

**cli db migrate**          Autogenerate a new revision file (Alias for 'revision...

**cli db revision**         Create a new revision file.

**cli db show**             Show the revision denoted by the given symbol.

**cli db stamp**            'stamp' the revision table with the given revision; don't run...

**cli db upgrade**          Upgrade to a later version

**cli dba**                 DBA backup / restore for the webapp application.

**cli dba backup**          Backup the database.

**cli dba export**          Export the database.

**cli dba inport**          Inport the database.

**cli dba loader**          Load the database.

**cli dba restore**         Restore the database.

**cli dba saver**           Load the database.

**cli run**                 Runs a development server.

**cli serve**               Serve commands

**cli serve dev**           Runs a development server.

**cli serve production**    Runs a production server.

**cli serve ssl**           Runs a SSL/TLS server.

**shell**                   Runs a shell in the app context.


# Using a single configuration file. 
A single configuration file holds all the information different environments, allthrough 
this is very compact and handidy, there is also `Using multiple configuration files.`    


## Configuratio file
The default configuration file is config.yml a different config file can be set  
with the FLASK_CFG environment variable.


## config.yml
A typical config file has four sections: COMMON, DEVELOPMENT, STAGING and PRODUCTION. 
The section COMMON is common to all sections that include '<<: *common' 

```
COMMON: &common
  SECRET_KEY:                     insecure
  SQLALCHEMY_TRACK_MODIFICATIONS: true
  HOST:                           localhost
  PORT:                           8000
  API_MODULE:                     conduit
  APP_PATH:                       .  # This directory
  ANGULAR_PATH:                   ./web/angular-realworld-example-app/dist
  BCRYPT_LOG_ROUNDS:              13
  DEBUG_TB_INTERCEPT_REDIRECTS:   false
  CACHE_TYPE:                     simple  # Can be "memcached", "redis", etc.
  SQLALCHEMY_TRACK_MODIFICATIONS: false
  JWT_AUTH_USERNAME_KEY:          email
  JWT_AUTH_HEADER_PREFIX:         Token
  JWT_HEADER_TYPE:                Token
  ALLOW_CORS_ORIGIN:              false
  CORS_ORIGIN_WHITELIST:          [
    'http://0.0.0.0:5000',
    'http://127.0.0.1:5000',
    'http://localhost:5000',
    'http://0.0.0.0:8000',
    'http://localhost:8000',
    'http://0.0.0.0:4200',
    'http://localhost:4200',
    'http://0.0.0.0:4000',
    'http://localhost:4000',
  ]
DEVELOPMENT: &development
  <<: *common
  DEBUG:                          true
  ENV:                            dev
  TESTING:                        true
  DATABASE:
    ENGINE:                       sqlite
    SCHEMA:                       dev.db
  SSL:
    CERTIFICATE:                  cert/dev.angular.crt
    KEYFILE:                      cert/dev.angular.key
  CACHE_TYPE:                     simple  # Can be "memcached", "redis", etc.
STAGING: &staging
  <<: *common
  SECRET_KEY:                     sortasecure
  ENV:                            stag
  DATABASE:
    ENGINE:                       postgresql
    USER:                         postgres
    PASSWD:                       password
    PASSWORD:                     staging_database
    HOST:                         localhost
    PORT:                         5432
  SSL:
    CERTIFICATE:                  cert/dev.angular.crt
    KEYFILE:                      cert/dev.angular.key
PRODUCTION: &production
  <<: *common
  SECRET_KEY:                     shouldbereallysecureatsomepoint
  ENV:                            prod
  DEBUG:                          false
  DATABASE:
    ENGINE:                       postgresql
    HOST:                         localhost
    PORT:                         5432
    SCHEMA:                       production
    USER:                         postgres
    PASSWORD:                     password
```


## config.json
A typical config file has four sections: COMMON, DEVELOPMENT, STAGING and PRODUCTION. 
The section COMMON is common to all sections that include "inport": "COMMON" 

```
{
  "COMMON":
  {
    "SECRET_KEY":                     "insecure",
    "HOST":                           "localhost",
    "PORT":                           8000,
    "APP_PATH":                       ".",
    "API_MODULE":                     "conduit",
    "PROJECT_PATH":                   ".",
    "ANGULAR_PATH":                   "./web/angular-realworld-example-app/dist",
    "BCRYPT_LOG_ROUNDS":              13,
    "DEBUG_TB_INTERCEPT_REDIRECTS":   false,
    "CACHE_TYPE":                     "simple",
    "SQLALCHEMY_TRACK_MODIFICATIONS": false,
    "JWT_AUTH_USERNAME_KEY":          "email",
    "JWT_AUTH_HEADER_PREFIX":         "Token",
    "JWT_HEADER_TYPE":                "Token",
    "JWT_EXPIRATION_DELTA":           "weeks=52",
    "ALLOW_CORS_ORIGIN":              false,
    "CORS_ORIGIN_WHITELIST": [
      "http://127.0.0.1:4000",
      "http://127.0.0.1:4200",
      "http://127.0.0.1:5000",
      "http://127.0.0.1:8000",
      "http://0.0.0.0:4000",
      "http://0.0.0.0:4200",
      "http://0.0.0.0:5000",
      "http://0.0.0.0:8000",
      "http://localhost:4000",
      "http://localhost:4200",
      "http://localhost:5000",
      "http://localhost:8000"
    ]
  },
  "DEVELOPMENT": {
    "inport": "COMMON",
    "DEBUG":                          true,
    "ENV":                            "dev",
    "TESTING":                        true,
    "DATABASE":
    {
      "ENGINE":                       "sqlite",
      "SCHEMA":                       "dev.db"
    },
    "SQLALCHEMY_TRACK_MODIFICATIONS": false,
    "SSL":
    {
      "CERTIFICATE":                  "cert/dev.angular.crt",
      "KEYFILE":                      "cert/dev.angular.key"
    },
    "ACCESS_TOKEN_EXPIRES":           "days=365"
  },
  "STAGING":
  {
    "inport": "COMMON",
    "SECRET_KEY":                     "sortasecure",
    "ENV":                            "staging",
    "DATABASE":
    {
      "ENGINE":                       "postgresql",
      "USER":                         "postgres",
      "PASSWD":                       "password",
      "SCHEMA":                       "staging",
      "HOST":                         "localhost",
      "PORT":                         5432
    },
    "SSL":
    {
      "CERTIFICATE":                  "cert/dev.angular.crt",
      "KEYFILE":                      "cert/dev.angular.key"
    }
  },
  "PRODUCTION":
  {
    "inport": "COMMON",
    "SECRET_KEY":                     "shouldbereallysecureatsomepoint",
    "ENV":                            "prod",
    "DEBUG":                          false,
    "DATABASE": {
      "ENGINE":                       "postgresql",
      "HOST":                         "localhost",
      "PORT":                         5432,
      "SCHEMA":                       "production",
      "USER":                         "postgres",
      "PASSWD":                       "password"
    },
    "SSL":
    {
      "CERTIFICATE":                  "cert/prod.angular.crt",
      "KEYFILE":                      "cert/prod.angular.key"
    }
  }
}
```


# Using multiple configuration files.
The multiple configuration use the `config` folder and within that folder, the folders 
`env` and `tsk`.
```
    config
        env
            ...
        tsk
            ...
```


## Master configuration 
In the folder `config` the master configuration, looks like the exmaple configuration below.
In basic the master configuration should contain the STAGED configuration.    


### config.conf
```
    SECRET_KEY:                     insecure
    SQLALCHEMY_TRACK_MODIFICATIONS: true
    HOST:                           localhost
    PORT:                           8000
    API_MODULE:                     conduit
    APP_PATH:                       .  # This directory
    ANGULAR_PATH:                   ./web/angular-realworld-example-app/dist
    BCRYPT_LOG_ROUNDS:              13
    DEBUG_TB_INTERCEPT_REDIRECTS:   false
    CACHE_TYPE:                     simple  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS: false
    JWT_AUTH_USERNAME_KEY:          email
    JWT_AUTH_HEADER_PREFIX:         Token
    JWT_HEADER_TYPE:                Token
    ALLOW_CORS_ORIGIN:              false
    CORS_ORIGIN_WHITELIST:          [
        'http://0.0.0.0:5000',
        'http://127.0.0.1:5000',
        'http://localhost:5000',
        'http://0.0.0.0:8000',
        'http://localhost:8000',
        'http://0.0.0.0:4200',
        'http://localhost:4200',
        'http://0.0.0.0:4000',
        'http://localhost:4000',
    ]
    LOGGING:                         !include config/log.config.yaml
    DATABASE:
        ENGINE:                       postgresql
        HOST:                         localhost
        PORT    :                     5432
        SCHEMA:                       production
        USER:                         postgres
        PASSWORD:                     password
```


## Custom configurations
Custom configuration files, do not replace the master configuration, but the keys override 
the master configuration, without changing the other keys in the master configuration.        
The filenames of custom configuration files must be in uppercase, where the extension of the 
filename is in lowercase (.conf).  


### Environment configuration 
Custom environment configurations are derived from the FLASK_ENV environment variable.
And are located in the folder `config/env`. Some standard custom configurations;

* DEVELOPMENT => `config/env/DEVELOPMENT.yaml`
The development configuration contains the standard development derivation.   
 
* STAGING     => `config/env/STAGING.yaml`
The should not any derivation for the STAGED environment, as the master contains the 
STANGED configuration. 

* PRODUCTION  => `config/env/PRODUCTION.yaml`
The shall contain the configuration for the production application.

#### Handle multiple developers configurations
Simply set the FLASK_ENV=<username> and define in the folder `config/env` a file
<username>.conf. 


### Task configuration
Custom task configurations are derived from the FLASK_TASK environment variable.
he default task is `webapp`, the tasks. And are located in the folder `config/tsk`.  
* WEBAPP      => `config/tsk/WEBAPP.yaml`


# Configuration keys
Both yaml and json files use the same configuration keys.


## ANGULAR_PATH
The configures the location of the angular web application. This may be 
a absolute or relative path.


## API_MODULE
This the the main modulename for the API for the angular web application.   


## APP_PATH
The root path of the application. This may be a absolute or relative 
path.


## CACHE_TYPE
Specifies which type of caching object to use. This is an import string 
that will be imported and instantiated. It is assumed that the import 
object is a function that will return a cache object that adheres to the 
werkzeug cache API.

For werkzeug.contrib.cache objects, you do not need to specify the 
entire import string, just one of the following names.

Built-in cache types:

* null:          NullCache (default)
* simple:        SimpleCache
* memcached:     MemcachedCache (pylibmc or memcache required)
* gaememcached:  GAEMemcachedCache
* redis:         RedisCache (Werkzeug 0.7 required)
* filesystem:    FileSystemCache
* saslmemcached: SASLMemcachedCache (pylibmc required)


## CACHE_NO_NULL_WARNING	
Silents the warning message when using cache type of ‘null’.


## CACHE_ARGS	
Optional list to unpack and pass during the cache class instantiation.


## CACHE_OPTIONS	
Optional dictionary to pass during the cache class instantiation.


## CACHE_DEFAULT_TIMEOUT	
The default timeout that is used if no timeout is specified. Unit of 
time is seconds.


## CACHE_THRESHOLD	
The maximum number of items the cache will store before it starts 
deleting some. Used only for SimpleCache and FileSystemCache


## CACHE_KEY_PREFIX	
A prefix that is added before all keys. This makes it possible to use 
the same memcached server for different apps. Used only for RedisCache, 
MemcachedCache and GAEMemcachedCache.


## CACHE_MEMCACHED_SERVERS	
A list or a tuple of server addresses. Used only for MemcachedCache


## CACHE_MEMCACHED_USERNAME	
Username for SASL authentication with memcached. 
Used only for SASLMemcachedCache


## CACHE_MEMCACHED_PASSWORD	
Password for SASL authentication with memcached. 
Used only for SASLMemcachedCache


## CACHE_REDIS_HOST	
A Redis server host. Used only for RedisCache.


## CACHE_REDIS_PORT	
A Redis server port. Default is 6379. Used only for RedisCache.


## CACHE_REDIS_PASSWORD	
A Redis password for server. Used only for RedisCache.


## CACHE_REDIS_DB	
A Redis db (zero-based number index). Default is 0. Used only for 
RedisCache.


## CACHE_DIR	
Directory to store cache. Used only for FileSystemCache.


## CACHE_REDIS_URL	
URL to connect to Redis server. Example redis://user:password@localhost:6379/2. 
Used only for RedisCache.


## SECRET_KEY
A secret key that will be used for securely signing the session cookie 
and can be used for any other security related needs by extensions or 
your application. It should be a long random string of bytes, although 
unicode is accepted too. For example, copy the output of this to your 
config:

python -c 'import os; print(os.urandom(16))'
b'_5#y2L"F4Q8z\n\xec]/'
Do not reveal the secret key when posting questions or committing code.

Default: None


## HOST
Sets the hostname or host IP address from where the web server is 
running. 
* localhost
* 127.0.0.1
* 0.0.0.0
* other hostname or IP address belonging to the host.  

For running in development mode or when runninng behind a reverse proxy
use 'localhost' or '127.0.0.1'.

This value sets the SERVER_NAME key of the configuration, do not use 
both.


## PORT
Sets the IP port number where the web server listens on. Default when 
omitted the value is 80.

This value append with HOST to set the SERVER_NAME key of the 
configuration, do not use both.


## BCRYPT_LOG_ROUNDS
Additionally a configuration value for BCRYPT_LOG_ROUNDS may be set in 
the configuration of the Flask app. If none is provided this will 
internally be assigned to 12. (This value is used in determining the 
complexity of the encryption, see bcrypt for more details.)

Prefferred value: 13


## BCRYPT_HASH_PREFIX
set the hash version using the BCRYPT_HASH_PREFIX field in the 
configuration of the Flask app. If not set, this will default to 2b. 
(See bcrypt for more details)


## BCRYPT_HANDLE_LONG_PASSWORDS
By default, the bcrypt algorithm has a maximum password length of 72 
bytes and ignores any bytes beyond that. A common workaround is to 
hash the given password using a cryptographic hash (such as sha256), 
take its hexdigest to prevent NULL byte problems, and hash the result 
with bcrypt. If the BCRYPT_HANDLE_LONG_PASSWORDS configuration value 
is set to True, the workaround described above will be enabled. 
Warning: do not enable this option on a project that is already using 
Flask-Bcrypt, or you will break password checking. Warning: if this 
option is enabled on an existing project, disabling it will break 
password checking.


## DEBUG_TB_ENABLED 
Enable the toolbar? app.debug.

Should be set to false or not set


## DEBUG_TB_HOSTS 
Whitelist of hosts to display toolbar any host.


## DEBUG_TB_INTERCEPT_REDIRECTS 
Should intercept redirects?
 
Should be set to false or not set.


## DEBUG_TB_PANELS 
List of module/class names of panels enable all built-in panels


## DEBUG_TB_PROFILER_ENABLED 
Enable the profiler on all requests False, user-enabled

Should be set to false or not set.


## DEBUG_TB_TEMPLATE_EDITOR_ENABLED 
Enable the template editor 

Should be set to false or not set.


## JWT_TOKEN_LOCATION
Where to look for a JWT when processing a request. The options are 
'headers', 'cookies', 'query_string', or 'json'. You can pass in a list 
to check more then one location, such as: ['headers', 'cookies']. 
Defaults to 'headers'


## JWT_SECRET_KEY	
The secret key needed for symmetric based signing algorithms, such as 
HS*. If this is not set, we use the flask SECRET_KEY value instead.


## JWT_PUBLIC_KEY	
The public key needed for asymmetric based signing algorithms, such as 
RS* or ES*. PEM format expected.


## JWT_PRIVATE_KEY	
The private key needed for asymmetric based signing algorithms, such as 
RS* or ES*. PEM format expected.


## JWT_HEADER_TYPE
What header to look for the JWT in a request. Defaults to 
'Authorization'

Token


## JWT_HEADER_NAME
What type of header the JWT is in. Defaults to 'Bearer'. This can be 
an empty string, in which case the header contains only the JWT (insead 
of something like HeaderName: Bearer <JWT>)


## JWT_IDENTITY_CLAIM	
Claim in the tokens that is used as source of identity. For 
interoperability, the JWT RFC recommends using 'sub'. Defaults to 
'identity' for legacy reasons.


## JWT_USER_CLAIMS	
Claim in the tokens that is used to store user claims. Defaults to 
'user_claims'.


## JWT_CLAIMS_IN_REFRESH_TOKEN	
If user claims should be included in refresh tokens. Defaults to False.


## JWT_ERROR_MESSAGE_KEY	
The key of the error message in a JSON error response when using the 
default error handlers. Defaults to 'msg'.


## JWT_QUERY_STRING_NAME	
What query paramater name to look for a JWT in a request. Defaults to 
'jwt'


## JWT_ALGORITHM	
Which algorithm to sign the JWT with. See here for the options. 
Defaults to 'HS256'.


## JWT_ACCESS_TOKEN_EXPIRES	
How long an access token should live before it expires. This takes a 
datetime.timedelta, and defaults to 15 minutes. Can be set to False 
to disable expiration.

Allowed labels with a value:
* days
* seconds
* microseconds
* milliseconds
* minutes
* hours
* weeks


## JWT_REFRESH_TOKEN_EXPIRES	
How long a refresh token should live before it expires. This takes a 
datetime.timedelta, and defaults to 30 days. Can be set to False to 
disable expiration.

Allowed labels with a value: 
* days
* seconds
* microseconds
* milliseconds
* minutes
* hours
* weeks


## JWT_IDENTITY_CLAIM	
Claim in the tokens that is used as source of identity. 
For interoperability, the JWT RFC recommends using 'sub'. 
Defaults to 'identity' for legacy reasons.


## JWT_USER_CLAIMS	
Claim in the tokens that is used to store user claims. 
Defaults to 'user_claims'.


## JWT_CLAIMS_IN_REFRESH_TOKEN	
If user claims should be included in refresh tokens. Defaults to False.


## JWT_ERROR_MESSAGE_KEY	
The key of the error message in a JSON error response when using the 
default error handlers. Defaults to 'msg'.


## JWT_DEFAULT_REALM	
The default realm. Defaults to Login Required


## JWT_AUTH_URL_RULE	
The authentication endpoint URL. Defaults to /auth.


## JWT_AUTH_ENDPOINT	
The authentication endpoint name. Defaults to jwt.


## JWT_AUTH_USERNAME_KEY	
The username key in the authentication request payload. Defaults to 
username.

Should be set to 'email'

## JWT_AUTH_PASSWORD_KEY	
The password key in the authentication request payload. Defaults to 
password.


## JWT_LEEWAY	
The amount of leeway given when decoding access tokens specified as an 
integer of seconds or a datetime.timedelta instance. Defaults to 
seconds=10.


## JWT_VERIFY	
Flag indicating if all tokens should be verified. Defaults to True. 
It is not recommended to change this value.


## JWT_AUTH_HEADER_PREFIX	
The Authorization header value prefix. Defaults to JWT as to not 
conflict with OAuth2 Bearer tokens. This is not a case sensitive 
value.

should be set to 'Token'


## JWT_VERIFY_EXPIRATION	
Flag indicating if all tokens should verify their expiration time. 
Defaults to True. It is not recommended to change this value.


## JWT_VERIFY_CLAIMS	
A list of claims to verify when decoding tokens. Defaults to 
[ ['signature', 'exp', 'nbf', 'iat'] ].


## JWT_REQUIRED_CLAIMS	
A list of claims that are required in a token to be considered valid. 
Defaults to [ [ 'exp', 'iat', 'nbf' ] ]


## JWT_ACCESS_COOKIE_NAME	
The name of the cookie that holds the access token. Defaults to 
access_token_cookie


## JWT_REFRESH_COOKIE_NAME	
The name of the cookie that holds the refresh token. Defaults to 
refresh_token_cookie


## JWT_ACCESS_COOKIE_PATH	
What path should be set for the access cookie. Defaults to '/', which 
will cause this access cookie to be sent in with every request. Should 
be modified for only the paths that need the access cookie


## JWT_REFRESH_COOKIE_PATH	
What path should be set for the refresh cookie. Defaults to '/', which 
will cause this refresh cookie to be sent in with every request. Should 
be modified for only the paths that need the refresh cookie


## JWT_COOKIE_SECURE	
If the secure flag should be set on your JWT cookies. This will only 
allow the cookies to be sent over https. Defaults to False, but in 
production this should likely be set to True.


## JWT_COOKIE_DOMAIN	
Value to use for cross domain cookies. Defaults to None which sets this 
cookie to only be readable by the domain that set it.


## JWT_SESSION_COOKIE	
If the cookies should be session cookies (deleted when the browser is 
closed) or persistent cookies (never expire). Defaults to True (session 
cookies).


## JWT_COOKIE_SAMESITE	
If the cookies should be sent in a cross-site browsing context. 
Defaults to None, which means cookies are always sent.


## JWT_COOKIE_CSRF_PROTECT	
Enable/disable CSRF protection when using cookies. Defaults to True.


## JWT_JSON_KEY	
Key to look for in the body of an application/json request. Defaults 
to 'access_token'


## JWT_REFRESH_JSON_KEY	
Key to look for the refresh token in an application/json request. 
Defaults to 'refresh_token'


## JWT_CSRF_METHODS	
The request types that will use CSRF protection. Defaults to [ [ 'POST', 
'PUT', 'PATCH', 'DELETE' ] ] 


## JWT_ACCESS_CSRF_HEADER_NAME	
Name of the header that should contain the CSRF double submit value 
for access tokens. Defaults to X-CSRF-TOKEN.


## JWT_REFRESH_CSRF_HEADER_NAME	
Name of the header that should contains the CSRF double submit value 
for refresh tokens. Defaults to X-CSRF-TOKEN.


## JWT_CSRF_IN_COOKIES	
If we should store the CSRF double submit value in another cookies when 
using set_access_cookies() and set_refresh_cookies(). Defaults to True. 
If this is False, you are responsible for getting the CSRF value to the 
callers (see: get_csrf_token(encoded_token)).


## JWT_ACCESS_CSRF_COOKIE_NAME	
Name of the CSRF access cookie. Defaults to 'csrf_access_token'. 
Only applicable if JWT_CSRF_IN_COOKIES is True


## JWT_REFRESH_CSRF_COOKIE_NAME	
Name of the CSRF refresh cookie. Defaults to 'csrf_refresh_token'. 
Only applicable if JWT_CSRF_IN_COOKIES is True


## JWT_ACCESS_CSRF_COOKIE_PATH	
Path for the CSRF access cookie. Defaults to '/'. Only applicable if 
JWT_CSRF_IN_COOKIES is True


## JWT_REFRESH_CSRF_COOKIE_PATH	
Path of the CSRF refresh cookie. Defaults to '/'. Only applicable if 
JWT_CSRF_IN_COOKIES is True


## JWT_BLACKLIST_ENABLED	
Enable/disable token revoking. Defaults to False


## JWT_BLACKLIST_TOKEN_CHECKS	
What token types to check against the blacklist. The options are 
'refresh' or 'access'. You can pass in a list to check more then one 
type. Defaults to ['access', 'refresh']. Only used if blacklisting is 
enabled.


## ALLOW_CORS_ORIGIN
To allow Cross-Origin Resource Sharing should be set to true otherwise 
false.

Default value: false


## CORS_ORIGIN_WHITELIST
When set to * any remote address is accepted, when a list of remote 
addresses is provided only those addresses are allowed.    

 
## DEBUG
Whether debug mode is enabled. When using flask run to start the 
development server, an interactive debugger will be shown for unhandled 
exceptions, and the server will be reloaded when code changes. 
The debug attribute maps to this config key. This is enabled when ENV 
is 'development' and is overridden by the FLASK_DEBUG environment 
variable. It may not behave as expected if set in code.

Do not enable debug mode when deploying in production.

Default: True if ENV is 'development', or False otherwise.


## ENV
What environment the app is running in. Flask and extensions may enable 
behaviors based on the environment, such as enabling debug mode. The env 
attribute maps to this config key. This is set by the FLASK_ENV 
environment variable and may not behave as expected if set in code.

Do not enable development when deploying in production.

Default: 'production'


## TESTING
Enable testing mode. Exceptions are propagated rather than handled by 
the the app’s error handlers. Extensions may also change their behavior 
to facilitate easier testing. You should enable this in your own tests.

Default: False

## SSL
This key ah two subkeys CERTIFICATE and KEYFILE. When those are set to 
valid files the web server shall use these to impose HTTPS.
When this is not present the web server imposes HTTP 


### CERTIFICATE
This is digital certificate file used for the web server. 


### KEYFILE
This is the private key file  used for the web server.
      

## PROPAGATE_EXCEPTIONS
Exceptions are re-raised rather than being handled by the app’s error 
handlers. If not set, this is implicitly true if TESTING or DEBUG is 
enabled.

Default: None


## PRESERVE_CONTEXT_ON_EXCEPTION
Don’t pop the request context when an exception occurs. If not set, 
this is true if DEBUG is true. This allows debuggers to introspect the 
request data on errors, and should normally not need to be set directly.

Default: None


## TRAP_HTTP_EXCEPTIONS
If there is no handler for an HTTPException-type exception, re-raise it 
to be handled by the interactive debugger instead of returning it as a 
simple error response.

Default: False


## TRAP_BAD_REQUEST_ERRORS
Trying to access a key that doesn’t exist from request dicts like args  
and form will return a 400 Bad Request error page. Enable this to treat  
the error as an unhandled exception instead so that you get the  
interactive debugger. This is a more specific version of 
TRAP_HTTP_EXCEPTIONS. If unset, it is enabled in debug mode.

Default: None
      
      
## SESSION_COOKIE_NAME
The name of the session cookie. Can be changed in case you already have 
a cookie with the same name.

Default: 'session'


## SESSION_COOKIE_DOMAIN
The domain match rule that the session cookie will be valid for. If not 
set, the cookie will be valid for all subdomains of SERVER_NAME. 
If False, the cookie’s domain will not be set.

Default: None


## SESSION_COOKIE_PATH
The path that the session cookie will be valid for. If not set, the 
cookie will be valid underneath APPLICATION_ROOT or / if that is not set.

Default: None


## SESSION_COOKIE_HTTPONLY
Browsers will not allow JavaScript access to cookies marked as “HTTP only” 
for security.

Default: True


## SESSION_COOKIE_SECURE
Browsers will only send cookies with requests over HTTPS if the cookie is 
marked “secure”. The application must be served over HTTPS for this to 
make sense.

Default: False


## SESSION_COOKIE_SAMESITE
Restrict how cookies are sent with requests from external sites. Can be 
set to 'Lax' (recommended) or 'Strict'. See Set-Cookie options.

Default: None


## PERMANENT_SESSION_LIFETIME
If session.permanent is true, the cookie’s expiration will be set this 
number of seconds in the future. Can either be a datetime.timedelta or 
an int.

Flask’s default cookie implementation validates that the cryptographic 
signature is not older than this value.

Default: timedelta(days=31) (2678400 seconds)

Allowed labels with a value: 
* days
* seconds
* microseconds
* milliseconds
* minutes
* hours
* weeks


## SESSION_REFRESH_EACH_REQUEST
Control whether the cookie is sent with every response when 
session.permanent is true. Sending the cookie every time (the default) 
can more reliably keep the session from expiring, but uses more 
bandwidth. Non-permanent sessions are not affected.

Default: True


## USE_X_SENDFILE
When serving files, set the X-Sendfile header instead of serving the 
data with Flask. Some web servers, such as Apache, recognize this and 
serve the data more efficiently. This only makes sense when using such 
a server.

Default: False


## SEND_FILE_MAX_AGE_DEFAULT
When serving files, set the cache control max age to this number of 
seconds. Can either be a datetime.timedelta or an int. Override this 
value on a per-file basis using get_send_file_max_age() on the 
application or blueprint.

Default: timedelta(hours=12) (43200 seconds)

Allowed labels with a value: 
* days
* seconds
* microseconds
* milliseconds
* minutes
* hours
* weeks


## SERVER_NAME
Inform the application what host and port it is bound to. Required for 
subdomain route matching support.

If set, will be used for the session cookie domain if SESSION_COOKIE_DOMAIN 
is not set. Modern web browsers will not allow setting cookies for 
domains without a dot. To use a domain locally, add any names that 
should route to the app to your hosts file.

127.0.0.1 localhost.dev

If set, url_for can generate external URLs with only an application 
context instead of a request context.

Default: None


## APPLICATION_ROOT
Inform the application what path it is mounted under by the 
application / web server.

Will be used for the session cookie path if SESSION_COOKIE_PATH is not 
set.

Default: '/'


## PREFERRED_URL_SCHEME
Use this scheme for generating external URLs when not in a request 
context.

Default: 'http'


## MAX_CONTENT_LENGTH
Don’t read more than this many bytes from the incoming request data. 
If not set and the request does not specify a CONTENT_LENGTH, no data 
will be read for security.

Default: None


## JSON_AS_ASCII
Serialize objects to ASCII-encoded JSON. If this is disabled, the JSON 
will be returned as a Unicode string, or encoded as UTF-8 by jsonify. 
This has security implications when rendering the JSON in to JavaScript 
in templates, and should typically remain enabled.

Default: True


## JSON_SORT_KEYS
Sort the keys of JSON objects alphabetically. This is useful for caching 
because it ensures the data is serialized the same way no matter what 
Python’s hash seed is. While not recommended, you can disable this for 
a possible performance improvement at the cost of caching.

Default: True


## JSONIFY_PRETTYPRINT_REGULAR
jsonify responses will be output with newlines, spaces, and indentation 
for easier reading by humans. Always enabled in debug mode.

Default: False


## JSONIFY_MIMETYPE
The mimetype of jsonify responses.

Default: 'application/json'

## TEMPLATES_AUTO_RELOAD
Reload templates when they are changed. If not set, it will be enabled 
in debug mode.

Default: None


## EXPLAIN_TEMPLATE_LOADING
Log debugging information tracing how a template file was loaded. This 
can be useful to figure out why a template was not loaded or the wrong 
file appears to be loaded.

Default: False


## MAX_COOKIE_SIZE
Warn if cookie headers are larger than this many bytes. Defaults to 4093. 
Larger cookies may be silently ignored by browsers. Set to 0 to disable 
the warning.


## DATABASE:
Contains at least the ENGINE and SCHEMA keys for the sqlite database.
When another database is used ENGINE, HOST, USER and SCHEMA are atleast 
present. Optional PORT and PASSWORD may be present.
  

### ENGINE
* postgresql
* postgresql+psycopg2   (same as postgresql)
* postgresql+pg8000
* mysql
* mysql+mysqldb         (same as mysql)
* mysql+mysqlconnector
* mysql+oursql
* oracle
* oracle+cx_oracle      (same as oracle)
* mssql
* mssql+pyodbc          (same as mssql)
* mssql+pymssql
* sqlite


### SCHEMA
This is the database schema name, or in case sqlite as engine the 
filename.


### HOST
The host dns or IP address to connect via TCP/IP connection to the SQL 
server.


### PORT
The port number to connect via TCP/IP connection to the SQL server.

### USER
The username to access the database.


### PASSWORD
The password to access the database.
      
      
## SQLALCHEMY_DATABASE_URI 
The database URI that should be used for the connection. Examples:

• sqlite:////tmp/test.db
• mysql://username:password@server/db

this should not be set, instead the DATABASE key and subkeys should be 
used. 

For a complete list of connection URIs head over to the SQLAlchemy 
documentation under (Supported Databases). This here shows some common 
connection strings. SQLAlchemy indicates the source of an Engine as a 
URI combined with optional keyword arguments to specify options for the 
Engine. The form of the URI is: 

    dialect+driver://username:password@host:port/database
    
Many of the parts in the string are optional. If no driver is specified 
the default one is selected (make sure to not include the + in that case).

Postgres:
    postgresql://scott:tiger@localhost/mydatabase

MySQL:
    mysql://scott:tiger@localhost/mydatabase

Oracle:
    oracle://scott:tiger@127.0.0.1:1521/sidname

SQLite (note that platform path conventions apply):
* Unix/Mac (note the four leading slashes)
    sqlite:////absolute/path/to/foo.db
* Windows (note 3 leading forward slashes and backslash escapes)
    sqlite:///C:\\absolute\\path\\to\\foo.db*
* Windows (alternative using raw string)
    sqlite:///C:\absolute\path\to\foo.db


## SQLALCHEMY_BINDS 
A dictionary that maps bind keys to SQLAlchemy connection URIs. For more 
information about binds see Multiple Databases with Binds.


## SQLALCHEMY_ECHO
If set to True SQLAlchemy will log all the statements issued to stderr 
which can be useful for debugging.


## SQLALCHEMY_RECORD_QUERIES
Can be used to explicitly disable or enable query recording. Query 
recording automatically happens in debug or testing mode. 
See get_debug_queries() for more information.


## SQLALCHEMY_NATIVE_UNICODE 
Can be used to explicitly disable native unicode support. This is 
required for some database adapters (like PostgreSQL on some Ubuntu 
versions) when used with improper database defaults that specify 
encoding-less databases.


## SQLALCHEMY_POOL_SIZE 
The size of the database pool. Defaults to the engine’s default 
(usually 5)


## SQLALCHEMY_POOL_TIMEOUT
Specifies the connection timeout in seconds for the pool.


## SQLALCHEMY_POOL_RECYCLE 
Number of seconds after which a connection is automatically recycled. 
This is required for MySQL, which removes connections after 8 hours 
idle by default. Note that Flask-SQLAlchemy automatically sets this to
2 hours if MySQL is used. Some backends may use a different default 
timeout value. For more information about timeouts see Timeouts.


## SQLALCHEMY_MAX_OVERFLOW 
Controls the number of connections that can be created after the pool 
reached its maximum size. When those additional connections are returned 
to the pool, they are disconnected and discarded.


## SQLALCHEMY_TRACK_MODIFICATIONS 
If set to True, Flask-SQLAlchemy will track modifications of objects 
and emit signals. The default is None, which enables tracking but issues
a warning that it will be disabled by default in the future. This 
requires extra memory and should be disabled if not needed.
      
Should be set to false for production environment.      
