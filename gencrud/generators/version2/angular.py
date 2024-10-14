import os.path
import shutil
import typing as t
import logging
import subprocess
import posixpath
from shutil import which
from datetime import datetime
from mako.template import Template
from mako.exceptions import text_error_template
from gencrud.util.exceptions import ModuleExistsAlready, MissingTemplateAttribute
# from gencrud.config.angular import AngularModule
# from gencrud.config.column import TemplateColumn
# from gencrud.config.object import TemplateObject
# from gencrud.config.service import TemplateService
from gencrud.configuraton import TemplateConfiguration
from gencrud.generators.servicelist import ServicesList, buildServiceLists
from gencrud.generators.version2.boilerplate import BOILERPLATE
from gencrud.generators.version2.angular_classes.route import Route, ROUTE_MODULE_TS
from gencrud.constants import *
import gencrud.version
import gencrud.util.utils


logger = logging.getLogger( 'gengrud.generate.angular' )


def routingModule( routing_ts: str, module: str, route: t.Union[ Route, t.List[ Route ] ], relative_path: str,
                   default_routing_ts: t.Optional[ str ] = None, service: t.Optional[ str ] = '', overwrite: bool = False ):
    # Read the routing file
    logger.info( f"Writing: {routing_ts} for module {service if service != '' else module}" )
    path = os.path.split( routing_ts )[ 0 ]
    if not os.path.exists( path ):
        os.makedirs( path )

    if os.path.exists( routing_ts ) and not overwrite:
        if os.path.exists( f"{routing_ts}.bak" ):
            os.remove( f"{routing_ts}.bak" )

        with open( routing_ts, 'r' ) as stream:
            text = stream.read().replace( '\r','' )

        # os.rename(routing_ts, f"{routing_ts}.bak")
        if f'{module}RoutingModule' not in text:
            raise Exception( f"Wrong module class {module}RoutingModule was not found" )

        routing_lines = text.split('\n')

    else:
        if isinstance( default_routing_ts, str ) and os.path.exists( default_routing_ts ):
            # Load template
            routing_lines = Template( filename = default_routing_ts ).render( module = module,
                                                                              rootRelative = relative_path,
                                                                              service = service ).split( '\n' )

        else:
            # Create new routing file
            routing_lines = Template( text = BOILERPLATE + ROUTE_MODULE_TS ).render( module = module,
                                                                                     rootRelative=relative_path,
                                                                                     service = service ).split( '\n' )

    if isinstance( route, list ):
        # generate the routes
        for _route in route:
            routing_lines = _route.updateRouteModule( routing_lines )

    else:
        # generate the route
        routing_lines = route.updateRouteModule( routing_lines )

    # Write the routing file
    with open( routing_ts, 'w', newline='' ) as stream:
        stream.write( '\n'.join( routing_lines ) )

    logger.debug( '\n'.join( routing_lines ) )
    return


def subModule( module_ts: str, module: str, objects: dict, relative_path: str,
               default_module_ts: t.Optional[ str ] = None,
               service: t.Optional[ str ] = '', overwrite: bool = False ):
    logger.info( f"Writing file {module_ts}")
    try:
        text = Template(filename=default_module_ts).render(module=module,
                                                           service=service,
                                                           rootRelative=relative_path,
                                                           objects=objects)
    except Exception:
        raise Exception( text_error_template().render() )

    if not os.path.exists( module_ts ) or overwrite:
        if os.path.exists( f"{module_ts}.bak" ):
            os.remove( f"{module_ts}.bak" )

        if os.path.exists( module_ts ):
            os.rename(module_ts, f"{module_ts}.bak")

        with open( module_ts, 'w', newline='' ) as stream:
            stream.write( text )

    logger.debug( text )
    return


def makeAngularClassName( name: str ):
    return name.title().replace('-','').replace('_','').replace('.','')


def makePosixPath( path: str, *args ):
    if path[1] == ':':
        path = path[2:]

    path = path.replace( '\\','/' )
    if len( args ) > 0:
        return posixpath.join( path, *args )

    return path


def getRelativePath( src, dst ):
    if dst.lower().endswith( ( '.ts', '.html' ) ):
        return posixpath.relpath( src, posixpath.split( dst )[ 0 ] )

    return posixpath.relpath( src, dst )


class ProviderList( list ):
    def __init__( self ):
        super().__init__()
        return

    def append( self, obj ):
        for duplicate in self:
            if obj[0] == duplicate[0]:
                # All ready in the provider list
                return

        return super().append( obj )


