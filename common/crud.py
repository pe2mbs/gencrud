import time
from flask import request, Response, Request
from sqlalchemy import and_, not_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from flask.globals import LocalProxy
import posixpath
import webapp2.api as API
from flask_jwt_extended import ( verify_jwt_in_request, get_jwt_identity )
from webapp2.common.exceptions import *
from datetime import date, timedelta, datetime
from sqlalchemy.orm import Query


def render_query(statement, dialect=None):
    """
    Generate an SQL expression string with bound parameters rendered inline
    for the given SQLAlchemy statement.
    WARNING: This method of escaping is insecure, incomplete, and for debugging
    purposes only. Executing SQL statements with inline-rendered user values is
    extremely insecure.
    Based on http://stackoverflow.com/questions/5631078/sqlalchemy-print-the-actual-query
    """
    if isinstance(statement, Query):
        if dialect is None:
            dialect = statement.session.bind.dialect

        statement = statement.statement

    elif dialect is None:
        dialect = statement.bind.dialect

    class LiteralCompiler(dialect.statement_compiler):

        def visit_bindparam(self, bindparam, within_columns_clause=False,
                            literal_binds=False, **kwargs):
            return self.render_literal_value(bindparam.value, bindparam.type)

        def render_array_value(self, val, item_type):
            if isinstance(val, list):
                return "{%s}" % ",".join([self.render_array_value(x, item_type) for x in val])

            return self.render_literal_value(val, item_type)

        def render_literal_value(self, value, type_):
            if isinstance(value, int):
                return str(value)

            elif isinstance(value, (str, date, datetime, timedelta)):
                return "'%s'" % str(value).replace("'", "''")

            elif isinstance(value, list):
                return "'{%s}'" % (",".join([self.render_array_value(x, type_.item_type) for x in value]))

            return super(LiteralCompiler, self).render_literal_value(value, type_)

    return LiteralCompiler(dialect, statement).process(statement)


def getDictFromRequest( request ):
    try:
        data = request.json

    except Exception:
        data = None

    if data is None:
        data = request.args

    if data is None:
        raise InvalidRequestExecption()

    return data


