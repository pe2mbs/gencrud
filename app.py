# -*- coding: utf-8 -*-
"""Main webapp application package."""
#
# Main webapp application package
# Copyright (C) 2018-2020 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>
#
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License GPL-2.0-only
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
import os
import sys
import yaml
import logging
import logging.config
import logging.handlers
import traceback
import importlib

from inspect import signature
from webapp2.version import version_no, date, author
import webapp2.api as API
from webapp2.common.log import loadLoggingFile, updateLogging, LoggerWriter, LOGGING_INFO
from webapp2.common.util import ResolveRootPath
from webapp2.common.jsonenc import WebAppJsonEncoder
from webapp2.common.angular import registerAngular
from webapp2.common.plugins import loadPlugins
from webapp2.extensions.register import registerExtensions
from webapp2.commands.register import registerCommands
from webapp2.extensions.flask import Flask
import webapp2.extensions.database              # noqa
import webapp2.extensions.marshmallow           # noqa
import webapp2.extensions.migrate               # noqa


# Try to load optional packages
try:
    import webapp2.extensions.stompmq

except ModuleNotFoundError:
    print( "webapp2.extensions.stompmq NOT loaded" )
    pass

try:
    import webapp2.extensions.jwt

except ModuleNotFoundError:
    print( "webapp2.extensions.jwt NOT loaded" )
    pass

try:
    import webapp2.extensions.cors

except ModuleNotFoundError:
    print( "webapp2.extensions.cors NOT loaded" )
    pass

try:
    import webapp2.extensions.cache

except ModuleNotFoundError:
    print( "webapp2.extensions.cache NOT loaded" )
    pass

try:
    import webapp2.extensions.bcrypt

except ModuleNotFoundError:
    print( "webapp2.extensions.bcrypt NOT loaded" )
    pass

try:
    import webapp2.extensions.websocket

except ModuleNotFoundError:
    print( "webapp2.extensions.websocket NOT loaded" )
    pass

try:
    from webapp2.extensions.mondash import dashboard

except Exception:
    print( "webapp2.monitoring.dashboard NOT loaded" )
    dashboard = None

__version__     = version_no
__date__        = date
__author__      = author


class NormalEndProcess( Exception ):
    pass


