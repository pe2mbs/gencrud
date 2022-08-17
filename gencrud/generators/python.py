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


def makePythonModules( root_path, *args ):
    def write__init__py():
        with open( os.path.join( root_path, '__init__.py' ), 'w+' ) as stream:
            # Write one newline to the file
            print( '', file = stream )

        return

    if len( args ) > 0:
        root_path = os.path.join( root_path, args[ 0 ] )
        if not os.path.isdir( root_path ):
            os.mkdir( root_path )

        makePythonModules( root_path, *args[ 1: ] )

    if len( args ) > 0:
        if not os.path.isfile( os.path.join( root_path, '__init__.py' ) ):
            write__init__py()

    return


def updatePythonProject( config: TemplateConfiguration, app_module ):   # noqa
    logger.debug( config.python.sourceFolder )
    # Copy the following files from the common-py folder to the source folder of the project
    for src_filename in ( 'common.py', 'main.py' ):
        fnd = os.path.abspath( os.path.join( config.python.sourceFolder, config.application, src_filename ) )
        if not os.path.isfile( fnd ):
            fns = os.path.abspath( os.path.join( config.python.commonFolder, src_filename ) )
            logger.debug( "Source: {}\nTarget: {}".format( fns, fnd ) )
            shutil.copy( fns, fnd )
    def makeMenuId( menu,prefix ):
        return hashlib.md5( (prefix + menu.caption).encode('ascii') ).hexdigest().upper()

    # retrieve default global menu structure from menu.yaml
    menuFilename = os.path.join( config.python.sourceFolder, config.application, 'menu.yaml' )
    if os.path.isfile( menuFilename ):
        with open( menuFilename, 'r' )  as stream:
            menuItems = yaml.load( stream, Loader = yaml.Loader )
            if menuItems is None:
                menuItems = []

    else:
        menuItems = []

    def processMenuStructure_V2( items, menu, id_prefix = '' ):
        foundMenu = False
        for menuItem in items:
            if menuItem[ MENU_DISPLAY_NAME_V2 ] == menu.caption:
                foundMenu = True
                if menu.menu is not None:
                    # sub menu
                    if MENU_CHILDREN_LABEL not in menuItem:
                        menuItem[ MENU_CHILDREN_LABEL ] = [ ]

                    if MENU_ID not in menuItem:
                        menuItem[ MENU_ID ] = makeMenuId( menu, id_prefix )

                    processMenuStructure_V2( menuItem[ MENU_CHILDREN_LABEL ],
                                             menu.menu,
                                             menuItem[ MENU_ID ] + '_' )

                else:
                    menuItem[ MENU_DISPLAY_NAME_V2 ] = menu.caption
                    menuItem[ MENU_ICON_NAME_V2 ] = menu.icon
                    menuItem[ MENU_ID ] = makeMenuId( menu, id_prefix )
                    if menu.route is not None:
                        menuItem[ MENU_ROUTE ] = menu.route

                    # elif menu.menu is not None:
                    #     if MENU_CHILDREN_LABEL not in menuItem:
                    #         menuItem[ MENU_CHILDREN_LABEL ] = [ ]
                    #
                    #     processMenuStructure_V2( menuItem[ MENU_CHILDREN_LABEL ],
                    #                              menu.menu,
                    #                              menuItem[ MENU_ID ] + '_' )

        if not foundMenu:
            newMenuItem = { MENU_DISPLAY_NAME_V2: menu.caption,
                            MENU_ID: makeMenuId( menu, id_prefix ),
                            MENU_ICON_NAME_V2: menu.icon }
            if menu.route is not None:
                newMenuItem[ MENU_ROUTE ] = menu.route

            elif menu.menu is not None:
                newMenuItem[ MENU_CHILDREN_LABEL ] = [ ]
                processMenuStructure_V2( newMenuItem[ MENU_CHILDREN_LABEL ],
                                         menu.menu,
                                         newMenuItem[ MENU_ID ] + '_' )

            if menu.hasBeforeAfter():
                index = -1
                if menu.after is not None:
                    for idx, menuItem in enumerate( items ):
                        if menuItem[ MENU_DISPLAY_NAME_V2 ] == menu.after:
                            index = idx + 1

                else: # before
                    for idx, menuItem in enumerate( items ):
                        if menuItem[ MENU_DISPLAY_NAME_V2 ] == menu.before:
                            index = idx

                items.insert( index, newMenuItem )

            else:
                items.insert( menu.index if menu.index >= 0 else (len( items ) + menu.index + 1), newMenuItem )

        return
    for cfg in config:
        if cfg.menu is None:
            continue
        processMenuStructure_V2( menuItems, cfg.menu )
    # write new global menu file based on the changes in the module yaml files
    with open( menuFilename, 'w' )  as stream:
        yaml.dump( menuItems, stream, default_style=False, default_flow_style=False )

    return


