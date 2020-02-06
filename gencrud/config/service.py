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
from gencrud.constants import *
from gencrud.config.base import TemplateBase
from gencrud.util.exceptions import MissingAttribute


class TemplateService( TemplateBase ):
    def __init__( self, **cfg ):
        TemplateBase.__init__( self, None )
        self.__config = cfg
        if C_NAME not in self.__config:
            raise MissingAttribute( S_SERVICE, C_NAME )

        if C_VALUE not in self.__config:
            raise MissingAttribute( S_SERVICE, C_VALUE )

        if C_LABEL not in self.__config:
            raise MissingAttribute( S_SERVICE, C_LABEL )

        if C_CLASS not in self.__config:
            raise MissingAttribute( S_SERVICE, C_CLASS )

        return

    @property
    def name( self ):
        return self.__config.get( C_NAME, None )

    @property
    def value( self ):
        return self.__config.get( C_VALUE, None )

    @property
    def label( self ):
        return self.__config.get( C_LABEL, None )

    @property
    def cls( self ):
        value = self.__config.get( C_CLASS, None )
        if value.endswith( 'Service' ):
            return value

        return '{}DataService'.format( value )

    @property
    def path( self ):
        if C_PATH in self.__config:
            return self.__config[ C_PATH ]

        return '../{}/service'.format( self.__config[ C_NAME ] )
