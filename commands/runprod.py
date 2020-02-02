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
import click
from flask.cli import ( pass_script_info,
                        DispatchingApp )


@click.command( 'runprod', short_help='Runs a production server.' )
@click.option( '--host', '-h', default='127.0.0.1',
              help='The interface to bind to.')
@click.option( '--port', '-p', default=8000,
              help='The port to bind to.')
@pass_script_info
def runprdCommand( info, host, port, *args, **kwargs ):
    from waitress import serve
    print( args )
    print( kwargs )

    app = DispatchingApp( info.load_app, use_eager_loading = True )
    applic = info.load_app()
    host = applic.config.get( 'HOST', host )
    port = applic.config.get( 'PORT', port )

    serve( app, host = host, port = port )
