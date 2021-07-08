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
import traceback
import sys
import socket
from flask import json, request, jsonify, render_template, make_response, Response
import werkzeug.exceptions

__version__     = "1.0"
__author__      = 'Marc Bertens-Nguyen'
__copyright__   = 'Copyright (C) 2018 - 2020'


app = None
saved_out = None
saved_err = None
try:
    import os
    import sys
    from webapp2.app import createApp
    import webapp2.api as API
    FLASK_OPTION = os.environ.get( 'FLASK_OPTION', None )
    SERVICE = os.environ.get( 'SERVICE', None )
    saved_out = sys.stdout
    saved_err = sys.stderr
    if ( FLASK_OPTION is not None and FLASK_OPTION == 'service' ) or SERVICE is not None:
        # For when flask is running from a service we need to point
        # STDERR and STDOUT to the NULL device.
        sys.stdout = open( os.devnull, 'w' )
        sys.stderr = open( os.devnull, 'w' )

    app = createApp( os.path.abspath( os.path.join( os.path.dirname( __file__ ), '..' ) ) )

except SystemExit:
    print( "SystemExit exception" )
    print( traceback.format_exc(),file = sys.stderr )
    raise

except Exception:
    print( traceback.format_exc(), file = sys.stderr )
    raise

finally:
    sys.stderr = saved_err
    sys.stdout = saved_out


def getHostByAddress( host_address ):
    result = []
    for item in socket.gethostbyaddr( host_address ):
        if isinstance( item, str ):
            result.append( item )
        elif isinstance( item, ( list, tuple ) ):
            result.append( "|".join( item ) )
        elif isinstance( item, int ):
            result.append( str( item ) )

    return ", ".join( result )


@app.errorhandler( Exception )
def handle_exception( e: Exception ):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    app.logger.error( "Error handler: {} :: {}".format( type( e ), e ) )
    if isinstance( e, werkzeug.exceptions.NotFound ):
        addresses = []
        for hostAddress in request.access_route:
            addresses.append( "{} = {}".format( hostAddress, getHostByAddress( hostAddress ) ) )

        e.description += "\nRequest URL {}\nSource address {}".format( request.url, ", ".join( addresses ) )
        response: Response = make_response( e.description, e.code )
        description = e.description

    if isinstance( e, werkzeug.exceptions.HTTPException ):
        response: Response = make_response( e.description, e.code )
        description = e.description

    elif isinstance( e, Exception ):
        response: Response = make_response( str( e ), 500 )
        description = str( e )

    else:
        response: Response= make_response( str( e ), 500 )
        description = str( e )

    app.logger.error( traceback.format_exc() )
    response_data = {}
    if e is MemoryError:
        # This is to shutdown the application to clean up the memory
        # and let Process monitor restart the application.
        raise SystemExit

    try:
        # replace the body with JSON
        response_data = {
            "code":         response.status_code,
            "name":         str( type( e ) ),
            "message":      description,
            "codeString":   werkzeug.exceptions.HTTP_STATUS_CODES[ response.status_code ],
            "url":          request.url,
            "request": {
                #"environ": request.environ,                        # This is a class
                "path": request.path,
                "full_path": request.full_path,
                "script_root": request.script_root,
                "url": request.url,
                "base_url": request.base_url,
                "url_root": request.url_root,
                "access_route": request.access_route,
                "args": request.args,
                "authorization": request.authorization,
                "blueprint": request.blueprint,
                "cache_control": str( request.cache_control ),
                "content_encoding": request.content_encoding,
                "content_length": request.content_length,
                "content_md5": request.content_md5,
                "content_type": request.content_type,
                "cookies": request.cookies,
                "data": request.data.decode( 'utf-8' ),
                "date": request.date,
                # "dict_storage_class": request.dict_storage_class, # This is a class
                "endpoint": request.endpoint,
                "files": request.files,
                "form": request.form,
                # "headers": request.headers,                       # This is a class
                "host": request.host,
                "host_url": request.host_url,
                "if_match": str( request.if_match ),
                "if_modified_since": str( request.if_modified_since ),
                "if_none_match": str( request.if_none_match ),
                "if_range": str( request.if_range ),
                "if_unmodified_since": str( request.if_unmodified_since ),
                "is_json": request.is_json,
                "is_multiprocess": request.is_multiprocess,
                "is_multithread": request.is_multithread,
                "is_run_once": request.is_run_once,
                "is_secure": request.is_secure,
                "json": request.json,
            },
            "traceback":    traceback.format_exc().splitlines( keepends = False )
        }
    except Exception:
        app.logger.error( traceback.format_exc() )

    response.data = json.dumps( response_data, indent = 4 )
    response.content_type = "application/json"
    return response
