# -*- coding: utf-8 -*-
"""Configuration module for the 'Main Angular application package'."""
#
# Configuration module for the 'Main Angular application package'.
# Copyright (C) 2018 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
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
import logging
import os
import sys
import errno
import copy
import yaml
import json
import datetime
from flask import Config as BaseConfig


class IncludeLoader( yaml.Loader ):
    """
    yaml.Loader subclass handles "!include path/to/foo.yml" directives in config
    files.  When constructed with a file object, the root path for includes
    defaults to the directory containing the file, otherwise to the current
    working directory. In either case, the root path can be overridden by the
    `root` keyword argument.

    When an included file F contain its own !include directive, the path is
    relative to F's location.

    Example:
        YAML file /home/frodo/one-ring.yml:
            ---
            Name: The One Ring
            Specials:
                - resize-to-wearer
            Effects:
                - !include path/to/invisibility.yml

        YAML file /home/frodo/path/to/invisibility.yml:
            ---
            Name: invisibility
            Message: Suddenly you disappear!

        Loading:
            data = IncludeLoader(open('/home/frodo/one-ring.yml', 'r')).get_data()

        Result:
            {'Effects': [{'Message': 'Suddenly you disappear!', 'Name':
                'invisibility'}], 'Name': 'The One Ring', 'Specials':
                ['resize-to-wearer']}
    """
    def __init__( self, *args, **kwargs ):
        super( IncludeLoader, self ).__init__( *args, **kwargs )
        self.add_constructor( '!include', self._include )
        if 'root' in kwargs:
            self.root = kwargs['root']

        elif isinstance( self.stream, file ):
            self.root = os.path.dirname( self.stream.name )

        else:
            self.root = os.path.curdir

    def _include( self, loader, node ):
        oldRoot = self.root
        filename = os.path.join(self.root, loader.construct_scalar(node))
        self.root = os.path.dirname( filename )
        data = yaml.load( open( filename, 'r' ) )
        self.root = oldRoot
        return data



class Config( BaseConfig ):
    """Flask config enhanced with a `from_yaml` and `from_json` methods."""

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
        env = os.environ.get( 'FLASK_ENV', 'DEVELOPMENT' )
        self[ 'ENVIRONMENT' ] = env.lower()
        try:
            with open( config_file ) as f:
                c = yaml.load( f )

        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False

            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise

        return self._modify( c.get( env, c ) )

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

        return self._modify( segment )

    def _modify( self, c ):
        """Internal updater to fix PATH's and DATABASE uri

        :param c:
        :return:
        """
        delta_keys = ( "PERMANENT_SESSION_LIFETIME", 
                       "SEND_FILE_MAX_AGE_DEFAULT",
                       "JWT_ACCESS_TOKEN_EXPIRES", 
                       "JWT_REFRESH_TOKEN_EXPIRES" )

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

    def _dump( self, segment = None ):
        logger = logging.getLogger( 'flask.app' )
        if segment is None:
            segment = self
            logger.info( "Dump configuration." )

        else:
            logger.info( "Dump segment configuration." )

        for key in sorted( segment.keys() ):
            logger.info( "%-30s : %s" % ( key, segment[ key ] ) )

        return
