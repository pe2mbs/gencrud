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
import os
import yaml
import json
import logging
import traceback
import importlib
from flask import Blueprint, jsonify
try:
    import webapp2.api as API
except ModuleNotFoundError:
    # Error handling
    raise SystemExit("You need to include the module webapp2. Follow instructions " +
        "on https://github.com/pe2mbs/gencrud/blob/master/doc/MANUAL.md")

__version__     = '1.1.0'
__copyright__   = '(c) Copyright 2018-2020, all rights reserved, GPL2 only'
__author__      = 'Marc Bertens-Nguyen'
__date__        = '2020-01-01'

menuItems = []
applicApi = Blueprint( 'applicApi', __name__ )
logger = logging.getLogger()
applicInfo = {
    'application': 'webTestrun for Account Payments',
    'logo': 'assets/images/logo-equensWorldline.png',
    'version': __version__,
    'ReleaseDate': __date__
}


def discoverModules():
    modules = []
    currentFolder = os.path.dirname( __file__ )
    _, rootPackage = os.path.split( currentFolder )
    for package in os.listdir( currentFolder ):
        packageFolder = os.path.join( currentFolder, package )
        if os.path.isdir( packageFolder ) and os.path.isfile( os.path.join( packageFolder, '__init__.py' ) ):
            module = importlib.import_module( ".".join( [ rootPackage, package ] ) )
            logger.info( "Loading module: {}".format( module.__name__ ) )
            modules.append( module )

    return modules


listModules = discoverModules()
plugins = []


def verifyMenuStruct( menu ):
    """Internal function to verify the menu structure, special for the function addMenu()

    :param menu:    menu struct
    :return:        None
    """
    if 'displayName' not in menu:
        raise Exception( "Menu has no displayName!: {} ".format( json.dumps( menu ) ) )

    if 'iconName' not in menu:
        raise Exception( "Menu has no iconName!: {} ".format( json.dumps( menu ) ) )

    if 'route' not in menu and 'children' not in menu:
        raise Exception( "Menu has no route or children!: {} ".format( json.dumps( menu ) ) )

    if 'children' in menu:
        for child in menu[ 'children' ]:
            verifyMenuStruct( child )

    return


def _registerMenu( root_menu, menu, before = None, after = None ):
    if before is None and after is None:
        # Just add it at the back
        root_menu.append( menu )
        return

    for idx, item in enumerate( root_menu ):
        if before is not None and item[ 'displayName' ] == before:
            # Found it
            root_menu.insert( idx, menu )
            return
        elif after is not None and item[ 'displayName' ] == after:
            # Found it
            root_menu.insert( idx + 1, menu )
            return

    if before is not None:
        raise Exception( "Menu item '{}' not found".format( before ) )

    raise Exception( "Menu item '{}' not found".format( after ) )


def registerMenu( menu, before = None, after = None ):
    global menuItems
    verifyMenuStruct( menu )
    _registerMenu( menuItems, menu, before, after )
    return


def registerSubMenu( menu, *args, before = None, after = None ):
    global menuItems
    verifyMenuStruct( menu )
    subMenu = menuItems
    found = False
    for arg in args:
        found = False
        for idx, item in enumerate( menuItems ):
            if item[ 'displayName' ] == arg:
                subMenu = item
                found = True
                break

    if not found:
        if before is not None:
            raise Exception( "Menu item '{}' not found".format( args ) )

        raise Exception( "Menu item '{}' not found".format( args ) )

    _registerMenu( subMenu, menu, before, after )
    return


def logMappedDrives():
    logger.info( "Mapped drives" )
    import win32api
    import pywintypes
    import ctypes
    drives = win32api.GetLogicalDriveStrings()
    for drive in drives.split('\000')[:-1]:
        try:
            result = win32api.GetVolumeInformation( drive )
            logger.info( "drive: {} - {} :: {}".format( drive, result[4], result[0] ) )

        except pywintypes.error as exc:
            logger.info( "drive: {} - {}".format( drive, exc.strerror ) )

    return


def registerApi( app, cors ):
    logger = app.logger
    # mapDrive( "E:", "\\\\sfp09021\\testrun", None, None, True )
    logMappedDrives()
    global menuItems, applicInfo
    with open( os.path.join( os.path.dirname( __file__ ), 'menu.yaml' ), 'r' ) as stream:
        menuItems = yaml.load( stream, Loader = yaml.Loader )

    releaseFile = os.path.join( os.path.dirname( __file__ ), 'release.yaml' )
    if os.path.isfile( releaseFile ):
        with open( releaseFile, 'r' ) as stream:
            applicInfo = yaml.load( stream, Loader = yaml.Loader )

    setattr( app,'registerMenu',registerMenu )
    setattr( app,'registerSubMenu',registerSubMenu )
    for module in listModules:
        app.logger.debug( 'registering module {0}'.format( module ) )
        module.registerApi( app,cors )

    if app.config.get( 'ALLOW_CORS_ORIGIN',False ):
        app.logger.info( 'Allowing CORS' )
        if app.config.get( 'ALLOW_CORS_ORIGIN',False ):
            origins = app.config.get( 'CORS_ORIGIN_WHITELIST','*' )
            cors.init_app( 'applicApi',origins = origins )

    logger.info( 'Register Menu route' )
    app.register_blueprint( applicApi )
    # This is temp. hook to load plugins
    for plugin in plugins:
        try:
            app.logger.debug( 'registering plugin {0}'.format( plugin ) )
            plugin.registerApi( app,cors )

        except Exception as exc:
            app.logger.error( traceback.format_exc() )

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

@applicApi.route( "/api/menu", methods=[ 'GET' ] )
def getAppMenu():
    return jsonify( menuItems )