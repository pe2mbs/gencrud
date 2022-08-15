from enum import Enum


class ValidatorType(Enum):
    REQUIRED = 1
    MINLENGTH = 2
    MAXLENGTH = 3


class Validator (object):
   
    def __init__( self, validatorType: ValidatorType, value ):
        self.__validatorType = validatorType
        self.__value = value

    @property
    def validatorType( self ):
        return self.__validatorType

    @property
    def value( self ):
        return self.__value
