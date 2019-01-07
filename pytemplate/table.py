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
        return sorted( [ col for col in self.__columns if col.index is not None ],
                       key = lambda column: column.index )


