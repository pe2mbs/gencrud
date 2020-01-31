# -*- coding: utf-8 -*-
"""Exception module for the 'Main Angular application package'."""
#
# Exception module for the 'Main Angular application package'.
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
from flask import jsonify


def template( data, code=500 ):
    return { 'message': { 'errors': { 'body': data } }, 'status_code': code }


USER_NOT_FOUND          = template( [ 'User not found' ], code = 404 )
USER_ALREADY_REGISTERED = template( [ 'User already registered' ], code = 422 )
UNKNOWN_ERROR           = template( [], code = 500 )
ARTICLE_NOT_FOUND       = template( [ 'Article not found' ], code = 404 )
COMMENT_NOT_OWNED       = template( [ 'Not your article' ], code = 422 )


class InvalidUsage( Exception ):
    status_code = 500

    def __init__( self, message, status_code = None, payload = None ):
        Exception.__init__( self )
        self.message = message
        if status_code is not None:
            self.status_code = status_code

        self.payload = payload

    def toJson( self ):
        rv = self.message
        return jsonify( rv )

    @classmethod
    def userNotFound( cls ):
        return cls( **USER_NOT_FOUND )

    @classmethod
    def userAlreadyRegistered( cls ):
        return cls( **USER_ALREADY_REGISTERED )

    @classmethod
    def unknownError( cls ):
        return cls( **UNKNOWN_ERROR )

    @classmethod
    def articleNotFound( cls ):
        return cls( **ARTICLE_NOT_FOUND )

    @classmethod
    def commentNotOwned( cls ):
        return cls( **COMMENT_NOT_OWNED )


class InvalidFileType( Exception ):
    pass
