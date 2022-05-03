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
import os
from flask_marshmallow import Marshmallow
from webapp2.common.tablemngt import TableManager


app             = None
menuItems       = []
applicInfo      = {}
coreApi         = None
listModules     = []
plugins         = []
loggingInfo     = {}
bcrypt          = None
migrate         = None
cache           = None
cors            = None
jwt             = None
mm              = Marshmallow()
stomp           = None
db              = None
socketio        = None
logger          = None
HERE            = os.path.abspath( os.path.dirname( __file__ ) )
PROJECT_ROOT    = os.path.join( HERE, os.pardir )
recordTracking  = None
dbtables        = TableManager()
memorytables    = TableManager()
