import typing as t
import os
import yaml


class Loader( yaml.SafeLoader ):
    """YAML Loader with `!include` constructor."""

    def __init__( self, stream: t.IO ) -> None:
        """Initialise Loader."""

        try:
            self._root = os.path.split( stream.name )[ 0 ]

        except AttributeError:
            self._root = os.path.curdir

        super().__init__( stream )
        return

def construct_include( loader: yaml.Loader, node: yaml.Node ) -> t.Any:
    """Include file referenced at node."""

    filename = os.path.abspath( os.path.join( loader._root, loader.construct_scalar( node ) ) )
    extension = os.path.splitext( filename)[ 1 ].lstrip( '.' )

    with open( filename, 'r' ) as f:
        if extension in ( 'yaml', 'yml', 'conf' ):
            return yaml.load( f, Loader )

        elif extension in ('json', ):
            import json
            return json.load(f)

        else:
            return ''.join( f.readlines() )


yaml.add_constructor( '!include', construct_include, Loader )


def load( stream, **kwargs ):
    return yaml.load( stream, Loader = Loader )


def dump( stream, data, **kwargs ):
    return yaml.dump( data, stream, **kwargs )