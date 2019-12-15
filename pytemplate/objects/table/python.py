
class PythonObject( object ):
    def __init__( self, obj ):
        self.__object   = obj
        self.__module   = None
        self.__class    = None
        if obj is not None and '.' in obj:
            self.__module, self.__class = obj.rsplit( '.', 1 )

        return

    @property
    def Available( self ):
        return self.__object is not None

    @property
    def Class( self ):
        return self.__class

    @property
    def Module( self ):
        return self.__module
