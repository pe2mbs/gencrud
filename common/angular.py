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
from mako.template import Template
from werkzeug.routing import BaseConverter
import webapp.api as API
import version

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
                                    "The frontend foldern was not found {}.".format( angular_path ),
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
class Feedback( API.db.Model ):
    __tablename__       = 'ap_feedback'
    F_ID                = API.db.Column( "f_id",        API.db.Integer, autoincrement = True, primary_key = True )
    F_NAME              = API.db.Column( "f_name",      API.db.String( 50 ), nullable = False )
    F_TYPE              = API.db.Column( "f_type",      API.db.Integer, nullable = False )
    F_VOTED             = API.db.Column( "f_voted",     API.db.Integer, nullable = False )
    F_SUBJECT           = API.db.Column( "f_subject",   API.db.String( 100 ), nullable = False )
    F_MESSAGE           = API.db.Column( "f_message",   API.db.Text, nullable = True )


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
    return jsonify( version = version.version,
                    copyright = version.copyright,
                    author = version.author )

