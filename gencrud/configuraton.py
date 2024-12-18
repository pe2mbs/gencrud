#
#   Python backend and Angular frontend code
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
import typing as t
import io
import gencrud.util.utils
from gencrud.config.object import TemplateObject, TemplateObjects
from gencrud.config.source import ( TemplateSourcePython, TemplateSourceAngular,
                                    TemplateSourceUnittest, TemplateSourceExtModels,
                                    TemplateSourceHelpPages )
from gencrud.config.options import TemplateOptions
from gencrud.config.references import TemplateReferences
from gencrud.config.dynamic.controls import DymanicControls
from gencrud.config.interface import Interface
from gencrud.constants import *
import jsonschema
from gencrud.schema import getSchema
import gencrud.myyaml as yaml

OptionalString = t.TypeVar( 'OptionalString', str, None )


class TemplateConfiguration( object ):
    def __init__( self, filename = None, **cfg ) -> None:
        # For some cases that the base config is required
        gencrud.util.utils.config = self
        if isinstance( filename, str ):
            with open( filename, 'r' ) as stream:
                self.__config = yaml.load( stream )

        elif isinstance( filename, io.IOBase ):
            self.__config = yaml.load( filename )

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
            GENCRUD_SCHEME = getSchema( self.__config.get( C_VERSION, 1 ) )
            jsonschema.Draft7Validator( GENCRUD_SCHEME )
            jsonschema.validate( instance = self.__config, schema = GENCRUD_SCHEME )

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
        self.__ext_models   = TemplateSourceExtModels( **self.__config )
        self.__help_pages   = TemplateSourceHelpPages( **self.__config )
        opts                = self.__config[ C_REFERENCES ] if C_REFERENCES in self.__config else { }
        self.__references   = TemplateReferences( **opts )
        self.__objects      = []
        for obj in self.__config[ C_OBJECTS ]:
            self.__objects.append( TemplateObject( self, **obj ) )

        self.__interface    = None
        if C_INTERFACE in self.__config:
            self.__interface = Interface( self, **self.__config[ C_INTERFACE ] )

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
    def ExtModels( self ) -> TemplateSourceExtModels:
        return self.__ext_models

    @property
    def HelpPages( self ) -> TemplateSourceHelpPages:
        return self.__help_pages


    @property
    def objects( self ) -> TemplateObjects:
        return self.__objects

    def __iter__( self ) -> t.Iterable[ TemplateObject ]:
        return iter( self.__objects )

    @property
    def application( self ) -> OptionalString:
        return self.__config.get( C_APPLICATION, None )

    @property
    def applicationType( self ) -> int:
        result = self.__config.get( C_APPLICATION, None )
        if isinstance( result, str ):
            return 1

        result = self.__config.get( "interface", None )
        if isinstance( result, dict ):
            if isinstance( result.get( 'backend' ), str ) and isinstance( result.get( 'frontend' ), str ):
                return 2

        raise Exception( "Invalid schema, missing application or interface" )

    def hasInterface( self ):
        return self.__interface is not None

    @property
    def Interface( self ) -> Interface:
        return self.__interface

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
