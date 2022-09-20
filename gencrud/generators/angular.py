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
import shutil
import logging
import datetime
import gencrud.version
from mako.template import Template
from mako import exceptions
import gencrud.util.utils
import gencrud.util.exceptions
from gencrud.constants import *
from gencrud.configuraton import TemplateConfiguration
from gencrud.util.typescript import TypeScript
from gencrud.util.positon import PositionInterface
from gencrud.util.sha import sha256sum
import posixpath
import time

logger = logging.getLogger()

LABEL_APP_ROUTES    = 'const appRoutes: Routes ='
LABEL_NG_MODULE     = '@NgModule('
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


def updateAngularAppModuleTs( config: TemplateConfiguration, app_module, exportsModules ):
    del exportsModules  # unused
    # File to edit 'app.module.ts'
    # inject the following;
    #   inport
    #   declarations:       search for 'declarations: ['
    #   imports:            search for 'imports: ['
    #   providers:          search for 'providers: ['
    #   entryComponents:    search for 'entryComponents: ['
    with open( os.path.join( config.angular.sourceFolder,
                             config.references.app_module.filename ), 'r' ) as stream:
        lines = stream.readlines()

    if config.options.backupFiles:
        gencrud.util.utils.backupFile( os.path.join( config.angular.sourceFolder,
                                                     config.references.app_module.filename ) )

    rangePos        = PositionInterface()
    sectionLines    = gencrud.util.utils.searchSection( lines,
                                                        rangePos,
                                                        LABEL_NG_MODULE + '{',
                                                      '})' )
    pos = sectionLines[ 0 ].find( '{' )
    sectionLines[ 0 ] = sectionLines[ 0 ][ pos: ]
    pos = sectionLines[ -1 ].find( '}' )
    sectionLines[ -1 ] = sectionLines[ -1 ][ : pos + 1 ]

    ts = TypeScript()
    NgModule = ts.parse( ''.join( sectionLines ) )

    def updateNgModule( section ):
        injectPoint = -1
        for idx, decl in enumerate( app_module[ section ] ):
            if config.references.app_routing.module in decl:
                injectPoint = idx

        for decl in app_module[ section ]:
            if decl != '' and decl not in NgModule[ section ]:
                NgModule[ section ].insert( injectPoint, decl )

    updateNgModule( NG_DECLARATIONS )
    updateNgModule( NG_PROVIDERS )
    updateNgModule( NG_IMPORTS )
    updateNgModule( NG_ENTRY_COMPONENTS )

    buffer = LABEL_NG_MODULE + ts.build( NgModule, 2 ) + ')'
    bufferLines = [ '{}\n'.format( x ) for x in buffer.split( '\n' ) ]
    gencrud.util.utils.replaceInList( lines, rangePos, bufferLines )

    updateImportSection( lines, app_module[ 'files' ] )
    with open( os.path.join( config.angular.sourceFolder,
                             config.references.app_module.filename ), 'w' ) as stream:
        for line in lines:
            stream.write( line )
            logger.debug( line.replace( '\n', '' ) )

    return


