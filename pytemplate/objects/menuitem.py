class TemplateMenuItem( object ):
    def __init__( self, key, **cfg ):
        self.__item = cfg[ key ]

    @property
    def index( self ):
        if 'index' in self.__item:
            return self.__item[ 'index' ]

        return -1

    @property
    def displayName( self ):
        return self.__item[ 'displayName' ]

    @property
    def iconName( self ):
        return self.__item[ 'iconName' ]

    @property
    def route( self ):
        if 'route' in self.__item:
            return self.__item[ 'route' ]

        return self.__item[ 'displayName' ]
