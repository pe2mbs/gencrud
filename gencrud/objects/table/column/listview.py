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
import logging

logger = logging.getLogger()


class TemplateListView( object ):
    def __init__( self, parent, **cfg ):
        self.__parent   = parent
        self.__cfg      = cfg
        return

    @property
    def width( self ):
        if 'width' not in self.__cfg:
            if hasattr( self.__parent, 'css' ):
                return self.__parent.css.width

        return self.__cfg.get( 'width', None )

    @property
    def index( self ):
        if 'index' not in self.__cfg:
            if hasattr( self.__parent, 'index' ):
                return self.__parent.index

        return self.__cfg.get( 'index', None )
