import os
import click
import yaml
from yamlinclude import YamlIncludeConstructor
import json
import csv
from sqlalchemy.engine.reflection import Inspector
import sqlalchemy.orm
import webapp2.api as API
from sqlalchemy.inspection import inspect
from flask.cli import with_appcontext
from flask.cli import AppGroup
from webapp2.commands.schema import ( listSchemas,
                                     getCurrentVersion,
                                     getCurrentSchema,
                                     copySchema,
                                     listTables )

YamlIncludeConstructor.add_to_loader_class( loader_class= yaml.FullLoader, base_dir = '.' )


@click.group( cls = AppGroup )
def dba():
    """DBA backup / restore for the webapp application."""


@dba.command( 'backup', short_help = 'Backup the database.' )
@click.option( '--list/--nolist', '_list', default = False, help = 'List the schemas.' )
@click.option( '--name', nargs=1, type=str, help="The name of the backup name." )
@click.option( '--schema', nargs=1, type=str, help="Backup to a different schema." )
@with_appcontext
def backup( _list, name, schema ):
    if _list:
        print( "Available schemas like {}".format( getCurrentSchema() ) )
        for sch in listSchemas():
            print( "> {}".format( sch ) )

        return

    API.app.logger.info( "DBA backup name: {} schema: {}".format( name, schema ) )
    oSchema = getCurrentSchema()
    if name is None:
        # Create schema based on the alembic version
        # If it exists drop the schema first
        if schema is None:
            # Backup within the current schema
            schema = '{}_{}'.format( oSchema, getCurrentVersion() )

    else:
        # Create schema based on the name
        # If it exists drop the schema first
        if schema is None:
            schema = '{}_{}'.format( oSchema, name )

        else:
            schema = '{}_{}'.format( schema, name )

    API.app.logger.info( "Copy '{}' to '{}'".format( oSchema, schema ) )
    copySchema( oSchema, schema )
    return


@dba.command( 'restore', short_help = 'Restore the database.' )
@click.option( '--list/--nolist', '_list', default = False, help = 'List the schemes.' )
@click.option( '--name', nargs=1, type=str, help="The name of the backup name to restore." )
@click.option( '--schema', nargs=1, type=str, help="Restore from a different schema." )
@with_appcontext
def restore( _list, name, schema ):
    if _list:
        print( "Available schemas like {}".format( getCurrentSchema() ) )
        for sch in listSchemas():
            print( "> {}".format( sch ) )

        return

    API.app.logger.info( "DBA restore name: {} schema: {}".format( name, schema ) )
    nSchema = getCurrentSchema()
    if name is None:
        if schema is None:
            schema = '{}_{}'.format( nSchema, getCurrentVersion() )

    else:
        if schema is None:
            schema = '{}_{}'.format( nSchema, name )

        else:
            schema = '{}_{}'.format( schema, name )

        if schema not in listSchemas():
            API.app.logger.error( "Need to supply a existing name" )
            restore( True, None )
            return

    API.app.logger.info( "Copy '{}' to '{}'".format( schema, nSchema ) )
    copySchema( schema, nSchema )
    return


EXPORT_HELP = """Export the database to a YAML, JSON, SQL or CSV file.

    dba export [ --fmt <type> ] [ --table <table-name> ] <filename> 


<filename>: The filename with or without the extension to be used to write the database information to.
"""


@dba.command( 'export', short_help = 'Export the database to a YAML, JSON, SQL or CSV file.',
              help = EXPORT_HELP )
@click.option( '--fmt',
               nargs = 1,
               default = "yaml",
               help = "Can be one of the following: YAML, JSON, SQL or CSV.",
               type = click.Choice( [ 'yaml', 'json', 'sql', 'csv' ], case_sensitive = False ) )
@click.option( '--table',
               nargs = 1,
               default = None,
               help = "The table name from the database." )
