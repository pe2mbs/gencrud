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
import json
import decimal
import datetime


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

