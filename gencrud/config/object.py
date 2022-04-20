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
from typing import List
import logging
from gencrud.config.menuitem import TemplateMenuItem
from gencrud.config.table import TemplateTable
from gencrud.config.actions import TemplateActions
from gencrud.config.extra import TemplateExtra
from gencrud.constants import *
from gencrud.config.base import TemplateBase
from gencrud.util.exceptions import MissingAttribute
from gencrud.config.mixin import TemplateMixin
import posixpath


logger = logging.getLogger()


class AngularModule( TemplateBase ):
    def __init__( self,parent, **cfg ):
        TemplateBase.__init__( self,parent )
        self.__config = cfg
        return

    @property
    def path( self ):
        return self.__config.get( C_PATH, self.get_default( C_PATH  ) )

    @property
    def cls( self ):
        # print( self.__config )
        return self.__config.get( C_CLASS, self.get_default( C_MODULE ) )

    @property
    def module( self ):
        return self.__config.get( C_MODULE, "module" )

    @property
    def importPath( self ):
        if '.' in self.path or '/' in self.path:
            # seems to be a full path
            path = posixpath.join( self.path, self.module )

        else:
            # Another module should be one level up in the filesystem
            path = posixpath.join( "..", self.path, self.module )

        return path

    # "import {{ {modCls} }} from '{path}';".format( modCls = mod.module, path = path ) )


class AngularModules( TemplateBase ):
    def __init__( self, parent, cfg ):
        TemplateBase.__init__( self, parent )
        self.__config       = []
        for i in cfg:
            self.__config.append( AngularModule( self, **i ) )

        return

    def __iter__(self):
        return iter( self.__config )

    @property
    def items(self):
        return self.__config


class InjectionBlockTemplate( TemplateBase ):
    def __init__( self, parent, cfg ):
        TemplateBase.__init__( self,parent )
        self.__config = cfg
        return

    def hasDeclarations( self ):
        return self.hasDialog() or self.hasScreen()

    @property
    def declarations( self ):
        declare = []
        if self.hasDialog():
            declare.append( self.dialogComponent() )

        if self.hasScreen():
            declare.append( self.screenComponent() )

        if len( declare ) > 0:
            return ", ".join( declare )

        return ""

    def hasEntryComponents( self ):
        return self.hasDialog()

    @property
    def entryComponents( self ):
        declare = [ ]
        if self.hasDialog():
            declare.append( self.dialogComponent() )

        if len( declare ) > 0:
            return ", ".join( declare )

        return ""

    def hasExports( self ):
        return self.hasDialog() or self.hasScreen() or self.hasProviders()

    @property
    def exports( self ):
        declare = []
        if self.hasDialog():
            declare.append( self.dialogComponent() )

        if self.hasScreen():
            declare.append( self.screenComponent() )

        if self.hasImports():
            declare.append( self.imports )

        if len( declare ) > 0:
            return ", ".join( declare )

        return ""

    def hasScreen( self ):
        return 'screen' in self.__config

    def screenComponent( self ):
        return self.__config.get( 'screen', None )

    def hasDialog( self ):
        return 'dialog' in self.__config

    def dialogComponent( self ):
        return self.__config.get( 'dialog', None )

    def hasProviders( self ):
        return 'providers' in self.__config

    @property
    def providers( self ):
        declare = [ ]
        if self.hasProviders():
            for provider in self.__config.get( 'providers',[ ] ):
                declare.append( provider )

        if len( declare ) > 0:
            return ", ".join( declare )

        return ""

    def hasImports( self ):
        return 'imports' in self.__config

    @property
    def imports( self ):
        declare = []
        if self.hasImports():
            for filename, objectName in self.__config.get( 'imports', {} ).items():
                declare.append( objectName )

        if len( declare ) > 0:
            return ", ".join( declare )

        return ""


class InjectionTemplate( TemplateBase ):
    def __init__( self,parent, cfg ):
        TemplateBase.__init__( self,parent )
        self.__config = cfg
        self.__moduleTs = InjectionBlockTemplate( self,self.__config.get( 'module.ts',None ) )
        return

    def hasModuleTs( self ):
        return 'module.ts' in self.__config

    @property
    def moduleTs( self ):
        return self.__moduleTs


