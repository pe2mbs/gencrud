#!/usr/bin/python3
#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2020 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#   Library General Public License for more details.
#
#   You should have received a copy of the GNU Library General Public
#   License GPL-2.0-only along with this library; if not, write to the
#   Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301 USA
#
from __future__ import print_function    # (at top of module)
import getopt
import json
import os
import sys
import glob
import traceback
import logging
import gencrud.util.utils
from gencrud.configuraton import TemplateConfiguration, my_safe_load
from gencrud.generators.python import generatePython
from gencrud.generators.angular import generateAngular
from gencrud.version import __version__, __author__, __email__, __copyright__
from gencrud.util.exceptions import ( InvalidEnvironment,
                                      EnvironmentInvalidMissing,
                                      MissingAngularEnvironment,
                                      FlaskEnvironmentNotFound,
                                      ModuleExistsAlready,
                                      InvalidSetting )
from gencrud.constants import *
logger = logging.getLogger()


def verifyLoadProject( config: TemplateConfiguration, env ):
    if env == C_ANGULAR:
        configFile  = os.path.join( '..', '..', 'angular.json' )
        root        = config.angular

    elif env == C_PYTHON:
        root = config.python
        if os.path.isfile( os.path.join( root.sourceFolder, 'config', 'config.conf' ) ):
            configFile = os.path.join( 'config', 'config.conf' )

        elif os.path.isfile( os.path.join( root.sourceFolder, 'config.yaml' ) ):
            configFile = 'config.yaml'

        elif os.path.isfile( os.path.join( root.sourceFolder, 'config.json' ) ):
            configFile = 'config.json'

        else:
            raise Exception( "Could not find the Python Flask configuration file."  )

    else:
        raise InvalidEnvironment( env )

    if os.path.isdir( root.sourceFolder ) and os.path.isfile( os.path.join( root.sourceFolder, configFile ) ):
        with open( os.path.join( root.sourceFolder, configFile ),
                   gencrud.util.utils.C_FILEMODE_READ ) as stream:
            if configFile.endswith( ( '.yaml', '.conf' ) ):
                data = my_safe_load( stream )

            else:
                data = json.load( stream )

        if data is None:
            raise EnvironmentInvalidMissing( env, root.sourceFolder, configFile )

    else:
        raise EnvironmentInvalidMissing( env, root.sourceFolder, configFile )

    # logger.debug( 'Configuration for {}: {}'.format( env, json.dumps( data, indent = 4 ) ) )
    if env == C_ANGULAR:
        # Check if we have a valid Angular environment
        if 'defaultProject' in data and 'projects' in data:
            if data[ 'defaultProject' ] not in data[ 'projects' ]:
                raise MissingAngularEnvironment( '{} projects'.format( data[ 'defaultProject' ] ) )

            else:
                data = data[ 'projects' ][ data[ 'defaultProject' ] ]

        else:
            raise MissingAngularEnvironment( 'tag defaultProject' )

    elif env == C_PYTHON:
        # Check if we have a valid Python-Flask environment
        if 'API_MODULE' in data:
            pass

        else:
            if not ( 'COMMON' in data and 'API_MODULE' in data[ 'COMMON' ] ):
                raise FlaskEnvironmentNotFound()

            logging.info( "Application: {} target application: {}".format( config.application, data[ 'COMMON' ][ 'API_MODULE' ] ) )
            if data[ 'COMMON' ][ 'API_MODULE' ] != config.application:
                raise FlaskEnvironmentNotFound()

            data = data[ 'COMMON' ]

    return data


def doWork( input_file ):
    with open( input_file, 'r' ) as stream:
        config = TemplateConfiguration( stream )

    if config.nogen:
        print( "This template is blocked for generation" )
        return

    if C_VERSION in config:
        gencrud.util.utils.version = config.version
        if gencrud.util.utils.version != 1:
            raise Exception( "Invalid configuration version: {}, must be 1".format( gencrud.util.utils.version ) )

    if config.options.generateFrontend:
        verifyLoadProject( config, C_ANGULAR )

    else:
        logger.info( "NOT generating frontend code" )

    if config.options.generateBackend:
        verifyLoadProject( config, C_PYTHON )

    else:
        logger.info( "NOT generating backend code" )

    if config.options.generateBackend:
        logger.info( "*** Generating Python backend source code.***" )
        generatePython( config,
                        [ os.path.abspath( os.path.join( config.python.templateFolder, t ) )
                                   for t in os.listdir( config.python.templateFolder ) ] )

    if config.options.generateFrontend:
        logger.info( "*** Generating Typescript Angular frontend source code. ***" )
        generateAngular( config,
                         [ os.path.abspath( os.path.join( config.angular.templateFolder, t ) )
                                        for t in os.listdir( config.angular.templateFolder ) ] )
    return


