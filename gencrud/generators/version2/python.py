import typing as t
from datetime import datetime
from mako.template import Template
import gencrud.version
import gencrud.util.utils
import gencrud.util.exceptions
import logging
import platform
import os.path
from gencrud.generators.version2.boilerplate import BOILERPLATE
import gencrud.myyaml as yaml
from gencrud.configuraton import TemplateConfiguration, TemplateObject


logger = logging.getLogger( 'gencrud.python' )
logger.setLevel( logging.DEBUG )


def generatePython( config: TemplateConfiguration, templates: t.List[ str ], flask_config: dict ):
    constants = []
    logger.info( f'interface : { config.Interface.Module }' )
    dt = datetime.now()
    generationDateTime = dt.strftime("%Y-%m-%d %H:%M:%S")
    userName = os.path.split(os.path.expanduser("~"))[1]
    if not os.path.exists( config.python.sourceFolder ):
        os.makedirs( config.python.sourceFolder )

    moduleFolder    = os.path.join( config.python.sourceFolder, config.Interface.Backend )
    modulePackage   = config.Interface.Module
    if not os.path.exists( moduleFolder ):
        os.makedirs( moduleFolder )

    modelsFilename = os.path.join( moduleFolder, 'models.py' )
    dbModels = BOILERPLATE.split( '\n' )
    if os.path.isfile( modelsFilename ):
        with open( modelsFilename, 'r' ) as stream:
            dbModels = stream.read().replace('\r','').split( '\n' )

    moduleInit  = BOILERPLATE.split( '\n' ) + [ '#', f'# Created by gencrud {generationDateTime} by {userName}' '#', '', '', 'def registerApis():', '    return' ]
    if os.path.exists( os.path.join( moduleFolder, '__init__.py' ) ):
        with open( os.path.join( moduleFolder, '__init__.py' ), 'r' ) as stream:
            moduleInit = stream.read().replace('\r','').split( '\n' )

    modules = flask_config.setdefault( 'API_MODULE', [] )
    if config.Interface.Backend not in modules:
        # Add the module to the API_MODULE loading list
        modules.append( config.Interface.Backend.replace( '/','.' ).replace( '\\','.' ) )

    backend = config.Interface.Backend.replace('/', '.').replace('\\', '.')
    modules = []
    for cfg in config:  # This iterates over the objects
        # Do the module __init__.py handling
        modules.append( {   'module': f"{ backend }.{ cfg.name }",
                            'model': cfg.cls,
                            'table': cfg.table.name.lower() } )

        module_import = f"import { backend }.{ cfg.name }.view"
        if module_import not in moduleInit:
            # Find last inport
            idx = 0
            imp = 0
            while idx < len( moduleInit ):
                if moduleInit[ idx ].startswith( '#' ):
                    # Skip the line
                    pass

                elif moduleInit[ idx ].startswith( 'import' ):
                    imp = 1

                elif imp == 1 and moduleInit[ idx ].strip() == '':
                    moduleInit.insert( idx, module_import )
                    imp = 2
                    break

                idx += 1

            if imp == 1:
                if len( moduleInit ) == 7:
                    # New file
                    moduleInit.insert( 3, module_import )
                    idx = 3

                else:
                    raise Exception( "Could not find import section" )

            # Now add the registerApi() call
            while idx < len( moduleInit ):
                if moduleInit[ idx ].startswith( "    return" ):
                    moduleInit.insert( idx, f"    { backend }.{ cfg.name }.view.registerApi()" )
                    imp = 3
                    break

                idx += 1

            if imp != 3:
                raise Exception("Could not find return")

        # Do the module - submodule handling
        module_models = f"from { backend }.{ cfg.name }.model import { cfg.cls }, { cfg.cls }Memory"
        if module_models not in dbModels:
            dbModels.append( f"# Table: { cfg.table.name.lower() }" )
            dbModels.append( module_models )

    NEWLINE = "\r\n" if platform.system() == 'Windows' else "\n"
    with open( os.path.join( moduleFolder, '__init__.py' ), 'w', newline = '' ) as stream:
        stream.write( NEWLINE.join( moduleInit ) )

    with open( os.path.join( moduleFolder, 'models.py' ), 'w', newline = '' ) as stream:
        stream.write( NEWLINE.join( dbModels ) )

    for cfg in config:  # This iterates over the objects
        cfg: TemplateObject
        modulePath = os.path.abspath( os.path.join( moduleFolder, cfg.name ) )
        for template in templates:
            if cfg.ignoreTemplates( template ):
                continue

            logger.info( f'template    : {template}' )
            if not os.path.exists( modulePath ):
                os.makedirs( modulePath )

            if not config.options.overWriteFiles:
                raise gencrud.util.exceptions.ModuleExistsAlready( cfg, modulePath )

            outputSourceFile = os.path.join( modulePath, gencrud.util.utils.sourceName( template ) )
            if config.options.backupFiles:
                gencrud.util.utils.backupFile(outputSourceFile)

            if os.path.isfile(outputSourceFile):
                # remove the file first
                os.remove(outputSourceFile)

            makoTemplate = Template( filename = template )
            with open( os.path.join( modulePath, outputSourceFile ), 'w', newline = '' ) as stream:
                stream.write( makoTemplate.render( obj = cfg,
                                                   root = config,
                                                   modules = modules,
                                                   date = generationDateTime,
                                                   version = gencrud.version.__version__,
                                                   username = userName ) )

    return

    #
    #
    #
    #
    # modules = updatePythonModels( config )
    # for cfg in config:
    #     modulePath = os.path.join(config.python.sourceFolder,
    #                               config.application,
    #                               cfg.name)
    #     logger.info('name        : {0}'.format(cfg.name))
    #     logger.info('class       : {0}'.format(cfg.cls))
    #     logger.info('table       : {0}'.format(cfg.table.tableName))
    #     logger.info('primary key : {0}'.format(cfg.table.primaryKey))
    #     logger.info('uri         : {0}'.format(cfg.uri))
    #     for col in cfg.table.columns:
    #         logger.info('- {0:<20}  {1}'.format(col.name, col.sqlAlchemyDef()))
    #
    #     for templ in templates:
    #         if cfg.ignoreTemplates(templ):
    #             continue
    #         logger.info('template    : {0}'.format(templ))
    #         if not os.path.isdir(config.python.sourceFolder):
    #             os.makedirs(config.python.sourceFolder)
    #
    #         if os.path.isdir(modulePath) and not config.options.overWriteFiles:
    #             raise gencrud.util.exceptions.ModuleExistsAlready(cfg, modulePath)
    #
    #         outputSourceFile = os.path.join(modulePath, gencrud.util.utils.sourceName(templ))
    #         if config.options.backupFiles:
    #             gencrud.util.utils.backupFile(outputSourceFile)
    #
    #         if os.path.isfile(outputSourceFile):
    #             # remove the file first
    #             os.remove(outputSourceFile)
    #
    #         makePythonModules(config.python.sourceFolder, config.application, cfg.name)
    #         with open(outputSourceFile, gencrud.util.utils.C_FILEMODE_WRITE + 'b') as stream:
    #             stream.write(Template(filename=os.path.abspath(templ)).render(obj=cfg,
    #                                                                           root=config,
    #                                                                           modules=modules,
    #                                                                           date=generationDateTime,
    #                                                                           version=gencrud.version.__version__,
    #                                                                           username=userName).encode('utf-8'))
    #
    #     for column in cfg.table.columns:
    #         if column.ui is not None:
    #             if column.ui.hasResolveList():
    #                 constants.append('# field {}.{} constants\n'.format(cfg.table.name, column.name))
    #                 for line in column.ui.createResolveConstants():
    #                     if line not in constants:
    #                         constants.append(line + '\n')
    #
    #                 constants.append('\n')
    #                 constants.append("C_{}_MAPPING = {}\n".format(column.name,
    #                                                               column.ui.resolveListPy))
    #                 constants.append('\n\n')
    #
    #     if len(constants) > 0:
    #         constants.insert(0, '# Generated by gencrud\n')
    #         filename = os.path.join(modulePath, 'constant.py')
    #         if config.options.backupFiles:
    #             gencrud.util.utils.backupFile(filename)
    #
    #         with open(filename, 'w') as stream:
    #             stream.writelines(constants)
    #
    # updatePythonProject(config, '')
    # return

