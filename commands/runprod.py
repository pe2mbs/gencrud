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
