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

app             = None
menuItems       = []
applicInfo      = {}
plugins         = None

bcrypt          = None
if bcrypt is None:
    import webapp2.extensions.bcrypt

migrate         = None
if migrate is None:
    import webapp2.extensions.migrate

cache           = None
if cache is None:
    import webapp2.extensions.cache

cors            = None
if cors is None:
    import webapp2.extensions.cors

jwt             = None
if jwt is None:
    import webapp2.extensions.jwt

mm              = None
if mm is None:
    import webapp2.extensions.marshmallow

stomp           = None
if stomp is None:
    import webapp2.extensions.stompmq

db              = None
if db is None:
    import webapp2.extensions.database

HERE            = os.path.abspath( os.path.dirname( __file__ ) )
PROJECT_ROOT    = os.path.join( HERE, os.pardir )

