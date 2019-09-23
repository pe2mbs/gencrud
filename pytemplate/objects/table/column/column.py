import sys
from nltk.tokenize import word_tokenize
import pytemplate.util.utils
from pytemplate.objects.table.column.listview import TemplateListView
from pytemplate.objects.table.column.relation import TemplateRelation
from pytemplate.objects.table.column.ui import TemplateUi
from pytemplate.objects.table.column.css import TemplateCss
from pytemplate.util.exceptions import InvalidSetting

class TemplateColumn( object ):
    def __init__( self, no_columns, table_name, **cfg ):
        '''
            field:              D_ROLE_ID       INT         AUTO_NUMBER  PRIMARY KEY

        :param cfg:
        :return:
        '''
        self.__tableName    = table_name
        self.__config       = cfg
        self.__field        = ''
        self.__sqlType      = ''
        self.__length       = 0
        self.__relationShip = None
        self.__choice       = None
        self.__attrs        = []
        self.__ui           = None
        self.__leadIn       = []

        if 'field' in cfg:
            tokens = [ x for x in word_tokenize( cfg.get( 'field', '' ) ) ]
            self.__field = tokens[ 0 ]
            self.__sqlType  = tokens[ 1 ]
            if self.__sqlType not in ( 'INT', 'BIGINT', 'CHAR', 'VARCHAR',
                                       'TEXT', 'CLOB',
                                       'BOOLEAN', 'DATE', 'TIME', 'TIMESTAMP',
                                       'FLOAT', 'REAL',  'INTERVAL', 'BLOB',
                                       'DECIMAL', 'NUMERIC' ):
                raise InvalidSetting( 'field', 'column', self.__field )

            offset = 2
            if offset < len( tokens ) and tokens[ offset ] == '(':
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
                    self.__attrs.append( 'NULL' )

                elif tokens[ offset ] == 'NOT':
                    offset += 1
                    if tokens[ offset ] == 'NULL':
                        self.__attrs.append( 'NOT NULL' )

                    else:
                        raise InvalidSetting( 'field', 'attr: "NOT ' + tokens[ offset ] + '"', self.__field )

                elif tokens[ offset ] == 'DEFAULT':
                    self.__attrs.append( 'DEFAULT {0}'.format( tokens[ offset + 1 ] ) )

                elif tokens[ offset ] == 'PRIMARY':
                    self.__attrs.append( 'PRIMARY KEY' )

                elif tokens[ offset ] == 'AUTO':
                    self.__attrs.append( 'AUTO NUMBER' )

                elif tokens[ offset ] == 'FOREIGN':
                    self.__attrs.append( 'FOREIGN KEY {0}'.format( tokens[ offset + 2 ] ) )
                    offset += 1

                else:
                    raise InvalidSetting( 'field', 'attr: "' + tokens[ offset ] + '"', self.__field )

                offset += 2

            self.__css = TemplateCss( no_columns, **self.__config.get( 'css', {} ) )
            if 'ui' in cfg and type( cfg[ 'ui' ] ) is dict:
                self.__ui = TemplateUi( **cfg.get( 'ui', {} ) )

            self.__relationShip = TemplateRelation( self, **self.__config.get( 'relationship', {} ) )
            self.__listview     = TemplateListView( self, **self.__config.get( 'listview', {} ) )
        return

    @property
    def leadIn( self ):
        return self.__leadIn

    @property
    def hasAutoUpdate( self ):
        return 'autoupdate' in self.__config

    @property
    def autoUpdate( self ):
        if 'autoupdate' in self.__config:
            if pytemplate.util.utils.verbose:
                print( "AUTO UPDATE ", self.__config[ 'autoupdate' ] )
            autoValue = self.__config[ 'autoupdate' ]
            if '(' in autoValue:
                # Python callable
                if '.' not in autoValue:
                    autoValue = 'common.{}'.format(autoValue)

                module_name, _ = autoValue.rsplit('.', 1 )
                import_statement = 'import {}'.format( module_name )
                if import_statement not in self.__leadIn:
                    self.__leadIn.append( import_statement )

            else:
                # A scalar
                pass
            if pytemplate.util.utils.verbose:
                print("AUTO UPDATE ", autoValue )

            return autoValue

        return None

    @property
    def listview( self ):
        return self.__listview

    def hasResolveList( self ):
        return self.__listview.hasResolveList()

    @property
    def tableName( self ):
        return self.__tableName

    # OBSOLETE: use the listview.index
    @property
    def index( self ):
        return self.__config.get( 'index', None )

    @property
    def uniqueKey( self ):
        return self.__config.get( 'unique-key', '' )

    def hasUniqueKey( self ):
        return 'unique-key' in self.__config

    def hasForeignKey( self ):
        return any( 'FOREIGN KEY' in x for x in self.__attrs )
        #return 'FOREIGN KEY' in self.__attrs

    def hasRelationship( self ):
        return self.hasForeignKey() and 'relationship' in self.__config

    @property
    def relationship( self ):
        return self.__relationShip

    @property
    def css( self ):
        return self.__css

    @property
    def name( self ):
        return self.__field

    def hasLabel( self ):
        return self.__config.get( 'label', '' ) != ''

    @property
    def label( self ):
        return self.__config.get( 'label', '' )

    def isPrimaryKey( self ):
        return 'PRIMARY KEY' in self.__attrs

    @property
    def ui( self ):
        return self.__ui

    def minimal( self ):
        return self.__config.get( 'minimal', '0' )

    def maximal( self ):
        if self.__sqlType == 'BIGINT':
            return self.__config.get( 'maximal', str( 2 ** 63 - 1 ) )

        elif self.__sqlType == 'NUMERIC' or self.__sqlType == 'DECIMAL':
            return self.__config.get( 'maximal', str( 2 ** ( self.__length * 8 ) - 1 ) )

        return self.__config.get( 'maximal', str( 2 ** 31 - 1 ) )

    @property
    def pType( self ):
        '''
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
        '''
        if self.__sqlType == 'CHAR' or self.__sqlType.startswith( 'VARCHAR' ):
            return 'db.String'

        elif self.__sqlType == 'INT':
            return 'db.Integer'

        elif self.__sqlType == 'BIGINT':
            return 'db.BigInteger'

        elif self.__sqlType == 'BOOLEAN':
            return 'db.Boolean'

        elif self.__sqlType == 'TIMESTAMP':
            return 'db.DateTime'

        elif self.__sqlType == 'DATE':
            return 'db.Date'

        elif self.__sqlType == 'FLOAT' or self.__sqlType == 'REAL':
            return 'db.Float'

        elif self.__sqlType == 'INTERVAL':
            return 'db.Interval'

        elif self.__sqlType == 'BLOB':
            return 'db.LargeBinary'

        elif self.__sqlType == 'NUMERIC' or self.__sqlType == 'DECIMAL':
            return 'db.Numeric'

        elif self.__sqlType == 'CLOB' or self.__sqlType == 'TEXT':
            return 'db.Text'

        elif self.__sqlType == 'TIME':
            return 'db.Time'

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
            return 'Date'

        elif self.__sqlType == 'TIMESTAMP':
            return 'Date'

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
            return 'Date'

        raise Exception( 'Invalid SQL type: {0}'.format( self.__sqlType ) )

    def isNumericField( self ):
        return self.__sqlType in ( "INT", "BIGINT", "FLOAT", "REAL", "INTERVAL", "NUMERIC", "DECIMAL" )

    def isBooleanField( self ):
        return self.__sqlType in ( "BOOLEAN", "INT" )

    def sqlAlchemyDef( self ):
        '''

            https://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Column

        :return:
        '''
        result = ''
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
                result += ', db.ForeignKey( "{0}" )'.format( attr.split( ' ' )[ 2 ] )

            elif attr.startswith( 'DEFAULT' ):
                value = attr.split( ' ' )[ 1 ]
                if self.isNumericField():
                    result += ', default = {0}'.format( value )

                elif self.isBooleanField():
                    if value.lower() == ( "true", "1", "yes" ):
                        result += ', default = True'

                    else:
                        result += ', default = False'

                else:
                    result += ', default = "{0}"'.format( value )

            else:
                print( 'Extra unknown attributes found: {0}'.format( attr ),
                       file = sys.stderr )

            defValue = self.DefaultValue()
            if defValue is not None:
                defValue, module_name, function = defValue
                if module_name is None:
                    # A scalar
                    result += ', default = {q}{val}{q}'.format( val = defValue, q = '"' if type( defValue ) is str else "" )

                else:
                    # Python callable
                    # Need to inject the module
                    import_statement = 'import {}'.format( module_name )
                    if import_statement not in self.__leadIn:
                        self.__leadIn.append( import_statement )

                    result += ', default = {mod}.{call}'.format( mod = module_name, call = function )

        result += ' )'
        return result

    def DefaultValue( self ):
        if 'default' in self.__config:
            module_name = function = None
            defValue = self.__config[ 'default' ]
            if '(' in defValue:
                # Python callable
                if '.' in defValue:
                    module_name, function = defValue.rsplit('.', 1 )

                else:
                    module_name = 'common'
                    function    = defValue

            else:
                # A scalar
                pass

            return ( defValue, module_name, function )

        return None

    @property
    def validators( self ):
        result = '[ '
        if 'NOT NULL' in self.__attrs:
            result += 'Validators.required, '

        if self.__length > 0:
            result += 'Validators.maxLength( {0} ), '.format( self.__length )

        result += ' ]'
        return result

    def angularUiInput( self ):
        return self.__ui.buildInputElement( self.__tableName,
                                            self.__field,
                                            self.__config.get( 'label', '' ),
                                            [ 'readonly' if self.isPrimaryKey() else '' ] )


