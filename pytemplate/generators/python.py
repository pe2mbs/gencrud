import json
import os
import sys
import logging
from mako.template import Template

import pytemplate.util.utils
import pytemplate.util.exceptions
from pytemplate.util.positon import PositionInterface

logger = logging.getLogger()

MENU_CHILDEREN_LABEL    = 'childeren'
MENU_DISPLAY_NAME       = 'displayName'
MENU_ICON_NAME          = 'iconName'
MENU_INDEX              = 'index'
MENU_ROUTE              = 'route'
LABEL_LIST_MODULES      = 'listModules = ['
LABEL_MENU_ITEMS        = 'menuItems = ['
LABEL_END_LIST          = ']'


def makePythonModules( root_path, *args ):
    def write__init__py():
        with open( os.path.join( root_path, '__init__.py' ), 'w+' ) as stream:
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


def updatePythonProject( config, app_module ):
    logger.debug( config.python.source )

    lines = []
    filename = os.path.join( config.python.source, config.application, 'main.py' )
    if os.path.isfile( filename ):
        lines = open( filename, 'r' ).readlines()
        pytemplate.util.utils.backupFile( filename )

    if len( lines ) <= 2:
        lines = open( os.path.join( os.path.dirname( __file__ ),
                                    '..',
                                    'common-py',
                                    'main.py' ), 'r' ).readlines()

    rangePos            = pytemplate.util.utils.findImportSection( lines )

    # update import section
    modules = []
    for table in config:
        line = 'import {0}.{1}   # import maintained by gencrud.py'.format( table.application, table.name )
        pytemplate.util.utils.insertLinesUnique( lines, rangePos, line )
        modules.append( '{0}.{1}'.format( table.application, table.name ) )

    sectionLines = pytemplate.util.utils.searchSection( lines,
                                                        rangePos,
                                                        LABEL_LIST_MODULES,
                                                        LABEL_END_LIST )
    del sectionLines[ 0 ]
    del sectionLines[ -1 ]
    for line in sectionLines:
        line = line.strip( ' ,\n' )
        if line not in modules:
            modules.append( line )

    sectionLines = [ LABEL_LIST_MODULES + '\n' ]
    for idx, mod in enumerate( modules ):
        sectionLines.append( '    {0}{1}\n'.format( mod,
                                                    '' if len( modules )-1 == idx else ',' ) )

    sectionLines.append( LABEL_END_LIST + '\n' )
    pytemplate.util.utils.replaceInList( lines, rangePos, sectionLines )

    sectionLines = pytemplate.util.utils.searchSection( lines,
                                                        rangePos,
                                                        LABEL_MENU_ITEMS,
                                                        LABEL_END_LIST )
    pos = sectionLines[ 0 ].find( '[' )
    sectionLines[ 0 ] = sectionLines[ 0 ][ pos: ]
    try:
        menuItems = json.loads( ''.join( sectionLines ) )

    except:
        print( ''.join( sectionLines ) )
        raise

    def createMenuItem( cfg ):
        return { MENU_DISPLAY_NAME: cfg.menuItem.displayName,
                 MENU_ICON_NAME: cfg.menuItem.iconName,
                 MENU_ROUTE: cfg.menuItem.route }

    def createRootMenuItem( cfg ):
        return { MENU_DISPLAY_NAME: cfg.menu.displayName,
                 MENU_ICON_NAME: cfg.menu.iconName,
                 MENU_CHILDEREN_LABEL: [ createMenuItem( cfg ) ] }

    for cfg in config:
        if cfg.menu is None:
            continue

        foundMenu = False
        for menuItem in menuItems:
            if menuItem[ MENU_DISPLAY_NAME ] == cfg.menu.displayName:
                foundMenu = True
                # Found the menu
                subMenuItems = menuItem[ MENU_CHILDEREN_LABEL ]
                foundSubMenu = False
                for subMenuItem in subMenuItems:
                    if subMenuItem[ MENU_DISPLAY_NAME ] == cfg.menuItem.displayName:
                        foundSubMenu = True
                        # update the route and icon information
                        subMenuItem[ MENU_ICON_NAME ]   = cfg.menuItem.iconName
                        subMenuItem[ MENU_ROUTE ]       = cfg.menuItem.route
                        # don't bother, its already there
                        break

                if not foundSubMenu:
                    # Add /insert the sub-menu
                    if cfg.menuItem.index < 0:
                        idx = ( len( subMenuItems ) + cfg.menuItem.index ) + 1

                    else:
                        idx = cfg.menuItem.index

                    subMenuItems.insert( idx, createMenuItem( cfg ) )
                    break

        if not foundMenu:
            if cfg.menu.index < 0:
                # from the end
                pos = ( len( menuItems ) + cfg.menu.index + 1 )

            else:
                pos = cfg.menu.index

            # insert at
            menuItems.insert( cfg.menu.index, createRootMenuItem( cfg ) )

    for idx, menuItem in enumerate( menuItems ):
        menuItem[ MENU_INDEX ] = idx
        if MENU_CHILDEREN_LABEL in menuItem:
            # Re-number the submenu
            for idx, subMenuItem in enumerate( menuItem[ MENU_CHILDEREN_LABEL ] ):
                subMenuItem[ MENU_INDEX ] = idx

    menuItemsBlock = ( "menuItems = " + json.dumps( menuItems, indent = 4 )).split( '\n' )
    pytemplate.util.utils.replaceInList( lines, rangePos, menuItemsBlock )

    open( filename, 'w' ).writelines( lines )
    return


