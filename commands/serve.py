import os
from flask.cli import AppGroup
import click
from flask.cli import ( pass_script_info,
                        CertParamType,
                        _validate_key,
                        get_debug_flag,
                        show_server_banner,
                        get_env,
                        DispatchingApp )


@click.group( cls = AppGroup )
def serve():
    """Serve commands"""


@serve.command( 'dev',
                short_help = 'Runs a development server.' )
@click.option( '--host', '-h',
               help = 'The interface to bind to.')
@click.option( '--port', '-p',
               help = 'The port to bind to.' )
@click.option( '--cert',
               type = CertParamType(),
               help = 'Specify a certificate file to use HTTPS.')
@click.option( '--key',
               type = click.Path( exists = True,
                                  dir_okay = False,
                                  resolve_path = True ),
               callback=_validate_key,
               expose_value = False,
               help = 'The key file to use when specifying a certificate.')
@click.option( '--reload/--no-reload',
               default = None,
               help = 'Enable or disable the reloader. By default the reloader '
                      'is active if debug is enabled.')
@click.option( '--debugger/--no-debugger',
               default = None,
               help = 'Enable or disable the debugger. By default the debugger '
                      'is active if debug is enabled.')
@click.option( '--eager-loading/--lazy-loader',
               default = None,
               help = 'Enable or disable eager loading. By default eager '
                      'loading is enabled if the reloader is disabled.' )
@click.option( '--with-threads/--without-threads',
               default = True,
               help = 'Enable or disable multithreading.' )
@pass_script_info
def dev( info, host, port, reload, debugger, eager_loading,
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
    applic      = info.load_app()
    print( "HOST {} PORT {}".format( host,port ) )
    if host is None:
        host        = applic.config.get( 'HOST', 'localhost' )

    if port is None:
        port        = applic.config.get( 'PORT', 5000 )

    else:
        port = int( port )

    print( "HOST {} PORT {}".format( host, port ) )
    appPath     = applic.config.get( 'APP_PATH', os.curdir )
    appApiMod   = applic.config.get( 'API_MODULE', '' )
    # As those files may change, but are only loaded when the application starts
    # we monitor them, so that the application restart when they change
    extra_files = [ os.path.join( appPath, appApiMod, 'menu.yaml' ),
                    os.path.join( appPath, appApiMod, 'release.yaml' ) ]
    from werkzeug.serving import run_simple
    run_simple( host, port, app,
                use_reloader = reload,
                reloader_type = 'stat',
                use_debugger = debugger,
                threaded = with_threads,
                ssl_context = cert,
                extra_files = extra_files )
    return


@serve.command( 'production',
                short_help = 'Runs a production server.' )
@click.option( '--host', '-h',
               default = '127.0.0.1',
               help = 'The interface to bind to.' )
@click.option( '--port', '-p',
               default = 8000,
               help = 'The port to bind to.' )
@pass_script_info
def production( info, host, port, *args, **kwargs ):
    import waitress
    app = DispatchingApp( info.load_app, use_eager_loading = True )
    applic = info.load_app()
    host = applic.config.get( 'HOST', host )
    port = applic.config.get( 'PORT', port )
    waitress.serve( app, host = host, port = port )
    return


@serve.command( 'staged',
                short_help = 'Runs a production server.' )
@click.option( '--host', '-h',
               default = '127.0.0.1',
               help = 'The interface to bind to.' )
@click.option( '--port', '-p',
               default = 8000,
               help = 'The port to bind to.' )
@pass_script_info
def staged( info, host, port, *args, **kwargs ):
    import waitress
    app = DispatchingApp( info.load_app, use_eager_loading = True )
    applic = info.load_app()
    host = applic.config.get( 'HOST', host )
    port = applic.config.get( 'PORT', port )
    waitress.serve( app, host = host, port = port )
    return

@serve.command( 'ssl',
                short_help = 'Runs a SSL/TLS server.')
@click.option( '--host', '-h',
               default = '127.0.0.1',
               help = 'The interface to bind to.')
@click.option( '--port', '-p',
               default = 5000,
               help='The port to bind to.')
@click.option( '--cert',
               type = CertParamType(),
               help='Specify a certificate file to use HTTPS.')
@click.option( '--key',
               type = click.Path( exists = True,
                                  dir_okay = False,
                                  resolve_path = True ),
               callback=_validate_key,
               expose_value = False,
               help = 'The key file to use when specifying a certificate.' )
@click.option( '--reload/--no-reload',
               default = None,
               help = 'Enable or disable the reloader. By default the reloader '
                      'is active if debug is enabled.')
@click.option( '--debugger/--no-debugger',
               default = None,
               help = 'Enable or disable the debugger. By default the debugger '
                      'is active if debug is enabled.')
@click.option( '--eager-loading/--lazy-loader',
               default = None,
               help = 'Enable or disable eager loading. By default eager '
                      'loading is enabled if the reloader is disabled.')
@click.option( '--with-threads/--without-threads',
               default = True,
               help = 'Enable or disable multithreading.')
@pass_script_info
def ssl( info, host, port, reload, debugger, eager_loading,
                   with_threads, cert, key ):
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

    appPath     = applic.config.get( 'APP_PATH', os.curdir )
    appApiMod   = applic.config.get( 'API_MODULE', '' )
    # As those files may change, but are only loaded when the application starts
    # we monitor them, so that the application restart when they change
    extra_files = [ os.path.join( appPath, appApiMod, 'menu.yaml' ),
                    os.path.join( appPath, appApiMod, 'release.yaml' ) ]
    from werkzeug.serving import run_simple
    run_simple( host, port, app,
                use_reloader = reload,
                reloader_type = 'stat',
                use_debugger = debugger,
                threaded = with_threads,
                ssl_context = cert,
                extra_files = extra_files )
    return
