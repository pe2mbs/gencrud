from pytemplate.column import TemplateColumn

class TemplateTable( object ):
    def __init__( self, **table ):
        self.__table        = table
        self.__columns      = []
        self.__primaryKey   = ''
        noColumns           = len( self.__table[ 'columns' ] )
        for col in self.__table[ 'columns' ]:
            column = TemplateColumn( noColumns,
                                     self.__table[ 'name' ],
                                     **col )
            self.__columns.append( column )
            if column.isPrimaryKey():
                self.__primaryKey = column.name

        return

    @property
    def tableName( self ):
        return self.__table.get( 'name', '' )

    @property
    def name( self ):
        return self.__table.get( 'name', '' )

    @property
    def columns( self ):
        return self.__columns

    @property
    def primaryKey( self ):
        return self.__primaryKey

    @property
    def imports( self ):
        result = []
        for col in self.__columns:
            result.extend( col.inports )

        return result

    @property
    def listViewColumns( self ):
        return sorted( [ col for col in self.__columns if col.index is not None ],
                       key = lambda column: column.index )


