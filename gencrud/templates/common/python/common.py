#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2020 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
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
import datetime
import sqlalchemy.sql.sqltypes
from dateutil import tz

try:
    import webapp2.api as API
except ModuleNotFoundError:
    # Error handling
    raise SystemExit("You need to include the module webapp2. Follow instructions " +
        "on https://github.com/pe2mbs/gencrud/blob/master/doc/MANUAL.md")


def convertDateTime( value ):
    value = value[ 0:22 ] + value[ 23: ]
    API.app.logger.debug( 'datetime.datetime.value: {}'.format( value ) )
    if value.startswith( '0000-00-00' ):
        value = datetime.datetime.utcnow()

    elif not value[ 0 ].isdigit():
        # 'Tue Aug 19 1975 23:15:30 GMT+0200 (CEST)'
        value = value.split( '(' )[ 0 ].strip()
        try:
            value = datetime.datetime.strptime( value,'%a %b %d %Y %H:%M:%S %Z%z' )

        except Exception:
            value = datetime.datetime.strptime( value,'%a %b %d %Y %H:%M:%S %z%Z' )

    # ELSE starts with digit
    elif value.endswith( 'Z' ):
        # ISO format without timezone
        value = datetime.datetime.strptime( value,'%Y-%m-%dT%H:%M:%S.%fZ' )

    elif 'T' in value:
        # ISO format with timezone
        if '+' in value:
            value = datetime.datetime.strptime( value, '%Y-%m-%dT%H:%M:%S.%f%z' )

        else:
            value = datetime.datetime.strptime( value,'%Y-%m-%dT%H:%M:%S%z' )

    else:
        # Plain format, local time ?
        value = datetime.datetime.strptime( value,'%Y-%m-%d %H:%M:%S' )

    return value


def fieldConversion( record, key, value, default = None ):
    try:
        _type = record.__table__.columns[ key ].type

    except Exception:
        _type = record.__table__.columns[ key.lower() ].type

    API.app.logger.debug( 'field {0} value {1} type {2}'.format( key, value, str( _type ) ) )
    if isinstance( _type, ( sqlalchemy.sql.sqltypes.Integer,
                            sqlalchemy.sql.sqltypes.INTEGER,
                            sqlalchemy.sql.sqltypes.BigInteger,
                            sqlalchemy.sql.sqltypes.INT,
                            sqlalchemy.sql.sqltypes.BIGINT ) ):
        try:
            if value is not None:
                value = int( str( value ) )

            elif default is not None:
                value = default

        except:
            if isinstance( default,int ):
                value = default

            else:
                value = 0

    elif isinstance( _type, ( sqlalchemy.sql.sqltypes.REAL,
                              sqlalchemy.sql.sqltypes.Float,
                              sqlalchemy.sql.sqltypes.FLOAT,
                              sqlalchemy.sql.sqltypes.DECIMAL,
                              sqlalchemy.sql.sqltypes.Numeric,
                              sqlalchemy.sql.sqltypes.NUMERIC ) ):
        try:
            if value is not None:
                value = float( str( value ) )

            elif default is not None:
                value = default

        except:
            if isinstance( default, float ):
                value = default

            else:
                value = 0.0

    elif isinstance( _type, ( sqlalchemy.sql.sqltypes.DateTime,
                              sqlalchemy.sql.sqltypes.DATETIME,
                              sqlalchemy.sql.sqltypes.TIMESTAMP ) ):
        if value is not None:
            value = convertDateTime( value )

        elif default is not None:
            value = default

    elif isinstance( _type, ( sqlalchemy.sql.sqltypes.Date,
                              sqlalchemy.sql.sqltypes.DATE ) ):
        # TODO: needs to be tested
        API.app.logger.debug( "Type date: '{}'".format( value ) )
        if value is not None:
            # UTC format, need to add local time diff
            if 'T' in value:
                utc  = convertDateTime( value )
                from_zone = tz.tzutc()
                to_zone = tz.tzlocal()
                utc = utc.replace( tzinfo = from_zone )
                value = utc.astimezone( to_zone )
                API.app.logger.debug( "Type datetime: '{}'".format( value ) )

            else:
                value = datetime.datetime.strptime( value, '%Y-%m-%d' )

            API.app.logger.debug( "Type date: '{}'".format( value ) )
            value = value.date()
            API.app.logger.debug( "Type date: '{}'".format( value ) )

        elif default is not None:
            value = default

    elif isinstance( _type, ( sqlalchemy.sql.sqltypes.Time,
                              sqlalchemy.sql.sqltypes.TIME ) ):
        # TODO: needs to be tested
        if value is not None:
            value = datetime.datetime.strptime( value, '%H:%M:%S' ).time()

        elif default is not None:
            value = default

    elif isinstance( _type, ( sqlalchemy.sql.sqltypes.Boolean,
                              sqlalchemy.sql.sqltypes.BOOLEAN ) ):
        if type( value ) is int:
            value = bool( value )

        elif type( value ) is str:
            value = bool( value )

        elif value is None:
            if default is not None:
                value = default

            else:
                value = False

    API.app.logger.debug( 'field {0} value {1}'.format( key, value ) )
    return value
