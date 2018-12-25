from pytemplate.source import TemplateSource
from pytemplate.object import TemplateObject


class TemplateConfiguration( object ):
    def __init__( self, **cfg ):
        self.__config   = cfg
        self.__python   = TemplateSource( 'python', **self.__config )
        self.__angular  = TemplateSource( 'angular', **self.__config )
        self.__objects  = []
        for obj in cfg[ 'objects' ]:
            #print( obj )
            self.__objects.append( TemplateObject( **obj ) )

        return

    @property
    def python( self ):
        return self.__python

    @property
    def angular( self ):
        return self.__angular

    @property
    def objects( self ):
        return self.__objects

    def __iter__( self ):
        return iter( self.__objects )

    @property
    def application( self ):
        return self.__objects[ 0 ].application
