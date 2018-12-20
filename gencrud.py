#!/usr/bin/python3
#
#   Python backend and Angular frontend code generation by Template
#   Copyright (C) 2018 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>
#
#   This library is free software; you can redistribute it and/or
#   modify it under the terms of the GNU Library General Public
#   License as published by the Free Software Foundation; either
#   version 2 of the License, or (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#   Library General Public License for more details.
#
#   You should have received a copy of the GNU Library General Public
#   License along with this library; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
import os
import sys
import yaml
import json
import getopt
from nltk.tokenize import word_tokenize
from mako.template import Template
import shutil

sslVerify = True
verbose = False

C_FILEMODE_UPDATE = 'r+'
C_FILEMODE_WRITE  = 'w'
C_FILEMODE_READ   = 'r'


class PositionInterface( object ):
    def __init__( self ):
        self.__start = 0
        self.__end = 0
        return

    @property
    def start( self ):
        return self.__start

    @start.setter
    def start( self, value ):
        self.__start = value
        return

    @property
    def end( self ):
        return self.__end

    @end.setter
    def end( self, value ):
        self.__end = value
        return

    def range( self ):
        return range( self.__start, self.__end + 1 )

    def dump( self, caption ):
        print( "{0}\n- start: {1} end {2}".format( caption, self.__start, self.__end ) )


class TemplateSource( object ):
    def __init__( self, type, **cfg ):
        self.__template = cfg[ 'templates' ][ type ]
        self.__source   = cfg[ 'source' ][ type ]
        return

    @property
    def source( self ):
        return os.path.abspath( os.path.normpath( self.__source ) )

    @property
    def template( self ):
        return os.path.abspath( os.path.normpath( self.__template ) )


