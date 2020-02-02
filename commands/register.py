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
from webapp.commands.clean import clean
from webapp.commands.lint import lint
from webapp.commands.rundev import rundevCommand
from webapp.commands.runssl import runsslCommand
from webapp.commands.runprod import runprdCommand
from webapp.commands.test import test
from webapp.commands.urls import urls

import webapp.api as API

def registerCommands():
    """Register Click commands.

       :param app:          The application object.
       :param module:       The actual application module.
       :return:             None.
    """
    API.app.logger.info( "Registering commands" )
    API.app.cli.add_command( test )
    API.app.cli.add_command( lint )
    API.app.cli.add_command( clean )
    API.app.cli.add_command( urls )
    API.app.cli.add_command( runsslCommand )
    API.app.cli.add_command( rundevCommand )
    API.app.cli.add_command( runprdCommand )
    return
