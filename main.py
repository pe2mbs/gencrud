import os
import sys
import yaml
import getopt
from nltk.tokenize import word_tokenize
from mako.template import Template

try:
    word_tokenize( "It's." )
except:
    import nltk
    nltk.download( 'punkt' )

verbose = False


class TemplateSource( object ):
    def __init__( self, type, **cfg ):
        self.__template = cfg[ 'templates' ][ type ]
        self.__source   = cfg[ 'source' ][ type ]
        return

    @property
    def source( self ):
        return self.__source

    @property
    def template( self ):
        return self.__template


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

            result += 'relationship( "{0}"'.format( self.__interface[0] )
            for rest in self.__interface[ 1: ]:
                result += rest

        result += ')'
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



def usage():
    return


def sourceName( templateName ):
    return os.path.splitext( os.path.basename( templateName ) )[ 0 ]


def makePythonModules( root_path, *args ):
    def write__init__py():
        with open( os.path.join( root_path, '__init__.py' ), 'w' ) as stream:
            print( '', file = stream )

    if len( args ) > 0:
        modulePath = os.path.join( root_path, args[ 0 ] )
        if not os.path.isdir( modulePath ):
            os.mkdir( modulePath )

        makePythonModules( modulePath, *args[ 1: ] )

        if not os.path.isfile( os.path.join( root_path, '__init__.py' ) ):
            write__init__py()

    else:
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

            makePythonModules( config.python.source, cfg.application, cfg.name )
            with open( os.path.join( config.python.source,
                                     cfg.application,
                                     cfg.name, sourceName( templ ) ), 'w' ) as stream:

                print( Template( filename=os.path.abspath( templ ) ).
                       render( obj = cfg ), file = stream )

            if verbose:
                print( "" )

    return


def generateAngular( templates, config ):
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

            makeAngularModule( config.angular.source, cfg.application,
                                            cfg.name )
            with open( os.path.join( config.angular.source,
                                     cfg.application,
                                     cfg.name, sourceName( templ ) ),
                       'w' ) as stream:
                print( Template( filename=os.path.abspath( templ ) ).
                       render( obj = cfg ), file = stream )

            if verbose:
                print( "" )

    return


def main():
    try:
        opts, args = getopt.getopt( sys.argv[1:], "hi:v", ["help", "input="] )

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

        else:
            assert False, "unhandled option"


    with open( inputFile, 'r' ) as stream:
        config = TemplateConfiguration( **yaml.load( stream ) )

    generatePython( [ os.path.abspath( os.path.join( config.python.template, t ) )
                                   for t in os.listdir( config.python.template ) ],
                    config )

    generateAngular( [ os.path.abspath( os.path.join( config.angular.template, t ) )
                                    for t in os.listdir( config.angular.template ) ],
                     config )

    return


if __name__ == '__main__':
    main()