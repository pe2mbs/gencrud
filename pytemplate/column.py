import sys
from nltk.tokenize import word_tokenize


class TemplateColumn( object ):
    def __init__( self, **cfg ):
        '''
            field:              D_ROLE_ID       INT         AUTO_NUMBER  PRIMARY KEY

        :param cfg:
        :return:
        '''
        self.__config       = cfg
        self.__field        = ''
        self.__sqlType      = ''
        self.__length       = 0
        self.__attrs        = []
        self.__interface    = None
        self.__import       = None
        if 'field' in cfg:
            tokens = [ x for x in word_tokenize( cfg[ 'field' ] ) ]
            #print( 'TOKENS:', tokens )
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
        '''

            https://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Column

        :return:
        '''
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
                    print( 'Extra unknown attributes found: {0}'.format( attr ),
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
