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

# Old names
C_DISPLAY_NAME  = 'displayName'
C_ICON_NAME     = 'iconName'


class TemplateMenuItem( TemplateBase ):
    def __init__( self, key, **cfg ):
        TemplateBase.__init__( self, None )
        self.__item = cfg[ key ]
        self.__submenu = None
        if C_MENU in self.__item:
            self.__submenu = TemplateMenuItem( C_MENU, **self.__item )

        return

    @property
    def index( self ) -> int:
        return self.__item.get( C_INDEX, -1 )

    @property
    def displayName( self ) -> str:
        return self.caption

    @property
    def caption( self ) -> str:
        return self.__item.get( C_CAPTION, self.__item.get( C_DISPLAY_NAME, '' ) )

    @property
    def iconName( self ) -> str:
        return self.icon

    @property
    def icon( self ) -> str:
        return self.__item.get( C_ICON, self.__item.get( C_ICON_NAME, '' ) )

    @property
    def route( self ) -> str:
        return self.__item.get( C_ROUTE, None )

    @property
    def menu( self ) -> object:
        return self.__submenu

    def activateItem( self ) -> str:
        if C_MENU in self.__item:
            return self.__submenu.activateItem()

        return self.route[1:] if self.route.startswith( '/' ) else self.route
