# -*- coding: utf-8 -*-
#
# Angular base module, containing the app factory function.
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
import webapp.api as API
import webapp.extensions.bcrypt
import webapp.extensions.cache
import webapp.extensions.database
import webapp.extensions.cors
import webapp.extensions.stompmq
import webapp.extensions.jwt
import webapp.extensions.marshmallow
import webapp.extensions.migrate

def registerExtensions( module ):
    """Register Flask extensions.

       :param app:          The application object.
       :param module:       The actual application module.
       :return:             None.
    """
    API.app.logger.info( "Registering extensions" )
    API.bcrypt.init_app( API.app )
    API.cache.init_app( API.app )
    API.db.init_app( API.app )
    API.mm.init_app( API.app )
    #migrate.init_app( API.app, API.db )
    API.migrate.init_app( API.app, API.db, render_as_batch = True )
    API.jwt.init_app( API.app )


    # Set the auth callbacks
    if hasattr( module, 'registerJwt' ):
        module.registerJwt( API.app, API.jwt )

    else:
        API.app.logger.info( "Not registering JWT" )

    return
