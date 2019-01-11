import logging
from flask import Blueprint, jsonify

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

