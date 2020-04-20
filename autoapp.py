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
import traceback
import sys

__version__     = "1.0"
__author__      = 'Marc Bertens-Nguyen'
__copyright__   = 'Copyright (C) 2018 - 2020'

try:
    import os
    from webapp2.app import createApp
    import webapp2.api as API


    app = createApp( os.path.abspath( os.path.join( os.path.dirname( __file__ ), '..' ) ) )

except Exception:
    print( traceback.format_exc(), file=sys.stderr )
