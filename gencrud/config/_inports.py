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
from nltk.tokenize import word_tokenize


class SourceItemImport( object ):
    def __init__( self, name = '', module = '' ):
        self.__name     = name
        self.__module   = module
        return

    @property
    def module( self ):
        return self.__module

    @property
    def name( self ):
        return self.__name


class SourceImport( object ):
    def __init__( self ):
        self.__pyList = []
        self.__tsList = []
        return

    @property
    def python(self):
        return self.__pyList

    @property
    def typescript(self):
        return self.__tsList

    def appendPy(self, data ):
        def exists( exist_name, exist_module ):
            found = False
            for obj in self.__pyList:
                if obj.module == exist_module and obj.name == exist_name:
                    found = True
                    break

            return found

        if type( data ) in ( list, tuple ):
            pass

        elif type( data ) is str:
            data = data.split( ',' )

        else:
            raise Exception( 'Invalid data type for python inport' )

        for importDef in data:
            name, module = word_tokenize( importDef )
            if not exists( name, module ):
                self.__pyList.append( SourceItemImport( name, module ) )

        return

    def appendTs(self, data ):
        def exists( exist_name, exist_module ):
            found = False
            for obj in self.__tsList:
                if obj.module == exist_module and obj.name == exist_name:
                    found = True
                    break

            return found

        if type( data ) in ( list, tuple ):
            pass

        elif type( data ) is str:
            data = data.split( ',' )

        else:
            raise Exception( 'Invalid data type for typescript inport' )

        for importDef in data:
            name, module = word_tokenize( importDef )
            if not exists( name, module ):
                self.__tsList.append( SourceItemImport( name, module ) )

        return

    def append( self, source, data ):
        if source == 'pyInport':
            self.appendPy( data )

        elif source == 'tsInport':
            self.appendTs( data )

        else:
            raise Exception( 'Invalid import type {0}'.format( source ) )

        return
