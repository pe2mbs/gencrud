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
from gencrud.util.typescript import TypeScript


class RouteTemplate( object ):
    def __init__( self, parent, **cfg ):
        self.__parent = parent
        self.__config = cfg
        return

    @property
    def name( self ):
        return self.__config.get( 'name', self.__parent.name )

    @property
    def label( self ):
        return self.__config.get( 'label', self.__parent.label )

    @property
    def cls( self ):
        return self.__config.get( 'class', None )

    @property
    def module( self ):
        return self.__config.get( 'module', None )

    def params( self ):
        return self.__config.get( 'params', {} )

    def routeParams( self ):
        params = self.params()
        if len( params ) > 0:
            items = {}
            for key, value in params.items():
                items[ key ] = value
            # (click) = "router.navigate( [ '/tr/edit', { queryParams: { id: 'TR_ID', mode: 'edit', value: row.TR_ID } } ] )"
            return '{{ queryParams: {} }}'.format( TypeScript().build( items ) )

        return ''

    def __repr__(self):
        return "<RouteTemplate name = '{}', label = '{}', class = {}, params = {}>".format(
                self.name, self.label, self.cls, self.params()
        )
