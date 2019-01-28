from pytemplate.objects.menuitem import TemplateMenuItem
from pytemplate.objects.table import TemplateTable
from pytemplate.objects.actions.actions import TemplateActions
from pytemplate.util.exceptions import InvalidSetting


class TemplateObject( object ):
    def __init__( self, **cfg ):
        self.__config       = cfg
        self.__columns      = []
        self.__primaryKey   = ''
        if 'menu' in cfg:
            self.__menuRoot = TemplateMenuItem( 'menu', **cfg )

        else:
            self.__menuRoot = None

        if 'menuItem' in cfg:
            self.__menuItem = TemplateMenuItem( 'menuItem', **cfg )

        else:
            self.__menuItem = None

        self.__actions      = TemplateActions( self.name,
                                               self.__config.get( 'actions', [] ) )
        self.__table        = TemplateTable( **self.__config.get( 'table', {} ) )
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
    def actions( self ):
        return self.__actions

    @property
    def menu( self ):
        return self.__menuRoot

    @property
    def menuItem( self ):
        return self.__menuItem

    @property
    def table( self ):
        return self.__table

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
            if field.ui is not None and ( field.ui.isCombobox() or field.ui.isChoice() ):
                result.append( 'public {name}Service: {cls}'.format(
                                name = field.ui.service.name,
                                cls = field.ui.service.cls ) )

        return ( FILLER if len( result ) > 0 else '' ) + ( FILLER_LF.join( result ) )

