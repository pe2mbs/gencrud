import json
import os
import shutil
import sys
from mako.template import Template
import pytemplate.util.utils
from pytemplate.generators.typescript_obj import TypeScript
from pytemplate.util.positon import PositionInterface
from pytemplate.util.sha import sha256sum

LABEL_APP_ROUTES    = 'const appRoutes: Routes ='
LABEL_NG_MODULE     = '@NgModule('
APP_MODULE          = 'app.module.ts'
APP_ROUTING_MODULE  = 'app.routingmodule.ts'
NG_ENTRY_COMPONENTS = 'entryComponents'
NG_IMPORTS          = 'imports'
NG_PROVIDERS        = 'providers'
NG_DECLARATIONS     = 'declarations'


def makeAngularModule( root_path, *args ):
    if len( args ) > 0:
        modulePath = os.path.join( root_path, args[ 0 ] )
        if not os.path.isdir( modulePath ):
            os.mkdir( modulePath )

        makeAngularModule( modulePath, *args[ 1: ] )

    return


def updateImportSection( lines, files ):
    rangePos = PositionInterface()
    stage = 0
    for lineNo, lineText in enumerate( lines ):
        lineText = lineText.strip( ' \n' )
        if stage == 0 and lineText.startswith( 'import' ):
            if lineText.endswith( ';' ):
                rangePos.end = lineNo

            else:
                stage = 1

        elif stage == 1:
            if lineText.endswith( ';' ):
                stage = 0
                rangePos.end = lineNo

    rangePos.end += 1
    for imp in files:
        foundLine = False
        for lineNo in rangePos.range():
            if imp in lines[ lineNo ]:
                foundLine = True
                break

        if not foundLine:
            lines.insert( rangePos.end, imp + '\n' )
            rangePos.end += 1


def updateAngularAppModuleTs( config, app_module, exportsModules ):
    if pytemplate.util.utils.verbose:
        print( config.angular.source )

    # File to edit 'app.module.ts'
    # inject the following;
    #   inport
    #   declarations:       search for 'declarations: ['
    #   imports:            search for 'imports: ['
    #   providers:          search for 'providers: ['
    #   entryComponents:    search for 'entryComponents: ['
    with open( os.path.join( config.angular.source, APP_MODULE ), 'r' ) as stream:
        lines = stream.readlines()

    pytemplate.util.utils.backupFile( os.path.join( config.angular.source, APP_MODULE ) )
    rangePos        = PositionInterface()
    sectionLines    = pytemplate.util.utils.searchSection( lines,
                                                           rangePos,
                                                           LABEL_NG_MODULE + '{',
                                                      '})' )
    pos = sectionLines[0].find( '{' )
    sectionLines[ 0 ] = sectionLines[ 0 ][ pos: ]
    pos = sectionLines[ -1 ].find( '}' )
    sectionLines[ -1 ] = sectionLines[ -1 ][ : pos + 1 ]

    ts = TypeScript()
    NgModule = ts.parse( ''.join( sectionLines ) )

    def updateNgModule( section ):
        for decl in app_module[ section ]:
            if decl != '' and decl not in NgModule[ section ]:
                NgModule[ section ].append( decl )

    updateNgModule( NG_DECLARATIONS )
    updateNgModule( NG_PROVIDERS )
    updateNgModule( NG_IMPORTS )
    updateNgModule( NG_ENTRY_COMPONENTS )

    buffer = LABEL_NG_MODULE + ts.build( NgModule, 2 ) + ')'
    bufferLines = [ '{}\n'.format ( x ) for x in buffer.split( '\n' ) ]
    pytemplate.util.utils.replaceInList( lines, rangePos, bufferLines )

    updateImportSection( lines, app_module[ 'files' ] )
    with open( os.path.join( config.angular.source, APP_MODULE ), 'w' ) as stream:
        for line in lines:
            stream.write( line )
            if pytemplate.util.utils.verbose:
                print( line, end = '' )

    return


