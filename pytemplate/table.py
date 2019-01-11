from pytemplate.column import TemplateColumn
from pytemplate._inports import SourceImport


class TemplateTable( object ):
    def __init__( self, **table ):
        self.__table        = table
        self.__columns      = []
        self.__primaryKey   = ''
        self.__inports      = SourceImport()
        noColumns           = len( self.__table[ 'columns' ] )
        for col in self.__table[ 'columns' ]:
            column = TemplateColumn( noColumns,
                                     self.__table[ 'name' ],
                                     **col )
            self.__columns.append( column )
            if column.isPrimaryKey():
                self.__primaryKey = column.name

        if 'tsInport' in table:
            source = 'tsInport'

        elif 'psInport' in table:
            source = 'tsInport'

        else:
            return

        self.__inports.append( source, table[ source ] )
        return

    # TODO: Add 'unique-key' property to YAML

    @property
    def tableName( self ):
        return self.__table.get( 'name', '' )

    @property
    def name( self ):
        return self.__table.get( 'name', '' )

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

            elif item.tsType == 'string':
                result.append( "( record.{0} || '' )".format( item.name ) )

        if len( result ) == 0:
            return "''"

        return (' + \r\n                   '.join( result ))

