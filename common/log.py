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
import logging
import os
import yaml
import json
from webapp2.common.exceptions import InvalidFileType
from functools import wraps

logObject = None


class LoggerWriter:
    def __init__( self, function ):
        # self.level is really like using log.debug(message)
        # at least in my case
        self.function = function
        return

    def write( self, message ):
        # if statement reduces the amount of newlines that are
        # printed to the logger
        if message != '\n':
            # self.function( message.replace( '\n', '\\n' ) )
            pass

        return

    def flush(self):
        # create a flush method so things can be flushed when the system wants to.
        # Simply returning is good enough.
        return


def getLogger( root = 'flask.app' ):
    """Gets the logger instance

    :param root:    The name of the logger instance
    :return:        Logger class
    """
    return logging.getLogger( root )


def appLogger( func ):
    """Decorator to log the entry of a function/procedure/route

    :param func:    the functions being called
    :return:        the decorator wrapper function
    """
    @wraps( func )
    def wrapper( *args, **kwargs ):
        global logObject
        if logObject is None:
            logObject = logging.getLogger( 'flask.app' )

        if logObject.level == logging.DEBUG:
            argList = ', '.join( args )
            kwargList = ', '.join( [ '{0} = {1}'.format( key, value ) for key, value in kwargs.items() ] )
            argList = ( argList if len( argList ) == 0 else ", " ) + kwargList
            if len( argList ) > 0:
                argList = ' ' + argList + ' '

            logObject.debug( "entrty:%s(%s)" % ( func.__name__, argList ) )

            result = func( *args, **kwargs )

            logObject.debug( "exit:%s => %s" % ( func.__name__, repr( result ) ) )
            return result

        return func( *args, **kwargs )

    return wrapper

from socket import gethostname

def updateKeywordArguments( kwargs ):
    MAPPED = {
        'hostname': gethostname,
        'pid':      os.getpid,
    }
    for key, value in MAPPED.items():
        if key not in kwargs:
            if callable( value ):
                kwargs[ key ] = value()

            else:
                kwargs[key] = value

    return kwargs


def updateLogging( tree, folder, verbose = False, level = None, **kwargs ):
    if folder is None:
        return tree

    os.makedirs( folder, exist_ok = True )
    kwargs = updateKeywordArguments( kwargs )
    for key in tree.keys():
        if key == 'filename':
            filepath, filename = os.path.split( tree[ key ] )
            if filepath == '':
                tree[ key ] = os.path.join( folder, tree[ key ] ).format( **kwargs )

            else:
                tree[ key ] = os.path.abspath( tree[ key ] ).format( **kwargs )

        elif key == 'level':
            if verbose:
                tree[ key ] = logging.DEBUG

            elif level is not None:
                tree[ key ] = level

        elif isinstance( tree[ key ], dict ):
            updateLogging( tree[ key ], folder, **kwargs )

        elif isinstance( tree[ key ], list ):
            for item in tree[ key ]:
                if isinstance( item, dict ):
                    updateLogging( item, folder, **kwargs )

    return tree

def loadLoggingFile( root_path, filename = None, folder = None, verbose = False, **kwargs ):
    def loadLoggingFileExt( root_path, filename ):
        logDict = { }
        if os.path.isfile( os.path.join( root_path, filename ) ):
            with open( os.path.join( root_path, filename ) ) as stream:
                if filename.lower().endswith( '.yaml' ):
                    logDict = yaml.load( stream )

                elif filename.lower().endswith( '.json' ):
                    logDict = json.load( stream )

                else:
                    raise InvalidFileType( os.path.isfile( os.path.join( root_path, filename ) ) )

        else:
            raise FileNotFoundError( os.path.isfile( os.path.join( root_path, filename ) ) )

        return logDict

    if filename is None:
        for filename in ( 'logging.yaml', 'logging.json' ):
            if os.path.isfile( os.path.join( root_path, filename ) ):
                return updateLogging( loadLoggingFileExt( root_path, filename ), folder, verbose, **kwargs )

        raise FileNotFoundError( root_path )

    return updateLogging( loadLoggingFileExt( root_path,filename ), folder, verbose, **kwargs )

LOGGING_INFO = {
    'version': 1,
    'formatters': {
        'default': {
            'format': "[%(asctime)s] %(levelname)s %(name)s in %(module)s.%(funcName)s( %(lineno)s ): %(message)s"
        },
        'console': {
        'format': "%(asctime)s %(levelname)s %(name)s in %(module)s: %(message)s"
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'console',
            'level': 'DEBUG',
        },
        'logfile': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'webapp2.log',
            'maxBytes': 10485760,
            'backupCount': 7,
            'formatter': 'default',
            'level': 'DEBUG',
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': [ 'console', 'logfile' ]
    },
    'loggers': {
        'flask.app': {
            'level': 'DEBUG'
        }
    }
}
