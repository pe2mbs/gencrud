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
import traceback
import importlib
from webapp.common.logger import loadLoggingFile, updateLogging
from webapp.extensions.register import registerExtensions
from webapp.common.angular import registerAngular
from webapp.commands.register import registerCommands
from webapp.common.exceptions import InvalidUsage
from webapp.extensions.flask import Flask
import webapp.api as API


def ResolveRootPath( path ):
    if path == '':
        path = os.path.abspath( os.path.join( os.path.dirname( __file__ ), '..' ) )

    elif path == '.':
        path = os.path.abspath( path )

    return path


def createApp( root_path, config_file = None, module = None, full_start = True, verbose = False ):
    """An application factory, as explained here:
       http://flask.pocoo.org/docs/patterns/appfactories/.

        :param root_path:   The the root path of the application.
        :param config_file: The configuration file to be used.
        :param module:       The actual application module.

        :return:            The application object.
    """
    API.app = None
    try:
        if 'FLASK_APP' not in os.environ:
            print( "Missing FLASK_APP environment variable", file = sys.stderr )
            exit( -1 )
        else:
            print( "FLASK_APP: {}".format( os.environ[ 'FLASK_APP' ] ) )

        if 'FLASK_ENV' not in os.environ:
            print( "Missing FLASK_ENV environment variable", file = sys.stderr )
            exit( -1 )
        else:
            print( "FLASK_ENV: {}".format( os.environ[ 'FLASK_ENV' ] ) )


        if config_file is None:
            if 'FLASK_APP_CONFIG' in os.environ:
                config_file = os.environ[ 'FLASK_APP_CONFIG' ]
                root_path, config_file = os.path.split( config_file )
                root_path = ResolveRootPath( root_path )

            else:
                config_file = 'config.yaml'
                root_path = ResolveRootPath( root_path )
                if not os.path.isfile( os.path.join( root_path, config_file ) ):
                    config_file = 'config.json'

        if not os.path.isfile( os.path.join( root_path, config_file ) ):
            print( "The config file is missing", file = sys.stderr )
            exit( -1 )

        API.app = Flask( __name__.split( '.' )[ 0 ],
                     static_url_path    = "",
                     root_path          = root_path,
                     static_folder      = root_path )
        logDict = {}
        API.app.logger.info( "Starting Flask application, loading configuration." )

        API.app.config.fromFile( os.path.join( root_path, config_file ) )

        # Setup logging for the application
        if 'logging' in API.app.config:
            logDict = API.app.config[ 'logging' ]

        if 'LOGGING' in API.app.config:
            logDict = API.app.config[ 'LOGGING' ]

        if len( logDict ) == 0:
            logDict = loadLoggingFile( root_path,
                                       folder = API.app.config[ 'LOGGING_FOLDER' ] if 'LOGGING_FOLDER' in API.app.config else None,
                                       verbose = verbose )

        else:
            if isinstance( logDict, str ):
                # filename
                logDict = loadLoggingFile( root_path,
                                           logDict,
                                           API.app.config[ 'LOGGING_FOLDER' ] if 'LOGGING_FOLDER' in API.app.config else None,
                                           verbose )

            elif isinstance( logDict, dict ):
                logDict = updateLogging( logDict,
                                         API.app.config[ 'LOGGING_FOLDER' ] if 'LOGGING_FOLDER' in API.app.config else None,
                                         verbose )

            else:
                print( "The logging key in config file is invalid", file = sys.stderr )

        logging.config.dictConfig( logDict )
        API.app.logger.log( API.app.logger.level,
                        "Logging Flask application: %s" % ( logging.getLevelName( API.app.logger.level ) ) )
        API.app.logger.info( "Config file: {}".format( os.path.join( root_path, config_file ) ) )
        API.app.logger.info( "{}".format( yaml.dump( API.app.config.struct, default_flow_style = False ) ) )
        if full_start:
            API.app.logger.info( "AngularPath : {}".format( API.app.config[ 'ANGULAR_PATH' ] ) )
            API.app.static_folder   = os.path.join( root_path, API.app.config[ 'ANGULAR_PATH' ] ) + "/"
            API.app.url_map.strict_slashes = False
            if module is None and 'API_MODULE' in API.app.config:
                API.app.logger.info("Loading module : {}".format( API.app.config[ 'API_MODULE' ] ) )
                module = importlib.import_module( API.app.config[ 'API_MODULE' ] )

            API.app.logger.info("Application module : {}".format( module ) )

            registerExtensions( module )
            if hasattr( module, 'registerExtensions' ):
                module.registerExtensions()

            API.app.logger.info( "Registering error handler" )
            if hasattr( module, 'registerErrorHandler' ):
                module.registerErrorHandler()

            else:
                def errorhandler( error ):
                    response = error.to_json()
                    response.status_code = error.status_code
                    return response

                API.app.errorhandler( InvalidUsage )( errorhandler )

            API.app.logger.info( "Registering SHELL context" )
            if hasattr( module, 'registerShellContext' ):
                module.registerShellContext()

            else:
                API.app.shell_context_processor( { 'db': API.db } )

            registerCommands()
            if hasattr( module, 'registerCommands' ):
                module.registerCommands()

            API.app.logger.info( "Registering blueprints" )
            if not API.app.config.get( "ALLOW_CORS_ORIGIN", False ):
                API.app.logger.info( "NOT allowing CORS" )

            registerAngular()
            if not hasattr( module, 'registerApi' ):
                raise Exception( "Missing registerApi() in module {}".format( module ) )

            module.registerApi()

    except Exception as exc:
        if API.app:
            API.app.logger.error( traceback.format_exc() )

        else:
            print( traceback.format_exc(), file = sys.stderr )

        raise

    return API.app
