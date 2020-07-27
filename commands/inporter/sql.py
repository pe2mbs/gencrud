from webapp2.commands.inporter.base import DbInporter
import webapp2.api as API


class SqlDbInporter( DbInporter ):
    CLEAR = False

    def loadTable( self, table, model, clear ):
        connection = API.db.session.connection()
        for idx, line in enumerate( self._stream.readlines() ):
            if line.startswith( '--' ):
                continue

            if idx == 0 and clear:
                API.db.session.delete( model )
                API.db.session.commit()

            try:
                line = line.replace( '\n', '' )
                API.app.logger.info( line )
                result = connection.execute( line )
                if result.rowcount != 1:
                    raise Exception( "row not inserted" )


            except Exception as exc:
                API.app.logger.error( exc )

        API.db.session.commit()
        return