@click.argument( 'filename' )
def export( fmt, filename, table ):
    if fmt == 'csv':
        if filename.endswith( fmt ):
            filename = filename.split( '.' )[ 0 ]

        for tbl in listTables():
            if table is not None and table != tbl:
                continue

            model = API.db.get_model_by_tablename( tbl )
            if model is None:
                continue

            API.app.logger.info( "Table: {}".format( tbl ) )
            records = API.db.session.query( model ).all()
            if len( records ) > 0:
                filename = "{}-{}.{}".format( filename, tbl, fmt )
                API.app.logger.info( "Output filename: {}".format( filename ) )
                with open( filename, 'w' ) as stream:
                    csvwriter = csv.writer( stream, delimiter = ';', quotechar = '"' )

                    csvwriter.writerow( records[ 0 ].toDict().keys() )
                    for record in records:
                        csvwriter.writerow( record.toDict().values() )

                API.app.logger.info( "No of records: {}".format( len( records ) ) )

            else:
                API.app.logger.warning( "Nothing to export" )

    else:
        if not filename.endswith( fmt ):
            filename += ".{}".format( fmt )

        API.app.logger.info( "Output filename: {}".format( filename ) )
        with open( filename, 'w' ) as stream:
            from sqlalchemy import Table
            # create dict per record ans save:
            blob = []
            for tbl in listTables():
                if table is not None and table != tbl:
                    continue

                model = API.db.get_model_by_tablename( tbl )
                if model is None:
                    continue

                API.app.logger.info( "Table: {}".format( tbl ) )
                records = API.db.session.query( model ).all()
                if 'sql' == fmt:
                    stream.write( "-- TABLE {}\n".format( tbl ) )
                    for record in records:
                        stream.write( "{}\n".format( record.toSql() ) )

                    API.app.logger.info( "No of records: {}".format( len( records ) ) )

                else:
                    blob.append( { 'table': tbl,
                                   'records': [ rec.toDict() for rec in records ] } )

                    API.app.logger.info( "No of records: {}".format( len( records ) ) )

            if fmt == 'yaml':
                yaml.dump( blob, stream, default_style = False, default_flow_style = False )

            elif fmt == 'json':
                json.dump( blob, stream, indent = 4 )

    return


INPORT_HELP = """Import the database from a YAML, JSON, SQL or CSV file.

    dba export [ --fmt <type> ] [ --table <table-name> ] <filename> 


<filename>: The filename with or without the extension to be used to write the database information to.
"""


@dba.command( 'inport',
              short_help = 'Inport the database from a YAML, JSON, SQL or CSV file.',
              help = INPORT_HELP )
@click.option( '--fmt',
               nargs = 1,
               default = "yaml",
               help = "Can be one of the following: YAML, JSON, SQL or CSV.",
               type = click.Choice( [ 'yaml', 'json', 'sql', 'csv' ], case_sensitive = False ) )
@click.option( '--table',
               nargs = 1,
               default = None,
               help = "The table name from the database to import from the data file." )
@click.argument( 'filename' )
def inport( fmt, filename, table ):
    if fmt in ( 'sql', 'yaml', 'json' ):
        if not filename.endswith( fmt ):
            filename += ".{}".format( fmt )

        if not os.path.isfile( filename ):
            API.app.logger.error( "Filename {} doesn't exists".format( filename ) )
            return

    if fmt == 'csv':
        if filename.endswith( fmt ):
            filename = filename.split( '.' )[ 0 ]

        if table is None and '-' in filename:
            name, table = filename.split( '-', 1 )

        else:
            name = filename

        for tbl in listTables():
            if table is not None and table != tbl:
                continue

            model = API.db.get_model_by_tablename( tbl )
            if model is None:
                continue

            filename = "{}-{}.{}".format( name, tbl, fmt )
            API.app.logger.info( "Input filename: {}".format( filename ) )
            if not os.path.isfile( filename ):
                API.app.logger.error( "Filename must be formatted as input filename {} doesn't exists".format( filename ) )
                continue

            with open( filename, 'r' ) as stream:
                csvreader = csv.reader( stream, delimiter = ';', quotechar = '"', quoting = csv.QUOTE_MINIMAL )
                it = iter( csvreader )
                header = it.__next__()
                for row in it:
                    obj = model()
                    for field, value in zip( header, row ):
                        setattr( obj, field, value )

                    API.db.session.add( obj )

                API.db.session.commit()

    else:
        with open( filename, 'r' ) as stream:
            blob = None
            if fmt == 'json':
                blob = json.load( stream )

            elif fmt == 'yaml':
                blob = yaml.load( stream )

            else: # sql
                connection = API.db.session.connection()
                for line in stream.readlines():
                    if line.startswith( '--' ):
                        continue

                    try:
                        line = line.replace( '\n', '' )
                        API.app.logger.info( line )
                        result = connection.execute( line )
                        if result.rowcount != 1:
                            raise Exception( "row not inserted" )


                    except Exception as exc:
                        API.app.logger.error( exc )

                API.db.session.commit()

            if blob:
                # Handle the yaml/json data
                for table_data in blob:
                    records = table_data[ 'records' ]
                    if len( records ) >  0:
                        model = API.db.get_model_by_tablename( table_data[ 'table' ] )
                        if model is None:
                            continue

                        for record in records:
                            obj = model()
                            for field, value in record.items():
                                setattr( obj, field, value )

                            API.db.session.add( obj )
                            API.db.session.commit()

    return