class TemplateColumn( object ):
    def __init__( self, **cfg ):
        """
            field:              D_ROLE_ID       INT         AUTO_NUMBER  PRIMARY KEY

        :param cfg:
        :return:
        """
        self.__config       = cfg
        self.__field        = ''
        self.__sqlType      = ''
        self.__length       = 0
        self.__attrs        = []
        self.__interface    = None
        self.__import       = None
        if 'field' in cfg:
            tokens = [ x for x in word_tokenize( cfg[ 'field' ] ) ]
            #print( "TOKENS:", tokens )
            self.__field = tokens[ 0 ]
            self.__sqlType  = tokens[ 1 ]
            offset = 2
            if self.__sqlType == 'RECORD':
                # relationship
                # RELATION <class>
                self.__interface = tokens[ offset: ]
                self._checkForImports( cfg )
                return

            elif tokens[ offset ] == '(':
                offset += 1
                self.__length   = int( tokens[ offset ] )
                offset += 2

            # attributes
            # NOT NULL
            # DEFAULT <value>
            # PRIMARY KEY
            # AUTO NUMBER
            # FOREIGN KEY <reference>
            while offset < len( tokens ):
                if tokens[ offset ] == 'NULL':
                    self.__attrs.append( 'NOT NULL' )

                elif tokens[ offset ] == 'DEFAULT':
                    self.__attrs.append( 'DEFAULT {0}'.format( tokens[ offset + 1 ] ) )

                elif tokens[ offset ] == 'PRIMARY':
                    self.__attrs.append( 'PRIMARY KEY' )

                elif tokens[ offset ] == 'AUTO':
                    self.__attrs.append( 'AUTO NUMBER' )

                elif tokens[ offset ] == 'FOREIGN':
                    self.__attrs.append( 'FOREIGN KEY {0}'.format( tokens[ offset + 2 ] ) )
                    offset += 1

                offset += 2

        self._checkForImports( cfg )
        return

    def _checkForImports( self, cfg ):
        if 'inport' in cfg:
            self.__import = []
            for importDef in cfg[ 'inport' ].split( ',' ):
                self.__import.append( [ x for x in word_tokenize( importDef ) ] )

        return

    @property
    def inports( self ):
        if self.__import is None:
            return []

        return self.__import

    @property
    def label( self ):
        return self.__config[ 'label' ]

    @property
    def index( self ):
        if 'index' in self.__config:
            return self.__config[ 'index' ]

        return None

    @property
    def uiObject( self ):
        return self.__config[ 'ui' ]

    @property
    def name( self ):
        return self.__field

    @property
    def name( self ):
        return self.__field

    def isPrimaryKey( self ):
        return 'PRIMARY KEY' in self.__attrs

    @property
    def pType( self ):
        """
            BigInteger          = BIGINT
            Boolean             = BOOLEAN or SMALLINT
            Date                = DATE
            DateTime            = TIMESTAMP
            Enum
            Float               = FLOAT or REAL.
            Integer             = INT
            Interval            = INTERVAL
            LargeBinary         = BLOB or BYTEA
            MatchType
            Numeric             = NUMERIC or DECIMAL.
            PickleType
            SchemaType
            SmallInteger
            String              = VARCHAR
            Text                = CLOB or TEXT.
            Time                = TIME
        :return:
        """
        if self.__sqlType == 'CHAR' or self.__sqlType.startswith( 'VARCHAR' ):
            return 'String'
        elif self.__sqlType == 'INT':
            return 'Integer'
        elif self.__sqlType == 'BIGINT':
            return 'BigInteger'
        elif self.__sqlType == 'BOOLEAN':
            return 'Boolean'
        elif self.__sqlType == 'DATE':
            return 'Date'
        elif self.__sqlType == 'FLOAT' or self.__sqlType == 'REAL':
            return 'Float'
        elif self.__sqlType == 'INTERVAL':
            return 'Interval'
        elif self.__sqlType == 'BLOB':
            return 'LargeBinary'
        elif self.__sqlType == 'NUMERIC' or self.__sqlType == 'DECIMAL':
            return 'Numeric'
        elif self.__sqlType == 'CLOB' or self.__sqlType == 'TEXT':
            return 'Text'
        elif self.__sqlType == 'TIME':
            return 'Time'

        raise Exception( 'Invalid SQL type: {0}'.format( self.__sqlType ) )

    @property
    def tsType( self ):
        if self.__sqlType == 'CHAR' or self.__sqlType.startswith( 'VARCHAR' ):
            return 'string'

        elif self.__sqlType == 'INT':
            return 'number'

        elif self.__sqlType == 'BIGINT':
            return 'number'

        elif self.__sqlType == 'BOOLEAN':
            return 'boolean'

        elif self.__sqlType == 'DATE':
            return 'string'

        elif self.__sqlType == 'FLOAT' or self.__sqlType == 'REAL':
            return 'number'

        elif self.__sqlType == 'INTERVAL':
            return 'Interval'

        elif self.__sqlType == 'BLOB':
            return 'LargeBinary'

        elif self.__sqlType == 'NUMERIC' or self.__sqlType == 'DECIMAL':
            return 'string'

        elif self.__sqlType == 'CLOB' or self.__sqlType == 'TEXT':
            return 'string'

        elif self.__sqlType == 'TIME':
            return 'string'

        elif self.__sqlType == 'RECORD':
            return '{}Record'.format( self.__interface[ 1 ] )

        raise Exception( 'Invalid SQL type: {0}'.format( self.__sqlType ) )

    def sqlAlchemyDef( self ):
        """

            https://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Column

        :return:
        """
        result = ''
        if self.__interface is None or self.__interface == '':
            result = 'db.Column( {0}'.format( self.pType )
            if self.__length != 0:
                result += '( {0} )'.format( self.__length )

            for attr in self.__attrs:
                if 'AUTO NUMBER' in attr:
                    result += ', autoincrement = True'

                elif 'PRIMARY KEY' in attr:
                    result += ', primary_key = True'

                elif 'NOT NULL' in attr:
                    result += ', nullable = False'

                elif attr.startswith( 'FOREIGN KEY' ):
                    result += ', ForeignKey( "{0}" )'.format( attr.split( ' ' )[ 2 ] )

                elif attr.startswith( 'DEFAULT' ):
                    result += ', default = "{0}"'.format( attr.split( ' ' )[ 1 ] )

                else:
                    print( "Extra unknown attributes found: {0}".format( attr ),
                           file = sys.stderr )
        else:

            result += 'relationship( "{0}"'.format( self.__interface[ 1 ] )

        result += ' )'
        return result

    @property
    def validators( self ):
        result = '[ '
        if 'NOT NULL' in self.__attrs:
            result += 'Validators.required, '

        if self.__length > 0:
            result += 'Validators.maxLength( {0} ), '.format( self.__length )

        result += ' ]'
        return result


