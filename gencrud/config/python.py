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


class PythonObject( TemplateBase ):
    def __init__( self, obj ):
        TemplateBase.__init__( self, None )
        self.__object   = obj
        self.__module   = None
        self.__class    = None
        if obj is not None and '.' in obj:
            self.__module, self.__class = obj.rsplit( '.', 1 )

        return

    @property
    def Available( self ):
        return self.__object is not None

    @property
    def Class( self ):
        return self.__class

    @property
    def Module( self ):
        return self.__module
