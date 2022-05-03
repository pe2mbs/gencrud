# -*- coding: utf-8 -*-
"""Database module for the 'Main Angular application package'.
including the SQLAlchemy database object and DB-related utilities."""
#
# Database module for the 'Main Angular application package'.
# Copyright (C) 2018 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
import logging
import threading
import sqlalchemy.orm as ORM
import sqlalchemy.types as types
import webapp2.api as API
from webapp2.common.compat import basestring
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask import g, current_app, has_request_context
from sqlalchemy.ext.compiler import compiles


# Fix described @ https://stackoverflow.com/questions/45527323/flask-sqlalchemy-upgrade-failing-after-updating-models-need-an-explanation-on-h
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


def get_model( name ):
    return db.Model._decl_class_registry.get( name, None )


def get_model_by_tablename( tablename ):
    for c in db.Model._decl_class_registry.values():
        if hasattr( c, '__tablename__' ) and c.__tablename__ == tablename:
            return c

    return None


class LONGTEXT( types.UserDefinedType ):
    item_type = types.Text
    def __init__( self ):
        return

    def get_col_spec( self, **kw ):
        return "LONGTEXT"

    def bind_processor( self, dialect ):
        def process( value ):
            return value

        return process

    def result_processor( self, dialect, coltype ):
        def process( value ):
            return value

        return process


class MEDIUMTEXT( types.UserDefinedType ):
    item_type = types.Text
    def __init__( self ):
        return

    def get_col_spec( self, **kw ):
        return "MEDIUMTEXT"

    def bind_processor( self, dialect ):
        def process( value ):
            return value

        return process

    def result_processor( self, dialect, coltype ):
        def process( value ):
            return value

        return process


@compiles(LONGTEXT, "sqlite")
def compile_binary_sqlite(type_, compiler, **kw):
    return "VARCHAR"


@compiles(MEDIUMTEXT, "sqlite")
def compile_binary_sqlite(type_, compiler, **kw):
    return "VARCHAR"


# MainThread db
db              = None
thread_db       = {}
if db is None:
    # Make sure that the db is initialized only once!
    db = SQLAlchemy( metadata = MetaData( naming_convention = naming_convention ) )
    API.db = db
    # if "mysql" in db.session.bind.dialect.name:
    #     # This is nessary for the QUERY below to read the changes make by other processes.
    #     logging.info( "SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED" )
    #     db.session.execute( "SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED" )

    db.get_model                = get_model
    db.get_model_by_tablename   = get_model_by_tablename
    # temp. vars
    # Column          = db.Column
    # relationship    = ORM.relationship
    # Model           = db.Model
    db.MEDIUMBLOB   = types._Binary
    db.LONGBLOB     = types._Binary
    db.MEDIUMTEXT   = MEDIUMTEXT
    db.LONGTEXT     = LONGTEXT
    db.MEDIUMCLOB   = MEDIUMTEXT
    db.LONGCLOB     = LONGTEXT
    thread_db       = { threading.currentThread().name: db }


def destroyDatabaseObject( obj ):
    global db, thread_db
    if db == obj:
        # delete the master, so everything goes !
        for name, tdb in thread_db.items():
            if tdb is not db:
                del tdb

        API.db = None
        del db
        db = None
        thread_db = {}

    elif len( thread_db ):
        for key, dbobj in thread_db.items():
            if dbobj == obj:
                # Delete one db object from the thread list
                del dbobj
                del thread_db[ key ]
                # All done, get the hell out of here
                break

    return

def getDataBase( app = None ):
    if has_request_context():
        return db

    if threading.currentThread().name in thread_db:
        return thread_db[ threading.currentThread().name ]

    if app is None:
        app = current_app

    logging.warning( "Create new DB session for application context" )
    db_thread = SQLAlchemy( metadata = MetaData( naming_convention = naming_convention ) )
    # This to configure the database
    db_thread.init_app( app )
    app.app_context().push()
    if "mysql" in db_thread.session.bind.dialect.name:
        # This is nessary for the QUERY below to read the changes make by other processes.
        app.logger.info( "SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED" )
        db_thread.session.execute( "SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED" )

    # Alias common SQLAlchemy names
    thread_db[ threading.currentThread().name ] = db_thread
    return db_thread


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` \
       to any declarative-mapped class.
    """
    __table_args__ = { 'extend_existing': True }

    id = db.Column( db.Integer, primary_key = True )

    @classmethod
    def get_by_id( cls, record_id ):
        """Get record by ID."""
        if any( ( isinstance( record_id, basestring ) and record_id.isdigit(),
                  isinstance( record_id, ( int, float ) ) ), ):
            return cls.query.get( int( record_id ) )


def referenceColumn( tablename, nullable = False, pk_name = 'id', **kwargs ):
    """Column that adds primary key foreign key reference.
    Usage: ::
        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    db = getDataBase()
    return db.Column( db.ForeignKey( '{0}.{1}'.format( tablename, pk_name ) ),
                   nullable = nullable,
                   **kwargs )
