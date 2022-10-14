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
#
from collections import defaultdict
import logging
from gencrud.config.base import TemplateBase
from gencrud.config._inports import SourceImport
from gencrud.config.column import TemplateColumn
from gencrud.config.inputgroup import InputGroup
from gencrud.config.tab import TemplateTabs
from gencrud.config.sort import SortInfo
from gencrud.config.mixin import TemplateMixin
import gencrud.util.utils as root
from gencrud.util.exceptions import *
from gencrud.constants import *
from gencrud.util.exceptions import InvalidViewSize
from typing import List

logger = logging.getLogger()


class RelationShip( TemplateBase ):
    def __init__( self, parent, relation ):
        TemplateBase.__init__( self, parent )
        self.__relation = relation
        return

    @property
    def cls( self ):
        return self.__relation.get( C_CLASS )

    @property
    def table( self ):
        return self.__relation.get( C_TABLE )

    @property
    def cascade( self ):
        return self.__relation.get( C_CASCADE )


class TemplateTable( TemplateBase ):
    def __init__( self, parent, **table ):
        TemplateBase.__init__( self, parent )
        self.__table            = table
        self.__columns          = []
        self.__groups           = []
        self.__primaryKey       = ''
        self.__secondaryKey     = ''
        self.__viewSort         = None
        self.__viewSize         = None
        self.__defaultViewSize  = 10
        self.__inports          = SourceImport()
        if C_NAME not in self.__table:
            raise MissingAttribute( C_TABLE, C_NAME )

        if C_COLUMNS not in self.__table:
            raise MissingAttribute( C_TABLE, C_COLUMNS )

        for col in self.__table[ C_COLUMNS ]:
            column = TemplateColumn( self, self.name, **col )
            self.__columns.append( column )
            if column.isPrimaryKey():
                self.__primaryKey = column.name

        if C_SECONDARY_KEY in table:
            self.__secondaryKey = table[C_SECONDARY_KEY]

        if C_VIEW_SORT in table:
            self.__viewSort = SortInfo( table[ C_VIEW_SORT ] )

        if C_VIEW_SIZE in table:
            if type( table[ C_VIEW_SIZE ] ) in ( int, str ):
                self.__viewSize = table[ C_VIEW_SIZE ]

            else:
                raise InvalidViewSize()

        groups = defaultdict(list)
        for column in self.__columns:
            if column.ui:
                if column.ui.group:
                    groups[column.ui.group].append(column)
                else:
                    groups[ C_NOGROUP ].append(column)
            # ad-on for sibling support
            for sibling in column.siblings:
                if sibling.ui:
                    if sibling.ui.group:
                        groups[sibling.ui.group].append(sibling)
                    else:
                        groups[ C_NOGROUP ].append(sibling)
        self.__groups = [InputGroup(group, fields) for group, fields in groups.items()]

        return

    @property
    def object( self ):
        return self.parent

    def __iter__(self):
        return iter( self.__columns )

    @property
    def config( self ):
        return self.object.config

    @property
    def groups ( self ) -> List[InputGroup]:
        return self.__groups

    def getFieldByName( self, name ):
        for column in self.__columns:
            if column.name == name:
                return column
        return None

    def groupInTab( self, group, tab ) -> bool:
        # iterate through fields of the tab
        for column in self.tabs().fieldsFor( tab ):
            # check for overlapping field between group and tab
            if column in group.fields:
                return True
        return False

    def hasInputGroups( self ) -> bool:
        return len( self.groups ) > 0

    def hasTabs( self, tp = C_DIALOG ) -> bool:
        if C_TABS in self.__table:
            return len( self.__table.get( C_TABS,[ ] ) ) > 0

        return len( self.__table.get( tp + C_TABS, [] ) ) > 0

    def tabs( self, tp = C_DIALOG ) -> TemplateTabs:
        if C_TABS in self.__table:
            return TemplateTabs( self,**self.__table.get( C_TABS,{ } ) )

        return TemplateTabs( self, **self.__table.get( tp + C_TABS, {} ) )

    def sortedInfo( self ) -> str:
        if self.__viewSort is not None:
            return self.__viewSort.htmlMaterialSorting()

        return ''

    def columnsHaveMultipleValues( self ) -> bool:
        for column in self.columns:
            if len(column.testdata.values) > 1:
                return True
        return False

    def maximumTestValues( self ) -> bool:
        return max( len( column.testdata.values ) for column in self.columns ) 

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
    def sortField( self ) -> str:
        if C_VIEW_SORT in self.__table:
            return self.__viewSort.field
        return self.__primaryKey

    @property
    def sortDirection( self ) -> str:
        if C_VIEW_SORT in self.__table:
            return self.__viewSort.direction
        return C_DESENDING

    @property
    def uniqueKey( self ) -> dict:
        values  = {}
        for key, value in self.__table.get( C_UNIQUE_KEY, {} ).items():
            if isinstance( value, str ):
                values[ key ] = ', '.join( [ "'{0}'".format( item.strip() ) for item in value.split( ',' ) ] )

            elif isinstance( value, ( list, tuple ) ):
                values[ key ] = ', '.join( [ "'{0}'".format( item.strip() ) for item in value ] )

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
    def relationShips( self ):
        return [ RelationShip( self, rs ) for rs in self.__table.get( C_RELATION_SHIP, [] ) ]

    @property
    def relationShipList( self ):
        return self.__table.get( C_RELATION_SHIP, [] )

    @property
    def columns( self ):
        return self.__columns

    @property
    def primaryKey( self ) -> str:
        return self.__primaryKey

    @property
    def secondaryKey( self ) -> str:
        return self.__secondaryKey

    @property
    def firstTextField( self ):
        for col in self.__columns:
            if col.isString():
                return col.name

        return self.__columns[ 1 ].name

    @property
    def listViewColumns( self ) -> list:
        return sorted( [ col for col in self.__columns if col.listview.index is not None ] +
                       [ sibling for col in self.__columns for sibling in col.siblings if sibling.listview.index is not None ],
                       key = lambda col: col.listview.index )

    @property
    def uiColumns( self ) -> list:
        return [ col for col in self.__columns if col.ui is not None ] +\
                [ sibling for col in self.__columns for sibling in col.siblings if sibling.ui is not None ]

    def buildFilter( self ) -> str:
        result = [ ]
        for item in self.listViewColumns:
            if item.ui.isUiType(C_CHOICE, C_CHOICE_AUTO) or item.ui.isUiType(C_COMBOBOX, C_COMBO):
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
