

def keyValueToHTML(key, value):
    if isinstance( value, bool ):
        value = str(value).lower()

    if key in ( 'id', 'mode' ):
        return '{}="{}"'.format(key, value)

    return '[{}]="{}"'.format( key, value )