class TemplateObject( object ):
    def __init__( self, **cfg ):
        self.__config       = cfg
        self.__columns      = []
        self.__primaryKey   = ''
        for col in cfg[ 'table' ][ 'columns' ]:
            #print( col )
            column = TemplateColumn( **col )
            self.__columns.append( column )
            if column.isPrimaryKey():
                self.__primaryKey = column.name

        return

    @property
    def application( self ):
        return self.__config[ 'application' ]

    @property
    def name( self ):
        return self.__config[ 'name' ]

    @property
    def cls( self ):
        return self.__config[ 'class' ]

    @property
    def uri( self ):
        return self.__config[ 'uri' ][ 'backend' ]

    @property
    def frontendUri( self ):
        return self.__config[ 'uri' ][ 'frontend' ]

    @property
    def menuCaption( self ):
        return self.__config[ 'menu' ][ 'caption' ]

    @property
    def menuIndex( self ):
        return self.__config[ 'menu' ][ 'backend' ]

    @property
    def tableName( self ):
        return self.__config[ 'table' ][ 'name' ]

    @property
    def columns( self ):
        return self.__columns

    @property
    def primaryKey( self ):
        return self.__primaryKey

    @property
    def imports( self ):
        result = []
        for col in self.__columns:
            result.extend( col.inports )

        return result


class TemplateConfiguration( object ):
    def __init__( self, **cfg ):
        self.__config   = cfg
        self.__python   = TemplateSource( 'python', **self.__config )
        self.__angular  = TemplateSource( 'angular', **self.__config )
        self.__objects  = []
        for obj in cfg[ 'objects' ]:
            #print( obj )
            self.__objects.append( TemplateObject( **obj ) )

        return

    @property
    def python( self ):
        return self.__python

    @property
    def angular( self ):
        return self.__angular

    @property
    def objects( self ):
        return self.__objects

    def __iter__( self ):
        return iter( self.__objects )


def sourceName( templateName ):
    return os.path.splitext( os.path.basename( templateName ) )[ 0 ]


def makePythonModules( root_path, *args ):
    def write__init__py():
        with open( os.path.join( root_path, '__init__.py' ), 'w+' ) as stream:
            print( '', file = stream )

        return

    if len( args ) > 0:
        root_path = os.path.join( root_path, args[ 0 ] )
        if not os.path.isdir( root_path ):
            os.mkdir( root_path )

        makePythonModules( root_path, *args[ 1: ] )

    if len( args ) > 0:
        if not os.path.isfile( os.path.join( root_path, '__init__.py' ) ):
            write__init__py()

    return


def makeAngularModule( root_path, *args ):
    if len( args ) > 0:
        modulePath = os.path.join( root_path, args[ 0 ] )
        if not os.path.isdir( modulePath ):
            os.mkdir( modulePath )

        makeAngularModule( modulePath, *args[ 1: ] )

    return


