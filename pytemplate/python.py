import os
import sys
import json
import pytemplate.utils
from pytemplate.positon import PositionInterface
from mako.template import Template

# TODO: Fix the position of the import statements in main.py

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


mainModuleText = '''import logging
##
#   Section maintained by gencrud.py
##
listModules = [

]

menuItems = [

]

##
#   End section maintained by gencrud.py
##
menuApi = Blueprint( 'menuApi', __name__ )
logger = logging.getLogger()


def registerApi( app, cors ):
    logger = app.logger
    for module in listModules:
        module.registerApi( app, cors )

    if app.config.get( 'ALLOW_CORS_ORIGIN', False ):
        app.logger.info( 'Allowing CORS' )
        if app.config.get( 'ALLOW_CORS_ORIGIN', False ):
            origins = app.config.get( 'CORS_ORIGIN_WHITELIST', '*' )
            cors.init_app( 'menuApi', origins = origins )

    logger.info( 'Register Menu route' )
    app.register_blueprint( menuApi )
    return


def registerExtensions( app, db ):
    return


def registerShellContext( app, db ):
    return


def registerCommands( app ):
    return

@menuApi.route( "/api/menu", methods=[ 'GET' ] )
def getUserMenu():
    return jsonify( menuItems )

'''
MENU_CHILDEREN_LABEL    = 'childeren'
MENU_DISPLAY_NAME       = 'displayName'
MENU_ICON_NAME          = 'iconName'
MENU_ROUTE              = 'route'
LABEL_LIST_MODULES      = 'listModules = ['
LABEL_MENU_ITEMS        = 'menuItems = ['
LABEL_END_LIST          = ']'

def updatePythonProject( config, app_module ):
    if pytemplate.utils.verbose:
        print( config.python.source )

    lines = []
    filename = os.path.join( config.python.source, config.application, 'main.py' )
    if os.path.isfile( filename ):
        lines = open( filename, 'r' ).readlines()
        pytemplate.utils.backupFile( filename )

    if len( lines ) <= 2:
        lines = mainModuleText.split( '\n' )
        lines = [ l + '\n' for l in lines ]

    rangePos            = PositionInterface()
    for lineNo, lineText in enumerate( lines ):
        if lineText.startswith( 'import' ):
            rangePos.end = lineNo

    rangePos.end += 1
    # update import section
    modules = []
    for table in config:
        line = 'import {0}.{1}   # import maintained by gencrud.py'.format( table.application, table.name )
        pytemplate.utils.insertLinesUnique( lines, rangePos, line )
        modules.append( '{0}.{1}'.format( table.application, table.name ) )

    sectionLines = pytemplate.utils.searchSection( lines,
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
    pytemplate.utils.replaceInList( lines, rangePos, sectionLines )

    sectionLines = pytemplate.utils.searchSection( lines,
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
                        # don't bother, its already there
                        break

                if not foundSubMenu:
                    # Add /insert the sub-menu
                    if cfg.menuItem.index < 0:
                        pos = len( subMenuItems ) + cfg.menuItem.index
                        if cfg.menu.index == -1 or pos > len( subMenuItems ):
                            subMenuItems.append( createMenuItem( cfg ) )

                        else:
                            subMenuItems.insert( pos, createMenuItem( cfg ) )

                    else:
                        subMenuItems.insert( cfg.menuItem.index, createMenuItem( cfg ) )


        if not foundMenu:
            if cfg.menu.index < 0:
                # from the end
                pos = len( menuItems ) + cfg.menu.index
                if cfg.menu.index == -1 or pos > len( menuItems ):
                    menuItems.append( createRootMenuItem( cfg ) )

                else:
                    menuItems.insert( pos, createRootMenuItem( cfg ) )

            else:
                # insert at
                menuItems.insert( cfg.menu.index, createRootMenuItem( cfg ) )


    menuItemsBlock = ( "menuItems = " + json.dumps( menuItems, indent = 4 )).split( '\n' )
    pytemplate.utils.replaceInList( lines, rangePos, menuItemsBlock )

    open( filename, 'w' ).writelines( lines )
    return


def generatePython( templates, config ):
    modules = []
    for cfg in config:
        backupDone = False
        for templ in templates:
            if pytemplate.utils.verbose:
                print( 'template    : {0}'.format( templ ) )
                print( 'application : {0}'.format( cfg.application ) )
                print( 'name        : {0}'.format( cfg.name ) )
                print( 'class       : {0}'.format( cfg.cls ) )
                print( 'table       : {0}'.format( cfg.table.tableName ) )
                for col in cfg.table.columns:
                    print( '- {0:<20}  {1}'.format( col.name, col.sqlAlchemyDef() ) )

                for imp in cfg.table.tsInports:
                    print( '  {0}  {1}'.format( imp.module, imp.name ) )

                for imp in cfg.table.pyInports:
                    print( '  {0}  {1}'.format( imp.module, imp.name ) )

                print( 'primary key : {0}'.format( cfg.table.primaryKey ) )
                print( 'uri         : {0}'.format( cfg.uri ) )

            if not os.path.isdir( config.python.source ):
                os.makedirs( config.python.source )

            modulePath = os.path.join( config.python.source,
                                   cfg.application,
                                   cfg.name )
            if os.path.isdir( modulePath ) and not pytemplate.utils.overWriteFiles:
                raise pytemplate.utils.ModuleExistsAlready( cfg, modulePath )

            makePythonModules( config.python.source, cfg.application, cfg.name )

            with open( os.path.join( modulePath, pytemplate.utils.sourceName( templ ) ), pytemplate.utils.C_FILEMODE_WRITE ) as stream:
                for line in Template( filename=os.path.abspath( templ ) ).render( obj = cfg ).split('\n'):
                    stream.write( line )

                # Open the __init__.py
                filename = os.path.join( modulePath, '__init__.py' )
                moduleName, _ = os.path.splitext( pytemplate.utils.sourceName( templ ) )
                importStr = 'from {0}.{1}.{2} import *'.format( cfg.application, cfg.name, moduleName )
                lines = []
                try:
                    lines = open( filename, pytemplate.utils.C_FILEMODE_READ ).readlines()

                except:
                    print( 'Error reading the file {0}'.format( filename ), file = sys.stdout )

                if pytemplate.utils.verbose:
                    print( lines, file = sys.stdout )

                pytemplate.utils.insertLinesUnique( lines,
                                                    PositionInterface( end = len( lines ) ),
                                                    importStr )
                if not backupDone:
                    pytemplate.utils.backupFile( filename )
                    modules.append( ( cfg.application, cfg.name ) )
                    backupDone = True

                open( filename, pytemplate.utils.C_FILEMODE_WRITE ).writelines( lines )

            if pytemplate.utils.verbose:
                print( '' )

    updatePythonProject( config, '' )
    return
