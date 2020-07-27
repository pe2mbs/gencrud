import webapp2.api as API
from webapp2.commands.exporter.base import *


class SqlDbExporter( DbExporter ):
    CLEAR = True

    def buildRecord( self, table, record ):
        if not hasattr( record,'toSql' ):
            raise InvalidModel( table )

        return record.toSql()

    def writeTable( self, table, records, clear ):
        self._stream.write( "-- TABLE {}\n".format( table ) )
        if clear:
            self._stream.write( "DELETE FROM {};\n".format( table ) )

        for record in records:
            try:
                self._stream.write( "{}\n".format( self.buildRecord( table, record ) ) )

            except InvalidModel:
                API.app.logger.warning( "No toSql() member in '{}' model class".format( table ) )

            except:
                raise

        API.app.logger.info( "No of records: {}".format( len( records ) ) )
        return


