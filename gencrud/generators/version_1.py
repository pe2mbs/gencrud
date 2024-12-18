from __future__ import print_function    # (at top of module)
import json
import os
import logging
import gencrud.util.utils
import gencrud.installer
from gencrud.configuraton import TemplateConfiguration
from gencrud.util.exceptions import ( InvalidEnvironment,
                                      EnvironmentInvalidMissing,
                                      MissingAngularEnvironment,
                                      FlaskEnvironmentNotFound )
from gencrud.constants import *
from gencrud.generators.version1.python import generatePython
from gencrud.generators.version1.angular import generateAngular
from gencrud.generators.version1.unittest import generateUnittest
import gencrud.myyaml as yaml

logger = logging.getLogger()


def verifyLoadProject( config: TemplateConfiguration, env ):
    if env == C_ANGULAR:
        configFile  = os.path.join( '..', '..', 'angular.json' )
        root        = config.angular

    elif env == C_PYTHON:
        root = config.python
        if os.path.isfile( os.path.join( root.sourceFolder, 'config', 'config.conf' ) ):
            configFile = os.path.join( 'config', 'config.conf' )

        elif os.path.isfile( os.path.join( root.sourceFolder, 'config.yaml' ) ):
            configFile = 'config.yaml'

        elif os.path.isfile( os.path.join( root.sourceFolder, 'config.json' ) ):
            configFile = 'config.json'

        else:
            raise Exception( "Could not find the Python Flask configuration file."  )

    else:
        raise InvalidEnvironment( env )

    if os.path.isdir( root.sourceFolder ) and os.path.isfile( os.path.join( root.sourceFolder, configFile ) ):
        with open( os.path.join( root.sourceFolder, configFile ),
                   gencrud.util.utils.C_FILEMODE_READ ) as stream:
            if configFile.endswith( ( '.yaml', '.conf' ) ):
                data = yaml.load( stream )

            else:
                data = json.load( stream )

        if data is None:
            raise EnvironmentInvalidMissing( env, root.sourceFolder, configFile )

    else:
        raise EnvironmentInvalidMissing( env, root.sourceFolder, configFile )

    # logger.debug( 'Configuration for {}: {}'.format( env, json.dumps( data, indent = 4 ) ) )
    if env == C_ANGULAR:
        # Check if we have a valid Angular environment
        if 'defaultProject' in data and 'projects' in data:
            if data[ 'defaultProject' ] not in data[ 'projects' ]:
                raise MissingAngularEnvironment( '{} projects'.format( data[ 'defaultProject' ] ) )

            else:
                data = data[ 'projects' ][ data[ 'defaultProject' ] ]

        else:
            raise MissingAngularEnvironment( 'tag defaultProject' )

    elif env == C_PYTHON:
        # Check if we have a valid Python-Flask environment
        if 'API_MODULE' in data:
            pass

        else:
            if not ( 'COMMON' in data and 'API_MODULE' in data[ 'COMMON' ] ):
                raise FlaskEnvironmentNotFound()

            logging.info( "Application: {} target application: {}".format( config.application, data[ 'COMMON' ][ 'API_MODULE' ] ) )
            # if data[ 'COMMON' ][ 'API_MODULE' ] != config.application:
            #     raise FlaskEnvironmentNotFound()

            if config.application not in data[ 'COMMON' ][ 'API_MODULE' ]:
                raise FlaskEnvironmentNotFound()

            data = data[ 'COMMON' ]

    return data


def version_1_StyleGeneration( config ):
    if config.options.generateFrontend:
        verifyLoadProject(config, C_ANGULAR)

    else:
        logger.info("NOT generating frontend code")

    if config.options.generateBackend:
        verifyLoadProject(config, C_PYTHON)

    else:
        logger.info("NOT generating backend code")

    if config.options.generateBackend:
        logger.info("*** Generating Python backend source code.***")
        templateFolder = config.python.templateFolder
        generatePython(config,
                       [os.path.abspath(os.path.join(templateFolder, t))
                        for t in os.listdir(templateFolder)])

    if config.options.generateFrontend:
        logger.info("*** Generating Typescript Angular frontend source code. ***")
        generateAngular(config,
                        [os.path.abspath(os.path.join(config.angular.templateFolder, t))
                         for t in os.listdir(config.angular.templateFolder)])

    if config.options.generateTests:
        logger.info("*** Generating Unittest source code. ***")
        generateUnittest(config,
                         [os.path.abspath(os.path.join(config.unittest.templateFolder, t))
                          for t in os.listdir(config.unittest.templateFolder)])

    return