def updatePythonModels( config:  TemplateConfiguration ):
    modelsFilename = os.path.join( config.python.sourceFolder, config.application, 'modules.yaml' )
    if os.path.isfile( modelsFilename ):
        with open( modelsFilename, 'r' ) as stream:
            modules = yaml.load( stream, Loader = yaml.Loader )

    else:
        modules = []

    for cfg in config:
        """
        - module: testrun.cal
          model: Calendar
        """
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

    # Now generate the models.py module
    template = os.path.abspath( os.path.join( config.python.commonFolder, 'models.py.templ' ) )
    modeles_py_file = os.path.join( config.python.sourceFolder, config.application, 'models.py' )
    with open( modeles_py_file, 'w' ) as stream:
        stream.write( Template( filename = template ).render( config = config, modules = modules ) )

    return modules

def generatePython( config: TemplateConfiguration, templates: list ):
    constants = []
    logger.info( 'application : {0}'.format( config.application ) )
    dt = datetime.datetime.now()
    generationDateTime = dt.strftime( "%Y-%m-%d %H:%M:%S" )
    userName = os.path.split( os.path.expanduser( "~" ) )[ 1 ]
    modules = updatePythonModels( config )
    for cfg in config:
        modulePath = os.path.join( config.python.sourceFolder,
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
            if not os.path.isdir( config.python.sourceFolder ):
                os.makedirs( config.python.sourceFolder )

            if os.path.isdir( modulePath ) and not config.options.overWriteFiles:
                raise gencrud.util.exceptions.ModuleExistsAlready( cfg, modulePath )
            outputSourceFile = os.path.join( modulePath, gencrud.util.utils.sourceName( templ ) )
            if config.options.backupFiles:
                gencrud.util.utils.backupFile( outputSourceFile )
            if os.path.isfile( outputSourceFile ):
                # remove the file first
                os.remove( outputSourceFile )
            makePythonModules( config.python.sourceFolder, config.application, cfg.name )
            with open( outputSourceFile,
                       gencrud.util.utils.C_FILEMODE_WRITE ) as stream:
                for line in Template( filename = os.path.abspath( templ ) ).render( obj = cfg,
                                                                                    root = config,
                                                                                    modules = modules,
                                                                                    date = generationDateTime,
                                                                                    version = gencrud.version.__version__,
                                                                                    username = userName ).split( '\n' ):
                    stream.write( line )
                    if sys.platform.startswith( 'linux' ):
                        stream.write( '\n' )
        for column in cfg.table.columns:
            if column.ui is not None:
                if column.ui.hasResolveList():
                    constants.append( '# field {}.{} constants\n'.format( cfg.table.name, column.name ) )
                    for line in column.ui.createResolveConstants():
                        if line not in constants:
                            constants.append( line + '\n' )

                    constants.append( '\n' )
                    constants.append( "C_{}_MAPPING = {}\n".format( column.name,
                                                                    column.ui.resolveListPy ) )
                    constants.append( '\n\n' )

        if len( constants ) > 0:
            constants.insert( 0, '# Generated by gencrud\n' )
            filename = os.path.join( modulePath, 'constant.py' )
            if config.options.backupFiles:
                gencrud.util.utils.backupFile( filename )

            with open( filename, 'w' ) as stream:
                stream.writelines( constants )
        entryPointsFile = os.path.join( modulePath, 'entry_points.py' )
        if len( cfg.actions.getCustomButtons() ) > 0 and not os.path.isfile( entryPointsFile ):
            # use the template from 'common-py'
            templateFolder  = config.python.commonFolder
            templateFile    = os.path.join( templateFolder, 'entry-points.py.templ' )

            with open( entryPointsFile, gencrud.util.utils.C_FILEMODE_WRITE ) as stream:
                with open( templateFile, 'r' ) as templateStream:
                    for line in Template( templateStream ).render( obj = cfg, root = config ).split( '\n' ):
                        stream.write( line + '\n' )
    updatePythonProject( config, '' )
    return
