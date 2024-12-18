import webapp2.api as API


class ModelMixin( object ):
    def toDict( self ):
        return self.dictionary

    def toSql( self ):
        data = self.dictionary
        values = repr( list( data.values() ) )[ 1: -2 ]
        return "INSERT INTO {} ( {} ) VALUES ( {} )".format( self.tablename, ", ".join( data.keys() ), values )

    def __str__( self ):
        return self.__repr__()

    def __rshift__( self, other ):  # >>
        if isinstance( other, ( ModelBase, BaseMemoryTable ) ):
            for field in self.fields():
                setattr( other, field, getattr( self, field ) )

            return

        raise Exception( "Could not {} shift data into {}".format( self.__class__.__name__, type( other ) ) )

    def __lshift__( self, other ):  # <<
        if isinstance( other, ( ModelBase, BaseMemoryTable ) ):
            for field in self.fields():
                setattr( self, field, getattr( other, field ) )

            return

        raise Exception( "Could not {} shift data into {}".format( type( other ), self.__class__.__name__ ) )

    def csv_header( self, sep = ';' ):
        return sep.join( self.fields() )

    def csv( self, sep = ';', qoute = '"' ):
        result = []
        for field in self.fields():
            obj = getattr( self, field )
            if isinstance( obj, ( int, float ) ):
                result.append( "{}".format( obj ) )

            elif isinstance( obj, str ):
                result.append( "{0}{1}{0}".format( qoute, obj.replace( '"', '\\"' ) ) )

            elif isinstance( obj, bool ):
                result.append( "{}".format( "true" if obj else "false" ) )

            elif isinstance( obj, bytes ):
                result.append( "{0}{1}{0}".format( qoute, obj.decode( 'utf-8' ).replace( '"', '\\"' ) ) )

            elif isinstance( obj, type(None) ):
                result.append( "null" )

        return sep.join( result )



class ModelBase( ModelMixin ):
    @property
    def dictionary( self ):
        result = {}
        for field in self.__mapper__._init_properties:
            result[ field ] = getattr( self, field )

        return result

    @classmethod
    def fields( cls ):
        return [ field for field in cls.__mapper__._init_properties ]

    def memoryInstance( self ):
        return BaseMemoryTable( self, meta = self.__class__ )

    def __repr__( self ):
        result_fields = []
        for field, value in self.dictionary.items():
            result_fields.append( "{} = {}".format( field, value  ) )

        return "<{} {}>".format( self.__class__.__name__, ", ".join( result_fields ) )



class BaseMemoryTable( ModelMixin ):
    def __init__( self, record = None, *args, **kwargs ):
        if 'meta' in kwargs:
            self.__metaobject = kwargs[ 'meta' ]
            self.__fields = self.__metaobject.fields()

        else:
            self.__metaobject = None
            self.__fields = []

        self.clear()
        self.set( record, **kwargs )
        return

    def clear( self ):
        if self.__metaobject is not None:
            for f in self.__fields:
                setattr( self, f, None )

        return

    def set( self, record = None, **kwargs ):
        if isinstance( record, self.__metaobject ):
            for field in self.__fields:
                setattr( self, field, getattr( record, field ) )

        for key, value in kwargs.items():
            setattr( self, key, value )

        return

    @classmethod
    def fetch( cls, *args, **kwargs ):
        query = API.db.session.query( self.__metaobject )
        for condition in args:
            query = query.filter( condition )

        return cls( query.one() )

    @classmethod
    def fetch_many( cls, *args, **kwargs ):
        result = [ ]
        query = API.db.session.query( self.__metaobject )
        for condition in args:
            query = query.filter( condition )

        if 'order_by' in kwargs:
            query = query.order_by( kwargs[ 'order_by' ] + " " + kwargs.get( 'order_dir', 'asc' ) )

        return [ cls( record ) for record in query.all() ]

    def __repr__( self ):
        return "<{}Memory {}>".format( self.__metaobject.__name__, ', '.join( [
            "{} = {}".format( f, getattr( self, f ) ) for f in self.__fields
        ] ) )

    @property
    def dictionary( self ):
        return { f: getattr( self, f ) for f in self.__fields }

    def __call__(self, *args, **kwargs):
        self.set( *args, **kwargs )
        return self



# class TestModel( API.db.Model, ModelBase ):
#     __tablename__ = 'users'
#     U_ID = Column( 'user_id', Integer, primary_key = True )
#     U_NAME = Column( 'user_name', String )
#     U_FULLNAME = Column( 'user_fullname', String )
#     U_NICKNAME = Column( 'user_nickname', String )
#
#
# class TestModelMemory( BaseMemoryTable ):
#     def __init__( self, record = None, *args, **kwargs ):
#         super( TestModelMemory, self ).__init__( record, *args, meta = TestModel, **kwargs )
#         return
