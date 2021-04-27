from flask import Flask
import datetime
import sqlalchemy.sql.sqltypes
import webapp2.api as API
import pytz
from dateutil import tz



class ViewBase( object ):
    def __init__( self, app:Flask = None ):
        self.__app:Flask = app
        return

    def initapp( self, app:Flask = None ):
        if app is not None:
            self.__app = app

        for route, view_func in routes:
            view_func = self.__app.route( route )( view_func )

        return

    @property
    def app( self ) -> Flask:
        return self.__app



class ModelBaseMixin( object ):
    # GENERATED_FIELDS = []
    # FOREIGNKEY_FIELDS = []

    def removeGeneratedFieldsFromRecord( cls, data ):
        for field in cls.GENERATED_FIELDS:
            if field in record:
                del record[ field ]

        for field in cls.FOREIGNKEY_FIELDS:
            if field in record and record[ 'field' ] == 0:
                record[ field ] = None

        return record

    @staticmethod
    def convertDateTime( value ):
        value = value[ 0:22 ] + value[ 23: ]
        API.app.logger.debug( 'datetime.datetime.value: {}'.format( value ) )
        if value.startswith( '0000-00-00' ):
            value = datetime.datetime.utcnow()

        elif not value[ 0 ].isdigit():
            # 'Tue Aug 19 1975 23:15:30 GMT+0200 (CEST)'
            value = value.split( '(' )[ 0 ].strip()
            try:
                value = datetime.datetime.strptime( value, '%a %b %d %Y %H:%M:%S %Z%z' )

            except Exception:
                value = datetime.datetime.strptime( value, '%a %b %d %Y %H:%M:%S %z%Z' )

        # ELSE starts with digit
        elif value.endswith( 'Z' ):
            # ISO format without timezone
            value = datetime.datetime.strptime( value, '%Y-%m-%dT%H:%M:%S.%fZ' )

        elif 'T' in value:
            # ISO format with timezone
            value = datetime.datetime.strptime( value, '%Y-%m-%dT%H:%M:%S%z' )

        else:
            # Plain format, local time ?
            value = datetime.datetime.strptime( value, '%Y-%m-%d %H:%M:%S' )

        return value

    @staticmethod
    def fieldConversion( record, key, value, default = None ):
        try:
            _type = record.__table__.columns[ key ].type

        except Exception:
            _type = record.__table__.columns[ key.lower() ].type

        API.app.logger.debug( 'field {0} value {1} type {2}'.format( key, value, str( _type ) ) )
        if isinstance( _type, (
        sqlalchemy.sql.sqltypes.Integer, sqlalchemy.sql.sqltypes.INTEGER, sqlalchemy.sql.sqltypes.BigInteger, sqlalchemy.sql.sqltypes.INT,
        sqlalchemy.sql.sqltypes.BIGINT) ):
            try:
                if value is not None:
                    value = int( str( value ) )

                elif default is not None:
                    value = default

            except:
                if isinstance( default, int ):
                    value = default

                else:
                    value = 0

        elif isinstance( _type, (sqlalchemy.sql.sqltypes.REAL, sqlalchemy.sql.sqltypes.Float, sqlalchemy.sql.sqltypes.FLOAT, sqlalchemy.sql.sqltypes.DECIMAL,
                                 sqlalchemy.sql.sqltypes.Numeric, sqlalchemy.sql.sqltypes.NUMERIC) ):
            try:
                if value is not None:
                    value = float( str( value ) )

                elif default is not None:
                    value = default

            except:
                if isinstance( default, float ):
                    value = default

                else:
                    value = 0.0

        elif isinstance( _type, (sqlalchemy.sql.sqltypes.DateTime, sqlalchemy.sql.sqltypes.DATETIME, sqlalchemy.sql.sqltypes.TIMESTAMP) ):
            if value is not None:
                value = convertDateTime( value )

            elif default is not None:
                value = default

        elif isinstance( _type, (sqlalchemy.sql.sqltypes.Date, sqlalchemy.sql.sqltypes.DATE) ):
            # TODO: needs to be tested
            API.app.logger.debug( "Type date: '{}'".format( value ) )
            if value is not None:
                # UTC format, need to add local time diff
                if 'T' in value:
                    utc = convertDateTime( value )
                    from_zone = tz.tzutc()
                    to_zone = tz.tzlocal()
                    utc = utc.replace( tzinfo = from_zone )
                    value = utc.astimezone( to_zone )
                    API.app.logger.debug( "Type datetime: '{}'".format( value ) )

                else:
                    value = datetime.datetime.strptime( value, '%Y-%m-%d' )

                API.app.logger.debug( "Type date: '{}'".format( value ) )
                value = value.date()
                API.app.logger.debug( "Type date: '{}'".format( value ) )

            elif default is not None:
                value = default

        elif isinstance( _type, (sqlalchemy.sql.sqltypes.Time, sqlalchemy.sql.sqltypes.TIME) ):
            # TODO: needs to be tested
            if value is not None:
                value = datetime.datetime.strptime( value, '%H:%M:%S' ).time()

            elif default is not None:
                value = default

        elif isinstance( _type, (sqlalchemy.sql.sqltypes.Boolean, sqlalchemy.sql.sqltypes.BOOLEAN) ):
            if type( value ) is int:
                value = bool( value )

            elif type( value ) is str:
                value = bool( value )

            elif value is None:
                if default is not None:
                    value = default

                else:
                    value = False

        API.app.logger.debug( 'field {0} value {1}'.format( key, value ) )
        return value

    @classmethod
    def getRecord( cls, data ):
        return cls.query.get( int( data[ cls.GENERATED_FIELDS[ 0 ] ] ) )

    @classmethod
    def newRecord( cls, data ):
        data = cls.removeGeneratedFieldsFromRecord( data )
        record = cls()
        for key, value in data.items():
            setattr( record, key, cls.fieldConversion( record, key, value ) )

        API.db.session.add( record )
        API.db.session.commit()
        return record

    @classmethod
    def getRecordId( cls, id ):
        return cls.query.get( int( id ) )

    @classmethod
    def delRecordId( cls, id ):
        record = cls.query.get( int( id ) )
        API.db.session.delete( record )
        API.db.session.commit()
        return

    @classmethod
    def putRecord( cls, data ):
        record = cls.query.get( data[ cls.GENERATED_FIELDS[ 0 ] ] )
        data = cls.removeGeneratedFieldsFromRecord( data )
        for key, value in data.items():
            setattr( record, key, cls.fieldConversion( record, key, value ) )

        API.db.session.commit()
        return record

    @classmethod
    def updateRecord( cls, data ):
        record = cls.query.get( data[ cls.GENERATED_FIELDS[ 0 ] ] )
        data = cls.removeGeneratedFieldsFromRecord( data )
        for key, value in data.items():
            setattr( record, key, cls.fieldConversion( record, key, value ) )

        API.db.session.commit()
        return record

    @classmethod
    def selectList( cls, label ):
        return db.session.query( cls ).order_by( getattr( cls, label ) )


