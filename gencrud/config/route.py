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
from gencrud.util.typescript import TypeScript
from gencrud.constants import *
from gencrud.config.base import TemplateBase
from gencrud.util.exceptions import MissingAttribute


class RouteTemplate( TemplateBase ):
    def __init__( self, parent, **cfg ):
        TemplateBase.__init__( self, parent )
        self.__config = cfg
        # if C_CLASS not in self.__config:
        #     raise MissingAttribute( C_TABLE, C_CLASS )

        return

    @property
    def name( self ):
        return self.__config.get( C_NAME, self.parent.name )

    @property
    def label( self ):
        return self.__config.get( C_LABEL, self.parent.label )

    @property
    def cls( self ):
        klasse = self.__config.get( C_CLASS, None )
        if klasse is None:
            if self.parent.type == 'screen':
                return "Screen{}Component".format( self.getObject().cls )

            return "Dialog{}Component".format( self.getObject().cls )

        return klasse

    @property
    def module( self ):
        return self.__config.get( C_MODULE, self.get_default( 'module' ) )

    @property
    def route( self ):
        return self.__config.get( C_ROUTE, None )

    def params( self ):
        return self.__config.get( C_PARAMS, {} )

    def routeParams( self, outerObject = True ):
        params = self.params()
        if len( params ) > 0:
            items = {}
            for key, value in params.items():
                items[ key ] = value

            return '{{ queryParams: {} }}'.format( TypeScript().build( items ) ) if outerObject else \
                '{}'.format( TypeScript().build( items ) )

        return '{ }'

    def __repr__(self):
        return "<RouteTemplate name = '{}', label = '{}', class = {}, params = {}>".format(
                self.name, self.label, self.cls, self.params()
        )
