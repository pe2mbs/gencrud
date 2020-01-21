#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2020 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
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
from gencrud.config.angularmod import TemplateAngularModule
from gencrud.config.base import TemplateBase


class TemplateReferences( TemplateBase ):
    def __init__( self, **cfg ):
        TemplateBase.__init__( self, None )
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
