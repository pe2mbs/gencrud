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
# --------
# dont delete, required for exec method
import os
import datetime
# ---------

logger = logging.getLogger()


class TemplateTestData( TemplateBase ):
    def __init__( self, parent, **cfg ):
        TemplateBase.__init__( self, parent )
        self.__values = []
        self.__cfg = cfg
        if C_VALUE in cfg:
            self.__values = [cfg[C_VALUE]]
        elif C_VALUES in cfg:
            self.__values = cfg[C_VALUES]
        return

    def __iter__( self ):
        return iter( self.__values )

    def __len__( self ):
        return len( self.__values )

    def __getitem__(self, item):
        return self.valueAt(item)

    @property
    def value( self ):
        if len(self.__values) > 0:
            val = self.__values[0]
            if val is None:
                return None
            if isinstance(val, str) and "python:" in val:
                return val[7:]
            return val
        return None


    def valueAt( self, index ):
        if len(self.__values) > index:
            val = self.__values[index]
            if val is None:
                return None
            if isinstance(val, str) and "python:" in val:
                return val[7:]
            return val
        return None

    @property
    def values( self ):
        return self.__values

    def hasStringValue( self ) -> bool :
        if len(self.__values) > 0:
            val = self.__values[0]
            if val is None:
                return False
            if isinstance(val, str) and "python:" in val:
                return False
            return isinstance(val, str)
        return False

    def hasJSONValue( self ) -> bool :
        if len(self.__values) > 0:
            val = self.__values[0]
            if val is None:
                return False
            return isinstance(val, dict)
        return False
