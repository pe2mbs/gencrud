

class InvalidModel( Exception ): pass


def keysToString( keys ):
    if len( keys ) > 1:
        return ', '.join( [ value for value in keys[ : -1 ] ] ) + ' and ' + keys[ -1 ]

    if len( keys ) == 1:
        return keys[ 0 ]

    return "?"


class DbExporterInporters( dict ):
    def __init__( self, d ):
        for key, value in d.items():
            self[ key ] = value

        return

    def hasClear2String( self ):
        result = [ ]
        for key,value in self.items():
            if value.CLEAR:
                result.append( key.upper() )

        return keysToString( result )

    def keysUpperCase( self ):
        return [ k.upper() for k in self.keys() ]

    def keysToString( self ):
        return keysToString( self.keysUpperCase() )


def CommandBanner( *args ):
    l = 76
    for line in args:
        if len( line ) > l:
            l = len( line )

    print( "+{}+".format( "-" * (l+2) ) )
    for line in args:
        print( "| {:{}} |".format( line, l ) )

    print( "+{}+".format( "-" * (l+2) ) )
    return
