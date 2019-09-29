

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
    def __init__( self, python, angular ):
        self.__python = python
        self.__angular = angular
        super( MissingSourceFolder, self ).__init__( 'Could find the source folders, please be at the project root or {} or {}'.
                                                     format( python, angular ) )


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

