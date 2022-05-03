import webapp2.api as API


class DbBaseMemory( object ):
    __model_cls__   = None

    def __init__( self, record = None, *args, **kwargs ):
        self.clear()
        self.set( record, **kwargs )
        return

    def clear( self ):
        for field in self.__model_cls__.__field_list__:
            setattr( self, field, None )

        return

    def set( self, record = None, **kwargs ):
        if isinstance( record, self.__model_cls__ ):
            for field in self.__model_cls__.__field_list__:
                setattr( self, field, getattr( record, field ) )

        for key, value in kwargs.items():
            setattr( self, key, value )

        return

    @classmethod
    def fetch( cls, *args, **kwargs ):
        query = API.db.session.query( cls.__model_cls__ )
        for condition in args:
            query = query.filter( condition )

        return cls( query.one() )

    @classmethod
    def fetch_many( cls, *args, **kwargs ):
        query = API.db.session.query( cls.__model_cls__ )
        for condition in args:
            query = query.filter( condition )

        if 'order_by' in kwargs:
            query = query.order_by( kwargs[ 'order_by' ] + " " + kwargs.get( 'order_dir', 'asc' ) )

        return [ cls( record ) for record in query.all() ]

    def __repr__( self ):
        return "<<{} {}>".format( self.__name__, ", ".join(
                [ "{} = {}".format( field, getattr( self, field ) ) for field in self.__model_cls__.__field_list__ ]
            ) )

    def __str__( self ):
        return self.__repr__()

    @property
    def dictionary( self ):
        return { field: getattr( self, field ) for field in self.__model_cls__.__field_list__ }
