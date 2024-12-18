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
import typing as t
from gencrud.constants import *


class InputGroup( object ):
    def __init__( self, name, fields ):
        self.__fields = fields
        self.__name = name
        return

    @property
    def name ( self ) -> str:
        return self.__name

    @property
    def fields( self ) -> t.List[ 'TemplateColumn' ]:
        return self.__fields

    def isLastInGroup( self, field ) -> bool:
        return self.__fields[ -1 ] == field

    def isFirstInGroup( self, field ) -> bool:
        return self.__fields[ 0 ] == field

    def inTab( self, tab_name: str ) -> bool:
        return self.__fields[ 0 ].tab.label == tab_name