def generatePython( templates, config ):
    modules = []
    global verbose
    for cfg in config:
        for templ in templates:
            if verbose:
                print( "template    : {0}".format( templ ) )
                print( "application : {0}".format( cfg.application ) )
                print( "name        : {0}".format( cfg.name ) )
                print( "class       : {0}".format( cfg.cls ) )
                print( "table       : {0}".format( cfg.tableName ) )
                for col in cfg.columns:
                    print( "- {0:<20}  {1}".format( col.name, col.sqlAlchemyDef() ) )
                    for imp in col.inports:
                        print( "  {0}  {1}".format( *imp ) )

                print( "primary key : {0}".format( cfg.primaryKey ) )
                print( "uri         : {0}".format( cfg.uri ) )

            if not os.path.isdir( config.python.source ):
                os.makedirs( config.python.source )

            makePythonModules( config.python.source, cfg.application, cfg.name )
            modulePath = os.path.join( config.python.source,
                                   cfg.application,
                                   cfg.name )

            with open( os.path.join( modulePath, sourceName( templ ) ), C_FILEMODE_WRITE ) as stream:
                for line in Template( filename=os.path.abspath( templ ) ).render( obj = cfg ).split('\n'):
                    stream.write( line )

                # Open the __init__.py
                with open( os.path.join( modulePath, '__init__.py' ), C_FILEMODE_UPDATE ) as stream:
                    stream.seek( 0, os.SEEK_END )
                    moduleName, _ = os.path.splitext( sourceName( templ ) )
                    importStr = 'from {0}.{1}.{2} import *'.format( cfg.application, cfg.name, moduleName )
                    print( "Try to add '{0}'".format( importStr ), file = sys.stderr )
                    try:
                        lines = stream.readlines()

                    except:
                        print( "Error reading the file", file = sys.stdout )
                        lines = ""

                    if verbose:
                        print( lines, file = sys.stdout )

                    if not importStr + '\n' in lines:
                        print( importStr, file = stream )

                modules.append( ( cfg.application, cfg.name ) )

            if verbose:
                print( "" )

    for applic, module in modules:
        with open( os.path.join( config.python.source,
                                 applic, '__init__.py' ), C_FILEMODE_UPDATE ) as stream:
            importStr = 'from {0}.{1} import *'.format( applic, module )
            print( "Try to add '{0}'".format( importStr ), file = sys.stderr )
            try:
                lines = stream.readlines()

            except:
                if verbose:
                    print( "Error reading the file", file = sys.stdout )

                lines = ""

            if verbose:
                print( lines, file = sys.stdout )

            if not importStr + '\n' in lines:
                print( importStr, file = stream )

    return

def backupFile( file_name ):
    idx = 1
    while os.path.isfile( file_name + '.~{0}'.format( idx ) ):
        idx += 1

    shutil.copyfile( file_name, file_name + '.~{0}'.format( idx ) )
    return


