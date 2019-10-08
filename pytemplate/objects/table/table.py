import logging
from pytemplate.objects.table._inports import SourceImport
from pytemplate.objects.table.column import TemplateColumn
import pytemplate.util.utils

logger = logging.getLogger()


class SortInfo( object ):
    def __init__( self, data ):
        self.__field    = data[ 'field' ]

        # 'asc'
        # 'desc'
        # ''
        if data[ 'order' ] in ( 'asc', 'desc', '' ):
            self.__order    = data[ 'order' ]

        else:
            raise Exception( "Sorting order must be one of the following: 'asc', 'desc' or ''")

        return

    @property
    def Field( self ):
        return self.__field

    @property
    def Order( self ):
        return self.__order

    def AngularInject( self ):
        return "this.sort.sort( ({ id: '{field}', start: '{order}' }) as MatSortable);".format( field = self.__field,
                                                                                                order = self.__order )

class PythonObject( object ):
    def __init__( self, obj ):
        self.__object   = obj
        self.__module   = None
        self.__class    = None
        if obj is not None and '.' in obj:
            self.__module, self.__class = obj.splitr( '.', 1 )

        return

    @property
    def Available( self ):
        return self.__object is not None

    @property
    def Class( self ):
        return self.__class

    @property
    def Module( self ):
        return self.__module


class TemplateMixin( object ):
    def __init__( self, mixin ):
        self.__model    = PythonObject( mixin[ 'model' ] if 'model' in mixin else None )
        self.__schema   = PythonObject( mixin[ 'schema' ] if 'schema' in mixin else None )
        self.__view     = PythonObject( mixin[ 'view' ] if 'view' in mixin else None )
        return

    @property
    def Model( self ):
        return self.__model

    @property
    def Schema( self ):
        return self.__schema

    @property
    def View( self ):
        return self.__view


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

        if 'mixin' in table:
            self.__mixin = TemplateMixin( table[ 'mixin' ] )

        if 'tsInport' in table:
            source = 'tsInport'

        elif 'pyInport' in table:
            source = 'pyInport'

        else:
            return

        self.__inports.append( source, table[ source ] )
        return

    @property
    def Mixin( self ):
        return self.__mixin

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
        if pytemplate.util.utils.lowerCaseDbIds:
            return self.__table.get( 'name', '' ).lower()

        return self.__table.get( 'name', '' )

    @property
    def name( self ):
        if pytemplate.util.utils.lowerCaseDbIds:
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
    def columns( self ):
        return self.__columns

    @property
    def primaryKey( self ):
        return self.__primaryKey

    @property
    def tsInports( self ):
        return self.__inports.typescript

    @property
    def pyInports( self ):
        return self.__inports.python

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
