import json
from webapp2.commands.inporter.yaml import YamlDbInporter, DbInporter


class JsonDbInporter( YamlDbInporter ):
    def open( self, filename ):
        DbInporter.open( self,filename )
        self._blob = json.load( self._stream )
        return
