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
import flask.json
import json
import decimal
import datetime


class WebAppJsonEncoder( flask.json.JSONEncoder ):
    def default( self, obj ):
        if isinstance( obj, ( bytes, bytearray ) ):
            return obj.decode('utf-8')

        elif isinstance( obj, datetime.datetime ):
            obj = obj.strftime( "%Y-%m-%dT%H:%M:%S%z" )
            if '+' not in obj:
                obj += "+00:00"

            return obj

        elif isinstance( obj, datetime.date ):
            return obj.strftime( "%Y-%m-%d" )

        elif isinstance( obj, datetime.time ):
            obj = obj.strftime( "%H:%M:%S%z" )
            if '+' not in obj:
                obj += "+00:00"

            return obj

        # default, if not bytes/byte-array object. Let Flask do it thing
        return flask.json.JSONEncoder.default( self, obj )



class JsonEncoder( json.JSONEncoder ):
    def default( self, obj ):
        if isinstance( obj, complex ):
            return [ obj.real, obj.imag ]

        elif isinstance( obj, decimal.Decimal ):
            if int(obj) == float( obj ):
                return int(obj)

            return float( obj )


        elif isinstance( obj, ( datetime.datetime, datetime.date, datetime.time ) ):
            return str( obj )

        try:
            # Let the base class default method raise the TypeError
            return json.JSONEncoder.default( self, obj )

        except:
            pass

        return str( obj )
