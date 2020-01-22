#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2020 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
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
from gencrud.constants import *
from gencrud.config.base import TemplateBase


class TemplateService( TemplateBase ):
    def __init__( self, **cfg ):
        TemplateBase.__init__( self, None )
        self.__cfg = cfg
        return

    @property
    def name( self ):
        return self.__cfg[ C_NAME ]

    @property
    def value( self ):
        return self.__cfg[ C_VALUE ]

    @property
    def label( self ):
        return self.__cfg[ C_LABEL ]

    @property
    def cls( self ):
        value = self.__cfg[ C_CLASS ]
        if value.endswith( 'Service' ):
            return value

        return '{}DataService'.format( value )

    @property
    def path( self ):
        if C_PATH in self.__cfg:
            return self.__cfg[ C_PATH ]

        return '../{}/service'.format( self.__cfg[ C_NAME ] )
