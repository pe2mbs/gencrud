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

from gencrud.objects.menuitem import TemplateMenuItem
from gencrud.objects.table import TemplateTable
from gencrud.objects.actions.actions import TemplateActions
from gencrud.objects.extra import TemplateExtra
from gencrud.constants import *

class TemplateObject( object ):
    def __init__( self, parent, **cfg ):
        self.__config       = cfg
        self.__parent       = parent
        self.__menu         = TemplateMenuItem( C_MENU, **cfg ) if C_MENU in cfg else None
        self.__actions      = TemplateActions( self, self.name, self.__config.get( C_ACTIONS, [] ) )
        self.__table        = TemplateTable( **self.__config.get( C_TABLE, {} ) )
        self.__extra        = TemplateExtra( self, **self.__config.get( C_EXTRA, {} ) )
        return

    #
    #   Configuration properties
    #
    @property
    def title( self ):
        return self.__config.get( C_TITLE, self.__config.get( C_CLASS, '<-Unknown->' ) )

    @property
    def name( self ):
        return self.__config.get( C_NAME, '' )

    @property
    def cls( self ):
        return self.__config.get( C_CLASS, '' )

    @property
    def uri( self ):
        return self.__config.get( C_URI, '' )

    @property
    def actions( self ):
        return self.__actions

    def hasExtra( self ):
        return self.__extra is not None

    @property
    def extra( self ):
        return self.__extra

    @property
    def menu( self ):
        return self.__menu

    @property
    def table( self ):
        return self.__table

    @property
    def actionWidth( self ):
        return self.__config.get( C_ACTION_WIDTH, '5%' )

    #
    #   internal functions and properties to gencrud
    #
    def orderBy( self ):
        orderList = []
        for field in self.__table.orderBy:
            orderList.append( 'order_by( {}.{} )'.format( self.cls, field ) )

        return '.'.join( orderList )

    @property
    def externalService( self ):
        FILLER = '                 , '
        FILLER_LF = '\r\n                 , '
        result = []
        for field in self.__table.columns:
            if field.ui is not None:
                if field.ui.isCombobox() or field.ui.isChoice():
                    if field.ui.service is not None:
                        result.append( 'public {name}Service: {cls}'.format(
                                        name = field.ui.service.name,
                                        cls = field.ui.service.cls ) )
                    elif field.ui.hasResolveList():
                        pass

                    else:
                        raise Exception( "service missing in {} in field {}".format( self.__table.name, field.name )  )

        return ( FILLER if len( result ) > 0 else '' ) + ( FILLER_LF.join( result ) )
