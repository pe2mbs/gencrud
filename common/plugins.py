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
import webapp2.api as API


def loadPlugins( root_path ):
    # Now check if there are plugins
    pluginsFolder = os.path.abspath( os.path.join( root_path, 'plugins') )
    if os.path.isdir( pluginsFolder ):
        for plugin in os.listdir( pluginsFolder ):
            # Found something
            pluginFolder = os.path.join( pluginsFolder, plugin )
            if os.path.isfile( os.path.join( pluginFolder,'__init__.py' ) ) and \
                    os.path.isfile(os.path.join(pluginFolder, '__main__.py') ):
                # It seems to be plugin, import it
                import importlib
                try:
                    API.plugins[ plugin ] = importlib.import_module( pluginFolder )

                except Exception as exc:
                    API.app.logger.error( "Loading plugin {} with error {}".format( pluginFolder, exc ) )

    return
