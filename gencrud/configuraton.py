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
import gencrud.util.utils
from gencrud.objects.object import TemplateObject
from gencrud.source import TemplateSourcePython, TemplateSourceAngular


class TemplateConfiguration( object ):
    def __init__( self, **cfg ):
        self.__config   = cfg
        self.__python   = TemplateSourcePython( **self.__config )
        self.__angular  = TemplateSourceAngular( **self.__config )
        self.__objects  = []
        for obj in cfg[ 'objects' ]:
            self.__objects.append( TemplateObject( self, **obj ) )

        return

    @property
    def python( self ):
        return self.__python

    @property
    def angular( self ):
        return self.__angular

    @property
    def objects( self ):
        return self.__objects

    def __iter__( self ):
        return iter( self.__objects )

    @property
    def application( self ):
        return self.__config.get( 'application', None )

    def options( self ):
        opts = self.__config.get( 'options', None )
        if opts is not None:
            gencrud.util.utils.useModule = opts.get( 'use-module', False )
            gencrud.util.utils.backupFiles = opts.get( 'backup', False )
            gencrud.util.utils.lowerCaseDbIds = opts.get( 'case-insensitive-db-ids', False )

        return
