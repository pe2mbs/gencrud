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
class TemplateImport():
    def __init__( self, **cfg ):
        self.__config = cfg
        return

    @property
    def module( self ):
        return self.__config.get( 'module', '' )

    @property
    def component( self ):
        return self.__config.get( 'component', '' )

    @property
    def type( self ):
        return self.__config.get( 'type', '' ).lower()

    @property
    def where( self ):
        return self.__config.get( 'where', 'app' ).lower()

    @property
    def path( self ):
        return self.__config.get( 'path', '.' )


class TemplateExtra( object ):
    def __init__( self, parent, **cfg ):
        self.__config       = cfg
        self.__parent       = parent
        self.__modules      = []
        self.__components   = [ ]
        for inp in self.__config.get( 'imports', [ ] ):
            if 'module' in inp:
                self.__modules.append( TemplateImport( **inp ) )

            elif 'component' in inp:
                self.__components.append( TemplateImport( **inp ) )

            else:
                raise Exception( "Missing module or component in imports" )

        return

    def getTypeScriptInports( self, where = 'app' ):
        result = []
        for inp in self.__modules:
            if inp.type == 'typescript' and inp.where == where:
                result.append( inp )

        return result

    def getPythonInports( self, where = 'app' ):
        result = [ ]
        for inp in self.__modules:
            if inp.type == 'python' and inp.where == where:
                result.append( inp )

        return result

    def getTypeScriptComponents( self, where = 'app' ):
        result = [ ]
        for inp in self.__components:
            if inp.type == 'typescript' and inp.where == where:
                result.append( inp )

        return result