def updateAngularAppRoutingModuleTs( config, app_module ):
    if not os.path.isfile( os.path.join( config.angular.source, APP_ROUTING_MODULE ) ):
        return

    with open( os.path.join( config.angular.source, APP_ROUTING_MODULE ), 'r' ) as stream:
        lines = stream.readlines()

    pytemplate.util.utils.backupFile( os.path.join( config.angular.source, APP_ROUTING_MODULE ) )

    imports = []
    entries = []
    for cfg in config:
        print( cfg.application, cfg.name, cfg.cls )
        imports.append( "import {{ {cls}TableComponent }} from './{app}/{mod}/table.component';".format( cls = cfg.cls ,
                                                                                                         app = cfg.application,
                                                                                                         mod = cfg.name ) )
        if cfg.menuItem is not None:
            entries.append( {
                'path': "'{}'".format( cfg.menuItem.route[1:] ),
                'component': '{cls}TableComponent'.format( cls = cfg.cls ),
                'data': { 'title': "'{cls} table'".format( cls = cfg.cls ) }
            } )

    rangePos = PositionInterface()
    sectionLines = pytemplate.util.utils.searchSection( lines,
                                                        rangePos,
                                                        LABEL_APP_ROUTES,
                                                   ']' )
    pos = sectionLines[ 0 ].find( '[' )
    sectionLines[ 0 ] = sectionLines[ 0 ][ pos: ]
    pos = sectionLines[ -1 ].find( ']' )
    sectionLines[ -1 ] = sectionLines[ -1 ][ : pos + 1 ]

    ts = TypeScript()
    appRoutes = ts.parse( ''.join( sectionLines ) )
    for entry in entries:
        if pytemplate.util.utils.verbose:
            print( entry )

        found = False
        for route in appRoutes:
            if route[ 'path' ] == entry[ 'path' ]:
                found = True
                break

        if not found:
            appRoutes.insert( -1, entry )

    if pytemplate.util.utils.verbose:
        print( '' )

    buffer = LABEL_APP_ROUTES + ' ' + ts.build( appRoutes, 2 ) + ';'
    bufferLines = [ '{}\n'.format( x ) for x in buffer.split( '\n' ) ]
    pytemplate.util.utils.replaceInList( lines, rangePos, bufferLines )

    updateImportSection( lines, imports )
    with open( os.path.join( config.angular.source, APP_ROUTING_MODULE ), 'w' ) as stream:
        for line in lines:
            stream.write( line )
            if pytemplate.util.utils.verbose:
                print( line, end = '' )

    return


def exportAndType( line ):
    return line.split( ' ' )[ 1 : 3 ]