def generatePython( templates, config ):
    modules = []
    for cfg in config:
        backupDone = False
        modulePath = os.path.join( config.python.source,
                                   cfg.application,
                                   cfg.name )
        for templ in templates:
            logger.info( 'template    : {0}'.format( templ ) )
            logger.info( 'application : {0}'.format( cfg.application ) )
            logger.info( 'name        : {0}'.format( cfg.name ) )
            logger.info( 'class       : {0}'.format( cfg.cls ) )
            logger.info( 'table       : {0}'.format( cfg.table.tableName ) )
            for col in cfg.table.columns:
                logger.info( '- {0:<20}  {1}'.format( col.name, col.sqlAlchemyDef() ) )

            for imp in cfg.table.tsInports:
                logger.info( '  {0}  {1}'.format( imp.module, imp.name ) )

            for imp in cfg.table.pyInports:
                logger.info( '  {0}  {1}'.format( imp.module, imp.name ) )

            logger.info( 'primary key : {0}'.format( cfg.table.primaryKey ) )
            logger.info( 'uri         : {0}'.format( cfg.uri ) )

            if not os.path.isdir( config.python.source ):
                os.makedirs( config.python.source )

            if os.path.isdir( modulePath ) and not pytemplate.util.utils.overWriteFiles:
                raise pytemplate.util.exceptions.ModuleExistsAlready( cfg, modulePath )

            makePythonModules( config.python.source, cfg.application, cfg.name )

            with open( os.path.join( modulePath, pytemplate.util.utils.sourceName( templ ) ), pytemplate.util.utils.C_FILEMODE_WRITE ) as stream:
                for line in Template( filename=os.path.abspath( templ ) ).render( obj = cfg ).split('\n'):
                    stream.write( line )

                # Open the __init__.py
                filename = os.path.join( modulePath, '__init__.py' )
                moduleName, _ = os.path.splitext( pytemplate.util.utils.sourceName( templ ) )
                importStr = 'from {0}.{1}.{2} import *'.format( cfg.application, cfg.name, moduleName )
                lines = []
                try:
                    lines = open( filename, pytemplate.util.utils.C_FILEMODE_READ ).readlines( )

                except:
                    logger.error( 'Error reading the file {0}'.format( filename ), file = sys.stdout )

                logger.info( lines )
                pytemplate.util.utils.insertLinesUnique( lines,
                                                         PositionInterface( end = len( lines ) ),
                                                         importStr )
                if not backupDone:
                    pytemplate.util.utils.backupFile( filename )
                    modules.append( ( cfg.application, cfg.name ) )
                    backupDone = True

                open( filename, pytemplate.util.utils.C_FILEMODE_WRITE ).writelines( lines )

        entryPointsFile = os.path.join( modulePath, 'entry_points.py' )
        if len( cfg.actions.getCustomButtons() ) > 0 and not os.path.isfile( entryPointsFile ):
            # use the template from 'common-py'
            templateFolder  = os.path.abspath( os.path.join( os.path.dirname( __file__ ), '..', 'common-py' ) )
            templateFile    = os.path.join( templateFolder, 'entry-points.py.templ' )

            with open( entryPointsFile, pytemplate.util.utils.C_FILEMODE_WRITE ) as stream:
                for line in Template( filename = templateFile ).render( obj = cfg ).split( '\n' ):
                    stream.write( line + '\n' )

    updatePythonProject( config, '' )
    return
