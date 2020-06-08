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
import webapp2.api as API
from inspect import signature

def registerExtensions( module ):
    """Register Flask extensions.

       :param app:          The application object.
       :param module:       The actual application module.
       :return:             None.
    """
    API.app.logger.info( "Registering extensions" )
    API.db.init_app( API.app )
    API.app.db = API.db
    API.mm.init_app( API.app )
    API.migrate.init_app( API.app, API.db, render_as_batch = True )
    # Optional extensions
    EXTENSIONS = API.app.config.get( 'USE_EXTENSIONS', { "BCRYPT": False,
                                                         "CACHE": False,
                                                         "JWT": False,
                                                         "STOMP": False } )
    if EXTENSIONS.get( "BCRYPT", False ):
        API.bcrypt.init_app( API.app )

    if EXTENSIONS.get( "CACHE", False ):
        API.cache.init_app( API.app )

    if EXTENSIONS.get( "JWT", False ):
        if hasattr( module, 'registerJwt' ):
            API.jwt.init_app( API.app )
            module.registerJwt( API.app, API.jwt )

        else:
            API.app.logger.info( "Not registering JWT" )

    if EXTENSIONS.get( "STOMP", False ):
        API.stomp.init_app( API.app )

    if module:
        if hasattr( module,'registerExtensions' ):
            sig = signature( module.registerExtensions )
            if len( sig.parameters ) == 2:
                module.registerExtensions( API.app, API.db )

            else:
                module.registerExtensions( )

    return
