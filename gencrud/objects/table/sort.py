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

DIRECTIONS = ( 'asc', 'desc', '' )


class SortInfo( object ):
    def __init__( self, data ):
        self.__field    = data[ 'field' ]
        self.__direction = 'asc'
        # 'asc'
        # 'desc'
        # ''
        if 'direction' in data:
            if data[ 'direction' ] in DIRECTIONS:
                self.__direction    = data[ 'direction' ]

            else:
                raise Exception( "Sorting order must be one of the following: 'asc', 'desc' or ''")

        return

    @property
    def Field( self ):
        return self.__field

    @property
    def Direction( self ):
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