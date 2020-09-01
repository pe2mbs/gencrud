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
from marshmallow import fields
import datetime


def getCurrentUser():
    return 'G101090'


def getCurrentUtcDateTime():
    return datetime.datetime.utcnow()


class SerializationDictField( fields.Field ):
    def __init__( self, default=fields.missing_, attribute=None, load_from=None, dump_to=None,
                 error=None, validate=None, required=False, allow_none=None, load_only=False,
                 dump_only=False, missing=fields.missing_, error_messages=None, dictionary = None, **metadata ):
        self.VALUES = dictionary
        fields.Field.__init__( self, default, attribute, load_from, dump_to,
                                    error, validate, required, allow_none, load_only,
                                    dump_only, missing, error_messages, **metadata )
        return

    def _serialize( self, value, attr, obj ):
        if value is None:
            return value
        else:
            if isinstance( value, ( bool, int ) ):
                try:
                    return self.VALUES[ value ]

                except KeyError:
                    return value

            else:
                return value

