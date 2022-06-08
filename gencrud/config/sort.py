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


class SortInfo( TemplateBase ):
    def __init__( self, data ):
        TemplateBase.__init__( self, None )
        self.__field    = data[ C_FIELD ]
        self.__direction = C_ASCENDING
        if C_DIRECTION in data:
            if data[ C_DIRECTION ] in C_DIRECTIONS:
                self.__direction    = data[ C_DIRECTION ]

            else:
                raise Exception( "Sorting order must be one of the following: {}".format( ', '.join( C_DIRECTIONS ) ) )

        return

    @property
    def field( self ):
        return self.__field

    @property
    def direction( self ):
        return self.__direction

    def htmlMaterialSorting( self ):
        return 'matSortActive="{}" matSortDirection="{}"'.format( self.__field, self.__direction )

    def injectAngular( self ):
        return self.AngularInject()

    def AngularInject( self ):
        return "this.sort.sort( {{ id: '{field}', start: '{order}' }} as MatSortable );".format( field = self.__field,
                                                                                                 order = self.__direction )

    def __repr__(self):
        return "<SortInfo >"
