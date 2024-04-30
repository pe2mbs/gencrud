import typing as t
from datetime import datetime
from mako.template import Template
import gencrud.version
import gencrud.util.utils
import gencrud.util.exceptions
import logging
import os.path
from gencrud.generators.version2.constant_gen import generatePythonConstants
from gencrud.generators.version2.boilerplate import BOILERPLATE
from gencrud.configuraton import TemplateConfiguration, TemplateObject
from gencrud.generators.version2.reformat import reformatPythonCode


logger = logging.getLogger( 'gencrud.python' )
# logger.setLevel( logging.DEBUG )


def update_gencrud_comment( lines: list ):
    idx = 0
    dt = datetime.now()
    generationDateTime = dt.strftime("%Y-%m-%d %H:%M:%S")
    userName = os.path.split(os.path.expanduser("~"))[1]
    while idx < len( lines ):
        if lines[ idx ].startswith(('#   Created by gencrud', '#   Updated by gencrud')):
            lines[idx] = f'#   Updated by gencrud {generationDateTime} by {userName}'
            break

        idx += 1

    return


def init_file( folder: str,  imports: t.List[ dict ], template: t.Union[ str, t.List[ str ] ] ):
    filename = os.path.join( folder, '__init__.py' )
    if os.path.exists( filename ):
        # Open the file and read
        with open( filename, 'r' ) as stream:
            lines = stream.read().replace('\r','').split( '\n' )

    else:
        # use template
        if isinstance( template, str ):
            lines = template.split( '\n' )

        elif isinstance( template, list ):
            lines = template

        else:
            raise ValueError('template not str or list')


    def endpoint( lines: t.List[ str ], startwith: str, indent: bool = False, last = False ):
        if last:
            last_line = 0
            found = False
            for idx, line in enumerate(lines):
                if indent and line.strip().startswith(startwith):
                    last_line = idx
                    found = True

                elif line.startswith(startwith):
                    last_line = idx
                    found = True

                elif found:
                    return last_line

        else:
            for idx, line in enumerate( lines ):
                if indent and line.strip().startswith( startwith ):
                    return idx

                elif line.startswith( startwith ):
                    return idx

        return len( lines )

    endboilerplate  = endpoint( lines, '#', last = True )
    end_import      = endpoint( lines, 'import', last = True )
    start_function  = endpoint( lines, 'def ' )
    end_function    = endpoint( lines, 'return', indent = True )
    if end_import == len( lines ):
        # This is a new file
        end_import = endboilerplate + 1

    else:
        end_import += 1

    updated = False
    for item in imports:
        if item[ 'import' ] in lines:
            continue

        # Not found in lines, so we are adding
        lines.insert( end_import, item[ 'import' ] )
        end_function += 1
        lines.insert( end_function, item[ 'register' ] )

    if os.path.exists( filename ) and updated:
        update_gencrud_comment( lines )

    with open( filename, 'w', newline = '' ) as stream:
        stream.write( '\n'.join( lines ) )

    return


def models_file( folder: str, imports: t.List[ dict ], template: t.Union[ str, t.List[ str ] ] ):
    filename = os.path.join( folder, 'models.py' )
    if os.path.exists( filename ):
        # Open the file and read
        with open(filename, 'r') as stream:
            lines = stream.read().replace('\r', '').split('\n')

    else:
        # use template
        if isinstance( template, str ):
            lines = template.split( '\n' )

        elif isinstance( template, list ):
            lines = template

        else:
            raise ValueError( 'template not str or list' )

    updated = False
    for item in imports:
        if item[ 'model' ] in lines:
            continue

        updated = True
        table = item[ 'table' ]
        cls   = item[ 'class' ]
        module = item[ 'module' ]
        lines.append( f"# Module '{module}' Table {table} with classes '{cls}', 'Memory{cls}'" )
        lines.append( item[ 'model' ] )

    if os.path.exists( filename ) and updated:
        update_gencrud_comment( lines )

    with open( filename, 'w', newline='' ) as stream:
        stream.write( '\n'.join( lines ) )

    return


def generatePython( config: TemplateConfiguration, templates: t.List[ str ], flask_config: dict ):
    constants = []
    logger.info( f'interface : { config.Interface.Backend }' )
    dt = datetime.now()
    generationDateTime = dt.strftime("%Y-%m-%d %H:%M:%S")
    userName = os.path.split(os.path.expanduser("~"))[1]
    if not os.path.exists( config.python.sourceFolder ):
        os.makedirs( config.python.sourceFolder )

    moduleFolder    = os.path.join( config.python.sourceFolder, config.Interface.Backend.Path )
    if not os.path.exists( moduleFolder ):
        os.makedirs( moduleFolder )

    modules = flask_config.setdefault( 'API_MODULE', [] )
    backendModule = config.Interface.Backend.Path.replace('/', '.').replace('\\', '.')
    if backendModule not in modules:
        # Add the module to the API_MODULE loading list
        modules.append( backendModule )

    backend = config.Interface.Backend.Path.replace('/', '.').replace('\\', '.')
    modules = []
    for cfg in config:  # This iterates over the objects
        # Do the module __init__.py handling
        modules.append( {   'module':   f"{ backend }.{ cfg.name }",
                            'class':    cfg.cls,
                            'table':    cfg.table.PythonName,
                            'import':   f"import { backend }.{ cfg.name }.view",
                            'register': f"    { backend }.{ cfg.name }.view.registerApi()",
                            'model':    f"from { backend }.{ cfg.name }.model import { cfg.cls }, { cfg.cls }Memory" } )

    # create / update the models.py file with all the models for this module
    models_file( moduleFolder,
                 modules,
                 BOILERPLATE + f"\n#   Created by gencrud {generationDateTime} by {userName}\n" )

    init_file( moduleFolder,
               modules,
               BOILERPLATE + f"\n# Created by gencrud {generationDateTime} by {userName}\n" + \
                "#\n\n\ndef registerApis():\n    return\n" )


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
            templateFilename = os.path.join( modulePath, outputSourceFile )
            with open( templateFilename, 'w', newline = '' ) as stream:
                stream.write( makoTemplate.render( obj = cfg,
                                                   root = config,
                                                   modules = modules,
                                                   date = generationDateTime,
                                                   version = gencrud.version.__version__,
                                                   username = userName ) )

            if templateFilename.lower().endswith( '.py' ):
                # execute yapf to format the Python code.
                reformatPythonCode( templateFilename, config )

        constantLines = generatePythonConstants( config, cfg )
        if len( constantLines ) > 0:
            filename = os.path.join( modulePath, 'constants.py' )
            with open( filename, 'w', newline = '' ) as stream:
                # Write the BOILERPLATE
                stream.write( BOILERPLATE )
                stream.write( '\n\n' )
                # Write the lines
                stream.write( '\n'.join( constantLines ) )

            reformatPythonCode( filename, config )

    return