def generateAngular( templates, config ):
    modules = []
    if not os.path.isdir( config.angular.source ):
        os.makedirs( config.angular.source )

    for cfg in config:
        modulePath = os.path.join( config.angular.source, cfg.application, cfg.name )
        if os.path.isdir( modulePath ) and not pytemplate.util.utils.overWriteFiles:
            raise pytemplate.util.utils.ModuleExistsAlready( cfg, modulePath )

        makeAngularModule( config.angular.source, cfg.application, cfg.name )
        for templ in templates:
            templateFilename = os.path.join( config.angular.source,
                                             cfg.application,
                                             cfg.name,
                                             pytemplate.util.utils.sourceName( templ ) )
            if os.path.isfile( templateFilename ):
                # First remove the old file
                os.remove( templateFilename )

            if 'dialog' in templ:
                if 'addedit' in templ:
                    if not ( cfg.actions.valid( 'new', 'dialog' ) or cfg.actions.valid( 'edit', 'dialog' ) ):
                        continue

                elif 'delete' in templ:
                    if not cfg.actions.valid( 'delete', 'dialog' ):
                        continue

            elif 'screen' in templ:
                if 'addedit' in templ:
                    if not ( cfg.actions.valid( 'new', 'screen' ) or cfg.actions.valid( 'edit', 'screen' ) ):
                        continue

                elif 'delete' in templ:
                    if not cfg.actions.valid( 'delete', 'screen' ):
                        continue

            if pytemplate.util.utils.verbose:
                print( 'template    : {0}'.format( templ ) )
                print( 'application : {0}'.format( cfg.application ) )
                print( 'name        : {0}'.format( cfg.name ) )
                print( 'class       : {0}'.format( cfg.cls ) )
                print( 'table       : {0}'.format( cfg.table.name ) )
                for col in cfg.table.columns:
                    print( '- {0:<20}  {1}'.format( col.name, col.sqlAlchemyDef() ) )

                for imp in cfg.table.tsInports:
                    print( '  {0}  {1}'.format( imp.module, imp.name ) )

                for imp in cfg.table.pyInports:
                    print( '  {0}  {1}'.format( imp.module, imp.name ) )

                print( 'primary key : {0}'.format( cfg.table.primaryKey ) )
                print( 'uri         : {0}'.format( cfg.uri ) )


            with open( templateFilename,
                       pytemplate.util.utils.C_FILEMODE_WRITE ) as stream:

                for line in Template( filename = os.path.abspath( templ ) ).render( obj = cfg ).split( '\n' ):
                    if line.startswith( 'export ' ):
                        modules.append( (cfg.application,
                                         cfg.name,
                                         pytemplate.util.utils.sourceName( templ ),
                                         exportAndType( line ) ) )

                    stream.write( line )
                    if sys.platform.startswith( 'linux' ):
                        stream.write( '\n' )

            if pytemplate.util.utils.verbose:
                print( '' )

    appModule = None
    exportsModules = []
    for app, mod, source, export in modules:
        app_module_json_file = os.path.join( config.angular.source,
                                           app, mod, 'app.module.json' )
        if os.path.isfile( app_module_json_file ):
            with open( app_module_json_file, 'r' ) as stream:
                try:
                    data = json.load( stream )

                except:
                    print( "Error in file: {0}".format( app_module_json_file ) )
                    raise

                if appModule is None:
                    appModule = data

                else:
                    appModule = pytemplate.util.utils.joinJson( appModule, data )

            os.remove( app_module_json_file )

        exportsModules.append( { 'application':   app,
                                 'modules':       mod,
                                 'source':        source,
                                 'export':        export } )

    with open( os.path.join( config.angular.source, 'app.module.json' ), 'w' ) as stream:
        json.dump( appModule, stream, indent = 4 )

    if pytemplate.util.utils.verbose:
        print( 'exportsModules' )

    for mod in exportsModules:
        if pytemplate.util.utils.verbose:
            print( mod )

    if pytemplate.util.utils.verbose:
        print( 'appModule' )

    for mod in appModule:
        if pytemplate.util.utils.verbose:
            print( mod )


    updateAngularAppModuleTs( config, appModule, exportsModules )
    updateAngularAppRoutingModuleTs( config, appModule )

    os.remove( os.path.join( config.angular.source, 'app.module.json' ) )
    copyAngularCommon( os.path.abspath( os.path.join( os.path.dirname( __file__ ), '..', 'common-ts' ) ),
                       os.path.join( config.angular.source, 'common' ) )
    return

def copyAngularCommon( source, destination ):
    files = os.listdir( source )
    for filename in files:
        if not os.path.isfile( os.path.join( destination, filename ) ) and \
               os.path.isfile( os.path.join( source, filename ) ):
            if pytemplate.util.utils.verbose:
                print( "Copy new file {0} => {1}".format( os.path.join( source, filename ),
                                                          os.path.join( destination, filename ) ) )
            shutil.copy( os.path.join( source, filename ),
                         os.path.join( destination, filename ) )

        elif os.path.isfile( os.path.join( destination, filename ) ):
            if sha256sum( os.path.join( destination, filename ) ) != sha256sum( os.path.join( source, filename ) ):
                # Hash differs, therefore replace the file
                if pytemplate.util.utils.verbose:
                    print( "Hash differs, therefore replace the file {0} => {1}".format( os.path.join( source, filename ),
                                                                                     os.path.join( destination, filename ) ) )
                shutil.copy( os.path.join( source, filename ),
                             os.path.join( destination, filename ) )

            elif pytemplate.util.utils.verbose:
                print( "{0} is the same {1}".format( os.path.join( source, filename ),
                                                     os.path.join( destination, filename ) ) )

        elif os.path.isdir( os.path.join( destination, filename ) ):
            copyAngularCommon( os.path.join( source, filename ), os.path.join( destination, filename ) )

    return