class ModelUserMixin( ModelBaseMixin ):
    GENERATED_FIELDS = [ "D_USER_ID", "D_ROLE_ID_FK", "D_ENABLED_LABEL", ]
    FOREIGNKEY_FIELDS = [ "D_ROLE_ID", ]

    def filteredRecords( self, filter ):
        return db.session.query( User ).filter_by( **filter ).\
                                        order_by( User.D_LAST_NAME ).\
                                        order_by( User.D_FIRST_NAME ).all()

    def allRecords( self ):
        return db.session.query( User ).\
                          order_by( User.D_LAST_NAME ).\
                          order_by( User.D_FIRST_NAME ).all()

    def selectListAttributes( self, data ):
        return ( data.get( 'value', GENERATED_FIELDS[ 0 ] ),    # primary key
                 data.get( 'label', 'D_USER_NAME' ) )   # first field name




class ViewCrudBase( ViewBase ):
    ROUTES = [
        ( '/api/{name}/list/<id>/<value>',  { 'methods': [ 'GET' ] },       'filteredRecords' ),
        ( '/api/user/list',                 { 'methods': [ 'GET' ] },       'allRecords' ),
        ( '/api/user/new',                  { 'methods': [ 'POST' ] },      'newRecord' ),
        ( '/api/user/get',                  { 'methods': [ 'GET' ] },       'getRecord' ),
        ( '/api/user/get/<int:id>',         { 'methods': [ 'GET' ] },       'getRecordId' ),
        ( '/api/user/<int:id>',             { 'methods': [ 'DELETE' ] },    'delRecordId' ),
        ( '/api/user/put',                  { 'methods': [ 'POST' ] },      'putRecord' ),
        ( '/api/user/update',               { 'methods': [ 'POST' ] },      'updateRecord' ),
        ( '/api/user/select',               { 'methods': [ 'GET' ] },       'selectList' ),
        ( '/api/user/lock',                 { 'methods': [ 'POST' ] },      'lockRecord' ),
        ( '/api/user/unlock',               { 'methods': [ 'POST' ] },      'unlockRecord' ),
    ]

    def __init__( self, name, model, app:Flask = None ):
        super( ViewCrudBase, self ).__init__( app )
        self.__name = name
        self.__model = model
        for route, options, funct in ViewCrudBase.ROUTES:
            if callable( funct ):
                self.add_url_rule( route, view_func = funct, **options )

            else:
                self.add_url_rule( route, view_func = getattr( self, funct ), **options )

        return

    def filteredRecords( self, id, value ):
        result = usersSchema.jsonify( self.__model.filteredRecords( { id: value } ) )
        API.app.logger.debug( 'GET: {}.filteredRecords( {}, {} ) -> {}'.format( self.__name, id, value, result ) )
        return result

    def allRecords( self ):
        result = usersSchema.jsonify( self.__model.allRecords() )
        API.app.logger.debug( 'GET: {}.allRecords() => {}'.format( self.__name, result ) )
        return result

    def newRecord( self ):
        data = request.json
        if data is None:
            return "Invalid request, missing UserRecord", 500

        API.app.logger.info( 'POST: {}.newRecord( {} )'.format( self.__name, repr( data ) ) )
        result = userSchema.jsonify( self.__model.newRecord( data ) )
        API.app.logger.debug( '{}.newRecord() => {}'.format( self.__name, result ) )
        return result

    def getRecord( self ):
        data = request.json
        if data is None:
            return "Invalid request, missing {} record".format( self.__name ), 500

        API.app.logger.info( 'GET: {}.getRecord( {} )'.format( self.__name, repr( data ) ) )
        result = userSchema.jsonify( self.__model.getRecord( data ) )
        API.app.logger.debug( '{}.getRecord() => {}'.format( self.__name, result ) )
        return result

    def getRecordId( self, id ):
        API.app.logger.info( 'GET: {}.getRecordId( {} )'.format( self.__name, id ) )
        result = userSchema.jsonify( self.__model.getRecordId( id ) )
        API.app.logger.debug( '{}.getRecordId() => {}'.format( result ) )
        return result

    def delRecordId( self, id ):
        API.app.logger.info( 'DELETE: {}.delRecordId( {} )'.format( self.__name, id ) )
        self.__model.delRecordId( id )
        result = jsonify( ok = True )
        API.app.logger.debug( '{}.delRecordId() -> {}'.format( self.__name, result ) )
        return result

    def putRecord( self ):
        data = request.json
        if data is None:
            return "Invalid request, missing UserRecord", 500

        API.app.logger.info( 'POST: {}.putRecord( {} )'.format( self.__name, repr( data ) ) )
        result = userSchema.jsonify( self.__model.putRecord( data ) )
        API.app.logger.debug( '{}.putRecord() -> {}'.format( self.__name, result ) )
        return result

    def updateRecord( self ):
        data = request.json
        API.app.logger.info( 'POST: {}.updateRecord( {} )'.format( self.__name, repr( data ) ) )
        result = userSchema.jsonify( self.__model.updateRecord( data ) )
        API.app.logger.debug( '{}.updateRecord() => {}'.format( self.__name, result ) )
        return result

    def selectList( self ):
        data = request.json
        if data is None:
            data = request.args

        API.app.logger.info( 'GET {}selectList( {} )'.format( self.__name, repr( data ) ) )
        value, label = self.__model.selectListAttributes( data )
        if ',' in label:
            labels = label.strip().split( ',' )
            separator = ' '
            label = labels[ 0 ]

        elif '-' in label:
            labels = label.strip().split( '-' )
            separator = '-'
            label = labels[ 0 ]

        elif ';' in label:
            labels = label.strip().split( ';' )
            separator = '; '
            label = labels[ 0 ]

        else:
            labels = [ ]
            separator = ''

        result = [ ]
        for record in self.__model.selectList( label ).all():
            if len( labels ) > 0:
                fields = [ getattr( record, lbl.strip() ) for lbl in labels ]
                result.append( { 'value': getattr( record, value ), 'label': separator.join( fields ) } )

            else:
                result.append( { 'value': getattr( record, value ), 'label': getattr( record, label ) } )

        API.app.logger.debug( '{}.selectList() => {}'.format( self.__name, result ) )
        return jsonify( result )

    def lockRecord( self ):
        data = request.json
        API.app.logger.info( 'POST: {}.lockRecord( {} )'.format( self.__name, repr( data ) ) )
        # TODO: This needs to be implemented for correct multiuser support
        return jsonify( { 'result': 'OK' } )

    def unlockRecord( self ):
        data = request.json
        API.app.logger.info( 'POST: {}.unlockRecord( {} )'.format( self.__name, repr( data ) ) )
        # TODO: This needs to be implemented for correct multiuser support
        return jsonify( { 'result': 'OK' } )


class UserViewCrudBase( ViewCrudBase ):
    ROUTES = [
        ( '/api/{name}/list/<id>/<value>',  { 'methods': [ 'GET' ] },       'filteredRecords' ),
        ( '/api/user/list',                 { 'methods': [ 'GET' ] },       'allRecords' ),
        ( '/api/user/new',                  { 'methods': [ 'POST' ] },      'newRecord' ),
        ( '/api/user/get',                  { 'methods': [ 'GET' ] },       'getRecord' ),
        ( '/api/user/get/<int:id>',         { 'methods': [ 'GET' ] },       'getRecordId' ),
        ( '/api/user/<int:id>',             { 'methods': [ 'DELETE' ] },    'delRecordId' ),
        ( '/api/user/put',                  { 'methods': [ 'POST' ] },      'putRecord' ),
        ( '/api/user/update',               { 'methods': [ 'POST' ] },      'updateRecord' ),
        ( '/api/user/select',               { 'methods': [ 'GET' ] },       'selectList' ),
        ( '/api/user/lock',                 { 'methods': [ 'POST' ] },      'lockRecord' ),
        ( '/api/user/unlock',               { 'methods': [ 'POST' ] },      'unlockRecord' ),
    ]
