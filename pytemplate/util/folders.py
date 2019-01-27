import os
import pathlib

class PathNotFoundException( Exception ):
    def __init__( self, path ):
        super( PathNotFoundException, self ).__init__( '{} not found.'.format( path ) )
        return


def findpath( curr: pathlib.Path, rel: str ):
    while True:
        curr = curr.parent
        test = pathlib.Path( os.path.abspath( os.path.join( str( curr ), rel ) ) )
        if test.is_dir():
            return curr

        if str( curr ) == curr.root:
            raise PathNotFoundException( rel )

    return