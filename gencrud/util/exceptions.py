#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2019 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation; either version 2 of the
#   License, or (at your option) any later version.
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


class ModuleExistsAlready( Exception ):
    def __init__( self, obj, path ):
        self.__obj = obj
        super( ModuleExistsAlready, self ).__init__( path )
        return


class InvalidSetting( Exception ):
    def __init__( self, prop, entity, name ):
        self.__property = prop
        self.__entity   = entity
        self.__name     = name
        super( InvalidSetting, self ).__init__( '{prop} in {entity} with name {name} has an invalid value.'.format(
            prop = prop,
            entity = entity,
            name = name ) )
        return


class MissingTemplate( Exception ):
    def __init__( self, template ):
        self.__template = template
        super( MissingTemplate, self ).__init__( 'No templates found in {0}'.
                                                 format( template ) )


class MissingSourceFolder( Exception ):
    def __init__( self, path ):
        self.__path = path
        super( MissingSourceFolder, self ).__init__( 'Could find the source folders, please be at the project root or {}'.
                                                     format( path ) )


class MissingTemplateFolder( Exception ):
    def __init__( self, path ):
        self.__path = path
        super( MissingTemplateFolder, self ).__init__( 'Could find the template folders, please be at the project root or {}'.
                                                     format( path ) )


class InvalidEnvironment( Exception ):
    def __init__( self, environment ):
        self.__environment = environment
        super( InvalidEnvironment, self ).__init__( 'Invalid environment {0} in verifyLoadProject'.
                                                    format( environment ) )


class EnvironmentInvalidMissing( Exception ):
    def __init__( self, environment, missing, config_file ):
        self.__environment = environment
        self.__missing  = missing
        self.__configFile = config_file
        super( EnvironmentInvalidMissing, self ).__init__( 'Error: {0} environment invalid, missing {1} in config file {2}'.
                                                           format( environment, missing, config_file ) )


class MissingAngularEnvironment( Exception ):
    def __init__( self, missing ):
        self.__missing = missing
        super( MissingAngularEnvironment, self ).__init__( 'Error: Angular environment not found, missing {}'.format( missing ) )


class FlaskEnvironmentNotFound( Exception ):
    def __init__( self ):
        super( FlaskEnvironmentNotFound, self ).__init__( 'Error: Python Flask environment not found' )


class TypeScriptFormatError( Exception ):
    def __init__( self, symbol, line, column ):
        super( TypeScriptFormatError, self ).__init__( 'format error: found {0} on line {1} column {2}'.format( symbol, line, column ) )


class TypeScriptInvalidStartDataType( Exception ):
    def __init__( self, data_type ):
        super( TypeScriptInvalidStartDataType, self ).__init__( 'invalid starting data type for {}'.format( data_type ) )


class PathNotFoundException( Exception ):
    def __init__( self, path ):
        super( PathNotFoundException, self ).__init__( '{} not found.'.format( path ) )
        return


class KeyNotFoundException( Exception ):
    def __init__( self, path ):
        super( KeyNotFoundException, self ).__init__( 'key {} not found.'.format( path ) )
        return


class InvalidPropertyValue( Exception ):
    pass


class InvalidViewSize( Exception ):
    def __init__(self):
        Exception.__init__( self, "Invalid parameter 'viewSize', may be integer (5, 10, 25, 100) or " +
                            "string with service class name of where the function getViewSize() resides." )
        return