class RecordLock( object ):
    def __init__( self, table, record_id ):
        self._table = table
        self._record_id = record_id
        self._data = None
        self._id = None
        return

    @property
    def data( self ):
        return self._data

    @property
    def id( self ):
        if isinstance( self._data, dict ) and self._record_id in self._data:
            return self._data[ self._record_id ]

        else:
            API.logger.debug( "ID: {} => {}".format( self._id, self._data ) )

        return self._id

    def removeId( self ):
        if isinstance( self._data, dict ):
            if self._record_id in self._data:
                del self._data[ self._record_id ]

        return

    @property
    def user( self ):
        try:
            user_info = get_jwt_identity()
            if user_info in ( None, '', 0 ):
                user_info = 'single.user'

        except:
            user_info = 'single.user'

        return user_info

    @classmethod
    def locked( cls, request, user = None ):
        from webapp2.common.locking.model import RecordLocks
        obj = cls()
        if user is None:
            user = obj.user

        obj._data = request
        try:
            if isinstance( request, int ):
                obj._id = request

            elif isinstance( request, LocalProxy ):
                obj._data = getDictFromRequest( request )
                if obj._record_id in obj._data:
                    obj._id = obj._data[ obj._record_id ]

                else:   # new record ?
                    raise NoResultFound

            else:
                raise InvalidRequestExecption( "Unknown {} object to get record information".format( request ) )

            API.logger.debug( "Is record lockec {}:{} not for {}".format( obj._table, obj._id, user ) )
            rec = API.db.session.query( RecordLocks ). \
                                 filter( and_( RecordLocks.L_TABLE == obj._table,
                                               RecordLocks.L_RECORD_ID == obj._id,
                                               RecordLocks.L_USER != user ) ).one()
            API.logger.warning( "Record is locked by {}".format( rec.L_USER ) )
            raise RecordLockedException( user = rec.L_USER )

        except NoResultFound:
            API.logger.debug( "Record NOT locked" )
            pass

        return obj

    @classmethod
    def unlock( cls, request, user = None ):
        from webapp2.common.locking.model import RecordLocks
        data = getDictFromRequest( request )
        obj = cls()
        if user is None:
            user = obj.user

        if user is None:
            user = 'single.user'

        API.logger.info( "request: {}".format( request ) )
        if isinstance( request, dict ):
            obj._data = request

        elif isinstance( request, Request ):
            obj._data = request.json

        elif isinstance( request, LocalProxy ):
            obj._data = getDictFromRequest( request )

        API.logger.debug( "unlock: {}".format( obj._data ) )
        if isinstance( obj._data, dict ):
            obj._id = data.get( obj._record_id, None )
            if obj._id is None:
                API.logger.error( 'Could not retrieve {} from record'.format( obj._record_id ) )
                return { 'result': 'OK', 'table': obj._table, 'id': obj._id }

        else:
            API.logger.error( 'data not a record'.format( obj._record_id ) )
            return { 'result': 'OK', 'table': obj._table, 'id': obj._id }

        try:
            API.logger.debug( "Unlocking {}:{} for {}".format( obj._table, obj._id, user ) )
            API.db.session.query( RecordLocks ).filter( and_( RecordLocks.L_TABLE == obj._table,
                                                               RecordLocks.L_RECORD_ID == obj._id,
                                                               RecordLocks.L_USER == user ) ).delete()
            API.db.session.commit()
            API.logger.debug( "Unlocking done" )

        except NoResultFound:
            API.logger.debug( "lock record not found for {}:{} by {}".format( obj._table, obj._id, user ) )

        return { 'result': 'OK', 'table': obj._table, 'id': obj._id }

    @classmethod
    def lock( cls, request, user = None ):
        from webapp2.common.locking.model import RecordLocks
        data = getDictFromRequest( request )
        obj = cls()
        if user is None:
            user = obj.user

        if user is None:
            user = 'single.user'

        API.logger.debug( "lock: {}".format( data ) )
        obj._id = data[ obj._record_id ]
        API.logger.debug( "Locking {}:{} for {}".format( obj._table, obj._id, user ) )
        API.db.session.add( RecordLocks( L_USER = user,
                                         L_RECORD_ID = obj._id,
                                         L_TABLE = obj._table,
                                         L_START_DATE = datetime.utcnow() ) )
        API.db.session.commit()
        API.logger.debug( "Locking done" )
        return { 'result': 'OK', 'table': obj._table, 'id': obj._id }


