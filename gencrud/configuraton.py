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
from typing import TypeVar
import gencrud.util.utils
from gencrud.objects.object import TemplateObject
from gencrud.source import TemplateSourcePython, TemplateSourceAngular
from gencrud.constants import *

OptionalString = TypeVar('OptionalString', str, None)


class TemplateOptions( object ):
    def __init__( self, **cfg ) -> None:
        self.__config = cfg
        return

    @property
    def useModule( self ) -> bool:
        # This override/set commandline options from the template defintion.
        return self.__config.get( C_USE_MODULE, gencrud.util.utils.useModule )

    @property
    def backupFiles( self ) -> bool:
        # This override/set commandline options from the template defintion.
        return self.__config.get( C_BACKUP, gencrud.util.utils.backupFiles )

    @property
    def ignoreCaseDbIds( self ) -> bool:
        # This override/set commandline options from the template defintion.
        return self.__config.get( C_IGNORE_CASE_DB_IDS, gencrud.util.utils.ignoreCaseDbIds )

    @property
    def overWriteFiles( self ) -> bool:
        # This override/set commandline options from the template defintion.
        return self.__config.get( C_OVERWRITE, gencrud.util.utils.overWriteFiles )

    @property
    def lazyLoading( self ) -> bool:
        # This override/set commandline options from the template defintion.
        return self.__config.get( C_LAZY_LOADING, gencrud.util.utils.lazyLoading )


class TemplateObjects( list ):
    pass


class TemplateAngularModule( object ):
    def __init__( self, default_filename, default_class, default_module = None, **cfg ):
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


class TemplateReferences( object ):
    def __init__( self, **cfg ):
        self.__config = cfg
        tmp             = self.__config[ C_APP_MODULE ] if C_APP_MODULE in self.__config else { }
        self.__main     = TemplateAngularModule( 'app.module.ts',
                                             'AppModule',
                                             **tmp )
        tmp             = self.__config[ C_APP_ROUTING ] if C_APP_ROUTING in self.__config else { }
        self.__rout     = TemplateAngularModule( 'app.routing.module.ts',
                                                'AppRoutingModule',
                                                **tmp )
        return

    @property
    def app_module( self ) -> TemplateAngularModule:
        return self.__main

    @property
    def app_routing( self ) -> TemplateAngularModule:
        return self.__rout


class TemplateConfiguration( object ):
    def __init__( self, **cfg ) -> None:
        # For some cases that the base config is required
        gencrud.util.utils.config = self
        self.__config       = cfg
        opts                = self.__config[ C_OPTIONS ] if C_OPTIONS in self.__config else { }
        self.__options      = TemplateOptions( **opts )
        self.__python       = TemplateSourcePython( **self.__config )
        self.__angular      = TemplateSourceAngular( **self.__config )
        opts                = self.__config[ C_REFERENCES ] if C_REFERENCES in self.__config else { }
        self.__references   = TemplateReferences( **opts )
        self.__objects      = TemplateObjects()
        for obj in self.__config[ C_OBJECTS ]:
            self.__objects.append( TemplateObject( self, **obj ) )

        return

    @property
    def python( self ) -> TemplateSourcePython:
        return self.__python

    @property
    def angular( self ) -> TemplateSourceAngular:
        return self.__angular

    @property
    def objects( self ) -> TemplateObjects:
        return self.__objects

    def __iter__( self ):
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
