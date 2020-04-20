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
import webapp2.api as API
from webapp2.commands.misc import cli
from webapp2.commands.dba import dba
from webapp2.commands.serve import serve


def registerCommands():
    """Register Click commands.

       :param app:          The application object.
       :param module:       The actual application module.
       :return:             None.
    """
    API.app.logger.info( "Registering commands" )
    API.app.cli.add_command( cli )
    API.app.cli.add_command( dba )
    API.app.cli.add_command( serve )
    return
