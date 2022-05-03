class TableManager( object ):
    def __init__(self):
        self.__tables = {}

    def register( self, cls ):
        self.__tables[ cls.__tablename__ ] = cls
        return

    def get( self, name ):
        try:
            return self.__tables[ name ]

        except Exception:
            pass

        return None

    def instanciate( self, name ):
        try:
            return self.__tables[ name ]()

        except Exception:
            pass

        return None
