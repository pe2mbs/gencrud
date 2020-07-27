import yaml
import webapp2.api as API
from webapp2.commands.exporter.base import *


class YamlDbExporter( DbExporter ):
    def __init__( self, filename = None ):
        DbExporter.__init__( self, filename )
        self._blob = []
        return

    def close( self ):
        API.app.logger.info( "Writing the output file" )
        yaml.dump( self._blob, self._stream, default_style = False, default_flow_style = False )
        DbExporter.close( self )
        return

    def writeTable( self, table, records ):
        for rec in records:
            try:
                self._blob.append( { 'table':   table,
                                     'records': [ self.buildRecord( table, rec ) ] } )

            except InvalidModel:
                API.app.logger.warning( "No toSql() member in '{}' model class".format( table ) )

            except:
                raise

        API.app.logger.info( "No of records: {}".format( len( records ) ) )
        return