def updateAngularAppRoutingModuleTs( config: TemplateConfiguration, app_module ):
    if config.options.useModule:
        return []

    del app_module  # unused
    if not os.path.isfile( os.path.join( config.angular.sourceFolder,
                                         config.references.app_routing.module ) ):
        return []

    with open( os.path.join( config.angular.sourceFolder,
                             config.references.app_routing.module ), 'r' ) as stream:
        lines = stream.readlines()

    if config.options.backupFiles:
        gencrud.util.utils.backupFile( os.path.join( config.angular.sourceFolder,
                                                     config.references.app_routing.module ) )

    imports = []
    entries = []
    for cfg in config:
        if cfg.menu is not None and cfg.menu.menu is not None:
            # Do we have child pages for new and edit?
            if not config.options.useModule:
                children = []
                for action in cfg.actions:
                    logger.info( "Action: {} {} {}".format( config.application, cfg.name, action ) )
                    if action.type == 'screen' and action.isAngularRoute():
                        logger.info( "Screen {} {} {}".format( config.application, cfg.name, action ) )
                        children.append( {  'path': "'{}'".format( action.route.name ),
                                            'component': "{}".format( action.route.cls ),
                                            'data': {
                                                'title': "'{cls} {label}'".format( cls = cfg.cls,
                                                                                   label = action.route.label ),
                                                'breadcrum': "'{}'".format( action.route.label )
                                            }
                                          } )
                        filename = 'table.component' if action.route.cls.endswith( 'TableComponent' ) else 'screen.component'
                        clsmod = cfg.name if action.route.module is None else action.route.module
                        component = "import {{ {cls} }} from './{app}/{module}/{filename}';".format( cls = action.route.cls,
                                                                                                     app = config.application,
                                                                                                     module = clsmod,
                                                                                                     filename = filename )
                        if component not in imports:
                            imports.append( component )

                # Get the actual route
                m = cfg.menu
                while m.menu is not None:
                    m = m.menu

                logger.info( "Action children: {} path {}".format( json.dumps( children, indent = 4 ),
                                                                   m.route[ 1: ] ) )
                if len( children ) > 0:
                    children.insert( 0, {
                        'path':      "''",
                        'component': '{cls}TableComponent'.format( cls = cfg.cls ),
                        'data':      { 'title':     "'{cls} table'".format( cls = cfg.cls ),
                                       'breadcrum': "'{}'".format( cfg.cls ) }
                    } )
                    routeItem = { 'path': "'{}'".format( m.route[ 1: ] ), 'children': children }

                else:
                    routeItem = {
                        'path':      "'{}'".format( m.route[ 1: ] ),
                        'component': '{cls}TableComponent'.format( cls = cfg.cls ),
                        'data':      { 'title':     "'{cls} table'".format( cls = cfg.cls ),
                                       'breadcrum': "'{}'".format( cfg.cls ) }
                    }

                entries.append( routeItem )

            elif not config.options.lazyLoading:
                routeItem = "{}Route".format( cfg.name )

                entries.append( routeItem )

            elif config.options.lazyLoading:
                # Get the actual route
                m = cfg.menu
                while m.menu is not None:
                    m = m.menu

                routeItem = {
                    "path": "'{}'".format( m.route[ 1: ] ),
                    "data": {
                        "breadcrumb": "'{cls} table'".format( cls = cfg.cls ),
                        "title":      "'{cls} table'".format( cls = cfg.cls ),
                    },
                    "loadChildren": "() => import( './{app}/{mod}/module' ).then( mod =>  mod.{cls}Module )".format(
                        app = config.application,
                        mod = cfg.name,
                        cls = cfg.cls
                    )
                }
                entries.append( routeItem )

        logger.info( "Inports: {} {} {}".format( config.application, cfg.name, cfg.cls ) )
        if config.options.useModule and config.options.lazyLoading:
            component = "import {{ {cls}TableComponent }} from './{app}/{mod}/table.component';".format( cls = cfg.cls,
                                                                                                         app = config.application,
                                                                                                         mod = cfg.name )

        elif config.options.useModule:
            component = "import {{ {cls}Module }} from './{app}/{mod}.module';".format( cls = cfg.cls,
                                                                                        app = config.application,
                                                                                        mod = cfg.name )

        else:
            component = "import {{ {cls}TableComponent }} from './{app}/{mod}/table.component';".format( cls = cfg.cls,
                                                                                                         app = config.application,
                                                                                                         mod = cfg.name )

        if component not in imports:
            imports.append( component )

    rangePos = PositionInterface()
    sectionLines = gencrud.util.utils.searchSection( lines,
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
        logger.debug( "Route: {}".format( json.dumps( entry ) ) )

        routeIdx = -1
        for idx, route in enumerate( appRoutes ):
            if route == entry:
                logger.error( "Found route: {}".format( route ) )
                logger.error( json.dumps( appRoutes ) )
                routeIdx = idx
                break

            if route[ C_PATH ] == entry:
                logger.info( "Found route: {}".format( route[ C_PATH ] ) )
                logger.info( json.dumps( appRoutes ) )
                routeIdx = idx
                break

        if routeIdx == -1:
            appRoutes.insert( -1, entry )

        else:
            appRoutes[ routeIdx ] = entry

    buffer = LABEL_APP_ROUTES + ' ' + ts.build( appRoutes, 2 ) + ';'
    bufferLines = [ '{}\n'.format( x ) for x in buffer.split( '\n' ) ]
    gencrud.util.utils.replaceInList( lines, rangePos, bufferLines )

    updateImportSection( lines, imports )
    with open( os.path.join( config.angular.sourceFolder, config.references.app_routing.module ), 'w' ) as stream:
        for line in lines:
            stream.write( line )
            logger.debug( line.replace( '\n', '' ) )

    return imports


def exportAndType( line ):
    return line.split( ' ' )[ 1: 3 ]

class ComponentsModules( list ):
    def append( self, new_item ):
        for app, name, source, exportType in list( self ):
            logger.info( "Component {} - {} - {} - {}".format( app, name, source, exportType ) )
            if not ( new_item[0] == app and new_item[1] == name and new_item[2] == source and new_item[3] == exportType ):
                logger.info("Adding component: {} - {} - {} - {}".format(*new_item))
                list.append( self, new_item )
                return

        if len( list( self ) ) == 0:
            logger.info("Adding component: {} - {} - {} - {}".format(*new_item))
            list.append( self, new_item )

        else:
            logger.error( "NOT ADDED COMPONENT {} - {} - {} - {}".format( *new_item ) )

        return

class ServicesList( list ):
    def __init__( self ):
        self.__mapper = {}
        super( ServicesList, self ).__init__()
        return

    def append( self, new_item ):
        if new_item.mapperName in self.__mapper:
            logger.error("NOT ADDED SERVICE {}".format( new_item ) )
            return

        logger.info("Adding service: {}".format( new_item ) )
        idx = len( self )
        list.append( self, new_item )
        self.__mapper[ new_item.mapperName ] = idx
        return

    def unique( self, *args ):
        logger.debug("ServicesList.unique: {}".format( args ) )
        intermediate  = {}
        for service in list( self ):
            key = ''.join( [ v for k, v in service.dictionary.items() if k in args ] )
            logger.debug( "ServicesList.service: {} => {} | {}".format( service, args, key ) )
            if key == '':
                continue

            intermediate[ key ] = service

        logger.debug("ServicesList.unique => {}".format( intermediate.values() ) )
        return intermediate.values()

    @property
    def externalService(self) -> str:
        FILLER = ( ' ' * 17 ) + ', '
        FILLER_LF = '\r\n{}'.format( FILLER )
        result = []
        for service in list( self.unique( 'class', 'name' ) ):
            result.append( 'public {name}Service: {cls}'.format( name = service.name, cls = service.cls ) )

        return (FILLER if len(result) > 0 else '') + (FILLER_LF.join(result))


def generateAngular( config: TemplateConfiguration, templates: list ):
    modules = ComponentsModules()
    if not os.path.isdir( config.angular.sourceFolder ):
        os.makedirs( config.angular.sourceFolder )

    dt = datetime.datetime.now()
    generationDateTime = dt.strftime( "%Y-%m-%d %H:%M:%S" )
    userName = os.path.split( os.path.expanduser( "~" ) )[ 1 ]
    for cfg in config:
        modulePath = os.path.join( config.angular.sourceFolder,
                                   config.application,
                                   cfg.name )
        if os.path.isdir( modulePath ) and not config.options.overWriteFiles:
            raise gencrud.util.exceptions.ModuleExistsAlready( cfg, modulePath )

        makeAngularModule( config.angular.sourceFolder,
                           config.application,
                           cfg.name )
        logger.info( 'application : {0}'.format( config.application ) )
        logger.info( 'name        : {0}'.format( cfg.name ) )
        logger.info( 'class       : {0}'.format( cfg.cls ) )
        logger.info( 'table       : {0}'.format( cfg.table.name ) )
        for col in cfg.table.columns:
            logger.info( '- {0:<20}: {1}'.format( col.name, col.tsType ) )

        logger.info( 'primary key : {0}'.format( cfg.table.primaryKey ) )
        logger.info( 'uri         : {0}'.format( cfg.uri ) )

        servicesList = ServicesList()
        for field in cfg.table.columns:
            if field.ui is not None and field.ui.isUiType(C_CHOICE, C_CHOICE_AUTO, C_COMBOBOX, C_COMBO, C_CHECKBOX) and field.hasService():
                field.ui.service.fieldLabel = field.label
                servicesList.append( field.ui.service )
            # required ad-on for the support of siblings, i.e., multiple usage of the same database field
            for sibling in field.siblings:
                if sibling.ui is not None and sibling.ui.isUiType(C_CHOICE, C_CHOICE_AUTO, C_COMBOBOX, C_COMBO, C_CHECKBOX) and sibling.hasService():
                    sibling.ui.service.fieldLabel = sibling.label
                    servicesList.append( sibling.ui.service )

        for templ in templates:
            templateFilename = os.path.join( config.angular.sourceFolder,
                                             config.application,
                                             cfg.name,
                                             gencrud.util.utils.sourceName( templ ) )
            if cfg.ignoreTemplates( templ ):
                continue

            if not config.options.overWriteFiles and os.path.isfile( templateFilename ):
                continue

            logger.info( 'template    : {0}'.format( templ ) )
            if config.options.backupFiles:
                gencrud.util.utils.backupFile( templateFilename )

            if os.path.isfile( templateFilename ):
                # First remove the old file
                os.remove( templateFilename )

            logger.info( 'template    : {0}'.format( templ ) )
            if C_SCREEN in templ:
                logger.debug( 'Action new  : {0}'.format( cfg.actions.get( C_NEW ).type ) )
                logger.debug( 'Action edit : {0}'.format( cfg.actions.get( C_EDIT ).type ) )
                if C_SCREEN in templ and C_SCREEN in (cfg.actions.get( C_NEW ).type, cfg.actions.get( C_EDIT ).type ):
                    logger.debug( "Adding screen for {}".format( templ ) )

                else:
                    logger.info( "Not adding {}".format( templ ) )
                    continue

            elif C_DIALOG in templ:
                logger.debug( 'Action new  : {0}'.format( cfg.actions.get( C_NEW ).type ) )
                logger.debug( 'Action edit : {0}'.format( cfg.actions.get( C_EDIT ).type ) )
                if C_COMPONENT in templ and C_DIALOG in ( cfg.actions.get( C_NEW ).type, cfg.actions.get( C_EDIT ).type ):
                    logger.info( "Adding dialog for {}".format( templ ) )

                elif C_DELETE in templ and cfg.actions.get( C_DELETE ).type == C_DIALOG:
                    logger.info( "Adding dialog for {}".format( templ ) )

                else:
                    logger.debug( "Not adding {}".format( templ ) )
                    continue

            else:
                pass

            with open( templateFilename, gencrud.util.utils.C_FILEMODE_WRITE ) as stream:
                try:
                    for line in Template( filename = os.path.abspath( templ ) ).render( obj = cfg,
                                                                                        root = config,
                                                                                        version = gencrud.version.__version__,
                                                                                        username = userName,
                                                                                        services = servicesList,
                                                                                        date = generationDateTime ).split( '\n' ):

                        if line.startswith( 'export ' ):
                            modules.append( ( config.application,
                                              cfg.name,
                                              gencrud.util.utils.sourceName( templ ),
                                              exportAndType( line ) ) )

                        stream.write( line )
                        if gencrud.util.utils.get_platform() == C_PLATFORM_LINUX:
                            stream.write( '\n' )

                except Exception:
                    logger.error( "Mako exception:" )
                    for line in exceptions.text_error_template().render_unicode().encode('ascii').split(b'\n'):
                        logger.error( line )

                    logger.error( "Mako done" )
                    raise

    appModule = {}
    exportsModules = []
    for app, mod, source, export in modules:
        # Update 'app.module.json'
        app_module_json_file = os.path.join( config.angular.sourceFolder,
                                             app,
                                             mod,
                                             'app.module.json' )
        if os.path.isfile( app_module_json_file ):
            with open( app_module_json_file, 'r' ) as stream:
                try:
                    data = json.load( stream )

                except Exception:
                    logger.error( "Error in file: {0}".format( app_module_json_file ) )
                    raise

                if appModule is None:
                    appModule = data

                else:
                    appModule = gencrud.util.utils.joinJson( appModule, data )

            # This is just to give the OS some time to actually close the file
            time.sleep(.01)
            os.remove( app_module_json_file )

        exportsModules.append( { 'application':   app,
                                 'modules':       mod,
                                 'source':        source,
                                 'export':        export } )

    # We need to un-double the 'files' entry
    newFiles = []
    for entry in appModule[ 'files' ]:
        if entry not in newFiles:
            newFiles.append( entry )

    appModule[ 'files' ] = newFiles
    # Write update 'app.module.json'
    with open( os.path.join( config.angular.sourceFolder, 'app.module.json' ), 'w' ) as stream:
        json.dump( appModule, stream, indent = 4 )

    logger.info( 'exportsModules' )
    for mod in exportsModules:
        logger.info( "exportsModule: {}".format( mod ) )

    logger.info( 'appModules: {}'.format( json.dumps( appModule, indent = 4 ) ) )
    for mod in appModule:
        logger.info( "appModule: {}".format( mod.strip( '\n' ) ) )

    imports = updateAngularAppRoutingModuleTs( config, appModule )
    for imp in imports:
        if imp not in appModule[ 'files' ]:
            appModule[ 'files' ].append( imp )

    appModule = createAngularComponentModuleTs( config, appModule )
    logger.info( "appModule: {}".format( json.dumps( appModule, indent = 4 ) ) )
    updateAngularAppModuleTs( config, appModule, exportsModules )

    os.remove( os.path.join( config.angular.sourceFolder, 'app.module.json' ) )
    copyAngularCommon( config, config.angular.commonFolder,
                       os.path.join( config.angular.sourceFolder, 'common' ) )
    return


def createAngularComponentModuleTs( config: TemplateConfiguration, appModule: dict ):
    if not config.options.useModule or not config.options.overWriteFiles:
        return appModule

    dt = datetime.datetime.now()
    generationDateTime = dt.strftime( "%Y-%m-%d %H:%M:%S" )
    userName = os.path.split( os.path.expanduser( "~" ) )[ 1 ]
    templ = os.path.abspath( os.path.join( config.angular.templateFolder, 'module.ts.templ' ) )
    imports = []
    files = []
    for cfg in config:
        filename = os.path.join( config.angular.sourceFolder,
                                 config.application,
                                 cfg.name,
                                 'module.ts'.format( cfg.name ) )
        if config.options.backupFiles:
            gencrud.util.utils.backupFile( filename )

        # Create the 'module.ts'
        with open( filename, 'w' ) as stream:
            # for item in cfg.modules.items:
            #     print( item )

            try:
                for line in Template( filename = templ ).render( obj = cfg,
                                                                 root = config,
                                                                 username = userName,
                                                                 date = generationDateTime,
                                                                 version = gencrud.version.__version__ ).split( '\n' ):
                    stream.write( line )
                    if gencrud.util.utils.get_platform() == C_PLATFORM_LINUX:
                        stream.write( '\n' )

            except Exception:
                logger.error("Mako exception:")
                for line in exceptions.text_error_template().render_unicode().encode('ascii').split(b'\n'):
                    logger.error(line)

                logger.error("Mako done")
                raise

        component = "import {{ {cls}Module }} from './{app}/{mod}/module';".format( cls = cfg.cls,
                                                                                    app = config.application,
                                                                                    mod = cfg.name )
        if component not in files:
            files.append( component )

        imp = "{cls}Module".format( cls = cfg.cls )
        if imp not in imports:
            imports.append( imp )

        # for mod in cfg.modules:
        #     if mod.cls not in imports:
        #         imports.append( mod.cls )
        #         files.append( "import {{ {modCls} }} from '{path}';".format( modCls = mod.cls,
        #                                                                      path = mod.importPath ) )

    appModule = {
        "files": [  "import { BrowserModule } from '@angular/platform-browser';",
                    "import { BrowserAnimationsModule } from '@angular/platform-browser/animations';",
                    "import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';",
                    "import { FormsModule, ReactiveFormsModule } from '@angular/forms';",
                    "import { CustomMaterialModule } from './material.module';",
                    "import { GenCrudModule } from './common/gencrud.module';",
                   ],
        "declarations": [],
        "imports": [ "BrowserModule",
                     "BrowserAnimationsModule",
                     "HttpClientModule",
                     "FormsModule",
                     "ReactiveFormsModule",
                     "CustomMaterialModule",
                     "GenCrudModule" ],

        "entryComponents": [ ],
            "providers": [
                { "multi": "true",
                  "provide": "HTTP_INTERCEPTORS",
                  "useClass": "AuthInterceptorService"
                } ]
    }

    for imp in files:
        if imp not in appModule[ 'files' ]:
            appModule[ 'files' ].append( imp )

    for imp in imports:
        if imp not in appModule[ 'imports' ]:
            appModule[ 'imports' ].append( imp )

    return appModule


def copyAngularCommon( config, source, destination ):
    files = os.listdir( source )
    for filename in files:
        if filename == 'gencrud.module.ts' and not config.options.useModule:
            continue

        if not os.path.isfile( os.path.join( destination, filename ) ) and \
               os.path.isfile( os.path.join( source, filename ) ):
            logger.debug( "Copy new file {0} => {1}".format( os.path.join( source, filename ),
                                                      os.path.join( destination, filename ) ) )
            if not os.path.isdir( destination ):
                os.makedirs( destination )

            shutil.copy( os.path.join( source, filename ),
                         os.path.join( destination, filename ) )

        elif os.path.isfile( os.path.join( destination, filename ) ):
            if sha256sum( os.path.join( destination, filename ) ) != sha256sum( os.path.join( source, filename ) ):
                # Hash differs, therefore replace the file
                logger.debug( "Hash differs, replace the file {0} => {1}".format( os.path.join( source, filename ),
                                                                                  os.path.join( destination, filename ) ) )
                shutil.copy( os.path.join( source, filename ),
                             os.path.join( destination, filename ) )

            else:
                logger.debug( "{0} is the same {1}".format( os.path.join( source, filename ),
                                                     os.path.join( destination, filename ) ) )

        elif os.path.isdir( os.path.join( source, filename ) ):
            copyAngularCommon( config, os.path.join( source, filename ), os.path.join( destination, filename ) )

    return