class TemplateObject( TemplateBase ):
    def __init__( self, parent, **cfg ):
        TemplateBase.__init__( self, parent )
        self.__config       = cfg
        if 'name' not in self.__config:
            raise MissingAttribute( 'object', 'name' )

        if 'uri' not in self.__config:
            raise MissingAttribute( 'object', 'url' )

        if 'table' not in self.__config:
            raise MissingAttribute( 'object', 'table' )

        self.__menu         = TemplateMenuItem( C_MENU, **cfg ) if C_MENU in cfg else None
        self.__actions      = TemplateActions( self, self.name, self.__config.get( C_ACTIONS, [] ) )
        self.__table        = TemplateTable( self, **self.__config.get( C_TABLE, {} ) )
        self.__extra        = TemplateExtra( self, **self.__config.get( C_EXTRA, {} ) )
        self.__mixin        = TemplateMixin( self, **self.__config.get( C_MIXIN, {} ) )
        return

    #
    #   Configuration properties
    #
    @property
    def title( self ) -> str:
        return self.__config.get( C_TITLE, self.__config.get( C_CLASS, '<-Unknown->' ) )

    @property
    def name( self ) -> str:
        return self.__config.get( C_NAME, '' )

    @property
    def module( self ) -> str:
        return self.__config.get( C_NAME, '' )

    @property
    def modules( self ):
        return AngularModules( self, self.__config.get( 'modules', [] ) )

    @property
    def cls( self ) -> str:
        return self.__config.get( C_CLASS, '' )

    @property
    def Mixin( self ):
        return self.__mixin

    @property
    def uri( self ) -> str:
        return self.__config.get( C_URI, '' )

    def hasMenu( self ):
        return self.__menu is not None

    def hasRoute( self ):
        return self.__menu is None

    @property
    def route( self ) -> str:
        route = self.__config.get( C_ROUTE, self.__config.get( C_NAME, '' ) )
        if route.startswith( '/' ):
            return route[ 1 : ]

        return route

    @property
    def actions( self ) -> TemplateActions:
        return self.__actions

    def hasExtra( self )  -> bool:
        return self.__extra is not None

    @property
    def extra( self ) -> TemplateExtra:
        return self.__extra

    @property
    def menu( self ) -> TemplateMenuItem:
        return self.__menu

    @property
    def table( self ) -> TemplateTable:
        return self.__table

    @property
    def actionWidth( self ) -> str:
        return self.__config.get( C_ACTION_WIDTH, '5%' )

    def hasAutoUpdate( self ):
        return 'autoupdate' in self.__config

    @property
    def injection( self ):
        return InjectionTemplate( self, self.__config.get( 'injection', {} ) )

    def ignoreTemplates( self, templateFilename: str ):
        if templateFilename.endswith( 'module.ts.templ' ):
            logger.info( "Ignore template {} ".format( templateFilename ) )
            return True

        for item in self.__config.get( 'ignore_templates', [] ):
            if not item.strip().endswith( '.templ' ):
                item = item.strip() + '.templ'

            if templateFilename.endswith( item ):
                logger.info( "Ignore template {} ".format( templateFilename ) )
                return True

        return False

    @property
    def AutoUpdate( self ):
        autoUpdate = self.__config.get( 'autoupdate', '' )
        if isinstance( autoUpdate, str ):
            if autoUpdate.isdigit():
                return int( autoUpdate )

            autoUpdate = 120

        return autoUpdate

    #
    #   internal functions and properties to gencrud
    #
    def orderBy( self ) -> str:
        orderList = []
        for field in self.__table.orderBy:
            orderList.append( 'order_by( {}.{} )'.format( self.cls, field ) )

        return '.'.join( orderList )

    # @property
    # def externalService( self ) -> str:
    #     FILLER = '                 , '
    #     FILLER_LF = '\r\n                 , '
    #     result = []
    #     for field in self.__table.columns:
    #         if field.ui is not None:
    #             if field.ui.isCombobox() or field.ui.isChoice():
    #                 if field.ui.service is not None:
    #                     result.append( 'public {name}Service: {cls}'.format(
    #                                     name = field.ui.service.name,
    #                                     cls = field.ui.service.cls ) )
    #                 elif field.ui.hasResolveList():
    #                     pass
    #
    #                 else:
    #                     raise Exception( "service missing in {} in field {}".format( self.__table.name, field.name )  )
    #
    #     return ( FILLER if len( result ) > 0 else '' ) + ( FILLER_LF.join( result ) )


TemplateObjects = List[ TemplateObject ]
