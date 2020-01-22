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
from mako.template import Template
from gencrud.config.dynamic.property import ControlProperty


class TemplateDymanicControl( object ):
    def __init__( self, parent, name, arguments, htmlTemplate ):
        self.__parent = parent
        self.__name = name
        self.__htmlTemplate = htmlTemplate
        self.__attributes = []
        for name, properties in arguments.items():
            self.__attributes.append( name )
            setattr( self, name, ControlProperty( name, **properties ) )

        return

    @property
    def name( self ):
        return self.__name

    @property
    def htmlTemplate( self ):
        return self.__htmlTemplate

    @property
    def parent( self ):
        return self.__parent

    def set( self, arguments ):
        for name, attributes in arguments.items():
            if hasattr( self, name ):
                getattr( self, name ).set( **attributes )

            else:
                setattr( self, name, ControlProperty( name, **attributes ) )

        return

    def get( self, arguments ):
        return


    def dump( self ):
        for attr in self.__attributes:
            print( "{}.{} = {}".format( self.name, attr, getattr( self, attr ) ) )

        return

    def getOptions( self, ui = None ):
        options = []
        for attr in self.__attributes:
            value = None
            if ui.isSet( attr ):
                value = ui.get( attr )

            if value is None:
                value = getattr( self, attr )
                if not value.isSet():
                    continue

                value = str( value )

            if value is None:
                continue

            options.append( '{}="{}"'.format( attr, value ) )

        return ' '.join( options )

    def build( self, field, table, obj, root ):
        return Template( self.__htmlTemplate ).render( this = self,
                                                       field = field,
                                                       table = table,
                                                       obj = obj,
                                                       root = root )
