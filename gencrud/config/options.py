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
from gencrud.constants import *
import gencrud.util.utils
from gencrud.config.base import TemplateBase


class TemplateOptions( TemplateBase ):
    def __init__( self, **cfg ) -> None:
        TemplateBase.__init__( self, None )
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

    @property
    def generateFrontend( self ) -> bool:
        # This override/set commandline options from the template defintion.
        return self.__config.get( C_GENERATE_FRONTEND, True )

    @property
    def generateBackend( self ) -> bool:
        # This override/set commandline options from the template defintion.
        return self.__config.get( C_GENERATE_BACKEND, True )

    @property
    def generateTests( self ) -> bool:
        # This override/set commandline options from the template defintion.
        return self.__config.get( C_GENERATE_TESTS, True )

    @property
    def copySupport( self ):
        return self.__config.get( 'copy-support-files', True )

    @property
    def useLocalTemplate( self ):
        return self.__config.get( 'use-local-template', False )