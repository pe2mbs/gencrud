# -*- coding: utf-8 -*-
"""Click commands for the 'Main Angular application package'."""
#
# Click commands for the 'Main Angular application package'.
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

import os
from glob import glob
from subprocess import call

import click
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.exceptions import MethodNotAllowed, NotFound
from flask.cli import ( pass_script_info,
                        CertParamType,
                        _validate_key,
                        get_debug_flag,
                        show_server_banner,
                        get_env,
                        DispatchingApp )

HERE            = os.path.abspath( os.path.dirname( __file__ ) )
PROJECT_ROOT    = os.path.join( HERE, os.pardir )
TEST_PATH       = os.path.join( PROJECT_ROOT, 'tests' )


@click.command()
def test():
    """Run the tests."""
    import pytest
    rv = pytest.main([TEST_PATH, '--verbose'])
    exit(rv)


@click.command()
@click.option('-f', '--fix-imports', default=False, is_flag=True,
              help='Fix imports using isort, before linting')
def lint( fix_imports ):
    """Lint and check code style with flake8 and isort."""
    skip = ['requirements']
    root_files = glob('*.py')
    root_directories = [
        name for name in next(os.walk('.'))[1] if not name.startswith('.')]
    files_and_directories = [
        arg for arg in root_files + root_directories if arg not in skip]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        click.echo('{}: {}'.format(description, ' '.join(command_line)))
        rv = call(command_line)
        if rv != 0:
            exit(rv)

    if fix_imports:
        execute_tool('Fixing import order', 'isort', '-rc')
    execute_tool('Checking code style', 'flake8')


@click.command()
def clean():
    """Remove *.pyc and *.pyo files recursively starting at current directory.
    Borrowed from Flask-Script, converted to use Click.
    """
    for dirpath, _, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                click.echo('Removing {}'.format(full_pathname))
                os.remove(full_pathname)


@click.command()
@click.option( '--url', default = None,
               help = 'Url to test (ex. /static/image.png)' )
@click.option( '--order', default = 'rule',
               help = 'Property on Rule to order by (default: rule)' )
@with_appcontext
def urls(url, order):
    """Display all of the url matching routes for the project.
    Borrowed from Flask-Script, converted to use Click.
    """
    rows = []
    column_headers = ('Rule', 'Endpoint', 'Arguments')

    if url:
        try:
            rule, arguments = ( current_app.url_map.bind('localhost')
                                .match(url, return_rule=True ) )
            rows.append(( rule.rule, rule.endpoint, arguments ) )
            column_length = 3

        except (NotFound, MethodNotAllowed) as e:
            rows.append(('<{}>'.format(e), None, None))
            column_length = 1

    else:
        rules = sorted( current_app.url_map.iter_rules(),
                        key = lambda rule: getattr( rule, order ) )
        for rule in rules:
            rows.append((rule.rule, rule.endpoint, None))

        column_length = 2

    str_template = ''
    table_width = 0

    if column_length >= 1:
        max_rule_length = max(len(r[0]) for r in rows)
        max_rule_length = max_rule_length if max_rule_length > 4 else 4
        str_template += '{:' + str(max_rule_length) + '}'
        table_width += max_rule_length

    if column_length >= 2:
        max_endpoint_length = max(len(str(r[1])) for r in rows)
        max_endpoint_length = ( max_endpoint_length if max_endpoint_length > 8 else 8 )
        str_template += '  {:' + str(max_endpoint_length) + '}'
        table_width += 2 + max_endpoint_length

    if column_length >= 3:
        max_arguments_length = max(len(str(r[2])) for r in rows)
        max_arguments_length = ( max_arguments_length if max_arguments_length > 9 else 9 )
        str_template += '  {:' + str(max_arguments_length) + '}'
        table_width += 2 + max_arguments_length

    click.echo(str_template.format(*column_headers[:column_length]))
    click.echo('-' * table_width)

    for row in rows:
        click.echo(str_template.format(*row[:column_length]))

    return


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

@click.command('rundev', short_help='Runs a development server.')
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
    applic = info.load_app()
    host = applic.config.get( 'HOST', host )
    port = applic.config.get( 'PORT', port )

    from werkzeug.serving import run_simple
    run_simple( host, port, app,
                use_reloader = reload,
                reloader_type = 'stat',
                use_debugger = debugger,
                threaded = with_threads,
                ssl_context = cert )

@click.command( 'runprod', short_help='Runs a production server.' )
@click.option( '--host', '-h', default='127.0.0.1',
              help='The interface to bind to.')
@click.option( '--port', '-p', default=8000,
              help='The port to bind to.')
@pass_script_info
def runProduction( info, host, port, *args, **kwargs ):
    from waitress import serve
    print( args )
    print( kwargs )

    app = DispatchingApp( info.load_app, use_eager_loading = True )
    applic = info.load_app()
    host = applic.config.get( 'HOST', host )
    port = applic.config.get( 'PORT', port )

    serve( app, host = host, port = port )