def resolve_fieldname( settings, table, field ):
    options = settings.get( 'options', {} )
    field_opr = options.get( 'fieldname', None )
    if isinstance( field, ( list, tuple ) ):
        result = []
        for fld in field:
            result.append( resolve_fieldname( settings, table, fld ) )

        field = result

    else:
        if field_opr is not None:
            field = getattr(field, field_opr)()

        prefix = settings.get('prefixes', {}).get(table, None)
        if prefix is not None and field_opr is not None:
            prefix = getattr(prefix, field_opr)()

        if prefix is not None and not field.startswith( prefix ):
            field = "{}{}".format( prefix, field )

    return field


def getReference( settings, table, field, value ):
    ref_model = API.db.get_model_by_tablename( table )
    query = API.db.session.query( ref_model )
    if isinstance( field, ( list, tuple ) ):
        for fld, val in zip( field, value ):
            fld = resolve_fieldname(settings, table, fld )
            query = query.filter( getattr( ref_model, fld ) == val )

    else:
        field = resolve_fieldname(settings, table, field)
        query = query.filter( getattr( ref_model, field ) == value )

    return query.one()


LOADER_HELP = """Load the database from a YAML or JSON file.

    dba loader [ --fmt <type> ] [ --table <table-name> ] <filename> 


<filename>: The filename with or without the extension to be used to write the database information to.
"""

@dba.command( 'loader',
              short_help = 'Load the database from a YAML or JSON file.',
              help = LOADER_HELP )
@click.option( '--fmt',
               nargs = 1,
               default = "yaml",
               help = "Can be one of the following: YAML or JSON.",
               type = click.Choice( [ 'yaml', 'json' ],
                                    case_sensitive = False ) )
@click.argument( 'filename', type = click.Path( exists = True ) )
def loader( fmt, filename ):
    if not filename.endswith( fmt ):
        filename = "{}.{}".format( filename, fmt )

    if not os.path.isfile( filename ):
        raise Exception( "File doesn't exists" )

    with open( filename,'r' ) as stream:
        data = yaml.load( stream, Loader=yaml.FullLoader)

    if '__magic__' not in data:
        raise Exception( "magic code missing, not a dba loader script." )

    if data[ '__magic__' ] != 'dba loader':
        raise Exception( "magic code invalid, not a dba loader script.")

    settings = data.get( '__settings__', {} )
    for table, values in data.items():
        if table.startswith( '__' ):
            continue

        model = API.db.get_model_by_tablename( table )
        if model is  None:
            continue

        for table_data in values:
            updateRecord( settings, model, table, table_data )

    return

def updateRecord( settings, model, table, table_data ):
    record = model()
    for field, value in table_data.items():
        if isinstance( value, ( bool, int, str, float ) ):
            field = resolve_fieldname( settings, table, field )
            API.app.logger.info( "Field: {}.{} with value {}".format( table, field, value ) )
            setattr( record, field, value )

        elif isinstance( value, ( tuple, list ) ):
            field = resolve_fieldname( settings, table, field )
            ref_record = getReference( settings, *value )
            setattr( record, field, inspect( ref_record ).identity[0] )
            API.app.logger.info( "Field: {}.{} with value {}".format(table, field, inspect( ref_record ).identity[0] ) )

        elif isinstance( value, dict ):
            field = resolve_fieldname( settings, table, field )
            ref_field = value.get( 'field', None )
            if ref_field is None:
                fields = value.get( 'fields' )
                if fields is None:
                    raise Exception( "missing field or fields" )

                ref_model = API.db.get_model_by_tablename( value.get( 'table' ) )
                if ref_model is None:
                    API.app.logger.error( "model is unknown: {}".format( value.get( 'table' ) ) )
                    continue

                ref_record = updateRecord( settings, ref_model, value.get( 'table' ), fields )

            else:
                ref_record = getReference( settings,
                                       value.get( 'table' ),
                                       value.get( 'field' ),
                                       value.get( 'value' ) )

            setattr( record, field, inspect( ref_record ).identity[0] )
            API.app.logger.info( "Field: {}.{} with value {}".format(table, field, inspect( ref_record ).identity[0] ) )

    # Need to check if the record already exists, with its unique key
    ukey = settings.get( 'unique-key', {} ).get( table, None )
    if ukey is not None:
        query = API.db.session.query( model )
        if ',' in ukey:
            ukey = ukey.replace( ' ', '' ).split( ',' )

        if isinstance( ukey, ( list, tuple ) ):
            for sukey in ukey:
                if isinstance( sukey, ( list, tuple ) ):
                    for ssukey in sukey:
                        ssukey = resolve_fieldname(settings, table, ssukey)
                        query = query.filter(getattr(model, ssukey) == getattr(record, ssukey))

                else:
                    sukey = resolve_fieldname( settings, table, sukey )
                    query = query.filter( getattr( model, sukey ) == getattr( record, sukey ) )

        else:
            ukey = resolve_fieldname( settings, table, ukey )
            query = query.filter( getattr( model, ukey ) == getattr( record, ukey ) )

        try:
            rec = query.one()
            API.app.logger.error( "Not inserting record, due to duplicate key: {}".format( ukey ) )
            return rec

        except sqlalchemy.orm.exc.NoResultFound:
            pass

    API.db.session.add( record )
    API.db.session.commit()
    return record


