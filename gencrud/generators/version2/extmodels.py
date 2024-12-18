import os.path
import logging
from datetime import datetime
from mako.template import Template
from gencrud.generators.version2.reformat import reformatPythonCode
from gencrud.generators.version2.constant_gen import generatePythonConstants
import gencrud.util.exceptions
import gencrud.util.utils
import gencrud.version
from gencrud.configuraton import TemplateConfiguration, TemplateObject


logger = logging.getLogger( 'gencrud.extmodels' )


def generateExtModels( config: TemplateConfiguration, templates: list ):
    dt = datetime.now()
    generationDateTime = dt.strftime("%Y-%m-%d %H:%M:%S")
    userName = os.path.split(os.path.expanduser("~"))[1]
    moduleFolder = config.ExtModels.sourceFolder
    for cfg in config:  # This iterates over the objects
        cfg: TemplateObject
        constants = "\n".join( generatePythonConstants( config, cfg ) )
        for template in templates:
            if cfg.ignoreTemplates( template ):
                continue

            logger.info( f'template    : {template}' )
            outputSourceFile = os.path.join( moduleFolder,
                                             gencrud.util.utils.sourceName( template, model = cfg.name ) )

            if not config.options.overWriteFiles and os.path.exists( moduleFolder ):
                raise gencrud.util.exceptions.ModuleExistsAlready( cfg, moduleFolder )

            if not os.path.exists( moduleFolder ):
                os.makedirs( moduleFolder )

            if config.options.backupFiles:
                gencrud.util.utils.backupFile( outputSourceFile )

            if os.path.isfile( outputSourceFile ):
                # remove the file first
                os.remove( outputSourceFile )

            makoTemplate = Template( filename = template )
            with open( outputSourceFile, 'w', newline = '' ) as stream:
                stream.write( makoTemplate.render( obj = cfg,
                                                   root = config,
                                                   constVariables = constants,
                                                   date = generationDateTime,
                                                   version = gencrud.version.__version__,
                                                   username = userName ) )

            if outputSourceFile.lower().endswith( '.py' ):
                # execute yapf to format the Python code.
                reformatPythonCode( outputSourceFile, config )

    return