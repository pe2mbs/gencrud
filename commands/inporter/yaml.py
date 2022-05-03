import yaml
import os
import datetime
from webapp2.commands.inporter.base import DbInporter
import sqlalchemy.sql.sqltypes as SQLTYPES
import webapp2.api as API


class YamlDbInporter( DbInporter ):
    def open( self,filename ):
        DbInporter.open( self,filename )
        self._blob = yaml.load( self._stream )
        return

    def _insertDict( self, blob, model, clear ):
        # Handle the yaml/json data
        if len( records ) > 0:
            self._insertList( blob[ 'records' ], model, clear )

        return

    def _insertList( self, records, model, clear ):
        connection = API.db.session.connection()
        if clear:
            connection.execute( "SET FOREIGN_KEY_CHECKS=0;" )
            connection.execute( "BEGIN WORK;" )
            connection.execute( "DELETE FROM {};".format( model.__table__ ) )

        for record in records:
            obj = model()
            API.app.logger.info( "Record: {}".format( record ) )
            for field, value in record.items():
                attr = model.__table__.c[ field ].type
                API.app.logger.info( "Field {} ({}) := {}".format( field, attr.python_type, value ) )
                if attr.python_type is datetime.datetime:
                    if value == '':
                        value = None

                    else:
                        # Some conversion is needed
                        value = datetime.datetime.strptime( value, '%Y-%m-%d %H:%M:%S' )

                setattr( obj, field.upper(), value )

            API.db.session.add( obj )

        API.db.session.commit()
        connection = API.db.session.connection()
        connection.execute( "SET FOREIGN_KEY_CHECKS=0;" )
        return

    def loadTable( self, table, model, clear ):
        if isinstance( self._blob, ( list, tuple ) ):
            # When importing json/yaml files without table info,
            # export maybe from MySQL workbench
            self._insertList( self._blob, model, clear )

        elif isinstance( self._blob, dict ):
            self._insertDict( self._blob[ table ], model, clear )


        return


