import re
import sys
import os.path

with open( os.path.join( 'gencrud', 'version.py' ), 'r' ) as stream:
    lines = stream.read().split( '\n' )

# Update the line '__version__     = '2.3.475''
for idx, line in enumerate( lines ):
    if line.startswith( '__version__' ):
        result = re.search( "__version__\s+=\s+\'(\d+)\.(\d+).(\d+)'", line )
        major = int( result.group( 1 ) )
        minor = int( result.group( 2 ) )
        build = int( result.group( 3 ) ) + 1
        lines[ idx ] = f"__version__     = '{major}.{minor}.{build}'"
        break

with open( os.path.join( 'gencrud', 'version.py' ), 'w', newline='' ) as stream:
    stream.write( '\n'.join( lines ) )

sys.exit()
