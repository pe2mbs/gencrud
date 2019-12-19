from gencrud.objects.table.python import PythonObject

class TemplateMixin( object ):
    def __init__( self, mixin ):
        self.__model    = PythonObject( mixin[ 'model' ] if mixin is not None and 'model' in mixin else None )
        self.__schema   = PythonObject( mixin[ 'schema' ] if mixin is not None and 'schema' in mixin else None )
        self.__view     = PythonObject( mixin[ 'view' ] if mixin is not None and 'view' in mixin else None )
        return

    @property
    def Model( self ):
        return self.__model

    @property
    def Schema( self ):
        return self.__schema

    @property
    def View( self ):
        return self.__view
