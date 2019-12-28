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


class TemplateMenuItem( object ):
    def __init__( self, key, **cfg ):
        self.__item = cfg[ key ]
        self.__submenu = None
        if 'menu' in self.__item:
            self.__submenu = TemplateMenuItem( 'menu', **self.__item )

        return

    @property
    def index( self ):
        return self.__item.get( 'index', -1 )

    @property
    def displayName( self ):
        return self.caption

    @property
    def caption( self ):
        return self.__item.get( 'caption', self.__item.get( 'displayName', '' ) )

    @property
    def iconName( self ):
        return self.icon

    @property
    def icon( self ):
        return self.__item.get( 'icon', self.__item.get( 'iconName', '' ) )

    @property
    def route( self ):
        return self.__item.get( 'route', self.caption )

    @property
    def menu( self ):
        return self.__submenu

    def activateItem( self ):
        if 'menu' in self.__item:
            return self.__submenu.activateItem()

        return self.route