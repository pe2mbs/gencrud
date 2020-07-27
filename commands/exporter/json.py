import json
from webapp2.common.logjson import JsonEncoder
import webapp2.api as API
from webapp2.commands.exporter.base import DbExporter
from webapp2.commands.exporter.yaml import YamlDbExporter


class JsonDbExporter( YamlDbExporter ):
    def close( self ):
        API.app.logger.info( "Writing the output file" )
        json.dump( self._blob, self._stream, indent = 4, cls = JsonEncoder )
        DbExporter.close( self )
        return
