#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2021 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#   Library General Public License for more details.
#
#   You should have received a copy of the GNU Library General Public
#   License GPL-2.0-only along with this library; if not, write to the
#   Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301 USA
#
#   gencrud: 2021-04-04 08:26:09 version 2.1.680 by user mbertens
#
from flask import Blueprint, request, jsonify
import webapp2.api as API
from webapp2.common.crud import CrudInterface, RecordLock
import traceback
from webapp2.common.locking.model import RecordLocks
from webapp2.common.locking.schema import RecordLocksSchema
from webapp2.common.locking.mixin import RecordLocksViewMixin


lockingApi = Blueprint( 'lockingApi', __name__ )


# Args is for downwards compatibility !!!!!
def registerApi( *args ):
    # Set the logger for the users module
    API.app.logger.info( 'Register RecordLocks routes' )
    API.app.register_blueprint( lockingApi )
    try:
        import webapp2.common.locking.entry_points  as EP
        if hasattr( EP, 'entryPointApi' ):
            API.app.logger.info( 'Register RecordLocks entrypoint routes' )
            API.app.register_blueprint( EP.entryPointApi )

        if hasattr( EP, 'registerWebSocket' ):
            EP.registerWebSocket()

    except ModuleNotFoundError as exc:
        if exc.name != 'webapp2.common.locking.entry_points':
            API.app.logger.error( traceback.format_exc() )

    except Exception:
        API.app.logger.error( traceback.format_exc() )

    # TODO: Here we need to add dynamically the menus for this module
    return



class RecordLocksRecordLock( RecordLock ):
    def __init__(self):
        RecordLock.__init__( self, 'locking', 'L_ID' )
        return


class RecordLocksCurdInterface( CrudInterface, RecordLocksViewMixin ):
    _model_cls = RecordLocks
    _lock_cls = RecordLocksRecordLock
    _schema_cls = RecordLocksSchema()
    _schema_list_cls = RecordLocksSchema( many = True )
    _uri = '/api/locking'
    _relations = []

    def __init__( self ):
        CrudInterface.__init__( self, lockingApi )
        RecordLocksViewMixin.__init__( self )
        return

    def beforeUpdate( self, record ):
        for field in ( "L_ID", ):
            if field in record:
                del record[ field ]

        if hasattr( RecordLocksViewMixin, 'beforeUpdate' ):
            record = RecordLocksViewMixin.beforeUpdate( self, record )


        return record


locking = RecordLocksCurdInterface()

