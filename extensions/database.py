# -*- coding: utf-8 -*-
"""Main webapp application package."""
#
# Main webapp application package
# Copyright (C) 2018-2020 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>
#
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License GPL-2.0-only
# as published by the Free Software Foundation.
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
import webapp.api as API
from sqlalchemy.orm import relationship
from webapp.common.compat import basestring
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Column


# Fix described @ https://stackoverflow.com/questions/45527323/flask-sqlalchemy-upgrade-failing-after-updating-models-need-an-explanation-on-h
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


def get_model( self, name ):
    return self.Model._decl_class_registry.get( name, None )


def get_model_by_tablename( self, tablename ):
    for c in self.Model._decl_class_registry.values():
        if hasattr( c, '__tablename__' ) and c.__tablename__ == tablename:
            return c

    return None


SQLAlchemy.get_model = get_model
SQLAlchemy.get_model_by_tablename = get_model_by_tablename

API.db = SQLAlchemy( metadata=MetaData( naming_convention = naming_convention ) )

# Alias common SQLAlchemy names
API.Column = API.db.Column
API.RelationShip = relationship
API.Model = API.db.Model


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK( object ):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` \
       to any declarative-mapped class.
    """
    __table_args__ = { 'extend_existing': True }

    id = API.db.Column( API.db.Integer, primary_key = True )

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
    return API.Column( API.db.ForeignKey( '{0}.{1}'.format( tablename, pk_name ) ),
                   nullable = nullable,
                   **kwargs )
