

def toggleInDict( d, key, value, recursive = False ):
    for k in d.keys():
        if k == key:
            d[ key ] = value

        elif recursive and type( d[ k ] ) is dict:
            d[ k ] = toggleInDict( d[ k ], key, value, recursive )

        elif recursive and type( d[ k ] ) is list:
            for idx, item in enumerate( d[ k ] ):
                if type( item ) is dict:
                    d[ k ][ idx ] = toggleInDict( d[ key ][ idx ], key, value, recursive )

    return d