SAVER_HELP = """Save the database to a YAML or JSON file.

    dba saver [ --fmt <type> ] [ --settings <filename-settings.yaml> ] <filename> 


<filename>: The filename with or without the extension to be used to write the database information to.
"""


@dba.command( 'saver',
              short_help = 'Save the database toa YAML or JSON file.',
              help = SAVER_HELP )
@click.option( '--fmt',
               nargs = 1,
               default = "yaml",
               help = "Can be one of the following: YAML or JSON.",
               type = click.Choice( [ 'yaml', 'json' ],
                                    case_sensitive = False ) )
@click.option( '--settings',
               nargs = 1,
               default = 'settings-dba-loader.yaml',
               help = 'Must be a YAML file with the settings, when not present a new one shall be generated. The default is "settings-dba-loader.yaml"' )
@click.argument( 'filename', nargs = 1 )
@click.argument( 'tables', nargs = -1 )
def saver( fmt, settings, filename, tables ):
    data = { '__magic__': 'dba loader' }
    settingsfile = settings
    settings = {}
    if os.path.isfile( settingsfile ):
        with open( settingsfile, 'r' ) as stream:
            settings = yaml.load(stream, Loader=yaml.FullLoader)

    allTables = len( tables ) == 0
    if allTables:
        tables = listTables()
        tables.remove( 'alembic_version' )

    prefixes = settings.get( 'prefixes', {} )
    uniquekeys = settings.get('unique-key', {} )
    options = settings.get('options', {} )
    updatePrefixes = len( prefixes ) == 0
    updateUniqueKeys = len( uniquekeys ) == 0
    if updatePrefixes or updateUniqueKeys:
        insp = Inspector.from_engine(API.db.engine)
        # Figure out the common prefixes.
        for tbl in tables:
            if updatePrefixes:
                model = API.db.get_model_by_tablename( tbl )
                mapper = inspect( model )
                flds = [ column.key for column in mapper.attrs ]
                if flds[ 0 ].isupper():
                    options[ "fieldname" ] = "upper"

                elif flds[ 0 ].islower():
                    options[ "fieldname" ] = "lower"

                if tbl not in prefixes:
                    prefixes[ tbl ] = os.path.commonprefix( flds )

            if updateUniqueKeys:
                ukeys = []
                for u in insp.get_unique_constraints( tbl ):
                    f = u.get( 'column_names', [] )
                    if len(f) == 1:
                        ukeys.append( f[ 0 ] )

                    else:
                        ukeys.append( f )

                if len( ukeys ) > 0:
                    uniquekeys[ tbl ] = ukeys

        settings[ 'prefixes' ] = prefixes
        settings[ 'unique-key' ] = uniquekeys
        settings[ 'options' ] = options
    # Now process the tables

    for tbl in tables:
        model = API.db.get_model_by_tablename( tbl )
        tbl_data = []
        for record in API.db.session.query( model ).all():
            tbl_data.append( record.toDict() )

        if len( tbl_data ):
            data[ tbl ] = tbl_data

    if not filename.endswith( fmt ):
        filename = "{}.{}".format( filename, fmt )

    if len( settings ):
        if fmt == 'yaml':
            data[ '__settings__' ] = '!include {}'.format( settingsfile )
            if not os.path.isfile( settingsfile ):
                with open( settingsfile, 'w') as stream:
                    yaml.dump( settings, stream )

        else:
            data['__settings__'] = settings

    with open( filename, 'w' ) as stream:
        if fmt == 'yaml':
            yaml.dump( data, stream )

        elif fmt == 'json':
            json.dump( data, stream )

    return
