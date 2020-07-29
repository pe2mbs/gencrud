#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2020 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
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
from flask import Blueprint, jsonify
import webapp2.app as API

__version__     = '1.1.0'
__copyright__   = '(c) Copyright 2018-2020, all rights reserved, GPL2 only'
__author__      = 'Marc Bertens-Nguyen'

##
#   Section maintained by gencrud.py
##
listModules = [

]

menuItems = [

]

##
#   End section maintained by gencrud.py
##
applicApi = Blueprint( 'applicApi', __name__ )


def registerApi():
    API.app.logger.info( 'Register Menu route' )
    API.app.register_blueprint( menuApi )
    API.app.logger.info( 'Register modules route' )
    for module in listModules:
        module.registerApi()

    return


def registerExtensions():
    API.app.logger.info( 'Register extensions' )
    for module in listModules:
        if hasattr( module, 'registerExtensions' ):
            module.registerExtensions()

    return


def registerShellContext():
    API.app.logger.info( 'Register shell context' )
    for module in listModules:
        if hasattr( module, 'registerShellContext' ):
            module.registerShellContext()

    return


def registerCommands():
    API.app.logger.info( 'Register extra commands' )
    for module in listModules:
        if hasattr( module, 'registerCommands' ):
            module.registerCommands()

    return


@applicApi.route( "/api/application/menu", methods=[ 'GET' ] )
def getUserMenu():
    return jsonify( menuItems )


@applicApi.route( "/api/application/version", methods=[ 'GET' ] )
def getAppVersion():
    return __version__


@applicApi.route( "/api/application/copyright", methods=[ 'GET' ] )
def getAppCopyright():
    return __copyright__


@applicApi.route( "/api/application/author", methods=[ 'GET' ] )
def getAppAuthor():
    return __author__


@applicApi.route( "/api/application/info", methods=[ 'GET' ] )
def getAppInfo():
    return jsonify( author = __author__,
                    copyright = __copyright__,
                    version = __version__ )

