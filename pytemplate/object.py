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

    @property
    def externalService( self ):
        FILLER = '                 , '
        FILLER_LF = '\r\n                 , '
        result = []
        for field in self.__table.columns:
            if field.ui is not None and ( field.ui.isCombobox() or field.ui.isChoice() ):
                result.append( 'public {name}Service: {cls}'.format(
                                name = field.ui.service.name,
                                cls = field.ui.service.cls ) )

        return ( FILLER if len( result ) > 0 else '' ) + ( FILLER_LF.join( result ) )