def createApp( root_path, config_file = None, module = None, full_start = True, verbose = False, logging_name = None, process_name = 'app' ):
    """An application factory, as explained here:
       http://flask.pocoo.org/docs/patterns/appfactories/.

        :param root_path:   The the root path of the application.
        :param config_file: The configuration file to be used, fully qualified path must be supplied.
        :param module:      The actual application module.

        :return:            The application object.
    """
    API.app = None
    saved_stderr = sys.stderr
    try:
        root_path = ResolveRootPath( root_path )
        print( "Starting Flask application, loading configuration." )
        API.app = Flask( __name__.split( '.' )[ 0 ],
                         static_url_path    = "",
                         root_path          = root_path,
                         static_folder      = root_path )

        try:
            # when no config_file is supplied check if the environment has an alternate
            # configuration
            if config_file is None and 'FLASK_APP_CONFIG' in os.environ:
                config_file = os.environ[ 'FLASK_APP_CONFIG' ]

            # Check if the config_file is set and exists
            if config_file is not None and os.path.isfile( config_file ):
                print( "Config file: {}".format( os.path.join( root_path, config_file ) ) )
                API.app.config.fromFile( os.path.join( root_path, config_file ) )

            # Is the config_file a folder ?
            elif config_file is not None and os.path.isdir( config_file ):
                print( "Config path: {}".format( config_file ) )
                API.app.config.fromFolder( config_file )

            # Normal loading of the configuration through the 'config' folder
            else:
                print( "Config path: {}".format( os.path.join( root_path, 'config' ) ) )
                API.app.config.fromFolder( os.path.join( root_path, 'config' ) )

        except Exception as exc:
            print( "Exception: {} during loading of the configuration".format( exc ),
                   file = sys.stderr )
            # Try to load configuration from know locations and files
            if config_file is None:
                current_dir = os.path.dirname( __file__ )
                for searchdir in [ os.path.join( current_dir, '..' ),
                                   current_dir ]:
                    for searchfile in[ 'config.yml', 'config.yaml', 'config.json', 'config.conf' ]:
                        print( os.path.abspath( os.path.join( searchdir, searchfile ) ) )
                        if os.path.isfile( os.path.abspath( os.path.join( searchdir, searchfile ) ) ):
                            config_file = os.path.abspath( os.path.join( searchdir, searchfile ) )
                            break

                    if config_file is not None:
                        break

            if config_file is None:
                print( "The config file is missing", file = sys.stderr )
                exit( -1 )

            print( "Config file: {}".format( os.path.join( root_path, config_file ) ) )
            API.app.config.fromFile( os.path.join( root_path, config_file ) )

        # Setup logging for the application
        if 'logging' in API.app.config:
            API.loggingInfo = API.app.config[ 'logging' ]

        elif 'LOGGING' in API.app.config:
            API.loggingInfo = API.app.config[ 'LOGGING' ]

        else:
            API.loggingInfo = LOGGING_INFO

        logArgs = {
            'pid': os.getpid(),
            'name': process_name
        }
        if isinstance( API.loggingInfo, str ):
            # filename
            API.loggingInfo = loadLoggingFile( root_path,
                                       API.loggingInfo,
                                       API.app.config[ 'LOGGING_FOLDER' ] if 'LOGGING_FOLDER' in API.app.config else None,
                                       verbose,
                                       **logArgs )

        elif isinstance( API.loggingInfo, dict ):
            API.loggingInfo = updateLogging( API.loggingInfo,
                                     API.app.config[ 'LOGGING_FOLDER' ] if 'LOGGING_FOLDER' in API.app.config else None,
                                     verbose,
                                     **logArgs )

        else:
            print( "The logging key in config file is invalid", file = sys.stderr )

        logging.config.dictConfig( API.loggingInfo )
        if logging_name is not None:
            API.app.logger  = logging.getLogger( logging_name )

        API.logger      = API.app.logger
        API.app.logger.warning( "Logging Flask application: {}".format( logging.getLevelName( API.app.logger.level ) ) )
        if os.environ.get( 'FLASK_DEGUG', 0 ) == 1:
            API.app.logger.info( "{}".format( yaml.dump( API.app.config.struct, default_flow_style = False ) ) )
        API.logger = API.app.logger
        sys.stderr = LoggerWriter( API.app.logger.warning )
        module = None
        API.logger.info( "Current process ID: {}".format( os.getpid() ) )
        sys.path.append( root_path )
        API.app.json_encoder = WebAppJsonEncoder
        registerExtensions( module )
        registerCommands()
        if not full_start:
            # Not starting the full application, therefore we do not load all the application modules.
            raise NormalEndProcess()

        loadPlugins( root_path )
        API.app.logger.info( "AngularPath : {}".format( API.app.config[ 'ANGULAR_PATH' ] ) )
        API.app.static_folder   = os.path.join( root_path, API.app.config[ 'ANGULAR_PATH' ] ) + "/"
        API.app.url_map.strict_slashes = False
        if module is None and 'API_MODULE' in API.app.config:
            API.app.logger.info("Loading module : {}".format( API.app.config[ 'API_MODULE' ] ) )
            # import testrun.main to import registerApi,registerExtensions,registerShellContext,registerCommands,registerErrorHandler
            module = importlib.import_module( API.app.config[ 'API_MODULE' ] + ".main" )

        API.app.logger.info("Application module : {}".format( module ) )
        registerAngular()
        if hasattr( module, 'registerApi' ):
            sig = signature( module.registerApi )
            if len( sig.parameters ) == 2:
                module.registerApi( API.app, API.db )

            else:
                module.registerApi()

        # Check for Flask_MonitoringDashboard
        if dashboard is None:
            raise NormalEndProcess()

        # Check for config attribute in main configuration
        if dashboard.config.init_from_config( API.app.config ):
            dashboard.bind( API.app )

    except NormalEndProcess:
        pass

    except Exception:
        # restore the STDERR, as we may have modified it.
        sys.stderr = saved_stderr
        if API.app:
            API.app.logger.error( traceback.format_exc() )

        else:
            print( traceback.format_exc(), file = sys.stderr )

        raise

    return API.app


def SetApiReferences( api ):
    """This is to copy the web application module, logger and database engine references to
    a custom api module where the main application can refer to.

    :param api:
    :return:
    """
    api.app     = API.app
    api.db      = API.app.db
    api.logger  = API.app.logger

    # TODO: This is at the wrong place, but now now it works
    API.C_TESTRUN_OBJECT = "testrunObject"
    return
