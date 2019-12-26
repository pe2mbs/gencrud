#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2019 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation; either version 2 of the
#   License, or (at your option) any later version.
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
import logging
from flask import Blueprint, jsonify

##
#   Section maintained by generator.py
##
listModules = [

]

menuItems = [

]

##
#   End section maintained by generator.py
##
menuApi = Blueprint( 'menuApi', __name__ )
logger = logging.getLogger()


def registerApi( app, cors ):
    logger = app.logger
    for module in listModules:
        module.registerApi( app, cors )

    if app.config.get( 'ALLOW_CORS_ORIGIN', False ):
        app.logger.info( 'Allowing CORS' )
        if app.config.get( 'ALLOW_CORS_ORIGIN', False ):
            origins = app.config.get( 'CORS_ORIGIN_WHITELIST', '*' )
            cors.init_app( 'menuApi', origins = origins )

    logger.info( 'Register Menu route' )
    app.register_blueprint( menuApi )
    return


def registerExtensions( app, db ):
    return


def registerShellContext( app, db ):
    return


def registerCommands( app ):
    return

@menuApi.route( "/api/menu", methods=[ 'GET' ] )
def getUserMenu():
    return jsonify( menuItems )

