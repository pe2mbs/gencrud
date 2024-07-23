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
from gencrud.util.typescript import TypeScript


class FilterInfo( TemplateBase ):
    def __init__( self, data ):
        TemplateBase.__init__( self, None )
        self.__column    = data[ C_COLUMN ]
        self.__value    = data[ C_VALUE ]
        self.__operator = data[ C_OPERATOR ]
        return

    @property
    def field( self ):
        return self.__column

    @property
    def value( self ):
        return self.__value

    @property
    def operator( self ):
        return self.__operator

    def __repr__(self):
        return "<FilterInfo >"

    def filterTypeScript( self ):
        return f'{{ column: "{self.__column}", operator: "{self.__operator}", value: {self.__value} }}'


class FilterInfoList( TemplateBase ):
    def __init__( self, data ):
        TemplateBase.__init__( self, None )
        self.__data = data
        self.__filters = []
        for filter in data:
            self.__filters.append( FilterInfo( filter ) )
        return

    def __iter__( self ):
        return iter( self.__filters )

    def __len__( self ):
        return len( self.__filters )

    def __getitem__( self, item ):
        return self.__filters[ item ]

    def filterTypeScript( self ):
        lines = []
        for filter in self.__filters:
            lines.append( filter.filterTypeScript() )

        return "[ " + ( ", ".join( lines ) ) + " ]"

    def toTypeScript( self ):
        return TypeScript().build( self.__data )


