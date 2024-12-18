#
#   Python backend and Angular frontend
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
import os
import posixpath
from gencrud.config.base import TemplateBase
from gencrud.constants import *


class FrontendInterface( TemplateBase ):
    def __init__( self, parent, **cfg ):
        TemplateBase.__init__(self, parent)
        self.__cfg = cfg
        return

    @property
    def Path(self):
        return self.__cfg.get( C_PATH )

    @property
    def Class(self) -> str:
        return self.__cfg.get( C_CLASS )

    @property
    def Filename( self ) -> str:
        return self.__cfg.get( C_FILENAME )

    @property
    def Templates( self ) -> dict:
        return self.__cfg.get( 'templates', {} )

    @property
    def Module( self ) -> str:
        return posixpath.split( self.__cfg.get( C_PATH ) )[ -1 ]


class BackendInterface( TemplateBase ):
    def __init__( self, parent, **cfg ):
        TemplateBase.__init__(self, parent)
        self.__cfg = cfg
        return

    @property
    def Path( self ):
        path = self.__cfg.get( C_PATH )
        if path is None:
            path = os.path.join( self.__cfg.get( C_PACKAGE ), self.__cfg.get( C_MODULE ) )

        return path

    @property
    def Module( self ):
        module = self.__cfg.get( C_MODULE )
        if module is None:
            return self.__cfg.get( C_PATH ).split( '/' )[ -1 ]

        return module

    @property
    def Package(self):
        package = self.__cfg.get( C_PACKAGE )
        if package is None:
            return self.__cfg.get( C_PATH ).split( '/' )[ 0 ]

        return package

    @property
    def PackageModule( self ):
        path = self.__cfg.get( C_PATH )
        if path is None:
            path = f"{ self.__cfg.get(C_PACKAGE) }.{ self.__cfg.get(C_MODULE) }"

        else:
            path = path.replace( '/', '.' ).replace( '\\', '.' )

        return path


class Interface( TemplateBase ):
    def __init__( self, parent, **cfg ):
        TemplateBase.__init__(self, parent)
        self.__cfg = cfg
        self.__frontend = FrontendInterface( self, **self.__cfg.get( C_FRONTEND, {} ) )
        self.__backend  = BackendInterface( self, **self.__cfg.get( C_BACKEND, {} ) )
        return

    @property
    def Backend(self) -> BackendInterface:
        return self.__backend

    @property
    def Frontend(self) -> FrontendInterface:
        return self.__frontend
