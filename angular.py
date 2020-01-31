# -*- coding: utf-8 -*-
"""Angular base API for the 'Main Angular application package'."""
#
# Angular base API for the 'Main Angular application package'
# Copyright (C) 2018 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
import os
from flask import Blueprint, send_from_directory, current_app, request, jsonify
from database import db
from werkzeug.routing import BaseConverter


class RegexConverter( BaseConverter ):
    def __init__( self, url_map, *items ):
        super( RegexConverter, self ).__init__( url_map )
        self.regex = items[ 0 ]


bluePrint   = Blueprint( 'angular', __name__ )


def registerAngular( app, cors ):
    # Set the logger for the oldangular module
    app.url_map.converters[ 'regex' ] = RegexConverter
    app.register_blueprint( bluePrint )
    return


@bluePrint.route( '/' )
def index():
    angular_path = current_app.config[ 'ANGULAR_PATH' ]
    env = current_app.config[ 'ENV' ]
    current_app.logger.info( "Angular dist (%s) : %s" % ( env, angular_path ) )
    try:
        if not os.path.isfile(os.path.join( angular_path, "index.html" ) ):
            current_app.logger.info( "Python says file not found" )

        return send_from_directory( angular_path, "index.html" )

    except Exception as exc:
        current_app.logger.error( exc )
        raise


@bluePrint.route( r"/<regex('\w\.(js|css|map)'):path>" )
def angularSource( path ):
    angular_path = current_app.config[ 'ANGULAR_PATH' ]
    env = current_app.config[ 'ENV' ]
    current_app.logger.info("Angular dist (%s) : %s" % ( env, angular_path ) )
    return send_from_directory( angular_path, path )

#
#   This part contains the standard /api/ routes other then loading the Angular application
#
#
class Feedback( db.Model ):
    __tablename__       = 'ap_feedback'
    F_ID                = db.Column( "f_id",        db.Integer, autoincrement = True, primary_key = True )
    F_NAME              = db.Column( "f_name",      db.String( 50 ), nullable = False )
    F_TYPE              = db.Column( "f_type",      db.Integer, nullable = False )
    F_VOTED             = db.Column( "f_voted",     db.Integer, nullable = False )
    F_SUBJECT           = db.Column( "f_subject",   db.String( 100 ), nullable = False )
    F_MESSAGE           = db.Column( "f_message",   db.Text, nullable = True )


@bluePrint.route( '/api/feedback', methods = [ 'PUT' ] )
def feedback():
    data    = request.json
    if data is None:
        return "Invalid request, missing Feedback data", 500

    current_app.logger.info( '/api/feedback PUT: {0}'.format( repr( data ) ) )
    record = Feedback()
    for key,value in request.json.items():
        setattr( record,key, value )

    db.session.add( record )
    db.session.commit()
    current_app.logger.debug( 'feedback() => ok' )
    return jsonify( status = 'ok' )


@bluePrint.route( "/api/database", methods=[ 'GET' ] )
def getDatabaseConfig():
    dbCfg = current_app.config[ 'DATABASE' ]
    if dbCfg.get( 'ENGINE', 'sqlite' ) == 'oracle':
        dbCfg[ 'SCHEMA' ] = dbCfg.get('TNS', '')

    return jsonify( engine   = dbCfg.get( 'ENGINE', 'sqlite' ),
                    database = dbCfg.get( 'SCHEMA', 'database.db' ),
                    username = dbCfg.get( 'USERNAME', '' ),
                    password = dbCfg.get( 'PASSWORD', '' ),
                    hostname = dbCfg.get( 'HOST', '' ),
                    hostport = dbCfg.get( 'PORT', 5432 ),
                )
