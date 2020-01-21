#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2020 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation; either version 2 of the
#   License, or (at your option) any later version.
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
import logging
import datetime
import sqlalchemy.sql.sqltypes

logger = logging.getLogger()


def fieldConversion( record, key, value, default = None ):
    try:
        _type = record.__table__.columns[ key ].type

    except Exception:
        _type = record.__table__.columns[ key.lower() ].type

    logger.debug( 'field {0} value {1} type {2}'.format( key, value, _type ) )
    if isinstance( _type, ( sqlalchemy.sql.sqltypes.Integer,
                            sqlalchemy.sql.sqltypes.INTEGER,
                            sqlalchemy.sql.sqltypes.BigInteger,
                            sqlalchemy.sql.sqltypes.INT,
                            sqlalchemy.sql.sqltypes.BIGINT ) ):
        if value is not None:
            value = int( str( value ) )

        elif default is not None:
            value = default

    elif isinstance( _type, ( sqlalchemy.sql.sqltypes.REAL,
                              sqlalchemy.sql.sqltypes.Float,
                              sqlalchemy.sql.sqltypes.FLOAT,
                              sqlalchemy.sql.sqltypes.DECIMAL,
                              sqlalchemy.sql.sqltypes.Numeric,
                              sqlalchemy.sql.sqltypes.NUMERIC ) ):
        if value is not None:
            value = float( str( value ) )

        elif default is not None:
            value = default

    elif isinstance( _type, ( sqlalchemy.sql.sqltypes.DateTime,
                              sqlalchemy.sql.sqltypes.DATETIME,
                              sqlalchemy.sql.sqltypes.TIMESTAMP ) ):
        if value is not None:
            value = value[0:22] + value[23:]
            logger.debug( 'datetime.datetime.value: {}'.format( value ) )
            if value.endswith( 'Z' ):
                value = datetime.datetime.strptime( value, '%Y-%m-%dT%H:%M:%S.00Z' )

            else:
                value = datetime.datetime.strptime( value, '%Y-%m-%dT%H:%M:%S%z' )

        elif default is not None:
            value = default

    elif isinstance( _type, ( sqlalchemy.sql.sqltypes.Date,
                              sqlalchemy.sql.sqltypes.DATE ) ):
        # TODO: needs to be tested
        if value is not None:
            value = datetime.datetime.strptime( value, '%Y-%m-%d' ).date()

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

    logger.debug( 'field {0} value {1}'.format( key, value ) )
    return value
