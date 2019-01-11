

class TemplateService( object ):
    def __init__( self, **cfg ):
        self.__cfg = cfg
        return

    @property
    def name( self ):
        return self.__cfg[ 'name' ]

    @property
    def value( self ):
        return self.__cfg[ 'value' ]

    @property
    def label( self ):
        return self.__cfg[ 'label' ]

    @property
    def cls( self ):
        value = self.__cfg[ 'class' ]
        if value.endswith( 'Service' ):
            return value

        return '{}DataService'.format( value )

    @property
    def path( self ):
        if 'path' in self.__cfg:
            return self.__cfg[ 'path' ]

        return '../{}/service'.format( self.__cfg[ 'name' ] )