def generateAngularRouting( config: TemplateConfiguration ):
    for obj in config.objects:
        declarations = [ ( f"{ obj.cls }TableComponent", './table.component' ) ]
        entryComponents = []
        moduleFolder = makePosixPath( config.Interface.Frontend.Path, obj.name )
        moduleRoutes = []
        actionRoute = Route()
        # Set up the route for the table overview
        actionRoute.setComponent( '', f'{obj.cls}TableComponent', './table.component')
        # Get the relative path of the root project for the current output file, here a dummy filename is used
        if obj.hasGuard():
            actionRoute.addCanActivate( obj.Guard.Class, posixpath.relpath( obj.Guard.Filename, moduleFolder ) )

        moduleRoutes.append( actionRoute )
        for action in obj.actions:
            if action.type == 'screen':
                if f"{ obj.cls }ScreenComponent" not in [ item[ 0 ] for item in declarations ]:
                    declarations.append( ( f"{ obj.cls }ScreenComponent", './screen.component' ) )

                actionRoute = Route()
                # Setup the specific route for the action
                if action.route is None:
                    raise MissingTemplateAttribute(f"action.route.class is missing for {action.name} ")

                actionRoute.setComponent( action.name, action.route.Class, f'./screen.component' )
                if obj.hasGuard():
                    actionRoute.addCanActivate( obj.Guard.Class, posixpath.relpath( obj.Guard.Filename, moduleFolder ) )

                moduleRoutes.append( actionRoute )

            elif action.type == 'dialog' and not action.hasApiFunction():
                if f"{obj.cls}DialogComponent" not in [item[0] for item in entryComponents]:
                    entryComponents.append( ( f"{obj.cls}DialogComponent", './dialog.component' ) )

        # # Remove if route file it exists, the module routing we just rebuild every time
        # filename = makePosixPath( config.angular.sourceFolder, moduleFolder, f"{obj.name}-routing.module.ts" )
        # if os.path.exists( filename ):
        #     os.remove( filename )
        #
        # # Build a new routing module
        # # Get the relative path of the root project for the current output file
        # relative = getRelativePath( makePosixPath( config.angular.sourceFolder ), filename )
        # routingModule( filename, obj.cls, moduleRoutes, relative,
        #                default_routing_ts = os.path.join( config.angular.templateFolder,
        #                                                   config.Interface.Frontend.Templates.get( 'route' ) ),
        #                service = f"{config.Interface.Backend.Path}/{obj.name}",
        #                overwrite = True )
        #
        # filename = makePosixPath( config.angular.sourceFolder, moduleFolder, f"module.ts" )
        # if os.path.exists(filename):
        #     os.remove( filename )
        #
        # module = posixpath.split(obj.route)[-1]
        # providers = ProviderList()
        # providers.append( ( f"{obj.cls}DataService", f'./service' ) )
        # # find all services used, as we need to attach in the 'providers' section of the module.ts
        # for column in obj.table.columns:
        #     column: TemplateColumn
        #     if column.hasService():
        #         service: TemplateService = column.ui.service
        #         relativeFilename = getRelativePath( makePosixPath( config.angular.sourceFolder, service.path ),
        #                                             makePosixPath( config.angular.sourceFolder, moduleFolder ) )
        #         service.RelativePath = relativeFilename
        #         providers.append( ( service.cls, relativeFilename.replace( '.ts', '' ) ) )
        #
        # if obj.hasProviders():
        #     for provider in obj.Providers:
        #         providers.append( ( provider.Class, provider.Filename.replace( '.ts', '' ) ) )
        #
        # imports = [
        #     ( f'{obj.cls}RoutingModule', f'./{obj.name}-routing.module' )
        # ]
        # for import_module in obj.modules:
        #     import_module: AngularModule
        #     # TODO: This need to be a relative path to be resolved
        #     moduleFilename = os.path.join( config.angular.sourceFolder, import_module.path )
        #     relative = getRootRelativePath( config, moduleFilename )
        #     _, localDir = moduleFilename.rsplit( '/', 1 )
        #     imports.append( ( import_module.cls, posixpath.join( relative, localDir, 'module' ) ) )
        #
        # if obj.injection.hasModuleTs():
        #     for inject in obj.injection.moduleTs:
        #         declarations.append( ( inject.cls, inject.file ) )
        #
        # objects = {
        #     "imports":          imports,
        #     "declarations":     declarations,
        #     "entryComponents":  entryComponents,
        #     "providers":        providers
        # }
        # # Get the relative path of the root project for the current output file
        # relative = getRelativePath(makePosixPath(config.angular.sourceFolder), filename)
        # subModule(  filename, obj.cls, objects, relative,
        #             default_module_ts = os.path.join( config.angular.templateFolder,
        #                                               config.Interface.Frontend.Templates.get('module') ),
        #             service = f"{config.Interface.Backend.Path}/{obj.name}",
        #             overwrite = True )
        # # Set up the segmented lazy loaded module, this routing shall be modified

        moduleFolder = makePosixPath( config.Interface.Frontend.Path )
        className = makeAngularClassName(config.Interface.Frontend.Path)

        moduleRoute = Route()
        guard = None
        # Write the pre-module package (routing & module)
        _, path = obj.route.rsplit( '/', 1 )
        moduleRoute.setLazyLoadedModule( path, f'./{obj.name}/module', obj.cls )
        filename = makePosixPath( config.angular.sourceFolder, moduleFolder, f'{config.Interface.Frontend.Path}-routing.module.ts')
        relative = getRelativePath( makePosixPath( config.angular.sourceFolder ), filename )
        if obj.hasGuard():
            guard = ( obj.Guard.Class, posixpath.join( relative, obj.Guard.Filename ) )

        if isinstance( guard, tuple ):
            moduleRoute.addCanActivate( *guard )

        routingModule( filename, className, moduleRoute, relative,
                       default_routing_ts=os.path.join( config.angular.templateFolder,
                                                        config.Interface.Frontend.Templates.get('sub-route') ) )

        # Get the relative path of the root project for the current output file
        filename = makePosixPath(config.angular.sourceFolder, moduleFolder,
                                 f'{config.Interface.Frontend.Path}.module.ts')
        templateFile = os.path.join(config.angular.templateFolder, 'extra', 'module.module.ts.templ')
        # Get the relative path of the root project for the current output file
        relative = getRelativePath(makePosixPath(config.angular.sourceFolder), filename)
        subModule( filename, className, { "imports": [ ( f'{className}RoutingModule',
                                                         f'./{config.Interface.Frontend.Path}-routing.module' ) ] },
                   relative,
                   default_module_ts = templateFile,
                   service = f"{config.Interface.Backend.Path}",
                   overwrite = False )

        # The last part to add/update the app-routing.module
        moduleRoute = Route()
        # Set up the lazy loaded in the app routing, this routing shall be modified
        module = config.Interface.Frontend.Path
        moduleClass = makeAngularClassName( module )
        moduleRoute.setLazyLoadedModule( module, f'./{module}/{module}.module', moduleClass )
        filename = os.path.join( config.angular.sourceFolder, 'app-routing.module.ts'  )
        routingModule( filename, 'App', moduleRoute, "." )

    return

