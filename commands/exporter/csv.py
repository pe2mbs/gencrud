import os
import csv
import webapp2.api as API
from webapp2.commands.exporter.base import *


class CsvDbExporter( DbExporter ):
    def open( self, filename ):
        return

    def writeTable( self, table, records ):
        basefilename, ext = os.path.splitext( self._filename )
        filename = '{}-{}{}'.format( basefilename, table, ext )
        with open( filename, 'w', newline='' ) as stream:
            if len( records ) > 0:
                csvwriter = csv.writer( stream, delimiter = ';',quotechar = '"' )
                try:
                    csvwriter.writerow( self.buildRecord( table, records[ 0 ] ).keys() )

                    for record in records:
                        try:
                            csvwriter.writerow( self.buildRecord( table, record ).values() )

                        except InvalidModel:
                            API.app.logger.warning( "No toSql() member in '{}' model class".format( table ) )

                        except:
                            raise

                except InvalidModel:
                    API.app.logger.warning( "No toSql() member in '{}' model class".format( table ) )

                except:
                    raise

                API.app.logger.info( "No of records: {}".format( len( records ) ) )

            else:
                API.app.logger.warning( "Nothing to export" )

        return
