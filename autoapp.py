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



saved_out = None
saved_err = None
try:
    import os
    import sys
    from webapp2.app import createApp
    import webapp2.api as API
    FLASK_OPTION = os.environ.get( 'FLASK_OPTION', None )
    SERVICE = os.environ.get( 'SERVICE', None )
    saved_out = sys.stdout
    saved_err = sys.stderr
    if ( FLASK_OPTION is not None and FLASK_OPTION == 'service' ) or SERVICE is not None:
        # For when flask is running from a service we need to point
        # STDERR and STDOUT to the NULL device.
        sys.stdout = open( os.devnull, 'w' )
        sys.stderr = open( os.devnull, 'w' )

    app = createApp( os.path.abspath( os.path.join( os.path.dirname( __file__ ), '..' ) ) )

except SystemExit:
    print( "SystemExit exception" )
    print( traceback.format_exc(),file = sys.stderr )

except Exception:
    print( traceback.format_exc(), file = sys.stderr )

finally:
    sys.stderr = saved_err
    sys.stdout = saved_out
