import yaml
import os
from webapp2.commands.inporter.base import DbInporter
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
        if clear:
            API.db.session.delete( model )
            API.db.session.commit()

        for record in records:
            obj = model()
            for field,value in record.items():
                setattr( obj,field,value )

            API.db.session.add( obj )
            API.db.session.commit()

        return

    def loadTable( self, table, model, clear ):
        if isinstance( self._blob, ( list, tuple ) ):
            # When importing json/yaml files without table info,
            # export maybe from MySQL workbench
            self._insertList( self._blob, model, clear )

        elif isinstance( self._blob, dict ):
            self._insertDict( self._blob[ table ], model, clear )

        return


