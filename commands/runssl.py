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
                        CertParamType,
                        _validate_key,
                        get_debug_flag,
                        show_server_banner,
                        get_env,
                        DispatchingApp )


@click.command('runssl', short_help='Runs a SSL/TLS server.')
@click.option('--host', '-h', default='127.0.0.1',
              help='The interface to bind to.')
@click.option('--port', '-p', default=5000,
              help='The port to bind to.')
@click.option('--cert', type = CertParamType(),
              help='Specify a certificate file to use HTTPS.')
@click.option('--key',
              type = click.Path( exists=True, dir_okay = False, resolve_path = True ),
              callback=_validate_key, expose_value = False,
              help='The key file to use when specifying a certificate.')
@click.option('--reload/--no-reload', default=None,
              help='Enable or disable the reloader. By default the reloader '
              'is active if debug is enabled.')
@click.option('--debugger/--no-debugger', default=None,
              help='Enable or disable the debugger. By default the debugger '
              'is active if debug is enabled.')
@click.option('--eager-loading/--lazy-loader', default=None,
              help='Enable or disable eager loading. By default eager '
              'loading is enabled if the reloader is disabled.')
@click.option('--with-threads/--without-threads', default=True,
              help='Enable or disable multithreading.')
@pass_script_info
def runsslCommand( info, host, port, reload, debugger, eager_loading,
                   with_threads, cert ):
    """Run a local development server.

    This server is for development purposes only. It does not provide
    the stability, security, or performance of production WSGI servers.

    The reloader and debugger are enabled by default if
    FLASK_ENV=development or FLASK_DEBUG=1.
    """
    debug = get_debug_flag()

    if reload is None:
        reload = debug

    if debugger is None:
        debugger = debug

    if eager_loading is None:
        eager_loading = not reload

    show_server_banner( get_env(), debug, info.app_import_path, eager_loading )
    app = DispatchingApp( info.load_app, use_eager_loading = eager_loading )

    if cert is None:
        ssl = info._loaded_app.config.get( 'SSL', {} )
        if ssl is {}:
            raise Exception( "'SSL' section in configuration is missing" )

        try:
            certificate = ssl[ 'CERTIFICATE' ]
            if not os.path.isfile( certificate ):
                raise Exception( "Certificate file '%s' not preset." )

            keyfile = ssl[ 'KEYFILE' ]
            if not os.path.isfile( keyfile ):
                raise Exception( "Certificate file '%s' not preset." )

            cert = ( certificate, keyfile )

        except AttributeError:
            pass

        except Exception as exc:
            raise

    from werkzeug.serving import run_simple
    run_simple( host, port, app,
                use_reloader = reload,
                reloader_type = 'stat',
                use_debugger = debugger,
                threaded = with_threads,
                ssl_context = cert )
