from pytemplate.column import TemplateColumn
from pytemplate.menuitem import TemplateMenuItem
from pytemplate.table import TemplateTable

class TemplateObject( object ):
    def __init__( self, **cfg ):
        self.__config       = cfg
        self.__columns      = []
        self.__primaryKey   = ''
        self.__menuRoot     = TemplateMenuItem( 'menu', **cfg )
        self.__menuItem     = TemplateMenuItem( 'menuItem', **cfg )
        self.__table        = TemplateTable( **cfg[ 'table' ] )

        noColumns           = len( cfg[ 'table' ][ 'columns' ] )
        for col in cfg[ 'table' ][ 'columns' ]:
            column = TemplateColumn( noColumns, **col )
            self.__columns.append( column )
            if column.isPrimaryKey():
                self.__primaryKey = column.name

        return

    @property
    def application( self ):
        return self.__config.get( 'application', '' )

    @property
    def name( self ):
        return self.__config.get( 'name', '' )

    @property
    def cls( self ):
        return self.__config.get( 'class', '' )

    @property
    def uri( self ):
        return self.__config.get( 'uri', '' )

    @property
    def menu( self ):
        return self.__menuRoot

    @property
    def menuItem( self ):
        return self.__menuItem

    @property
    def table( self ):
        return self.__table

    '''
    # TODO: move to TemplateTable() class
    @property
    def tableName( self ):
        return self.__config[ 'table' ][ 'name' ]

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
        return sorted( [ col for col in self.__columns if col.index is not None ] )
    '''