def generateAngular( config: TemplateConfiguration, templates: list, angular_config: dict ):
    generateAngularRouting( config )
    dt = datetime.now()
    generationDateTime = dt.strftime("%Y-%m-%d %H:%M:%S")
    userName = os.path.split(os.path.expanduser("~"))[1]
    for cfg in config:
        moduleFolder = makePosixPath( config.angular.sourceFolder,
                                     config.Interface.Frontend.Path,
                                     cfg.name )
        if os.path.isdir( moduleFolder ) and not config.options.overWriteFiles:
            raise gencrud.util.exceptions.ModuleExistsAlready( cfg, moduleFolder )

        if not os.path.exists( moduleFolder ):
            os.makedirs( moduleFolder )

        logger.info( f'module      : {moduleFolder}')
        logger.info( f'name        : {cfg.name}')
        logger.info( f'class       : {cfg.cls}')
        logger.info( f'table       : {cfg.table.name}')
        for col in cfg.table.columns:
            logger.info( f'- {col.name:<20}: {col.tsType}')

        logger.info('primary key : {0}'.format(cfg.table.primaryKey))
        logger.info('uri         : {0}'.format(cfg.uri))
        servicesList, fullServiceList = buildServiceLists(cfg.table.columns)
        for template in templates:
            if os.path.isdir( template ) or cfg.ignoreTemplates(template):
                continue

            logger.info( template )
            sourceFilename = makePosixPath( config.angular.sourceFolder,
                                                 config.Interface.Frontend.Path,
                                                 cfg.name,
                                                 gencrud.util.utils.sourceName(template))

            if not config.options.overWriteFiles and os.path.isfile(sourceFilename):
                continue

            logger.info('template    : {0}'.format(template))
            # if config.options.backupFiles:
            #     gencrud.util.utils.backupFile(sourceFilename)
            #
            # if os.path.isfile(sourceFilename):
            #     # First remove the old file
            #     os.remove(sourceFilename)

            logger.debug('Action new  : {0}'.format(cfg.actions.get(C_NEW).type))
            logger.debug('Action edit : {0}'.format(cfg.actions.get(C_EDIT).type))
            if C_SCREEN in template:
                if not ( C_SCREEN in template and C_SCREEN in ( cfg.actions.get(C_NEW).type, cfg.actions.get(C_EDIT).type ) ):
                    logger.info("Not adding {}".format(template))
                    continue

                logger.debug("Adding screen for {}".format(template))

            elif C_DIALOG in template:
                if C_COMPONENT in template and C_DIALOG in (cfg.actions.get(C_NEW).type, cfg.actions.get(C_EDIT).type):
                    logger.info("Adding dialog for {}".format(template))

                elif C_DELETE in template and cfg.actions.get( C_DELETE ).type == C_DIALOG:
                    logger.info("Adding dialog for {}".format(template))

                else:
                    logger.debug("Not adding {}".format(template))
                    continue

            relative = getRelativePath( makePosixPath( config.angular.sourceFolder ), sourceFilename )
            filename, fileext = os.path.splitext(sourceFilename)
            sourceFilenameTmp = f"{filename}.new{fileext}"
            with open( sourceFilenameTmp, gencrud.util.utils.C_FILEMODE_WRITE + 'b' ) as stream:
                try:
                    templateData = Template( filename = os.path.abspath( template ) ).render( obj= cfg,
                                                                     root = config,
                                                                     version = gencrud.version.__version__,
                                                                     username = userName,
                                                                     rootRelative = relative,
                                                                     services = servicesList,
                                                                     allServices = fullServiceList,
                                                                     date = generationDateTime)
                    stream.write( templateData.encode('utf-8') )

                except Exception:
                    logger.error( f"Mako exception on { template }:" )
                    logger.error( text_error_template().render_unicode() )
                    logger.error( "Mako done" )
                    raise

            if sourceFilename.lower().endswith( ('.html','.ts' ) ):
                # execute prettier to format the Typescript and HTML code.
                prettier = which( 'prettier' )
                if isinstance( prettier, str ) and os.path.exists( os.path.join( config.python.sourceFolder, '.prettierrc.yaml' ) ):
                    # Prettier installed,
                    logger.info( f"Using {prettier} to format the code {os.path.basename( sourceFilename )}" )
                    result = subprocess.Popen( ( prettier, '--write', sourceFilenameTmp ),
                                               shell = True,
                                               stdout = subprocess.PIPE,
                                               stderr = subprocess.STDOUT )
                    for line in result.stdout.readlines():
                        logger.info( line.decode('utf-8') )

                    result.wait()

            if sourceFilename.lower().endswith('.ts'):
                if not gencrud.util.utils.compareAngularFile(sourceFilenameTmp, sourceFilename):
                    if os.path.exists( sourceFilename ):
                        os.remove(sourceFilename)

                    shutil.copy( sourceFilenameTmp, sourceFilename )

            elif sourceFilename.lower().endswith('.html'):
                if not gencrud.util.utils.compareHtmlFile(sourceFilenameTmp, sourceFilename):
                    if os.path.exists( sourceFilename ):
                        os.remove(sourceFilename)

                    shutil.copy(sourceFilenameTmp, sourceFilename)

            else:
                if os.path.exists(sourceFilename):
                    os.remove(sourceFilename)

                shutil.copy(sourceFilenameTmp, sourceFilename)

            os.remove(sourceFilenameTmp)

        logger.debug( f"Module {cfg.name} folder: {moduleFolder}" )
        # Now check if there are any mixin's missing
        if cfg.mixin.angular.hasTableComponent():
            filename = os.path.abspath( os.path.join( moduleFolder, cfg.mixin.angular.TableComponent.actualFilename ) )
            if not os.path.exists( filename ):
                logger.warning( f'Missing angular table mixin: { filename }' )

        if cfg.mixin.angular.hasScreenComponent():
            filename = os.path.abspath( os.path.join(moduleFolder, cfg.mixin.angular.ScreenComponent.actualFilename ) )
            if not os.path.exists( filename ):
                logger.warning( f'Missing angular component mixin: { filename }' )

        if cfg.mixin.angular.hasComponentDialog():
            filename = os.path.abspath( os.path.join(moduleFolder, cfg.mixin.angular.ComponentDialog.actualFilename ) )
            if not os.path.exists( filename ):
                logger.warning( f'Missing angular dialog mixin: { filename }' )

        if len( cfg.Declare.Module ) > 0:
            for declare in cfg.Declare.Module:
                filename = os.path.abspath( os.path.join(moduleFolder, declare.actualFilename) )
                if not os.path.exists( filename ):
                    logger.warning( f'Missing angular module: { filename } for component { declare.cls }' )

        if len( cfg.Declare.Component ) > 0:
            for declare in cfg.Declare.Component:
                filename = os.path.abspath( os.path.join(moduleFolder, declare.actualFilename) )
                if not os.path.exists( filename ):
                    logger.warning( f'Missing angular declaration: { filename } for component { declare.cls }' )

        if len( cfg.Declare.Service ) > 0:
            for declare in cfg.Declare.Service:
                filename = os.path.abspath( os.path.join(moduleFolder, declare.actualFilename) )
                if not os.path.exists( filename ):
                    logger.warning( f'Missing angular service: { filename } for component { declare.cls }' )


    return

