import os
import sys
import json
import pytemplate.utils
from pytemplate.positon import PositionInterface
from mako.template import Template


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
logger = logging.getLogger()


def registerApi( app, cors ):
    for module in listModules:
        module.registerApi( app, cors )

    return


def registerExtensions( app, db ):
    return


def registerShellContext( app, db ):
    return


def registerCommands( app ):
    return

'''

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

    # update import section
    modules = []
    for table in config:
        line = 'import {0}.{1} # import maintained by gencrud.py'.format( table.application, table.name )
        pytemplate.utils.insertLinesUnique( lines, rangePos, line )
        modules.append( '{0}.{1}'.format( table.application, table.name ) )

    sectionLines = pytemplate.utils.searchSection( lines,
                                                   rangePos,
                                                   'listModules = [',
                                                   ']' )
    pos = sectionLines[ 0 ].find( '[' )
    sectionLines[ 0 ] = sectionLines[ 0 ][ pos: ]
    sectionLines = json.loads( ''.join( sectionLines ) )
    for module in modules:
        if module not in sectionLines:
            sectionLines.append( module )

    sectionLines = json.dumps( sectionLines, indent = 4 ).split( '\n' )
    sectionLines[ 0 ] = 'listModules = ' + sectionLines[ 0 ]
    pytemplate.utils.replaceInList( lines, rangePos, sectionLines )

    sectionLines = pytemplate.utils.searchSection( lines,
                                                   rangePos,
                                                   'menuItems = [',
                                                   ']' )
    pos = sectionLines[ 0 ].find( '[' )
    sectionLines[ 0 ] = sectionLines[ 0 ][ pos: ]
    menuItems = json.loads( ''.join( sectionLines ) )

    def createMenuItem( cfg ):
        return { 'displayName': cfg.menuItem.displayName,
                 'iconName': cfg.menuItem.iconName,
                 'route': cfg.menuItem.route }

    def createRootMenuItem( cfg ):
        return { 'displayName': cfg.menu.displayName,
                 'iconName': cfg.menu.iconName,
                 'children': [ createMenuItem( cfg ) ] }

    for cfg in config:
        foundMenu = False
        for menuItem in menuItems:
            if menuItem[ 'displayName' ] == cfg.menu.displayName:
                foundMenu = True
                # Found the menu
                subMenuItems = menuItem[ 'children' ]
                foundSubMenu = False
                for subMenuItem in subMenuItems:
                    if subMenuItem[ 'displayName' ] == cfg.menuItem.displayName:
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


    menuItemsBlock = ("menuItems = " + json.dumps( menuItems, indent = 4 )).split( '\n' )
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
                    for imp in col.inports:
                        print( '  {0}  {1}'.format( *imp ) )

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

    for applic, module in modules:
        filename = os.path.join( config.python.source,
                                 applic, '__init__.py' )
        importStr = 'from {0}.{1} import *'.format( applic, module )
        lines = []
        if pytemplate.utils.verbose:
            print( 'Try to add "{0}"'.format( importStr ), file = sys.stderr )

        try:
            lines = open( filename, pytemplate.utils.C_FILEMODE_READ ).readlines()

        except:
            if pytemplate.utils.verbose:
                print( 'Error reading the file {0}'.format( filename ), file = sys.stdout )

        if pytemplate.utils.verbose:
            print( lines, file = sys.stdout )

        pytemplate.utils.insertLinesUnique( lines,
                                            PositionInterface( end = len( lines ) ),
                                            importStr )
        pytemplate.utils.backupFile( filename )
        open( filename, pytemplate.utils.C_FILEMODE_WRITE ).writelines( lines )

    updatePythonProject( config, '' )
    return