def banner():
    print( '''gencrud - Python backend and Angular frontend code generation, version {version}
Copyright (C) {copyright} {author} <{email}>
'''.format( version = __version__, author = __author__, email = __email__, copyright = __copyright__ ) )


def usage( msg = '' ):
    banner()
    if msg != '':
        print( "{msg}\n".format( msg = msg ), file = sys.stderr )

    print( '''
Syntax:
    gencrud [options] { input-file1 [ input-fileN] }
                      { [<yaml-template-folder>/]* }

Parameters:


Options:
    -h / --help                         This help information.
    -b / --backup                       Make backup of the original project files files.
    -o / --overwrite                    Force overwriting the files.
    -c / --ignore-case-db-ids           All database names shall be in lower case. 
    -M / --module                       Create module component for template and use GenCrudModule.
                                        instead of adding the components directly into app.module.ts   
    -s / --ssl-verify                    Disable the verification of ssl certificate when    
                                        retrieving some external profile data.
    -v                                  Verbose option, prints what the tool is doing.
    -V / --version                      Print the version of the tool.
''' )
    return


def main():
    FORMAT = '%(levelname)s %(message)s'
    logging.basicConfig( format = FORMAT, level=logging.WARNING, stream = sys.stdout )
    try:
        opts, args = getopt.getopt( sys.argv[1:],
                                    'hi:s:obvVcM', [ 'help',
                                                     'input=',
                                                     'ssl-verify=',
                                                     'overwrite',
                                                     'backup'
                                                     'module'
                                                     'version',
                                                     'ignore-case-db-ids' ] )

    except getopt.GetoptError as err:
        # print help information and exit:
        usage( str( err ) )
        sys.exit( 2 )

    try:
        for o, a in opts:
            if o == '-v':
                if logger.level == logging.WARNING:
                    logger.setLevel( logging.INFO )

                else:
                    logger.setLevel( logging.DEBUG )

            elif o in ( '-h', '--help' ):
                usage()
                sys.exit()

            elif o in ( '-M', '--module' ):
                gencrud.util.utils.useModule = True

            elif o in ( '-b', '--backup' ):
                gencrud.util.utils.backupFiles = True

            elif o in ( '-c', '--case-insensitive-db-ids' ):
                gencrud.util.utils.ignoreCaseDbIds = True

            elif o in ( '-o', '--overwrite' ):
                gencrud.util.utils.overWriteFiles = True

            elif o in ('-V', '--version'):
                print( '{0}'.format( __version__ ) )
                sys.exit()

            elif o.lower() in ( '-s', '--ssl-verify' ):
                gencrud.util.utils.sslVerify = a.lower() == 'true'

            else:
                assert False, 'unhandled option'

        gencrud.util.utils.check_nltk()
        if len( args ) == 0:
            usage( 'Missing input file(s)' )
            sys.exit( 1 )

        banner()
        for arg in args:
            if '*' in arg:
                # Wild card handling
                for filename in glob.glob( os.path.abspath( os.path.expanduser( arg ) ) ):
                    print( "Filename: {} from wildcard".format( filename ) )
                    if filename.lower().endswith( '.yaml' ):
                        doWork( filename )

            else:
                print( "Filename: {}".format( arg ) )
                doWork( arg )

        print( "Done" )

    except ModuleExistsAlready as exc:
        logger.error( 'Module already exists: {}'.format( str( exc ) ) )
        logger.error( 'You can use the --overwrite option to avoid this error.' )

    except InvalidSetting as exc:
        logger.error( "Invalid setting" )
        logger.error( str( exc ) )

    except FileNotFoundError as exc:
        logger.error( "File not found" )
        if exc.filename in args:
            logger.error( "Input file '{0}' is not found.".format( exc.filename ) )

        else:
            logger.debug( traceback.format_exc() )
            logger.error( exc )

    except Exception as exc:
        logger.error( "Exception" )
        logger.debug( traceback.format_exc() )
        logger.error( exc )

    return


if __name__ == '__main__':
    if sys.version_info.major >= 3 and sys.version_info.minor >= 5:
        main()

    else:
        banner()
        print( "Error: This script runs with Python 3.5 or higher.")
