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
from gencrud.constants import *

C_APP                   = 'app'


class TemplateImport( object ):
    def __init__( self, **cfg ):
        self.__config = cfg
        return

    @property
    def module( self ) -> str:
        return self.__config.get( C_MODULE, '' )

    @property
    def component( self ) -> str:
        return self.__config.get( C_COMPONENT, '' )

    @property
    def type( self ) -> str:
        return self.__config.get( C_TYPE, '' ).lower()

    @property
    def where( self ) -> str:
        return self.__config.get( C_WHERE, C_APP ).lower()

    @property
    def path( self ) -> str:
        return self.__config.get( C_PATH, '.' )


class TemplateExtra( object ):
    def __init__( self, parent, **cfg ):
        self.__config       = cfg
        self.__parent       = parent
        self.__modules      = []
        self.__components   = [ ]
        for inp in self.__config.get( C_IMPORTS, [ ] ):
            if C_MODULE in inp:
                self.__modules.append( TemplateImport( **inp ) )

            elif C_COMPONENT in inp:
                self.__components.append( TemplateImport( **inp ) )

            else:
                raise Exception( "Missing module or component in imports" )

        return

    def getTypeScriptInports( self, where = C_APP ) -> list:
        result = []
        for inp in self.__modules:
            if inp.type == C_TYPESCRIPT and inp.where == where:
                result.append( inp )

        return result

    def getPythonInports( self, where = C_APP ) -> list:
        result = [ ]
        for inp in self.__modules:
            if inp.type == C_PYTHON and inp.where == where:
                result.append( inp )

        return result

    def getTypeScriptComponents( self, where = C_APP ) -> list:
        result = [ ]
        for inp in self.__components:
            if inp.type == C_TYPESCRIPT and inp.where == where:
                result.append( inp )

        return result
