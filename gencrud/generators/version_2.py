#
#   Python backend and Angular frontend
#   Copyright (C) 2018-2024 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
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
import typing as t
import logging
import json
import gencrud.myyaml as yaml
import os
import gencrud.util.utils
from gencrud.configuraton import TemplateConfiguration
from gencrud.util.exceptions import EnvironmentInvalidMissing, MissingAngularEnvironment
from gencrud.generators.version2.python import generatePython
from gencrud.generators.version2.angular import generateAngular
from gencrud.generators.version2.unittest import generateUnittest
from gencrud.generators.version2.extmodels import generateExtModels
from gencrud.generators.version2.help_pages import generateHelpPages


logger = logging.getLogger()


def verifyLoadAngularProject( config: TemplateConfiguration ) -> t.Tuple[ str, dict ]:
    """Find the Angular project

    :param config:      The template configuration
    :return:            The Angular configuration
    """
    configFile  = os.path.join( '..', '..', 'angular.json' )
    root        = config.angular
    if os.path.isdir( root.sourceFolder ) and os.path.isfile( os.path.join( root.sourceFolder, configFile ) ):
        configFile = os.path.abspath( os.path.join( root.sourceFolder, configFile ) )
        with open( configFile, gencrud.util.utils.C_FILEMODE_READ ) as stream:
            data = json.load( stream )

        if data is None:
            raise EnvironmentInvalidMissing( "ANGULAR", root.sourceFolder, configFile )

    else:
        raise EnvironmentInvalidMissing( "ANGULAR", root.sourceFolder, configFile )

    if 'defaultProject' in data and 'projects' in data:
        if data[ 'defaultProject' ] not in data[ 'projects' ]:
            raise MissingAngularEnvironment('{} projects'.format(data['defaultProject']))

    else:
        raise MissingAngularEnvironment( 'tag defaultProject' )

    return configFile, data


def verifyLoadPythonProject( config: TemplateConfiguration ) -> t.Tuple[ str, dict ]:
    """Find the configuration of the Python Flask project

    :param config:      The template configuration
    :return:            The Flask configuration
    """
    root = config.python
    configFile = os.path.join( 'config', 'config.conf')
    if os.path.isdir( root.sourceFolder ):
        if os.path.isdir( os.path.join( root.sourceFolder, "config" ) ) and \
                          os.path.isfile( os.path.join( root.sourceFolder, configFile ) ):
            configFile = os.path.abspath( os.path.join( root.sourceFolder, configFile ) )
            with open( os.path.join( os.path.join( root.sourceFolder, configFile ) ),
                       gencrud.util.utils.C_FILEMODE_READ) as stream:
                data = yaml.load( stream, Loader=yaml.Loader )

        elif os.path.isfile( os.path.join( root.sourceFolder, 'config.yaml' ) ):
            configFile = os.path.abspath( os.path.join( root.sourceFolder, 'config.yaml' ) )
            with open( configFile, gencrud.util.utils.C_FILEMODE_READ ) as stream:
                data = yaml.load( stream, Loader = yaml.Loader )

        if data is None:
            raise EnvironmentInvalidMissing( "PYTHON", root.sourceFolder, configFile )

    else:
        raise EnvironmentInvalidMissing( "PYTHON", root.sourceFolder, configFile )

    return configFile, data


def version_2_StyleGeneration( config: TemplateConfiguration ):
    flaskConfig = {}
    angularConfig = {}
    if config.options.generateFrontend:
        angularCfgFile, angularConfig = verifyLoadAngularProject( config )

    else:
        logger.info("NOT generating frontend code")

    if config.options.generateBackend:
        flaskCfgFile, flaskConfig = verifyLoadPythonProject( config )

    else:
        logger.info("NOT generating backend code")

    if config.options.generateBackend:
        logger.info( "*** Generating Python backend source code.***" )
        templateFolder = config.python.templateFolder
        generatePython( config,
                        [ os.path.abspath( os.path.join( templateFolder, t ) )
                            for t in os.listdir( templateFolder ) ],
                        flaskConfig )

    if config.options.GenerateExtModels:
        logger.info("*** Generating External models source code.***")
        templateFolder = config.ExtModels.templateFolder
        generateExtModels( config, [ os.path.abspath( os.path.join( templateFolder, t ) )
                            for t in os.listdir( templateFolder ) ] )


    if config.options.generateFrontend:
        logger.info( "*** Generating Typescript Angular frontend source code. ***" )
        generateAngular( config,
                         [ os.path.abspath( os.path.join( config.angular.templateFolder, t ) )
                            for t in os.listdir( config.angular.templateFolder ) ],
                         angularConfig )

    if config.options.GenerateHelpPages:
        logger.info( "*** Generating Help pages. ***" )
        generateHelpPages( config, [ os.path.abspath( os.path.join( config.HelpPages.templateFolder, t ) )
                                     for t in os.listdir( config.HelpPages.templateFolder ) ],
                           flaskConfig )

    if config.options.generateTests:
        logger.info( "*** Generating Unittest source code. ***" )
        generateUnittest( config,
                          [ os.path.abspath( os.path.join(config.unittest.templateFolder, t ) )
                            for t in os.listdir( config.unittest.templateFolder ) ],
                          flaskConfig )

    if config.options.generateBackend or config.options.GenerateHelpPages or config.options.generateTests:
        # Update the FLASK configuration
        with open( flaskCfgFile, 'w' ) as stream:   # noqa
            yaml.dump( stream, flaskConfig )

    # As we are not making any modification to the Ansgular configuration its NOT saved.
    return
