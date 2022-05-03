class CrudModelMixin( object ):
    def toDict( self ):
        return self.dictionary

    @property
    def dictionary( self ):
        return { field: getattr( self, field ) for field in self.__field_list__ }

    @property
    def json( self ):
        return json.dumps( self.dictionary, cls = JsonEncoder )

    def toSql( self ):
        data = self.dictionary
        values = repr( data.values() ).split( '[' )[ 1 ].split( ']' )[ 0 ]
        return "INSERT INTO {} ( {} ) VALUES ( {} )".format( self.__tablename__,
                                                             ", ".join( data.keys() ),
                                                             values )

    def __repr__( self ):
        return "<{} {}>".format( self.__class__.__name__, ", ".join( [
                    "{} = {}".format( field, getattr( self, field ) ) for field in self.__field_list__
        ] ) )

    def __str__( self ):
        return self.__repr__()
