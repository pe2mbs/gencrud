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
import logging
from gencrud.constants import *
from gencrud.config.base import TemplateBase

logger = logging.getLogger()


class TemplateListView( TemplateBase ):
    def __init__( self, parent, **cfg ):
        TemplateBase.__init__( self, parent )
        self.__cfg      = cfg
        return

    def __len__( self ):
        return len( self.__cfg )

    def get( self, name, def_value ):
        return self.__cfg.get( name, def_value )

    @property
    def width( self ):
        if C_WIDTH not in self.__cfg:
            if hasattr( self.parent, C_CSS ):
                return self.parent.css.width

        return self.__cfg.get( C_WIDTH, None )

    @property
    def index( self ):
        if C_INDEX not in self.__cfg:
            if hasattr( self.parent, C_INDEX ):
                return self.parent.index

        return self.__cfg.get( C_INDEX, None )

    @property
    def filter( self ):
        return self.__cfg.get( C_FILTER, False )

    @property
    def sort( self ):
        return self.__cfg.get( C_SORT, False )