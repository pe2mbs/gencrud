import webapp2.api as API
from sqlalchemy.exc import IntegrityError, InternalError, ProgrammingError
from datetime import datetime, time, date

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

def mapFieldLists( connection, destination, source ):
    def Diff( li1, li2 ):
        return ( list( list( set( li1 ) - set( li2 ) ) + list( set( li2 ) - set( li1 ) ) ) )

    def Common( li1, li2 ):
        return list( set( li1 ).intersection( li2 ) )

    def GetFieldList( table_schema ):
        result = connection.execute( "SHOW FULL COLUMNS FROM {};".format( table_schema ) )
        fieldList = [ ]
        fieldData = {}
        for field, field_type, _, field_null, field_index, *field_options in result:
            fieldList.append( field )
            field_type, *field_type1 = field_type.split('(')
            field_len = 0
            if len( field_type1 ) > 0:
                field_len = int( field_type1[0].split(')')[0] )

            fieldData[ field ] = {
                'type': field_type,
                'length': field_len,
                'null': field_null,
                'index': field_index,
                'option': field_options
            }

        return fieldData, list( sorted( fieldList ) )

    destInfo, destFields = GetFieldList( destination )
    srcInfo, srcFields = GetFieldList( source )
    if len( Diff( destFields, srcFields ) ) > 0:
        srcAppendFields = [ ]
        destAppendFields = [ ]
        commonFields = Common( destFields,srcFields )
        # Get fields from destination not in common, therefor we need default values
        for field in Diff( commonFields, destFields ):
            fieldData = destInfo[ field ]
            if fieldData[ 'null' ].lower() == 'no':
                if fieldData[ 'type' ].lower() in ( 'char', 'varchar', 'text', 'longtext', 'blob' ):
                    srcAppendFields.append( '""' )
                    destAppendFields.append( field )

                elif fieldData[ 'type' ].lower() in ( 'int', 'long', 'tinyint' ):
                    srcAppendFields.append( '0' )
                    destAppendFields.append( field )

                elif fieldData[ 'type' ].lower() == 'datetime':
                    srcAppendFields.append( datetime.utcnow() )
                    destAppendFields.append( field )

                elif fieldData[ 'type' ].lower() == 'date':
                    srcAppendFields.append( datetime.utcnow().date() )
                    destAppendFields.append( field )

                elif fieldData[ 'type' ].lower() == 'time':
                    srcAppendFields.append( datetime.utcnow().time() )
                    destAppendFields.append( field )

        srcFields = commonFields + srcAppendFields
        destFields = commonFields + destAppendFields

    return ", ".join( destFields ), ", ".join( srcFields )


def copySchema2( destSchema, srcSchema, clear, ignore_errors = False ):
    def reccount( connection, schema_table ):
        try:
            for rec in connection.execute( "select count(*) from {};".format( schema_table ) ):
                return rec[ 0 ]

        except Exception:
            pass

        return 0

    INSERT_INTO = "INSERT INTO {destSchema}.{table} ( {destFields} ) SELECT {srcFields} FROM {srcSchema}.{table};"
    resultTable = {}
    errorTable = {}
    connection = API.db.session.connection()
    API.app.logger.info( "Begin work" )
    connection.execute( "SET FOREIGN_KEY_CHECKS=0;" )
    connection.execute( "BEGIN WORK;" )
    total = 0
    errors = 0
    table = ''
    try:
        for table in listTables( destSchema, exclude = [ 'alembic_version' ] ):
            # Now map the two field lists
            try:
                destFieldList, srcFieldList = mapFieldLists( connection,
                                                             "{}.{};".format( destSchema, table ),
                                                             "{}.{};".format( srcSchema, table ) )
            except ProgrammingError:
                if ignore_errors:
                    API.app.logger.error( "Skipping '{}' table".format( table ) )
                    continue

                raise

            except Exception:
                raise

            if clear:
                API.app.logger.info( "Clear '{}' table".format( table ) )
                connection.execute( "DELETE FROM {}.{};".format( destSchema, table ) )

            print( "Copying table '{}'".format( table ) )
            cmd = INSERT_INTO.format( destSchema = destSchema, destFields = destFieldList,
                                      srcSchema = srcSchema, srcFields = srcFieldList,
                                      table = table )

            count = 0
            try:
                connection.execute( cmd )
                count = reccount( connection, "{}.{};".format( destSchema, table ) )
                resultTable[ table ] = count
                API.app.logger.info( "{} Inserted into '{}' table".format( count, table ) )
                total += count

            except ProgrammingError as exc:
                API.app.logger.error( "Exception on table {}: {} ".format( table, exc ) )
                if ignore_errors:
                    if count == 0:
                        count = reccount( connection,"{}.{};".format( srcSchema,table ) )

                    errors += count
                    errorTable[ table ] = count
                    API.app.logger.error( "Skipping '{}' table".format( table ) )

                else:
                    raise

            except IntegrityError as exc:
                API.app.logger.error( "Exception on table {}: {} ".format( table,exc ) )
                if ignore_errors:
                    if count == 0:
                        count = reccount( connection,"{}.{};".format( srcSchema,table ) )

                    errors += count
                    API.app.logger.error( "InternalError {} not inserted into '{}' table".format( count,table ) )
                    errorTable[ table ] = count

                else:
                    raise

            except InternalError as exc:
                API.app.logger.error( "Exception on table {}: {} ".format( table,exc ) )
                if ignore_errors:
                    if count == 0:
                        count = reccount( connection,"{}.{};".format( srcSchema,table ) )

                    errors += count
                    API.app.logger.error( "InternalError {} not inserted into '{}' table".format( count,table ) )
                    errorTable[ table ] = count
                else:
                    raise

            except Exception as exc:
                API.app.logger.error( exc )
                API.app.logger.error( "{} {} not inserted into '{}' table".format( type(exc), count, table ) )

        API.app.logger.info( "Commit work" )
        connection.execute( "COMMIT WORK;" )
        API.app.logger.info( "{} records copied".format( total ) )

    except ( IntegrityError, InternalError, ProgrammingError ) as exc:
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
    return resultTable, errorTable, total, errors