def updateAngularProject( config, app_module ):
    print( config.angular.source )
    # File to edit 'app.module.ts'
    # inject the following;
    #   inport
    #   declarations:       search for 'declarations: ['
    #   imports:            search for 'imports: ['
    #   providers:          search for 'providers: ['
    #   entryComponents:    search for 'entryComponents: ['
    with open( os.path.join( config.angular.source, 'app.module.json' ), 'w' ) as stream:
        json.dump( app_module, stream, indent = 4 )

    with open( os.path.join( config.angular.source, 'app.module.ts' ), 'r' ) as stream:
        lines = stream.readlines()

    backupFile( os.path.join( config.angular.source, 'app.module.ts' ) )
    stage           = 0
    importPos       = PositionInterface()
    declModulePos   = PositionInterface()
    impModulePos    = PositionInterface()
    entryModulePos  = PositionInterface()
    provModulePos   = PositionInterface()
    for lineNo, lineText in enumerate( lines ):
        if stage == 0:
            if lineText.startswith( 'import' ):
                importPos.end = lineNo

            elif lineText.startswith( '@NgModule' ):
                stage += 1

        elif stage == 1:
            if 'declarations: [' in lineText:
                declModulePos.start = lineNo

            if '],' in lineText:
                declModulePos.end = lineNo
                stage += 1

        elif stage == 2:
            if 'imports: [' in lineText:
                impModulePos.start = lineNo

            if '],' in lineText:
                impModulePos.end = lineNo
                stage += 1

        elif stage == 3:
            if 'entryComponents: [' in lineText:
                entryModulePos.start = lineNo

            if '],' in lineText:
                entryModulePos.end = lineNo
                stage += 1

        elif stage == 4:
            if 'providers: [' in lineText:
                provModulePos.start = lineNo

            if '],' in lineText:
                provModulePos.end = lineNo
                stage += 1

    if verbose:
        importPos.dump( "importPos" )
        declModulePos.dump( "declModulePos" )
        impModulePos.dump( "impModulePos" )
        entryModulePos.dump( "entryModulePos" )
        provModulePos.dump( "provModulePos" )

    for line in app_module[ 'providers' ]:
        found = False
        for idx in provModulePos.range():
            if line in lines[ idx ]:
                found = True

        if not found:
            if verbose:
                print( 'inject providers [{0}] @ {1}'.format( line, provModulePos.end + 1 ) )

            lines.insert( provModulePos.end, '    {0}\n'.format( line ) )
            provModulePos.end += 1

    for line in app_module[ 'entryComponents' ]:
        found = False
        for idx in entryModulePos.range():
            if line in lines[ idx ]:
                found = True

        if not found:
            if verbose:
                print( 'inject entryComponents [{0}] @ {1}'.format( line, entryModulePos.end + 1 ) )

            lines.insert( entryModulePos.end, '    {0}\n'.format( line ) )
            entryModulePos.end += 1

    for line in app_module[ 'imports' ]:
        found = False
        for idx in impModulePos.range():
            if line in lines[ idx ]:
                found = True

        if not found:
            if verbose:
                print( 'inject imports [{0}] @ {1}'.format( line, impModulePos.end + 1 ) )

            lines.insert( impModulePos.end, '    {0}\n'.format( line ) )
            impModulePos.end += 1

    for line in app_module[ 'declarations' ]:
        found = False
        for idx in declModulePos.range():
            if line in lines[ idx ]:
                found = True

        if not found:
            if verbose:
                print( 'inject declarations [{0}] @ {1}'.format( line, declModulePos.end + 1 ) )

            lines.insert( declModulePos.end, '    {0}\n'.format( line ) )
            declModulePos.end += 1

    for line in app_module[ 'files' ]:
        found = False
        for idx in importPos.range():
            if line in lines[ idx ]:
                found = True

        if not found:
            if verbose:
                print( 'inject files [{0}] @ {1}'.format( line, importPos.end + 1 ) )

            lines.insert( importPos.end + 1, line + '\n' )
            importPos.end += 1


    with open( os.path.join( config.angular.source, 'app.module.ts' ), 'w' ) as stream:
        for line in lines:
            stream.write( line )
            if verbose:
                print( line, end = '' )

    os.remove( os.path.join( config.angular.source, 'app.module.json' ) )
    return


def joinJson( json1, json2 ):
    result = {}
    for key, value in json2.items():
        if key not in result:
            result[ key ] = value

    for key, value in json1.items():
        if type( value ) in ( list, tuple ):
            for item in value:
                if item not in result[ key ]:
                    result[ key ].append( item )

        elif type( value ) is dict:
            result[ key ] = joinJson( result[ key ], value )

        else:
            result[ key ] = value

    return result


