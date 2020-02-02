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


class TemplateAngularModule( object ):
    def __init__( self, default_filename, default_class, default_module = None, **cfg ):
        TemplateBase.__init__( self, None )
        self.__filename = default_filename
        self.__class = default_class
        self.__module = default_module or default_class
        self.__config = cfg
        return

    @property
    def filename( self ) -> str:
        return self.__config.get( C_FILENAME, self.__filename )

    @property
    def cls( self ) -> str:
        return self.__config.get( C_CLASS, self.module if self.__class is None else self.__class )

    @property
    def module( self ) -> str:
        return self.__config.get( C_MODULE, self.__module )
