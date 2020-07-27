from webapp2.common.util import InvalidModel, DbExporterInporters

class DbExporter( object ):
    CLEAR = False

    def __init__( self, filename = None ):
        self._filename = filename
        self._stream   = None
        return

    def open( self, filename ):
        if self._stream is None:
            self._stream = open( filename, 'w' )

        return

    def close( self ):
        if self._stream is not None:
            self._stream.close()

        self._stream = None
        return

    def writeTable( self, table, records, clear ):
        return

    def buildRecord( self, table, record ):
        if not hasattr( record, 'toDict' ):
            raise InvalidModel( table )

        return record.toDict()


class DbExporters( DbExporterInporters ): pass
