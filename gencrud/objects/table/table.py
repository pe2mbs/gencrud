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
from gencrud.objects.table._inports import SourceImport
from gencrud.objects.table.column import TemplateColumn
from gencrud.objects.table.column.tab import TemplateTabs
from gencrud.objects.table.sort import SortInfo
from gencrud.objects.table.mixin import TemplateMixin
import gencrud.util.utils

logger = logging.getLogger()


class TemplateTable( object ):
    def __init__( self, **table ):
        self.__table            = table
        self.__columns          = []
        self.__primaryKey       = ''
        self.__viewSort         = None
        self.__viewSize         = None
        self.__defaultViewSize  = 10
        self.__inports          = SourceImport()
        noColumns               = len( self.__table[ 'columns' ] )
        for col in self.__table[ 'columns' ]:
            column = TemplateColumn( noColumns,
                                     self.name,
                                     **col )
            self.__columns.append( column )
            if column.isPrimaryKey():
                self.__primaryKey = column.name

        if 'viewSort' in table:
            self.__viewSort = SortInfo( table[ 'viewSort' ] )

        if 'viewSize' in table:
            if type( table[ 'viewSize' ] ) in ( int, str ):
                self.__viewSize = table[ 'viewSize' ]

            else:
                raise Exception( "Invalid parameter 'viewSize', may be integer (5, 10, 25, 100) or string with service class name of where the function getViewSize() resides." )

        self.__mixin = TemplateMixin( table[ 'mixin' ] if 'mixin' in table else None )
        return

    def hasTabs( self, tp = 'dialog' ):
        return len( self.__table.get( tp + 'tabs', [] ) ) > 0

    def tabs( self, tp = 'dialog' ):
        return TemplateTabs( self, **self.__table.get( tp + 'tabs', {} ) )

    @property
    def Mixin( self ):
        return self.__mixin

    def sortedInfo( self ):
        if self.__viewSort is not None:
            return self.__viewSort.htmlMaterialSorting()

        return ''

    @property
    def leadIn( self ):
        result = []
        for column in self.__columns:
            for leadin in column.leadIn:
                if leadin not in result:
                    result.append( leadin )

        return '\n'.join( result )

    @property
    def tableName( self ):
        if gencrud.util.utils.lowerCaseDbIds:
            return self.__table.get( 'name', '' ).lower()

        return self.__table.get( 'name', '' )

    @property
    def name( self ):
        if gencrud.util.utils.lowerCaseDbIds:
            return self.__table.get( 'name', '' ).lower()

        return self.__table.get( 'name', '' )

    @property
    def orderBy( self ):
        return self.__table.get( 'order-by', [ self.__primaryKey ] )

    @property
    def uniqueKey( self ):
        values  = {}
        for value in self.__table.get( 'unique-key', {} ):
            for key in value.keys():
                values[ key ] = ', '.join( [ "'{0}'".format( x ) for x in value[ key ] ] )

        return values

    def hasUniqueKey( self ):
        if 'unique-key' in self.__table:
            if type( self.__table.get( 'unique-key', None ) ) in ( dict, tuple, list ):
                return True

        return False

    @property
    def hasAutoUpdate( self ):
        for field in self.__columns:
            if field.hasAutoUpdate:
                return True

        return False

    @property
    def columns( self ):
        return self.__columns

    @property
    def primaryKey( self ):
        return self.__primaryKey

    @property
    def listViewColumns( self ):
        return sorted( [ col for col in self.__columns if col.listview.index is not None ],
                       key = lambda col: col.listview.index )

    def buildFilter( self ):
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

        return (' + \r\n                   '.join( result ))

    @property
    def viewSort( self ):
        return self.__viewSort

    @property
    def hasViewSizeService( self ):
        if self.__viewSize is not None:
            return type( self.__viewSize ) is str

        return False

    @property
    def hasViewSizeValue( self ):
        if self.__viewSize is not None:
            return type( self.__viewSize ) is int

        return False

    @property
    def viewSize( self ):
        return self.__viewSize

    def __repr__(self):
        return "<TemplateTable >"