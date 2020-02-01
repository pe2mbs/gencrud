# -*- coding: utf-8 -*-
"""logger API for the 'Main Angular application package'"""
#
# logger API for the 'Main Angular application package'
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
import yaml
import json
from webapp.common.exceptions import InvalidFileType
from functools import wraps

logObject = None


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


def updateLogging( tree, folder, verbose = False, level = None ):
    if folder is None:
        return tree

    os.makedirs( folder, exist_ok = True )
    for key in tree.keys():
        if key == 'filename':
            filepath, filename = os.path.split( tree[ key ] )
            if filepath == '':
                tree[ key ] = os.path.join( folder, tree[ key ] ).format( pid = os.getpid() )

            else:
                tree[ key ] = os.path.abspath( tree[ key ] ).format( pid = os.getpid() )

        elif key == 'level':
            if verbose:
                tree[ key ] = logging.DEBUG

            elif level is not None:
                tree[ key ] = level

        elif isinstance( tree[ key ], dict ):
            updateLogging( tree[ key ], folder )

        elif isinstance( tree[ key ], list ):
            for item in tree[ key ]:
                if isinstance( item, dict ):
                    updateLogging( item, folder )

    return tree

def loadLoggingFile( root_path, filename = None, folder = None, verbose = False ):
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
                return updateLogging( loadLoggingFileExt( root_path, filename ), folder, verbose )

        raise FileNotFoundError( root_path )

    return updateLogging( loadLoggingFileExt( root_path,filename ), folder, verbose )
