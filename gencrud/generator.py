#!/usr/bin/python3
#
#   Python backend and Angular frontend code generation by gencrud
#   main generator script
#   Copyright (C) 2018-2023 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
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
import os
from shutil import which
import sys
import glob
import traceback
import logging
import gencrud.util.utils
import gencrud.installer
from gencrud.configuraton import TemplateConfiguration
from gencrud.version import __version__, __author__, __email__, __copyright__
from gencrud.util.exceptions import ModuleExistsAlready, InvalidSetting, MissingTemplateAttribute
from gencrud.generators.version_1 import version_1_StyleGeneration
from gencrud.generators.version_2 import version_2_StyleGeneration
from gencrud.constants import *
import pypac.os_settings
from pypac.parser import PACFile
from pypac import get_pac
from gencrud.schema.export import exportSchema


logger = logging.getLogger()


class ToolNotFound( Exception ):
    pass


class CodingStyleMissing( Exception ):
    pass


def initializeCodeGenerationProcess( input_file ):
    with open( input_file, 'r' ) as stream:
        config = TemplateConfiguration( stream )

    if config.nogen:
        print( "This template is blocked for generation" )
        return

    if config.options.UsePrettier:
        if which( 'prettier' ) in ( None, '' ):
            raise ToolNotFound( 'prettier not found, install tool with "npm install -g prettier"' )

        if isinstance( config.options.PrettierStyle, str ):
            # Must be a filename
            if not os.path.exists( config.options.PrettierStyle ):
                raise CodingStyleMissing( config.options.PrettierStyle )

    if config.options.UseYapf:
        if which('yapf') in (None, ''):
            # Is ths a vierual environment module ?
            if not os.path.exists( os.path.join(os.path.split(sys.executable)[0], 'yapf.exe') ):
                raise ToolNotFound('yapf not found, install tool with "pip install yapf"')

        if isinstance( config.options.YapfStyle, str ):
            if config.options.YapfStyle not in ( 'pep8', 'google' ):
                # Check filename
                if not os.path.exists( config.options.YapfStyle ):
                    raise CodingStyleMissing( config.options.YapfStyle )

    gencrud.util.utils.version = config.version
    if gencrud.util.utils.version not in ( 1, 2 ):
        raise Exception( "Invalid configuration version: {}, must be 1 or 2".format( gencrud.util.utils.version ) )

    if gencrud.util.utils.version == 1:
        # old style generation Angular without lazy loading
        version_1_StyleGeneration( config )

    elif gencrud.util.utils.version == 2:
        # new style generation Angular with lazy loading and python submodules
        version_2_StyleGeneration( config )

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
    -r / --recurse                      do recursive generation of all templates.
    -e / --extension <extension>        to override the default extension .yaml 
    -i / --ignore <folder>              ignore folder (by default all folders starting with 'template' are ignored.   
    -o / --overwrite                    Force overwriting the files.
    -c / --ignore-case-db-ids           All database names shall be in lower case. 
    -M / --module                       Create module component for template and use GenCrudModule.
                                        instead of adding the components directly into app.module.ts   
    -s / --ssl-verify                    Disable the verification of ssl certificate when    
                                        retrieving some external profile data.
    -p / --proxy <addr|pac>             Using the IP address, url address of the proxy or the address for the PAC file
    -P / --proxy-system                 Use system proxy Windows Only 
    -v                                  Verbose option, prints what the tool is doing.
    -V / --version                      Print the version of the tool.
    -I / --install <angular-version>    Install templates into project, angular-version is the major Angular version 
                                        to be installed. current supported versions 8, 10 and 12
    -E/--export-schema <version>        exports the schema into version-<X>.yamls                                                                               
''' )
    return


def main():
    FORMAT = '%(levelname)s %(message)s'
    logging.basicConfig( format = FORMAT, level=logging.WARNING, stream = sys.stdout )
    try:
        opts, args = getopt.getopt( sys.argv[1:],
                                    'hs:obvVcMri:e:np:PI:E:',
                                    [
                                        'help',
                                        'ssl-verify=',
                                        'overwrite',
                                        'backup',
                                        'module',
                                        'recursive',
                                        'ignore=',
                                        'extension='
                                        'version',
                                        'ignore-case-db-ids',
                                        'proxy=',
                                        'proxy-system',
                                        'install=',
                                        'nltk-update',
                                        'export-schema='
                                    ] )

    except getopt.GetoptError as err:
        # print help information and exit:
        usage( str( err ) )
        sys.exit( 2 )

    ignoreFolders = [ ]
    recursive = False
    extension   = '.yaml'
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

            elif o in ('-r', '--recursive'):
                recursive = True

            elif o in ('-e', '--extension'):
                extension = a

            elif o in ('-i', '--ignore'):
                ignoreFolders.append( a )

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

            elif o in ( '-P', '--proxy-system' ):
                if pypac.os_settings.ON_WINDOWS:
                    gencrud.util.utils.proxyUrl = get_pac( url = pypac.os_settings.autoconfig_url_from_registry() )

                else:
                    raise Exception( "use manual proxy settings" )
            elif o in ( '-E', '--export-schema' ):
                if a.isdigit():
                    version = int( a )

                if not isinstance( version, int ):
                    raise ValueError( "version {version} not a valid number (1/2)" )

                elif version not in ( 1, 2 ):
                    raise ValueError( "version {version} not a valid number (1/2)")

                exportSchema( version, f'schema-v{version}' )
                sys.exit()

            elif o.lower() in ( '-p', '--proxy' ):
                pacFile = None
                if a.startswith( 'http' ):
                    if a.endswith( '.pac' ):
                        # PAC file
                        pacFile = a
                    else:
                        # URL
                        gencrud.util.utils.proxyUrl = a

                elif a[0].isdigit():
                    import socket
                    try:
                        socket.inet_aton( a.split( ':' )[ 0 ] )
                        # legal IP address
                        gencrud.util.utils.proxyUrl = a

                    except socket.error:
                        # Not legal
                        if os.path.isfile( a ) and os.path.exists( a ):
                            # PAC file
                            pacFile = a

                if pacFile is not None:
                    if pacFile.startswith( 'http' ):
                        pac = get_pac( url = pacFile )

                    else:
                        with open( pacFile, 'r' ) as stream:
                            pac = PACFile( stream.read() )

                    gencrud.util.utils.proxyUrl = pac

            elif o.lower() in ( '-n', '--nltk-update' ):
                gencrud.util.utils.update_nltk()

            elif o in ( '-I', '--install' ):
                gencrud.installer.install( int( a ) )
                print( "Done" )
                raise SystemExit()

            else:
                assert False, 'unhandled option'

        gencrud.util.utils.check_nltk()
        if len( args ) == 0:
            usage( 'Missing input file(s)' )
            sys.exit( 1 )

        banner()
        if recursive:
            def doRecursiveFolders( path, extension, ignore_folders ):
                with os.scandir(path) as it:
                    for entry in it:
                        entry: os.DirEntry
                        if entry.name.startswith('.') and entry.is_dir():
                            print( f'Skipping: {entry.name}')
                            continue

                        if entry.is_dir():
                            if entry.name in ignore_folders:
                                print(f'Skipping: {entry.name}')
                                continue

                            elif entry.name.startswith( 'template' ):
                                print(f'Skipping: {entry.name}')
                                continue

                            else:
                                doRecursiveFolders( os.path.join( path, entry.name ), extension, ignore_folders )
                                continue

                        if not entry.name.endswith( extension ):
                            print(f'Skipping: {entry.name}')
                            continue

                        filename = os.path.join( path, entry.name )
                        print( f"Filename: {filename} from wildcard" )
                        initializeCodeGenerationProcess( filename )

            for arg in args:
                doRecursiveFolders( os.path.abspath( os.path.expanduser( arg ) ), extension, ignoreFolders )

        else:
            for arg in args:
                if '*' in arg:
                    # Wild card handling
                    for filename in glob.glob( os.path.abspath( os.path.expanduser( arg ) ) ):
                        if filename.endswith( tuple( ignoreFolders ) ):
                            continue

                        print( f"Filename: {filename} from wildcard" )
                        if filename.lower().endswith( extension ):
                            # process the configuration file and create code files
                            initializeCodeGenerationProcess( filename )

                else:
                    print( "Filename: {}".format( arg ) )
                    initializeCodeGenerationProcess( arg )

        print( "Done" )
    except MissingTemplateAttribute as exc:
        print( exc )

    except ModuleExistsAlready as exc:
        logger.error( 'Module already exists: {}'.format( str( exc ) ) )
        logger.error( 'You can use the --overwrite option to avoid this error.' )

    except InvalidSetting as exc:
        logger.exception( "Invalid setting" )

    except FileNotFoundError as exc:
        logger.error( "File not found" )
        if exc.filename in args:
            logger.error( f"Input file '{exc.filename}' is not found." )

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
