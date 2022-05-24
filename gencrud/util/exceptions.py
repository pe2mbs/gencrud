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


class ModuleExistsAlready( Exception ):
    def __init__( self, obj, path ):
        self.__obj = obj
        super( ModuleExistsAlready, self ).__init__( path )
        return


class InvalidSetting( Exception ):
    def __init__( self, prop, entity, name, expected = None ):
        self.__property = prop
        self.__entity   = entity
        self.__name     = name
        TEXT = '{prop} in {entity} with name {name} has an invalid value.'
        if isinstance( expected, str ):
            TEXT += '\nExpected : {expected}'
            self.__expected = expected

        elif isinstance( expected, ( list, tuple ) ):
            TEXT += '\nExpected one of {expected}'
            self.__expected = ', '.join( expected[:-1] )
            self.__expected += "  or {}".format( expected[ :-1 ] )

        elif isinstance( expected, dict ):
            TEXT += '\nExpected one of {expected}'
            keys = list( expected.keys() )
            self.__expected = ', '.join( keys[ : -1 ] )
            self.__expected += "  or {}".format( keys[ -1 ] )

        else:
            self.__expected = None

        super( InvalidSetting, self ).__init__( TEXT.format( prop = prop,
                                                             entity = entity,
                                                             name = name,
                                                             expected = self.__expected ) )
        return


class MissingTemplate( Exception ):
    def __init__( self, template ):
        self.__template = template
        super( MissingTemplate, self ).__init__( 'No templates found in {0}'.
                                                 format( template ) )


class MissingCommon( Exception ):
    def __init__( self, common ):
        self.__common = common
        super( MissingCommon, self ).__init__( 'No common templates found in {0}'.
                                                 format( common ) )


class MissingSourceFolder( Exception ):
    def __init__( self, path ):
        self.__path = path
        super( MissingSourceFolder, self ).__init__( 'Could not find the source folders, please be at the project root or {}'.
                                                     format( path ) )


class MissingTemplateFolder( Exception ):
    def __init__( self, path ):
        self.__path = path
        super( MissingTemplateFolder, self ).__init__( 'Could not find the template folders, please be at the project root or {}'.
                                                     format( path ) )


class MissingCommonFolder( Exception ):
    def __init__( self, path ):
        self.__path = path
        super( MissingCommonFolder, self ).__init__( 'Could not find the common template folders, please be at the project root or {}'.
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


class MissingAttribute( Exception ):
    def __init__( self, group, name ):
        Exception.__init__( self, "Missing '{1}' in section '{0}'".format( group, name ) )
