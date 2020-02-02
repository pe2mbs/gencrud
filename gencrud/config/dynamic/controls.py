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
from gencrud.config.dynamic.control import TemplateDymanicControl


class DymanicControls( object ):
    def __init__( self, controls ):
        self.__cfg = controls
        self.__controls = {}
        self.parse()
        return

    def parse( self ):
        for name, value in self.__cfg.items():
            # all types shall be in lowercase
            if any( c.islower() for c in name ):
                # Add new control
                self.__controls[ name ] = TemplateDymanicControl( self,
                                              name,
                                              arguments = value[ 'properties' ],
                                              htmlTemplate = value[ 'html' ] )

        return

    def append( self, obj ):
        self.__controls[ obj.name ] = obj
        return

    def get( self, name ):
        if name in self.__controls:
            return self.__controls[ name ]

        return None

    def dump( self ):
        for name, control in self.__controls.items():
            print( "{} : ".format( name ) )
            control.dump()

