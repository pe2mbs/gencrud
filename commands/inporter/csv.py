import os
import csv
import webapp2.api as API
from webapp2.commands.inporter.base import DbInporter


class CsvDbInporter( DbInporter ):
    def loadTable( self, table, model, clear ):
        fn, ext = os.path.splitext( self._filename )
        filename = "{}-{}{}".format( fn, table, ext )
        self.open( filename )
        csvreader = csv.reader( self._stream, delimiter = ';',quotechar = '"',quoting = csv.QUOTE_MINIMAL )
        it = iter( csvreader )
        header = it.__next__()
        if header is not None:
            if clear:
                API.db.session.delete( model )
                API.db.session.commit()

            for row in it:
                obj = model()
                for field,value in zip( header,row ):
                    setattr( obj,field,value )

                API.db.session.add( obj )

            API.db.session.commit()

        self.close()
        return
