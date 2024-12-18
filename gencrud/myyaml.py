#
#   Python backend and Angular frontend
#   Copyright (C) 2018-2024 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#   Library General Public License for more details.
#
#   You should have received a copy of the GNU Library General Public
#   License GPL-2.0-only along with this library; if not, write to the
#   Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301 USA
#
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