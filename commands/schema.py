import webapp2.api as API
from sqlalchemy.exc import IntegrityError

def getCurrentSchema():
    return API.app.config[ 'DATABASE' ][ 'SCHEMA' ]


def listSchemas( schema = None, all = False, exclude = None ):
    data = API.db.session.connection().execute( "SHOW DATABASES" )
    if schema is None:
        current_schema = getCurrentSchema()

    else:
        current_schema = schema

    if not isinstance( exclude, ( tuple, list ) ):
        exclude = []

    result = []
    for rec, *args in data:
        if all or rec.startswith( current_schema ) or rec == current_schema:
            if rec in exclude:
                continue

            result.append( rec )

    return result


def listTables( schema = None, exclude = None ):
    if schema is None:
        schema = getCurrentSchema()

    if exclude is None:
        exclude = []

    data = API.db.session.connection().execute( "SHOW TABLES FROM {}".format( schema ) )
    result = []
    for rec,*args in data:
        if rec not in exclude:
            result.append( rec )

    return result


def getCurrentVersion( schema = None ):
    version_num = ''
    if schema is None:
        schema = getCurrentSchema()

    try:
        data = API.db.session.connection().execute( "SELECT version_num FROM {}.alembic_version".format( schema ) )
        if data.rowcount > 0:
            version_num = data.fetchone()[0]

    except:
        return None

    return version_num


def copySchema( oSchema, nSchema ):
    connection = API.db.session.connection()
    connection.execute( "DROP DATABASE IF EXISTS {}".format( nSchema ) )
    connection.execute( "CREATE DATABASE {}".format( nSchema ) )

    for table in listTables( oSchema ):
        cmd = "CREATE TABLE {nSchema}.{table} SELECT * FROM {oSchema}.{table}".format( oSchema = oSchema,
                                                                                       nSchema = nSchema,
                                                                                       table = table )
        connection.execute( cmd )

    return

def copySchema2( destSchema, srcSchema, clear ):
    resultTable = {}
    connection = API.db.session.connection()
    API.app.logger.info( "Begin work" )
    connection.execute( "SET FOREIGN_KEY_CHECKS=0;" )
    connection.execute( "BEGIN WORK;" )
    total = 0
    table = ''
    try:
        for table in listTables( destSchema, exclude = [ 'alembic_version' ] ):
            result = connection.execute( "SHOW COLUMNS FROM {}.{};".format( destSchema,table ) )
            fields = [ ]
            for field, *args in result:
                fields.append( field )

            fieldList = ", ".join( fields )
            if clear:
                API.app.logger.info( "Clear '{}' table".format( table ) )
                connection.execute( "DELETE FROM {}.{};".format( destSchema, table ) )

            print( "Copying table '{}'".format( table ) )
            cmd = "INSERT INTO {destSchema}.{table} ( {fields} ) SELECT {fields} FROM {srcSchema}.{table};".format( destSchema = destSchema,
                                                                                                              srcSchema = srcSchema,
                                                                                                              table = table,
                                                                                                              fields = fieldList )

            connection.execute( cmd )
            count = 0
            for rec in connection.execute( "select count(*) from {}.{};".format( destSchema, table ) ):
                count = rec[ 0 ]

            resultTable[ table ] = count
            API.app.logger.info( "{} Inserted into '{}' table".format( count, table ) )
            total += count

        API.app.logger.info( "Commit work" )
        connection.execute( "COMMIT WORK;" )
        API.app.logger.info( "{} records copied".format( total ) )

    except IntegrityError as exc:
        if exc.orig is not None:
            API.app.logger.error( "{} in table {}".format( exc.orig.args[ 1 ], table ) )

        else:
            API.app.logger.error( "{} in table {}".format( exc.args[ 0 ],table ) )

        API.app.logger.info( "Rollback work" )
        connection.execute( "ROLLBACK WORK;" )

    except Exception as exc:
        API.app.logger.info( "Rollback work" )
        API.app.logger.error( exc )
        connection.execute( "ROLLBACK WORK;" )

    connection.execute( "SET FOREIGN_KEY_CHECKS=1;" )
    return resultTable, total
