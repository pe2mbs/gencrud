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
from platform import system
from gencrud.constants import C_PLATFORMS

class TemplateBase( object ):
    def __init__( self, parent ):
        self.__parent = parent
        platf = system().lower()
        if platf == "darwin":  # as platform.system() for OS-X returns Darwin we translate for consistency.
            platf = "osx"

        if platf not in C_PLATFORMS:
            raise Exception( "Unsupported platform: {}".format( platf ) )

        self.__platform = platf
        return

    @property
    def platform( self ):
        return self.__platform

    @property
    def parent( self ):
        return self.__parent

    def get_default( self, name ):
        p = self.parent
        while p is not None:
            if hasattr( p, name ):
                return getattr( p, name )

            p = p.parent

        return None

    def getObject( self ):
        from gencrud.config.object import TemplateObject
        if isinstance( self, TemplateObject ):
            return self

        return self.__parent.getObject()
