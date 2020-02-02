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
from gencrud.util.exceptions import InvalidPropertyValue

C_INTEGER   = 'int'
C_STRING    = 'str'
C_BOOLEAN   = 'bool'
C_LIST      = 'list'


class ControlProperty( object ):
    def __init__( self, name, type, default = None, allowed = None, **kwargs ):
        self.__name = name
        self.__value = None
        self.__type = None
        self.__default = None
        self.__allowed = []
        self.set(  type, default, allowed, **kwargs )
        return

    @property
    def name( self ):
        return self.__name

    @property
    def type( self ):
        return self.__type

    @property
    def default( self ):
        return self.__default

    @property
    def allowed( self ):
        return self.__allowed

    def set( self, type, default = None, allowed = None, **kwargs ):
        self.__type = type
        self.__default = default
        self.__allowed = allowed
        for name, setting in kwargs.items():
            setattr( self, name, setting )

        return

    def isSet( self ):
        return self.__value is not None

    @property
    def value( self ):
        if self.__value is None:
            return self.__default

        return self.__value

    @value.setter
    def value( self, val ):
        self.__value = val
        return

    def __int__(self):
        if self.__type == C_INTEGER:
            return int( self.value )

        raise InvalidPropertyValue( self.__name )

    def __str__(self):
        if self.__type in ( C_STRING, C_INTEGER ):
            return str( self.value )

        elif self.__type == C_BOOLEAN:
            return str( self.value ).lower()

        elif self.__type == C_LIST:
            if self.__value is list:
                return ','.join( self.__value )

            return ''

        raise InvalidPropertyValue( self.__name )

    def __bool__(self):
        if self.__type == C_BOOLEAN:
            return

        raise InvalidPropertyValue( self.__name )
