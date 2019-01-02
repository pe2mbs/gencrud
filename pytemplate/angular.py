import json
import shutil
import yaml
import os
import io
import sys
import pytemplate.utils
from pytemplate.typescript_obj import TypeScript
from mako.template import Template
from pytemplate.positon import PositionInterface

def makeAngularModule( root_path, *args ):
    if len( args ) > 0:
        modulePath = os.path.join( root_path, args[ 0 ] )
        if not os.path.isdir( modulePath ):
            os.mkdir( modulePath )

        makeAngularModule( modulePath, *args[ 1: ] )

    return


def updateAngularProject( config, app_module ):
    if pytemplate.utils.verbose:
        print( config.angular.source )
    # File to edit 'app.module.ts'
    # inject the following;
    #   inport
    #   declarations:       search for 'declarations: ['
    #   imports:            search for 'imports: ['
    #   providers:          search for 'providers: ['
    #   entryComponents:    search for 'entryComponents: ['
    with open( os.path.join( config.angular.source, 'app.module.ts' ), 'r' ) as stream:
        lines = stream.readlines()

    pytemplate.utils.backupFile( os.path.join( config.angular.source, 'app.module.ts' ) )
    rangePos        = PositionInterface()

    sectionLines    = pytemplate.utils.searchSection( lines,
                                                      rangePos,
                                                      '@NgModule({',
                                                      '})' )
    pos = sectionLines[0].find( '{' )
    sectionLines[ 0 ] = sectionLines[ 0 ][ pos: ]
    pos = sectionLines[ -1 ].find( '}' )
    sectionLines[ -1 ] = sectionLines[ -1 ][ : pos + 1 ]

    ts = TypeScript()
    NgModule = ts.parse( ''.join( sectionLines ) )

    for decl in app_module[ 'declarations' ]:
        if decl != '' and decl not in NgModule[ 'declarations' ]:
            NgModule[ 'declarations' ].append( decl )

    for decl in app_module[ 'providers' ]:
        if decl != '' and decl not in NgModule[ 'providers' ]:
            NgModule[ 'providers' ].append( decl )

    for decl in app_module[ 'imports' ]:
        if decl != '' and decl not in NgModule[ 'imports' ]:
            NgModule[ 'imports' ].append( decl )

    for decl in app_module[ 'entryComponents' ]:
        if decl != '' and decl not in NgModule[ 'entryComponents' ]:
            NgModule[ 'entryComponents' ].append( decl )

    buffer = '@NgModule(' + ts.build( NgModule, 2 ) + ')'
    bufferLines = [ '{}\n'.format ( x ) for x in buffer.split( '\n' ) ]
    pytemplate.utils.replaceInList( lines, rangePos, bufferLines )

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
    for imp in app_module[ 'files' ]:
        foundLine = False
        for lineNo in rangePos.range():
            if imp in lines[ lineNo ]:
                foundLine = True
                break

        if not foundLine:
            lines.insert( rangePos.end + 1, imp + '\n' )
            rangePos.end += 1

    with open( os.path.join( config.angular.source, 'app.module.ts' ), 'w' ) as stream:
        for line in lines:
            stream.write( line )
            if pytemplate.utils.verbose:
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
        if os.path.isdir( modulePath ) and not pytemplate.utils.overWriteFiles:
            raise pytemplate.utils.ModuleExistsAlready( cfg, modulePath )

        makeAngularModule( config.angular.source, cfg.application, cfg.name )
        for templ in templates:
            if pytemplate.utils.verbose:
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

            with open( os.path.join( config.angular.source,
                                     cfg.application,
                                     cfg.name, pytemplate.utils.sourceName( templ ) ),
                       pytemplate.utils.C_FILEMODE_WRITE ) as stream:

                for line in Template( filename = os.path.abspath( templ ) ).render( obj = cfg ).split( '\n' ):
                    if line.startswith( 'export ' ):
                        modules.append( ( cfg.application,
                                          cfg.name,
                                          pytemplate.utils.sourceName( templ ),
                                          exportAndType( line ) ) )

                    stream.write( line )
                    if sys.platform.startswith( 'linux' ):
                        stream.write( '\n' )

            if pytemplate.utils.verbose:
                print( '' )

    appModule = None
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
                    appModule = pytemplate.utils.joinJson( appModule, data )

            os.remove( app_module_json_file )

        if 'exports' in appModule:
            appModule[ 'exports' ].append( { 'application':   app,
                                             'modules':       mod,
                                             'source':        source,
                                             'export':        export } )

        else:
            appModule[ 'exports' ] = [ { 'application':   app,
                                         'modules':       mod,
                                         'source':        source,
                                         'export':        export } ]

    with open( os.path.join( config.angular.source, 'app.module.json' ), 'w' ) as stream:
        json.dump( appModule, stream, indent = 4 )

    updateAngularProject( config, appModule )
    os.remove( os.path.join( config.angular.source, 'app.module.json' ) )
    # Now copy the common files from common-ts to

    if os.path.isdir( os.path.join( config.angular.source, 'common' ) ):
        if pytemplate.utils.overWriteFiles:
            shutil.rmtree( os.path.join( config.angular.source, 'common' ) )

            shutil.copytree( os.path.abspath( os.path.join( os.path.dirname( __file__ ), 'common-ts' ) ),
                     os.path.join( config.angular.source, 'common' ) )

    else:
        shutil.copytree( os.path.abspath( os.path.join( os.path.dirname( __file__ ), 'common-ts' ) ),
                         os.path.join( config.angular.source, 'common' ) )

    return
