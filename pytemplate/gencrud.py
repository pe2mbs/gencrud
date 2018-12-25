#!/usr/bin/python3
#
#   Python backend and Angular frontend code generation by Template
#   Copyright (C) 2018 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>
#
#   This library is free software; you can redistribute it and/or
#   modify it under the terms of the GNU Library General Public
#   License as published by the Free Software Foundation; either
#   version 2 of the License, or (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#   Library General Public License for more details.
#
#   You should have received a copy of the GNU Library General Public
#   License along with this library; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
from __future__ import print_function    # (at top of module)
import os
import sys
import yaml
import json
import getopt
import traceback
from pytemplate.version import __version__, __author__, __email__, __copyright__
from pytemplate.configuraton import TemplateConfiguration
import pytemplate.utils
from pytemplate.angular import generateAngular
from pytemplate.python import generatePython


def verifyLoadProject( env, config ):
    result = None
    if env == 'angular':
        configFile = os.path.join( '..', '..', 'angular.json' )
        root = config.angular

    elif env == 'python':
        configFile = 'config.json'
        root = config.python

    else:
        raise Exception( 'Invalid environment {0} in verifyLoadProject'.format( env ) )

    if os.path.isdir( root.source ) and os.path.isfile( os.path.join( root.source, configFile ) ):
        with open( os.path.join( root.source, configFile ), pytemplate.utils.C_FILEMODE_READ ) as stream:
            data = json.load( stream )

        if data is None:
            raise Exception( 'Error: {1} environment invalid, missing {0}'
                         .format( os.path.join( config.angular.source, configFile ),
                                  env ) )

    else:
        raise Exception( 'Error: {1} environment not found, missing {0}'
                         .format( os.path.join( config.angular.source, configFile ),
                                  env ) )

    if env == 'angular':
        # Check if we have a valid Angular environment
        if 'defaultProject' in data and 'projects' in data:
            if data[ 'defaultProject' ] not in data[ 'projects' ]:
                raise Exception( 'Error: Angular environment not found, missing {} projects'.format( data[ 'defaultProject' ] ) )

            else:
                data = data[ 'projects' ][ data[ 'defaultProject' ] ]

        else:
            raise Exception( 'Error: Angular environment not found, missing tag defaultProject' )

    elif env == 'python':
        # Check if we have a valid Python-Flask environment
        if not ( 'COMMON' in data and 'API_MODULE' in data[ 'COMMON' ] ):
            raise Exception( 'Error: Python Flask environment not found' )

        if data[ 'COMMON' ][ 'API_MODULE' ] != config.objects[ 0 ].application:
            raise Exception( 'Error: Not correct Python Flask environment not found' )

    return data


def doWork( inputFile ):
    with open( inputFile, 'r' ) as stream:
        config = TemplateConfiguration( **yaml.load( stream ) )

    verifyLoadProject( 'angular', config )
    verifyLoadProject( 'python', config )

    generatePython( [ os.path.abspath( os.path.join( config.python.template, t ) )
                                   for t in os.listdir( config.python.template ) ],
                    config )

    generateAngular( [ os.path.abspath( os.path.join( config.angular.template, t ) )
                                    for t in os.listdir( config.angular.template ) ],
                     config )

    return


def banner():
    print( '''gencrud - Python backend and Angular frontend code generation, version {version}
Copyright (C) {copyright} {autor} <{email}>
'''.format( version = __version__, autor = __author__, email = __email__, copyright = __copyright__ ) )

def usage( msg = '' ):
    banner()
    if msg != '':
        print( "{msg}\n".format( msg = msg ), file = sys.stderr )

    print( '''
Syntax:
    gencrud [options] [input-file1 ... input-fileN]

Parameters:


Options:
    -h / --help         This help information.
    -b / --backup       Make backup of the orginal project files files.
    -o / --overwrite    Force overwriting the files.
    -s / --sslverify    Disable the verification of ssl certificate when
                        retrieving some external profile data.
    -v                  Verbose option, prints what the tool is doing.
    -V / --version      Print the version of the tool.
''' )
    return


def main():

    try:
        opts, args = getopt.getopt( sys.argv[1:],
                                    'hi:s:obvV', [ 'help',
                                                   'input=',
                                                   'sslverify=',
                                                   'overwrite',
                                                   'backup'
                                                   'version' ] )

    except getopt.GetoptError as err:
        # print help information and exit:
        usage( str( err ) )
        sys.exit( 2 )

    try:
        for o, a in opts:
            if o == '-v':
                pytemplate.utils.verbose = True

            elif o in ( '-h', '--help' ):
                usage()
                sys.exit()

            elif o in ( '-b', '--backup' ):
                pytemplate.utils.backupFiles = True

            elif o in ( '-o', '--overwrite' ):
                pytemplate.utils.overWriteFiles = True

            elif o in ('-V', '--version'):
                print( '{0}'.format( __version__ ) )
                sys.exit()

            elif o.lower() in ( '-s', '--sslverify' ):
                pytemplate.utils.sslVerify = a.lower() == 'true'

            else:
                assert False, 'unhandled option'

        pytemplate.utils.check_nltk()
        if len( args ) == 0:
            usage( 'Missing input file(s)' )
            sys.exit( 1 )

        banner()
        for arg in args:
            doWork( arg )
    except pytemplate.utils.ModuleExistsAlready as exc:
        print( 'Module already exists: {}'.format( str( exc ) ), file = sys.stderr )
        print( 'You can use the --overwrite option to avoid this error.', file = sys.stderr )

    except Exception as exc:
        if pytemplate.utils.verbose:
            traceback.print_exc()

        print( exc, file = sys.stderr )

    return


if __name__ == '__main__':
    main()
