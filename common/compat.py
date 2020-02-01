# -*- coding: utf-8 -*-
"""Python 2/3 compatibility module for the 'Main Angular application package'."""
#
# Python 2/3 compatibility module for the 'Main Angular application package'.
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

import sys

PY2 = int( sys.version[ 0 ] ) == 2

if PY2:
    text_type       = unicode  # noqa
    binary_type     = str
    string_types    = (str, unicode)  # noqa
    unicode         = unicode  # noqa
    basestring      = basestring  # noqa
else:
    text_type       = str
    binary_type     = bytes
    string_types    = (str,)
    unicode         = str
    basestring      = (str, bytes)
