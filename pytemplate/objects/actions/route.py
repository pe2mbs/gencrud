from pytemplate.util.typescript import TypeScript


class RouteTemplate( object ):
    def __init__( self, parent, **cfg ):
        self.__parent = parent
        self.__config = cfg
        return

    @property
    def name( self ):
        return self.__config.get( 'name', self.__parent.name )

    @property
    def label( self ):
        return self.__config.get( 'label', self.__parent.label )

    @property
    def cls( self ):
        return self.__config.get( 'class', None )

    @property
    def module( self ):
        return self.__config.get( 'module', None )

    def params( self ):
        return self.__config.get( 'params', [] )

    def __repr__(self):
        return "<RouteTemplate name = '{}', label = '{}', class = {}, params = {}>".format(
                self.name, self.label, self.cls, self.params()
        )

    def routeParams( self ):
        params = self.params()
        if len( params ) > 0:
            items = {}
            for key, value in params.items():
                items[ key ] = value

            return '[queryParams]="{}"'.format( TypeScript().build( items ) )

        return ''