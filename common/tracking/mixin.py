import traceback
from flask import request, jsonify
import json
import dateutil.parser
from flask_jwt_extended import get_jwt_identity
import webapp2.api as API
from webapp2.common.crud import getDictFromRequest, render_query
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
import webapp2.common.tracking.constant as constant
from webapp2.common.tracking.model import Tracking


class TrackingViewMixin( object ):
    C_NOT_RESTORE_MESSAGE = "Could not restore record"


    def __init__( self ):
        self.registerRoute( 'retrieve', self.retrieveRecords, methods = [ 'POST' ] )
        self.registerRoute( 'rollback', self.rollbackRecord, methods = [ 'POST' ] )
        return

    def rollbackRecord( self ):
        self.checkAuthentication()
        user_info = get_jwt_identity()
        data = getDictFromRequest( request )
        API.app.logger.debug( 'GET: {}/rollback by {}'.format( self._uri, user_info ) )
        API.app.logger.debug( data )
        query = API.db.session.query( Tracking )
        query = query.filter( Tracking.T_ID == data[ 'T_ID' ] )
        record = None
        try:
            record: Tracking = query.one()
            if record.T_ACTION == constant.C_T_ACTION_DELETE:
                restoreRecord = API.dbtables.instanciate( record.T_TABLE )
                for key, value in json.loads( record.T_CONTENTS ).items():
                    if hasattr( restoreRecord, key ):
                        setattr( restoreRecord, key, value )

                API.db.session.delete( record )
                API.db.session.add( restoreRecord )
                API.db.session.commit()

            elif record.T_ACTION == constant.C_T_ACTION_UPDATE:
                restoreRecord = API.db.session.query( API.dbtables.get( record.T_TABLE ) ).get( record.T_RECORD_ID )
                for key, value in json.loads( record.T_CONTENTS ).items():
                    setattr( restoreRecord, key, value )

                API.db.session.delete( record )
                API.db.session.commit()

            elif record.T_ACTION == constant.C_T_ACTION_INSERT:
                restoreRecord = API.db.session.query( API.dbtables.get( record.T_TABLE ) ).get( record.T_RECORD_ID )
                API.db.session.delete( record )
                API.db.session.delete( restoreRecord )
                API.db.session.commit()

            else:
                Exception( "Invalid/unsupported action code" )

        except IntegrityError:
            API.db.session.delete( record )
            return jsonify( ok = False,
                            message = self.C_NOT_RESTORE_MESSAGE,
                            reason = "Record already present" )

        except NoResultFound:
            API.db.session.delete( record )
            return jsonify( ok = False,
                            message = self.C_NOT_RESTORE_MESSAGE,
                            reason = "Record not found" )

        except Exception as exc:
            API.logger.error( traceback.format_exc() )
            return jsonify( ok = False,
                            message = self.C_NOT_RESTORE_MESSAGE,
                            reason = str( exc ) )

        return jsonify( ok = True )

    def retrieveRecords( self, **kwargs ):
        self.checkAuthentication()
        user_info = get_jwt_identity()
        data = getDictFromRequest( request )
        API.app.logger.debug( 'GET: {}/retrieve by {}'.format( self._uri, user_info ) )
        API.app.logger.debug( data )
        query = API.db.session.query( Tracking )
        query = query.filter( Tracking.T_RECORD_ID == data[ 'T_RECORD_ID' ] )
        data[ 'T_CHANGE_DATE_TIME' ] = dateutil.parser.parse( data[ 'T_CHANGE_DATE_TIME' ] ).replace( microsecond = 0 )
        API.app.logger.debug( data )
        query = query.filter( Tracking.T_CHANGE_DATE_TIME >= data[ 'T_CHANGE_DATE_TIME' ] )
        query = query.order_by( Tracking.T_CHANGE_DATE_TIME )
        API.app.logger.debug( "SQL-QUERY : {}".format( render_query( query ) ) )
        records = query.all()
        API.app.logger.debug( "Result: {}".format( records ) )
        return self._schema_list_cls.jsonify( records )
