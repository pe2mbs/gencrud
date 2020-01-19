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
#
import logging
from gencrud.config.base import TemplateBase
from gencrud.config._inports import SourceImport
from gencrud.config.column import TemplateColumn
from gencrud.config.tab import TemplateTabs
from gencrud.config.sort import SortInfo
from gencrud.config.mixin import TemplateMixin
import gencrud.util.utils as root
from gencrud.constants import *

logger = logging.getLogger()


class InvalidViewSize( Exception ):
    def __init__(self):
        Exception.__init__( self, "Invalid parameter 'viewSize', may be integer (5, 10, 25, 100) or " +
                            "string with service class name of where the function getViewSize() resides." )
        return


class TemplateTable( TemplateBase ):
    def __init__( self, parent, **table ):
        TemplateBase.__init__( self, parent )
        self.__table            = table
        self.__columns          = []
        self.__primaryKey       = ''
        self.__viewSort         = None
        self.__viewSize         = None
        self.__defaultViewSize  = 10
        self.__inports          = SourceImport()
        for col in self.__table[ C_COLUMNS ]:
            column = TemplateColumn( self, self.name, **col )
            self.__columns.append( column )
            if column.isPrimaryKey():
                self.__primaryKey = column.name

        if C_VIEW_SORT in table:
            self.__viewSort = SortInfo( table[ C_VIEW_SORT ] )

        if C_VIEW_SIZE in table:
            if type( table[ C_VIEW_SIZE ] ) in ( int, str ):
                self.__viewSize = table[ C_VIEW_SIZE ]

            else:
                raise InvalidViewSize()

        self.__mixin = TemplateMixin( table[ C_MIXIN ] if C_MIXIN in table else None )
        return

    @property
    def object( self ):
        return self.parent

    def __iter__(self):
        return iter( self.__columns )

    @property
    def config( self ):
        return self.object.config

    def hasTabs( self, tp = C_DIALOG ) -> bool:
        return len( self.__table.get( tp + C_TABS, [] ) ) > 0

    def tabs( self, tp = C_DIALOG ) -> TemplateTabs:
        return TemplateTabs( self, **self.__table.get( tp + C_TABS, {} ) )

    @property
    def Mixin( self ) -> TemplateMixin:
        return self.__mixin

    def sortedInfo( self ) -> str:
        if self.__viewSort is not None:
            return self.__viewSort.htmlMaterialSorting()

        return ''

    @property
    def leadIn( self ) -> str:
        result = []
        for column in self.__columns:
            for leadin in column.leadIn:
                if leadin not in result:
                    result.append( leadin )

        logger.info( "LeadIn = {}".format( result ) )
        return '\n'.join( result )

    @property
    def tableName( self ) -> str:
        if root.config.options.ignoreCaseDbIds:
            return self.__table.get( C_NAME, '' ).lower()

        return self.__table.get( C_NAME, '' )

    @property
    def name( self ) -> str:
        if root.config.options.ignoreCaseDbIds:
            return self.__table.get( C_NAME, '' ).lower()

        return self.__table.get( C_NAME, '' )

    @property
    def orderBy( self ) -> list:
        return self.__table.get( C_ORDER_BY, [ self.__primaryKey ] )

    @property
    def uniqueKey( self ) -> dict:
        values  = {}
        for value in self.__table.get( C_UNIQUE_KEY, {} ):
            for key in value.keys():
                values[ key ] = ', '.join( [ "'{0}'".format( x ) for x in value[ key ] ] )

        return values

    def hasUniqueKey( self ) -> bool:
        if C_UNIQUE_KEY in self.__table:
            if type( self.__table.get( C_UNIQUE_KEY, None ) ) in ( dict, tuple, list ):
                return True

        return False

    @property
    def hasAutoUpdate( self ) -> bool:
        for field in self.__columns:
            if field.hasAutoUpdate:
                return True

        return False

    @property
    def columns( self ):
        return self.__columns

    @property
    def primaryKey( self ) -> str:
        return self.__primaryKey

    @property
    def listViewColumns( self ) -> list:
        return sorted( [ col for col in self.__columns if col.listview.index is not None ],
                       key = lambda col: col.listview.index )

    def buildFilter( self ) -> str:
        result = [ ]
        for item in self.listViewColumns:
            if item.ui.isChoice() or item.ui.isCombobox():
                result.append( "( this.{0}_Label( record.{0} ) )".format( item.name ) )

            elif item.ui.isCheckbox() or item.ui.isSliderToggle():
                result.append( "( this.{0}_Label( record.{0} ) )".format( item.name ) )

            elif item.tsType == 'string':
                result.append( "( record.{0} || '' )".format( item.name ) )

        if len( result ) == 0:
            return "''"

        return ' + \r\n                   '.join( result )

    @property
    def viewSort( self ) -> SortInfo:
        return self.__viewSort

    @property
    def hasViewSizeService( self ) -> bool:
        if self.__viewSize is not None:
            return type( self.__viewSize ) is str

        return False

    @property
    def hasViewSizeValue( self ) -> bool:
        if self.__viewSize is not None:
            return type( self.__viewSize ) is int

        return False

    @property
    def viewSize( self ):
        return self.__viewSize

    def __repr__(self):
        return "<TemplateTable name={}, table={}>".format( self.name, self.tableName )
