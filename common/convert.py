from dateutil.parser import parse
from dateutil.tz import gettz

to_zone = gettz( 'Europe/Amsterdam' )

def value2Label( dictionary, value ):
    try:
        return dictionary[ value ]

    except Exception:
        return value


def utcDateString2Local( value, fmt = '%Y-%m-%d' ):
    return parse( value ).astimezone( to_zone ).date().strftime( fmt )