def generateAngular( templates, config ):
    modules = []
    if not os.path.isdir( config.angular.source ):
        os.makedirs( config.angular.source )

    for cfg in config:
        modules.append( [ cfg.application, cfg.name ] )
        makeAngularModule( config.angular.source, cfg.application, cfg.name )
        for templ in templates:
            if verbose:
                print( "template    : {0}".format( templ ) )
                print( "application : {0}".format( cfg.application ) )
                print( "name        : {0}".format( cfg.name ) )
                print( "class       : {0}".format( cfg.cls ) )
                print( "table       : {0}".format( cfg.tableName ) )
                for col in cfg.columns:
                    print( "- {0:<20}  {1}".format( col.name, col.sqlAlchemyDef() ) )
                    for imp in col.inports:
                        print( "  {0}  {1}".format( *imp ) )

                print( "primary key : {0}".format( cfg.primaryKey ) )
                print( "uri         : {0}".format( cfg.uri ) )

            with open( os.path.join( config.angular.source,
                                     cfg.application,
                                     cfg.name, sourceName( templ ) ),
                       C_FILEMODE_WRITE ) as stream:
                for line in Template( filename=os.path.abspath( templ ) ).render( obj = cfg ).split('\n'):
                    stream.write( line )
                    if sys.platform.startswith( 'linux' ):
                        stream.write( '\n' )

            if verbose:
                print( "" )

    appModule = None
    for app, mod in modules:
        app_module_json_file = os.path.join( config.angular.source,
                                           app, mod, 'app.module.json' )
        with open( app_module_json_file, 'r' ) as stream:
            data = json.load( stream )
            if appModule is None:
                appModule = data

            else:
                appModule = joinJson( appModule, data )

        os.remove( app_module_json_file )

    updateAngularProject( config, appModule )
    return


def verifyLoadProject( root, configFile ):
    result = None
    if os.path.isdir( root.source ) and os.path.isfile( os.path.join( root.source, configFile ) ):
        with open( os.path.join( root.source, configFile ), C_FILEMODE_READ ) as stream:
            result = json.load( stream )

        return result

    return result


def usage():
    return


def main():
    try:
        opts, args = getopt.getopt( sys.argv[1:], "hi:s:v", [ "help", "input=", 'sslverify=' ] )

    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit( 2 )

    inputFile   = None
    global verbose
    for o, a in opts:
        if o == "-v":
            verbose = True

        elif o in ("-h", "--help"):
            usage()
            sys.exit()

        elif o in ("-i", "--input"):
            inputFile = a

        elif o.lower() in ( '-s', '--sslverify' ):
            global sslVerify
            sslVerify   = a.lower() == 'true'

        else:
            assert False, "unhandled option"

    try:
        word_tokenize( "It's." )

    except:
        from nltk import download
        if not sslVerify:
            from ssl import _create_unverified_context
            from six.moves.urllib.request import install_opener, HTTPSHandler, build_opener

            ctx = _create_unverified_context()
            opener = build_opener( HTTPSHandler( context = ctx ) )
            install_opener( opener )

        download( 'punkt' )

    with open( inputFile, 'r' ) as stream:
        config = TemplateConfiguration( **yaml.load( stream ) )

    data = verifyLoadProject( config.angular, 'angular.json' )
    if data is not None:
        # Check if we have a valid Angular environment
        if 'defaultProject' in data and 'projects' in data:
            if data[ 'defaultProject' ] not in data[ 'projects' ]:
                print( 'Error: Angular environment not found' )
            else:
                proj = data[ 'projects' ][ data[ 'defaultProject' ] ]

        else:
            print( 'Error: Angular environment not found' )
            return

    else:
        print( 'Error: Angular environment not found' )
        return

    data = verifyLoadProject( config.python, 'config.json' )
    if data is not None:
        # Check if we have a valid Python-Flask environment
        if not ( 'COMMON' in data and 'API_MODULE' in data[ 'COMMON' ] ):
            print( 'Error: Python Flask environment not found' )
            return

        if data[ 'COMMON' ][ 'API_MODULE' ] != config.objects[ 0 ].application:
            print( 'Error: Not correct Python Flask environment not found' )
            return

    else:
        print( 'Error: Python Flask environment not found' )
        return

    generatePython( [ os.path.abspath( os.path.join( config.python.template, t ) )
                                   for t in os.listdir( config.python.template ) ],
                    config )

    generateAngular( [ os.path.abspath( os.path.join( config.angular.template, t ) )
                                    for t in os.listdir( config.angular.template ) ],
                     config )

    return


if __name__ == '__main__':
    main()