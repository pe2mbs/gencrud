# -*- coding: utf-8 -*-
"""Main webapp application package."""
#
# Main webapp application package
# Copyright (C) 2018-2020 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>
#
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License GPL-2.0-only
# as published by the Free Software Foundation.
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
from mako.template import Template
from werkzeug.routing import BaseConverter
import webapp2.api as API
from webapp2.extensions.database import db


__version__         = '2.0.0'
__copyright__       = '(c) Copyright 2018-2020 Marc Bertens-Nguyen, all rights reserved'
__author__          = 'Marc Bertens-Nguyen'


ERROR_HTML = """<html>
<head>
    <title>Exception: Angular application is missing // Werkzeug Debugger</title>
    <link rel="stylesheet" href="?__debugger__=yes&amp;cmd=resource&amp;f=style.css" type="text/css">
    <link rel="shortcut icon" href="?__debugger__=yes&amp;cmd=resource&amp;f=console.png">
    <script src="?__debugger__=yes&amp;cmd=resource&amp;f=jquery.js"></script>
    <script src="?__debugger__=yes&amp;cmd=resource&amp;f=debugger.js"></script>
</head>
<body style="background-color: #fff">
    <div class="debugger">
        <h1>webapp Exception</h1>
        <div class="detail">
            <p class="errormsg">Exception: ${ message }</p>
        </div>
        <h2 class="traceback">${ reason }</h2>

        <div class="explanation">
            ${ explanation }
        </div>
    </body>
</html>"""


def renderErrorPage( message, reason = '', explanation = '' ):
    return Template( ERROR_HTML ).render( message = message,
                                          reason = reason,
                                          explanation = explanation )


class RegexConverter( BaseConverter ):
    def __init__( self, url_map, *items ):
        super( RegexConverter, self ).__init__( url_map )
        self.regex = items[ 0 ]


bluePrint   = Blueprint( 'angular', __name__ )


def registerAngular():
    # Set the logger for the oldangular module
    API.app.url_map.converters[ 'regex' ] = RegexConverter
    API.app.register_blueprint( bluePrint )
    return


@bluePrint.route( '/' )
def index():
    angular_path = current_app.config[ 'ANGULAR_PATH' ]
    env = current_app.config[ 'ENV' ]
    current_app.logger.info( "Angular dist ({}) : {}".format( env, angular_path ) )
    try:
        if os.path.isdir( angular_path ):
            if os.path.isfile( os.path.join( angular_path, "index.html" ) ):
                return send_from_directory( angular_path, "index.html" )

            current_app.logger.info( "Python says file not found" )
            return renderErrorPage( "Angular application is missing",
                                    "The frontend application was not found at {}".format( angular_path ),
                                    """Correct the ANGULAR_PATH in the configuration
                                     or perform the <pre># ng build</pre> in the frontend folder to
                                     (re-)create the Angular application.
                                     """ )
        else:
            current_app.logger.info( "ANGULAR_PATH incorrect {}.".format( angular_path ) )
            current_app.logger.info( "ANGULAR_PATH incorrect {}.".format( angular_path ) )
            return renderErrorPage( "ANGULAR_PATH incorrect {}.".format( angular_path ),
                                    "The frontend folder was not found {}.".format( angular_path ),
                                    "Correct the ANGULAR_PATH in the configuration." )

    except Exception as exc:
        current_app.logger.error( exc )
        raise


@bluePrint.route( r"/<regex('\w\.(js|css|map)'):path>" )
def angularSource( path ):
    angular_path = current_app.config[ 'ANGULAR_PATH' ]
    env = current_app.config[ 'ENV' ]
    current_app.logger.info( "Angular dist ({}) : {}".format( env, angular_path ) )
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
    F_STATUS            = db.Column( "f_status",    db.Integer, nullable = True )
    F_DATETIME          = db.Column( "f_datetime",  db.DateTime, nullable = True )


@bluePrint.route( '/api/feedback', methods = [ 'PUT' ] )
def feedback():
    data    = request.json
    if data is None:
        return "Invalid request, missing Feedback data", 500

    current_app.logger.info( '/api/feedback PUT: {0}'.format( repr( data ) ) )
    record = Feedback()
    for key,value in request.json.items():
        setattr( record,key, value )

    API.db.session.add( record )
    API.db.session.commit()
    current_app.sendMail( record )
    current_app.logger.debug( 'feedback() => ok' )
    return jsonify( status = 'ok' )


@bluePrint.route( "/api/database", methods=[ 'GET' ] )
def getDatabaseConfig():
    dbCfg = current_app.config[ 'DATABASE' ]
    if dbCfg.get( 'ENGINE', 'sqlite' ) == 'oracle':
        dbCfg[ 'SCHEMA' ] = dbCfg.get('TNS', '' )

    return jsonify( engine   = dbCfg.get( 'ENGINE', 'sqlite' ),
                    database = dbCfg.get( 'SCHEMA', 'database.db' ),
                    username = dbCfg.get( 'USERNAME', '' ),
                    password = dbCfg.get( 'PASSWORD', '' ),
                    hostname = dbCfg.get( 'HOST', '' ),
                    hostport = dbCfg.get( 'PORT', 5432 ) )


@bluePrint.route( "/api/version", methods=[ 'GET' ] )
def getVersionInfo():
    return jsonify( version = __version__,
                    copyright = __copyright__,
                    author = __author__ )
