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
import json
import os
import sys
import yaml
import logging
import shutil
import datetime
import hashlib
import gencrud.version
from mako.template import Template
from gencrud.configuraton import TemplateConfiguration
import gencrud.util.utils
import gencrud.util.exceptions
from gencrud.util.positon import PositionInterface
import gencrud.util.utils as API

logger = logging.getLogger()

MENU_CHILDREN_LABEL    = 'children'
MENU_DISPLAY_NAME       = 'displayName'
MENU_ICON_NAME          = 'iconName'

MENU_DISPLAY_NAME_V2    = 'caption'
MENU_ICON_NAME_V2       = 'icon'

MENU_INDEX              = 'index'
MENU_ID                 = 'id'
MENU_ROUTE              = 'route'
#LABEL_LIST_MODULES      = 'listModules = ['
#LABEL_MENU_ITEMS        = 'menuItems = ['
#LABEL_END_LIST          = ']'


def makeUnittestModules( root_path, *args ):
    def write__init__py():
        with open( os.path.join( root_path, '__init__.py' ), 'w+' ) as stream:
            # Write one newline to the file
            print( '', file = stream )

        return

    if len( args ) > 0:
        root_path = os.path.join( root_path, args[ 0 ] )
        if not os.path.isdir( root_path ):
            os.mkdir( root_path )

        makeUnittestModules( root_path, *args[ 1: ] )

    if len( args ) > 0:
        if not os.path.isfile( os.path.join( root_path, '__init__.py' ) ):
            write__init__py()

    return


def updateUnittestDirectory( config: TemplateConfiguration, app_module ):   # noqa
    logger.debug( config.unittest.sourceFolder )
    # Copy the following files from the common-py folder to the source folder of the project
    for src_filename in ['generic.py']:
        fnd = os.path.abspath( os.path.join( config.unittest.sourceFolder, config.application, src_filename ) )
        if not os.path.isfile( fnd ):
            fns = os.path.abspath( os.path.join( config.unittest.commonFolder, src_filename ) )
            logger.debug( "Source: {}\nTarget: {}".format( fns, fnd ) )
            shutil.copy( fns, fnd )

    return


def generateCommonTemplateFiles( config:  TemplateConfiguration ):

    modelsFilename = os.path.join( config.python.sourceFolder, config.application, 'modules.yaml' )
    if os.path.isfile( modelsFilename ):
        with open( modelsFilename, 'r' ) as stream:
            modules = yaml.load( stream, Loader = yaml.Loader )

    else:
        modules = []
    """
    for cfg in config:
        module_name = "{}.{}".format( config.application, cfg.name )
        found = False
        for module in modules:
            if module.get( 'module' ) == module_name:
                module[ 'model' ] = cfg.cls
                module[ 'table' ] = cfg.table.name.lower()
                found = True
                break


        if not found:
            modules.append( { 'module': module_name,
                              'model': cfg.cls,
                              'table': cfg.table.name.lower() } )

    with open( modelsFilename, 'w' ) as stream:
        yaml.dump( modules, stream, Dumper = yaml.Dumper )
     """

    # Now generate the suite.py module
    template = os.path.abspath( os.path.join( config.unittest.commonFolder, 'suite.py.templ' ) )
    suite_py_file = os.path.join( config.unittest.sourceFolder, config.application, 'suite.py' )
    with open( suite_py_file, 'w' ) as stream:
        for line in  Template( filename = template ).render( config = config, modules = modules ).split( '\n' ):
            stream.write( line )

    return

def generateUnittest( config: TemplateConfiguration, templates: list ):
    logger.info( 'application : {0}'.format( config.application ) )
    dt = datetime.datetime.now()
    generationDateTime = dt.strftime( "%Y-%m-%d %H:%M:%S" )
    userName = os.path.split( os.path.expanduser( "~" ) )[ 1 ]
    generateCommonTemplateFiles( config )
    for cfg in config:
        modulePath = os.path.join( config.unittest.sourceFolder,
                                   config.application,
                                   cfg.name )
        logger.info( 'name        : {0}'.format( cfg.name ) )
        logger.info( 'class       : {0}'.format( cfg.cls ) )
        logger.info( 'table       : {0}'.format( cfg.table.tableName ) )
        logger.info( 'primary key : {0}'.format( cfg.table.primaryKey ) )
        logger.info( 'uri         : {0}'.format( cfg.uri ) )
        for col in cfg.table.columns:
            logger.info( '- {0:<20}  {1}'.format( col.name, col.sqlAlchemyDef() ) )
        for templ in templates:
            if cfg.ignoreTemplates( templ ):
                continue
            logger.info( 'template    : {0}'.format( templ ) )
            if not os.path.isdir( config.unittest.sourceFolder ):
                os.makedirs( config.unittest.sourceFolder )

            if os.path.isdir( modulePath ) and not config.options.overWriteFiles:
                raise gencrud.util.exceptions.ModuleExistsAlready( cfg, modulePath )
            outputSourceFile = os.path.join( modulePath, gencrud.util.utils.sourceName( templ ) )
            if config.options.backupFiles:
                gencrud.util.utils.backupFile( outputSourceFile )
            if os.path.isfile( outputSourceFile ):
                # remove the file first
                os.remove( outputSourceFile )
            makeUnittestModules( config.unittest.sourceFolder, config.application, cfg.name )
            with open( outputSourceFile,
                       gencrud.util.utils.C_FILEMODE_WRITE ) as stream:
                for line in Template( filename = os.path.abspath( templ ) ).render( obj = cfg,
                                                                                    root = config,
                                                                                    date = generationDateTime,
                                                                                    version = gencrud.version.__version__,
                                                                                    username = userName ).split( '\n' ):
                    stream.write( line )
                    if sys.platform.startswith( 'linux' ):
                        stream.write( '\n' )

    updateUnittestDirectory( config, '' )
    return
