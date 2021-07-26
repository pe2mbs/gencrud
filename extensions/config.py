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
import traceback
import logging
import os
import sys
import errno
import copy
import json
import datetime
from flask import Config as BaseConfig
from webapp2.common.iterahead import lookahead
from ruamel import yaml



def my_compose_document(self):
    self.get_event()
    node = self.compose_node(None, None)
    self.get_event()
    # self.anchors = {}    # <<<< commented out
    return node


yaml.SafeLoader.compose_document = my_compose_document


def yaml_include( loader, node ):
    if node.value.startswith( '.' ):
        include_name = os.path.join( os.path.dirname( node.start_mark.name ), node.value )

    else:
        include_name = node.value

    include_name = os.path.abspath( include_name )
    with open( include_name, 'r' ) as inputfile:
        data = my_safe_load( inputfile, master = loader )
        return data


yaml.add_constructor( "!include", yaml_include, Loader=yaml.SafeLoader )


def my_safe_load(stream, Loader=yaml.SafeLoader, master=None):
    loader = Loader(stream)
    if master is not None:
        loader.anchors = master.anchors

    try:
        return loader.get_single_data()

    finally:
        loader.dispose()


class Config( BaseConfig ):
    """Flask config enhanced with a `from_yaml` and `from_json` methods."""

    def _configOverRide( self, result, override ):
        for key, value in override.items():
            if isinstance( value, dict ):
                if key not in result:
                    result[ key ] = {}

                result[ key ] = self._configOverRide( result[ key ], value )

            else:
                result[ key ] = value

        return result

    def fromFolder( self, config_folder, silent = False ):
        """First the config/config.yal is loaded as the master configuration.

        Second in sub-folder config/env is checked that a <{FLASK_ENV}>.yaml is located,
        If so it loaded and the attributes from this file are overriding the config.

        Third in sub-folder config/tsk is checked that a <{FLASK_TASK}>.yaml is located,
        If so it loaded and the attributes from this file are overriding the config.


        :param config_folder:
        :param silent:
        :return:
        """
        result = {}
        try:
            if os.path.isdir( config_folder ):
                # Master configuration
                configFile = os.path.join( config_folder, 'config.conf' )
                if os.path.isfile( configFile ):
                    with open( configFile, 'r' ) as stream:
                        result = my_safe_load( stream )

                else:
                    raise Exception( 'No master configuration present {}'.format( configFile ) )

                env = os.environ.get( 'FLASK_ENV', 'DEVELOPMENT' ).upper()
                envFolder = os.path.join( config_folder, 'env' )
                if os.path.isdir( envFolder ):
                    configFile = os.path.join( envFolder, '{}.conf'.format( env.upper() ) )
                    if os.path.isfile( configFile ):
                        with open( configFile, 'r' ) as stream:
                            result = self._configOverRide( result, my_safe_load( stream ) )

                    else:
                        print( "No ENVIRONENT config", file = sys.stderr )

                else:
                    # no custom configutions at all.
                    print( "No 'env' folder for ENVIRONEMNT configurations", file = sys.stderr )

                self[ 'ENVIRONMENT' ] = env.lower()
                tsk = os.environ.get( 'FLASK_TASK', 'WEBAPP' ).upper()
                tskFolder = os.path.join( config_folder, 'tsk' )
                if os.path.isdir( tskFolder ):
                    configFile = os.path.join( tskFolder, '{}.conf'.format( tsk.upper() ) )
                    if os.path.isfile( configFile ):
                        with open( configFile, 'r' ) as stream:
                            result = self._configOverRide( result, my_safe_load( stream ) )

                    else:
                        print( "No TASK config", file = sys.stderr )

                self[ 'WEBAPP_TASK' ] = tsk.lower()

            else:
                raise Exception( "Configuration folder not present: {}".format( config_folder ) )

            return self._modify( result )

        except Exception:
            print( traceback.format_exc() )
            raise

    def fromFile( self, config_file, silent=False ):
        """Load the configuration from a file, currently JSON and YAML formats
        are supported

        :param config_file:     the filename of the JSON or YAML file.
                                This can either be an absolute filename
                                or a filename relative to the root path.
        :param silent:          set to ``True`` if you want silent failure
                                for missing files.
        :return:                ``True`` if able to load config,
                                ``False`` otherwise.
        """

        ext = os.path.splitext( config_file )[ 1 ]
        if ext == '.json':
            result = self.fromJson( config_file )

        elif ext in ( '.yml', '.yaml' ):
            result = self.fromYaml( config_file )

        else:
            raise Exception( "Could not load file type: '%s'" % ( ext ) )

        return result

    def fromYaml( self, config_file, silent=False ):
        """Load the configuration from a file, currently YAML formats
        are supported

        :param config_file:     the filename of the YAML file.
                                This can either be an absolute filename
                                or a filename relative to the root path.
        :param silent:          set to ``True`` if you want silent failure
                                for missing files.
        :return:                ``True`` if able to load config,
                                ``False`` otherwise.
        """

        # Get the Flask environment variable, if not exist assume development.
        env = os.environ.get( 'FLASK_ENV', 'DEVELOPMENT' ).upper()
        self[ 'ENVIRONMENT' ] = env.lower()
        try:
            with open( config_file ) as f:
                c = my_safe_load( f )

        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False

            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise

        taskSection = c.get( 'COMMON_TASKS', {} ).get( os.environ.get( 'FLASK_TASK', 'webapp' ), {} )
        return self._modify( c.get( env, c ), taskSection )

    def fromJson( self, config_file, silent=False ):
        """Load the configuration from a file, currently JSON formats
        are supported

        :param config_file:     the filename of the JSON file.
                                This can either be an absolute filename
                                or a filename relative to the root path.
        :param silent:          set to ``True`` if you want silent failure
                                for missing files.
        :return:                ``True`` if able to load config,
                                ``False`` otherwise.
        """

        # Get the Flask environment variable, if not exist assume development.
        env = os.environ.get( 'FLASK_ENV', 'DEVELOPMENT' )
        self[ 'ENVIRONMENT' ] = env.lower()
        try:
            with open( config_file ) as f:
                c = json.load( f )

        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False

            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise

        # Get the environment segment
        segment = copy.copy( c.get( env, c ) )
        # self.__dump( segment )
        if 'inport' in segment:
            # Get the import segment
            c = copy.copy( c.get( segment[ 'inport' ], {} ) )
            # join the selected segment and imported segment, making sure that
            # the selected segment has priority over the imported segement
            c.update( segment )
            segment = c

        if 'COMMON_TASKS' in c:
            taskSection = c.get( 'COMMON_TASKS', {} ).get( os.environ.get( 'FLASK_TASK', 'webapp' ), {} )

        else:
            taskSection = {}

        return self._modify( segment, taskSection )

    def _modify( self, c, taskSection = None ):
        """Internal updater to fix PATH's and DATABASE uri

        :param c:
        :return:
        """
        delta_keys = ( "PERMANENT_SESSION_LIFETIME",
                       "SEND_FILE_MAX_AGE_DEFAULT",
                       "JWT_ACCESS_TOKEN_EXPIRES",
                       "JWT_REFRESH_TOKEN_EXPIRES" )

        if isinstance( taskSection, dict ):
            # print( "taskSection", taskSection )

            def resolveKeys( path, keys, value ):
                for key, more in lookahead( keys ):
                    if more:
                        path = path[ key ]

                    else:
                        path[ key ] = value
                        return

                return

            def resolveKey( path, upd ):
                for key, value in  upd.items():
                    if '.' in key:
                        resolveKeys( c, key.split( '.' ), value )

                    elif isinstance( value, dict ):
                        path[ key ] = resolveKey( path[ key ], value )

                    else:
                        path[ key ] = value

                return path

            try:
                resolveKey( c, taskSection )

            except Exception:
                logging.getLogger().exception( "Resolving the config failed" )

        for key in c.keys():
            if key.isupper():
                # Is the variable '**PATH**' in the name and starts with a dot.
                if "PATH" in key and c[ key ].startswith( '.' ):
                    # Resolve the path to a full path
                    self[ key ] = os.path.abspath( os.path.join( self.root_path, c[ key ] ) )

                else:
                    def func( value ):
                        try:
                            return int( value )

                        except Exception as exc:
                            pass

                        return value

                    if key in delta_keys:
                        if '=' in c[ key ]:
                            # convert the string to a dict.
                            settings = dict( map( func, x.split( '=' ) ) for x in c[ key ].split( ',' ) )
                            self[ key ] = datetime.timedelta( **settings )

                        else:
                            self[ key ] = c[ key ]

                    else:
                        self[ key ] = c[ key ]

        if 'DATABASE' in c:
            database_cfg = c[ 'DATABASE' ]
            engine = database_cfg[ 'ENGINE' ]
            if engine == 'sqlite':
                # For Sqlite the connect string is different, contains path and database filename
                database_cfg[ 'APP_PATH' ] = self[ 'APP_PATH' ]
                db_uri = '{ENGINE}:///{APP_PATH}/{SCHEMA}'.format( **database_cfg )

            elif engine == 'oracle':
                db_uri = '{ENGINE}://{USERNAME}:{PASSWORD}@{TNS}'.format(**database_cfg)

            else:
                # For other databases
                if 'HOST' not in database_cfg:
                    database_cfg[ 'HOST' ] = 'localhost'

                if 'PORT' not in database_cfg:
                    # 'HOST_ADDRESS' set to 'HOST' variable
                    database_cfg[ 'HOST_ADDRESS' ] = database_cfg[ 'HOST' ]

                else:
                    # 'HOST_ADDRESS' set to 'HOST' and 'PORT' variable
                    database_cfg[ 'HOST_ADDRESS' ] = '{HOST}:{PORT}'.format( **database_cfg )

                if 'USERNAME' in database_cfg and 'PASSWORD' in database_cfg:
                    # Include username and password into the 'HOST_ADDRESS'
                    database_cfg[ 'HOST_ADDRESS' ] = '{USERNAME}:{PASSWORD}@{HOST_ADDRESS}'.format( **database_cfg )

                elif 'USERNAME' in database_cfg:
                    # Include username into the 'HOST_ADDRESS'
                    database_cfg[ 'HOST_ADDRESS' ] = '{USERNAME}@{HOST_ADDRESS}'.format( **database_cfg )

                db_uri = '{ENGINE}://{HOST_ADDRESS}/{SCHEMA}'.format( **database_cfg )

            self[ 'SQLALCHEMY_DATABASE_URI' ] = db_uri

        if self[ 'ENVIRONMENT' ] not in ( 'prod' ):
            self._dump()

        return True

    def _dump( self, segment = None, stream = None ):
        logger = logging.getLogger( 'flask.app' )
        def logit( data ):
            if stream:
                print( data )

            else:
                logger.info( data )

        if segment is None:
            segment = self
            logit( "Dump configuration." )

        else:
            logit( "Dump segment configuration." )

        for key in sorted( segment.keys() ):
            logit( "%-30s : %s" % ( key, segment[ key ] ) )

        return

    @property
    def struct( self ):
        return dict( self )