class CrudInterface( object ):
    _model_cls = None
    _lock_cls = None
    _schema_cls = None
    _schema_list_cls = None
    _lock = True
    _uri = ''
    _relations = []
    _delayed = False

    def __init__( self, blue_print, use_jwt = False ):
        self._blue_print = blue_print
        self.registerRoute( 'list/<id>/<value>', self.filteredList, methods = [ 'GET' ] )
        self.registerRoute( 'pagedlist', self.pagedList, methods = [ 'POST' ] )
        self.registerRoute( 'list', self.recordList, methods = [ 'GET' ] )
        self.registerRoute( 'new', self.newRecord, methods = [ 'POST' ] )
        self.registerRoute( 'get', self.recordGet, methods = [ 'GET' ] )
        self.registerRoute( 'get/<int:id>', self.recordGetId, methods = [ 'GET' ] )
        self.registerRoute( '<int:id>', self.recordDelete, methods = [ 'DELETE' ] )
        self.registerRoute( 'put', self.recordPut, methods = [ 'POST' ] )
        self.registerRoute( 'update', self.recordPatch, methods = [ 'POST' ] )
        self.registerRoute( 'select', self.selectList, methods = [ 'GET' ] )
        self.registerRoute( 'lock', self.lock, methods = [ 'POST' ] )
        self.registerRoute( 'unlock', self.unlock, methods = [ 'POST' ] )
        self.__useJWT   = use_jwt
        return

    @property
    def useJWT( self ):
        return self.__useJWT

    @useJWT.setter
    def useJWT( self, value ):
        self.__useJWT = value
        return

    def registerRoute( self, rule, function, endpoint = None, **options ):
        self._blue_print.add_url_rule( posixpath.join( self._uri, rule ),
                                       endpoint,
                                       function,
                                       **options )
        return

    def checkAuthentication( self ):
        if self.__useJWT:
            verify_jwt_in_request()

        return

    def pagedList( self ):
        self.checkAuthentication()
        t1 = time.time()
        data = getDictFromRequest( request )
        if self.__useJWT:
            user_info = get_jwt_identity()
            API.app.logger.debug( 'POST: {}/pagedlist by {}'.format( self._uri, user_info ) )
        filter = data.get( 'filters', [] )
        API.app.logger.debug( "Filter {}".format( filter ) )
        query = API.db.session.query( self._model_cls )
        for item in filter:
            operator = item.get( 'operator', None )
            if operator is None:
                continue

            column  = item.get( 'column', None )
            value1, value2   = item.get( 'value', [ None, None ] )
            API.app.logger.debug( "Filter {} {} {} / {}".format( column, operator, value1, value2 ) )
            if operator == 'EQ':
                query = query.filter( getattr( self._model_cls, column ) == value1 )

            elif operator == '!EQ':
                query = query.filter( getattr( self._model_cls, column ) != value1 )

            elif operator == 'GT':
                query = query.filter( getattr( self._model_cls, column ) > value1 )

            elif operator == 'LE':
                query = query.filter( getattr( self._model_cls, column ) < value1 )

            elif operator == 'GT|EQ':
                query = query.filter( getattr( self._model_cls, column ) >= value1 )

            elif operator == 'LE|EQ':
                query = query.filter( getattr( self._model_cls, column ) <= value1 )

            elif operator == 'EM':
                query = query.filter( getattr( self._model_cls, column ) == "" )

            elif operator == '!EM':
                query = query.filter( getattr( self._model_cls, column ) != "" )

            elif operator == 'CO':
                query = query.filter( getattr( self._model_cls, column ).like( "%{}%".format( value1 ) ) )

            elif operator == '!CO':
                query = query.filter( not_( getattr( self._model_cls, column ).contains( value1 ) ) )

            elif operator == 'BT': # Between
                query = query.filter( getattr( self._model_cls, column ).between( value1, value2 ) )

            elif operator == 'SW': # Startswith
                query = query.filter( getattr( self._model_cls, column ).like( "{}%".format( value1 ) ) )

            elif operator == 'EW': # Endswith
                query = query.filter( getattr( self._model_cls, column ).like( "%{}".format( value1 ) ) )

        API.app.logger.debug( "SQL-QUERY : {}".format( render_query( query ) ) )
        recCount = query.count()
        API.app.logger.debug( "SQL-QUERY count {}".format( recCount ) )
        sorting = data.get( 'sorting', None )
        if isinstance( sorting, dict ):
            column = sorting.get( 'column', None )
            if column is not None:
                if sorting.get( 'direction', 'asc' ) == 'asc':
                    query = query.order_by( getattr( self._model_cls, column ) )

                else:
                    query = query.order_by( getattr( self._model_cls, column ).desc() )

        pageIndex = data.get( 'pageIndex', 0 )
        pageSize = data.get( 'pageSize', 1 )
        API.app.logger.debug( "SQL-QUERY limit {} / {}".format( pageIndex, pageSize ) )
        if ( ( pageIndex * pageSize ) > recCount ):
            pageIndex = 0

        query = query.limit( pageSize ).offset( pageIndex * pageSize )
        result:Response = self._schema_list_cls.jsonify( query.all() )
        API.app.logger.debug( "RESULT count {} => {}".format( recCount, result.json ) )
        result = jsonify(
            records = result.json,
            pageSize = pageSize,
            page = pageIndex,
            recordCount = recCount
        )
        if self._delayed and t1 + 1 > time.time():
            API.app.logger.debug( 'filteredList waiting: {}'.format( ( t1 + 1 ) - time.time() ) )
            time.sleep( ( t1 + 1 ) - time.time() )

        API.app.logger.debug( 'filteredList => {}'.format( result ) )
        return result

    def filteredList( self, id, value ):
        t1 = time.time()
        self.checkAuthentication()
        filter = { id: value }
        API.app.logger.debug( 'GET: {}/list/{}/{} by {}'.format( self._uri, id, value, self._lock_cls().user ) )
        recordList = API.db.session.query( self._model_cls ).filter_by( **filter ).all()
        result = self._schema_list_cls.jsonify( recordList )
        API.app.logger.debug( 'filteredList => count: {}'.format( len( recordList ) ) )
        if self._delayed and t1 + 1 > time.time():
            API.app.logger.debug( 'filteredList waiting: {}'.format( ( t1 + 1 ) - time.time() ) )
            time.sleep( ( t1 + 1 ) - time.time() )

        return result

    def recordList( self ):
        self.checkAuthentication()
        API.app.logger.debug( 'GET: {}/list by {}'.format( self._uri, self._lock_cls().user ) )
        recordList = API.db.session.query( self._model_cls ).all()
        result = self._schema_list_cls.jsonify( recordList )
        API.app.logger.debug( 'recordList => count: {}'.format( len( recordList ) ) )
        return result

    def newRecord( self, **kwargs ):
        self.checkAuthentication()
        locker = kwargs.get( 'locker', self._lock_cls.locked( request ) )
        API.app.logger.debug( 'POST: {}/new {} by {}'.format( self._uri, repr( locker.data), locker.user ) )
        locker.removeId()
        record = self.updateRecord( locker.data, self._model_cls(), locker.user )
        API.db.session.add( record )
        API.db.session.commit()
        result = self._schema_cls.jsonify( record )
        rec_id = getattr( record, self._model_cls.__field_list__[ 0 ] )
        API.recordTracking.insert( self._model_cls.__tablename__,
                                   rec_id,
                                   record.dictionary,
                                   locker.user )
        API.app.logger.debug( 'newRecord() => {0}'.format( record ) )
        return result

    def recordGet( self, **kwargs ):
        self.checkAuthentication()
        locker = kwargs.get( 'locker', self._lock_cls.locked( request ) )
        API.app.logger.debug( 'GET: {}/get {} by {}'.format( self._uri, repr( locker.data ), locker.user ) )
        record = self._model_cls.query.get( locker.id )
        result = self._schema_cls.jsonify( record )
        API.app.logger.debug( 'recordGet() => {0}'.format( result ) )
        return result

    def recordGetId( self, id, **kwargs ):
        self.checkAuthentication()
        locker = kwargs.get( 'locker', self._lock_cls.locked( int( id ) ) )
        API.app.logger.debug( 'GET: {}/get/{} by {}'.format( self._uri, locker.id, locker.user ) )
        record = self._model_cls.query.get( locker.id )
        result = self._schema_cls.jsonify( record )
        API.app.logger.debug( 'recordGetId() => {0}'.format( record ) )
        return result

    def recordDelete( self, id, **kwargs ):
        self.checkAuthentication()
        locker = kwargs.get( 'locker', self._lock_cls.locked( int( id ) ) )
        API.app.logger.debug( 'DELETE: {} {} by {}'.format( self._uri, locker.data, locker.user ) )
        record = self._model_cls.query.get( locker.id )
        if self._lock:
            recordData = record.dictionary
            for relation in self._relations:
                # Now
                if 'delete' in relation.get( 'cascade' ):
                    cascadeRecords = []
                    for relRecord in getattr( record, relation.get( 'table', '' ) + '_relation' ):
                        cascadeRecords.append( relRecord.dictionary )

                    recordData[ relation.get( 'class', '' ) ] = cascadeRecords

            API.recordTracking.delete( self._model_cls.__tablename__,
                                       locker.id,
                                       recordData,
                                       locker.user )

        API.app.logger.debug( 'Deleting record: {}'.format( record ) )
        API.db.session.delete( record )
        API.app.logger.debug( 'Commit delete' )
        message = ''
        try:
            API.db.session.commit()
            result = True

        except IntegrityError:
            message = 'Could not delete due relations still exists'
            result = False

        API.app.logger.debug( 'recordDelete() => {} {}'.format( result, record ) )
        return jsonify( ok = result, reason = message ), 200 if result else 409

    def updateRecord( self, data: dict, record: any, user = None ):
        self.checkAuthentication()
        if isinstance( record, int ):
            record = API.db.session.query( self._model_cls ).get( record )

        elif isinstance( record, self._model_cls ):
            pass

        else:
            Exception( "Missing record ref" )

        # the .data was added after the merge from github into gitlab since
        # unmarshalresult objects have a data attribute containing the result
        result = self._schema_cls.load( self.beforeUpdate( data ) ).data
        API.app.logger.debug( "{}".format( result ) )
        if len( result ) > 1:
            for field, value in result.items():
                API.app.logger.debug( "{} := '{}'".format( field, value ) )
                setattr( record, field, value )

        else:
            raise Exception( result.errors )

        return self.beforeCommit( record )

    def beforeUpdate( self, data ):
        """before update hook (insert, update), when we need to alter the dictionary before we update the
        record class

        :param data:    dictionary with record fields and values
        :return:        dictionary with record fields and values (altered)
        """
        return data

    def beforeCommit( self, record ):
        """before commit hook (insert, update), when we need to change fields before committing the record
        to the database.

        :param record:  record modal class
        :return:        record modal class
        """
        return record

    def recordPut( self, **kwargs ):
        self.checkAuthentication()
        locker = kwargs.get( 'locker', self._lock_cls.locked( request ) )
        API.app.logger.debug( 'POST: {}/put {} by {}'.format( self._uri, repr( locker.data ), locker.user ) )
        record = self.updateRecord( locker.data, locker.id, locker.user )
        result = self._schema_cls.jsonify( record )
        API.recordTracking.update( self._model_cls.__tablename__,
                                   locker.id,
                                   record.dictionary,
                                   locker.user )
        API.db.session.commit()
        API.app.logger.debug( 'recordPut() => {0}'.format( record ) )
        return result

    def recordPatch( self, **kwargs ):
        self.checkAuthentication()
        locker = kwargs.get( 'locker', self._lock_cls.locked( request ) )
        API.app.logger.debug( 'POST: {}/update {} by {}'.format( self._uri, repr( locker.data ), locker.user ) )
        record = self.updateRecord( locker.data, locker.id, locker.user )
        API.db.session.commit()
        result = self._schema_cls.jsonify( record )
        API.app.logger.debug( 'recordPatch() => {}'.format( record ) )
        return result

    def selectList( self ):
        name_field = self._model_cls.__field_list__[ 1 ]
        for fld in self._model_cls.__field_list__:
            if fld.endswith( 'NAME' ):
                name_field = fld
                break

        self.checkAuthentication()
        data = getDictFromRequest( request )
        API.app.logger.debug( 'GET {}/select: {} by {}'.format( self._uri, repr( data ), self._lock_cls().user ) )
        value = data.get( 'value', self._model_cls.__field_list__[ 0 ] )    # primary key
        label = data.get( 'label', name_field )  # first field name
        labels = label.split(',')
        # TODO if label contains comma, split --> list
        # ' '.join( [ getattr( record, l ) for l in labels ] )
        result = [ { 'value': getattr( record, value ),
                     'label': ' '.join( [ str(getattr( record, l )) for l in labels ] ) }
                                for record in API.db.session.query( self._model_cls ).order_by( getattr( self._model_cls, labels[0] ) ).all()
        ]
        API.app.logger.debug( 'selectList => count: {}'.format( len( result ) ) )
        # API.app.logger.debug( 'selectList => result: {}'.format( result ) )
        return jsonify( result )

    def lock( self ):
        if self._lock:
            self.checkAuthentication()
            return jsonify( self._lock_cls.lock( request ) )

        return ""

    def unlock( self ):
        if self._lock:
            self.checkAuthentication()
            return jsonify( self._lock_cls.unlock( request ) )

        return ""
