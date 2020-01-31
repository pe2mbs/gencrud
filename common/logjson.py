import json
import decimal
import datetime

class JsonEncoder( json.JSONEncoder ):
    def default( self, obj ):
        if isinstance( obj, complex ):
            return [ obj.real, obj.imag ]

        elif isinstance( obj, decimal.Decimal ):
            if int(obj) == float( obj ):
                return int(obj)

            return float( obj )


        elif isinstance( obj, ( datetime.datetime, datetime.date, datetime.time ) ):
            return str( obj )

        try:
            # Let the base class default method raise the TypeError
            return json.JSONEncoder.default( self, obj )

        except:
            pass

        return str( obj )

