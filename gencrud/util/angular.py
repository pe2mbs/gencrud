

def keyValueToHTML(key, value):
    if isinstance(value, bool):
        value = str(value).lower()
    return '[{}]="{}"'.format( key, value )