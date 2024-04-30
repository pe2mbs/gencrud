#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2024 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
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
import typing as t
from gencrud.constants import *
from gencrud.config.base import TemplateBase


class TemplateModule( TemplateBase ):
    def __init__( self, parent, provider: dict ):
        super().__init__( parent )
        self.provider = provider
        return

    @property
    def Filename( self ) -> str:
        return self.provider.get( C_FILENAME )

    @property
    def Class( self ) -> str:
        return self.provider.get( C_CLASS )


class TemplateProviders( TemplateBase ):
    def __init__( self, parent, providers ):
        super().__init__( parent )
        self.__providers = [ TemplateModule( self, provider ) for provider in providers ]

    def __iter__(self) -> t.Iterator[ TemplateModule ]:
        return iter( self.__providers )

    def hasProviders( self ) -> bool:
        return len( self.__providers ) > 0
