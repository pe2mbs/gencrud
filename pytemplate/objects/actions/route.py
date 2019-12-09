

class RouteTemplate( object ):
    def __init__( self, parent, **cfg ):
        self.__parent = parent
        self.__config = cfg
        return

    def name( self ):
        return self.__config.get( 'name', self.__parent.name )

    def label( self ):
        return self.__config.get( 'label', self.__parent.label )

    def cls( self ):
        return self.__config.get( 'class', None )

    def params( self ):
        return self.__config.get( 'params', [] )


