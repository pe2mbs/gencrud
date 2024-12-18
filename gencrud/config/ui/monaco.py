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
from gencrud.config.base import TemplateBase
from gencrud.constants import *


class TemplateMonacoAction( TemplateBase ):
    def __init__( self, parent, **cfg ):
        TemplateBase.__init__(self, parent)
        self.__cfg = cfg
        return

    @property
    def Tooltip( self ) -> str:
        return self.__cfg.get( C_TOOLTIP, '' )

    @property
    def Action( self ) -> str:
        return self.__cfg.get( C_ACTION, '' )

    @property
    def Icon( self ) -> str:
        return self.__cfg.get( C_ICON, '' )


class TemplateMonaco( TemplateBase ):
    def __init__( self, parent, **cfg ):
        TemplateBase.__init__(self, parent)
        self.__cfg = cfg
        self.__actionBar = []
        for action in self.__cfg.get( C_EDITOR_ACTION_BAR, [] ):
            self.__actionBar.append( TemplateMonacoAction( self, **action ) )

        return

    def hasHeight( self ) -> bool:
        return C_HEIGHT in self.__cfg

    @property
    def Height( self ) -> str:
        return self.__cfg.get( C_HEIGHT, '100px' )

    @property
    def Function( self ) -> str:
        return self.__cfg.get( C_FUNCTION )

    @property
    def File( self ) -> str:
        return self.__cfg.get( C_FILENAME )

    def hasFunctionFile( self ) -> bool:
        return C_FUNCTION in self.__cfg and C_FILENAME in self.__cfg

    def hasActionBar( self ):
        return len( self.__actionBar ) > 0

    @property
    def Actionbar( self ) -> list:
        return self.__actionBar

    @property
    def Language( self ) -> str:
        return self.__cfg.get( C_EDITOR_LANGUAGE, 'text' )

    @property
    def Minimap( self ) -> str:
        return "true" if self.__cfg.get( C_EDITOR_MINIMAP ) else 'false'

    @property
    def Theme( self ) -> str:
        return self.__cfg.get( C_EDITOR_THEME, 'vs-dark' )