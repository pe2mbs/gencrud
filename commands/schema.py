import webapp.api as API


def getCurrentSchema():
    return API.app.config[ 'DATABASE' ][ 'SCHEMA' ]


def listSchemas( schema = None ):
    data = API.db.session.connection().execute( "SHOW DATABASES" )
    if schema is None:
        current_schema = getCurrentSchema()

    else:
        current_schema = schema

    result = []
    for rec, *args in data:
        if rec.startswith( current_schema ) or rec == current_schema:
            result.append( rec )

    return result


def listTables( schema = None ):
    if schema is None:
        schema = getCurrentSchema()

    data = API.db.session.connection().execute( "SHOW TABLES FROM {}".format( schema ) )
    return [ rec for rec, *args in data ]


def getCurrentVersion():
    version_num = ''
    data = API.db.session.connection().execute( "SELECT version_num FROM {}.alembic_version".format( getCurrentSchema() ) );
    if data.rowcount > 0:
        version_num = data.fetchone()[0]

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
