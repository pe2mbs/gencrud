import click
from flask.cli import ( pass_script_info,
                        CertParamType,
                        _validate_key,
                        get_debug_flag,
                        show_server_banner,
                        get_env,
                        DispatchingApp )


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
def rundevCommand( info, host, port, reload, debugger, eager_loading,
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


