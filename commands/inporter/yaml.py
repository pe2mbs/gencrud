import yaml
import os
from webapp2.commands.inporter.base import DbInporter
import webapp2.api as API


class YamlDbInporter( DbInporter ):
    def open( self,filename ):
        DbInporter.open( self,filename )
        self._blob = yaml.load( self._stream )
        return

    def _insert( self, blob, model, clear ):
        # Handle the yaml/json data
        records = blob[ 'records' ]
        if len( records ) > 0:
            if clear:
                API.db.session.delete( model )
                API.db.session.commit()

            for record in records:
                obj = model()
                for field,value in record.items():
                    setattr( obj, field, value )

                API.db.session.add( obj )
                API.db.session.commit()

    def loadTable( self, table, model, clear ):
        self._insert( self._blob[ table ], model, clear )
        return


