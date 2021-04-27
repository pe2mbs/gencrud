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
import os
from gencrud.util.exceptions import (MissingTemplate,
                                     MissingSourceFolder,
                                     KeyNotFoundException,
                                     MissingTemplateFolder,
                                     PathNotFoundException)
from gencrud.util.utils import get_platform
from gencrud.constants import *
from gencrud.config.base import TemplateBase


class TemplateSource( TemplateBase ):
    def __init__( self, tp, cfg ):
        TemplateBase.__init__( self, None )
        self.__config = cfg
        self.__key = tp
        self.__source = self.__config.get( self.platform, self.__config ).get( C_SOURCE, {} )
        return

    @property
    def baseFolder( self ) -> str:
        folder = self.__source.get( C_BASE, os.getcwd() )
        if not os.path.isdir( folder ):
            raise PathNotFoundException( folder )

        return folder

    @property
    def sourceFolder( self ) -> str:
        folder = self.__source.get( self.__key, None )
        if folder is None:
            raise KeyNotFoundException( "{}.{}".format( C_SOURCE, self.__key ) )

        if not folder.startswith( os.path.sep ):
            # not absolute path
            # first test with baseFolder
            if os.path.isdir( os.path.join( self.baseFolder, folder ) ):
                folder = os.path.join( self.baseFolder, folder )

            folder = os.path.abspath( folder )

        if not os.path.isdir( folder ):
            raise MissingSourceFolder( folder )

        return folder

    def __repr__( self ):
        return """<TemplateSource {key}
        base = {base} 
        source = {src}
        template = {templ}>""".format( key      = self.__key,
                                       src      = self.sourceFolder,
                                       templ    = self.templateFolder,
                                       base     = self.baseFolder )


class TemplateSourcePython( TemplateSource ):
    def __init__( self, cfg ):
        TemplateSource.__init__( self, C_PYTHON, cfg )
        return


class TemplateSourceAngular( TemplateSource ):
    def __init__( self, cfg ):
        TemplateSource.__init__( self, C_ANGULAR, cfg )
        return
