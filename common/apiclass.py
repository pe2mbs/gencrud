import os
from flask_marshmallow import Marshmallow
from webapp2.common.tablemngt import TableManager


class ApiClass( object ):
    def __init__( self ):
        self.app             = None
        self.menuItems       = []
        self.applicInfo      = {}
        self.plugins         = None
        self.coreApi         = None
        self.listModules     = []
        self.plugins         = []
        self.loggingInfo     = {}
        self.bcrypt          = None
        self.migrate         = None
        self.cache           = None
        self.cors            = None
        self.jwt             = None
        self.use_jwt         = False
        self.mm              = Marshmallow()
        self.stomp           = None
        self.db              = None
        self.redis           = {}
        self.socketio        = None
        self.logger          = None
        self.HERE            = os.path.abspath( os.path.join( os.path.dirname( __file__ ), '..' ) )
        self.PROJECT_ROOT    = os.path.join( self.HERE, os.pardir )
        self.recordTracking  = None
        self.dbtables        = TableManager()
        self.memorytables    = TableManager()
