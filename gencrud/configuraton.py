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
from ruamel import yaml
import os
import io
import gencrud.util.utils
from gencrud.config.object import TemplateObject, TemplateObjects
from gencrud.config.source import TemplateSourcePython, TemplateSourceAngular, TemplateSourceUnittest
from gencrud.config.options import TemplateOptions
from gencrud.config.references import TemplateReferences
from gencrud.config.dynamic.controls import DymanicControls
from gencrud.constants import *
from gencrud.util.exceptions import MissingAttribute
import jsonschema
from gencrud.schema import GENCRUD_SCHEME


OptionalString = TypeVar( 'OptionalString', str, None )

def my_compose_document(self):
    self.get_event()
    node = self.compose_node(None, None)
    self.get_event()
    # self.anchors = {}    # <<<< commented out
    return node


yaml.SafeLoader.compose_document = my_compose_document


def yaml_include( loader, node ):
    if node.value.startswith( '.' ):
        include_name = os.path.join( os.path.dirname( node.start_mark.name ), node.value )

    else:
        include_name = node.value

    include_name = os.path.abspath( include_name )
    with open( include_name, 'r' ) as inputfile:
        data = my_safe_load( inputfile, master = loader )
        return data


yaml.add_constructor( "!include", yaml_include, Loader=yaml.SafeLoader )


def my_safe_load(stream, Loader=yaml.SafeLoader, master=None):
    loader = Loader(stream)
    if master is not None:
        loader.anchors = master.anchors

    try:
        return loader.get_single_data()

    finally:
        loader.dispose()

#
# class IncludeLoader( yaml.SafeLoader ):
#     def __init__( self, stream ):
#         self._root = os.path.split( stream.name )[ 0 ]
#         super( IncludeLoader, self ).__init__( stream )
#         return
#
#     def include( self, node ):
#         filename = os.path.join( self._root, self.construct_scalar( node ) )
#
#         with open( filename, 'r' ) as f:
#             return yaml.load( f, Loader = IncludeLoader )
#
# IncludeLoader.add_constructor( '!include', IncludeLoader.include )


class TemplateConfiguration( object ):
    def __init__( self, filename = None, **cfg ) -> None:
        # For some cases that the base config is required
        gencrud.util.utils.config = self
        if isinstance( filename, str ):
            with open( filename, 'r' ) as stream:
                self.__config = my_safe_load( stream )

        elif isinstance( filename, io.IOBase ):
            self.__config = my_safe_load( filename )

        else:
            self.__config       = cfg
        
        # in case there is a 'defaults' field specified, we need to concat
        # its content with the root dict. This is a workaround since
        # include cannot be used at root level alongside other fields
        if C_DEFAULTS in self.__config:
            self.__config = dict(self.__config[C_DEFAULTS], **self.__config)
            del self.__config[C_DEFAULTS]

        # Veryfy the loaded template against the schema
        try:
            jsonschema.Draft7Validator(GENCRUD_SCHEME)
            jsonschema.validate(instance=self.__config, schema=GENCRUD_SCHEME)

        except jsonschema.SchemaError as exc:
            print(exc)
            raise SystemExit

        except jsonschema.ValidationError as exc:
            print(exc)
            raise SystemExit

        self.__controls     = None
        controls            = cfg.get( C_CONTROLS, None )
        if controls is not None:
            self.__controls = DymanicControls( controls )

        opts                = self.__config[ C_OPTIONS ] if C_OPTIONS in self.__config else { }
        self.__options      = TemplateOptions( **opts )
        # encapsulate the information where python/angular templates are located and where
        # the output location is
        self.__python       = TemplateSourcePython( **self.__config )
        self.__angular      = TemplateSourceAngular( **self.__config )
        self.__unittest     = TemplateSourceUnittest( **self.__config )
        opts                = self.__config[ C_REFERENCES ] if C_REFERENCES in self.__config else { }
        self.__references   = TemplateReferences( **opts )
        self.__objects      = []
        for obj in self.__config[ C_OBJECTS ]:
            self.__objects.append( TemplateObject( self, **obj ) )
        return

    @property
    def nogen( self ):
        return self.__config.get( C_NO_GENERATE, False )

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
    def unittest( self ) -> TemplateSourceUnittest:
        return self.__unittest

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
        return self.__config.get( C_VERSION, C_VERSION_DEFAULT )