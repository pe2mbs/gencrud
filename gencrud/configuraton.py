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
from typing import TypeVar, Iterable
import yaml
import os
import gencrud.util.utils
from gencrud.config.object import TemplateObject, TemplateObjects
from gencrud.config.source import TemplateSourcePython, TemplateSourceAngular
from gencrud.config.options import TemplateOptions
from gencrud.config.references import TemplateReferences
from gencrud.config.dynamic.controls import DymanicControls
from gencrud.constants import *
from gencrud.util.exceptions import MissingAttribute


OptionalString = TypeVar( 'OptionalString', str, None )


class IncludeLoader( yaml.SafeLoader ):
    def __init__( self, stream ):
        self._root = os.path.split( stream.name )[ 0 ]
        super( IncludeLoader, self ).__init__( stream )
        return

    def include( self, node ):
        filename = os.path.join( self._root, self.construct_scalar( node ) )

        with open( filename, 'r' ) as f:
            return yaml.load( f, Loader = IncludeLoader )

IncludeLoader.add_constructor( '!include', IncludeLoader.include )


class TemplateConfiguration( object ):
    def __init__( self, **cfg ) -> None:
        # For some cases that the base config is required
        gencrud.util.utils.config = self
        self.__config       = cfg
        self.__controls     = None
        if 'objects' not in self.__config:
            raise MissingAttribute( 'root', 'objects' )

        if 'application' not in self.__config:
            raise MissingAttribute( 'root', 'application' )

        self.__noGenerate   = cfg.get( 'nogen', False )
        controls            = cfg.get( 'controls', None )
        if controls is not None:
            self.__controls = DymanicControls( controls )

        opts                = self.__config[ C_OPTIONS ] if C_OPTIONS in self.__config else { }
        self.__options      = TemplateOptions( **opts )
        self.__python       = TemplateSourcePython( **self.__config )
        self.__angular      = TemplateSourceAngular( **self.__config )
        opts                = self.__config[ C_REFERENCES ] if C_REFERENCES in self.__config else { }
        self.__references   = TemplateReferences( **opts )
        self.__objects      = []
        for obj in self.__config[ C_OBJECTS ]:
            self.__objects.append( TemplateObject( self, **obj ) )

        return

    @property
    def nogen( self ):
        return self.__noGenerate

    @property
    def parent( self ):
        return None

    @property
    def python( self ) -> TemplateSourcePython:
        return self.__python

    @property
    def angular( self ) -> TemplateSourceAngular:
        return self.__angular

    @property
    def objects( self ) -> TemplateObjects:
        return self.__objects

    def __iter__( self ) -> Iterable[ TemplateObject ]:
        return iter( self.__objects )

    @property
    def application( self ) -> OptionalString:
        return self.__config.get( C_APPLICATION, None )

    @property
    def options( self ) -> TemplateOptions:
        return self.__options

    @property
    def references( self ) -> TemplateReferences:
        return self.__references

    @property
    def controls( self ) -> DymanicControls:
        return self.__controls

    @property
    def version( self ):
        return self.__config.get( 'version', 1 )