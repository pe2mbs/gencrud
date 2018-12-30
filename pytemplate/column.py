import sys
from nltk.tokenize import word_tokenize
from pytemplate.css import TemplateCss

class TemplateChoice( object ):
    # TODO: implement the choice/combobox
    def __init__( self, **cfg ):
        self.__cfg = cfg
        return

    @property
    def service( self ):
        return self.__cfg.get( 'service', '' )

    @property
    def cls( self ):
        return self.__cfg.get( 'class', '' )

    @property
    def function( self ):
        return self.__cfg.get( 'function', '' )

    @property
    def value( self ):
        return self.__cfg.get( 'value', '' )

    @property
    def label( self ):
        return self.__cfg.get( 'label', '' )




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
        self.__choice       = None
        self.__attrs        = []
        self.__interface    = None
        if 'field' in cfg:
            tokens = [ x for x in word_tokenize( cfg.get( 'field', '' ) ) ]
            self.__field = tokens[ 0 ]
            self.__sqlType  = tokens[ 1 ]
            offset = 2
            if self.__sqlType == 'RECORD':
                # relationship
                # RELATION <class>
                if tokens[ offset ] == 'RELATION':
                    self.__interface = tokens[ offset + 1 ]

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

            self.__css = TemplateCss( no_columns, **self.__config.get( 'css', {} ) )
            if 'choice' in cfg:
                self.__choice = TemplateChoice( **cfg.get( 'list', {} ) )

        return

    @property
    def tableName( self ):
        return self.__tableName

    @property
    def label( self ):
        return self.__config.get( 'label', '' )

    @property
    def index( self ):
        return self.__config.get( 'index', None )

    @property
    def css( self ):
        return self.__css

    @property
    def uiObject( self ):
        return self.__config.get( 'ui', 'textbox' )

    @property
    def name( self ):
        return self.__field

    def isPrimaryKey( self ):
        return 'PRIMARY KEY' in self.__attrs

    def isTextbox( self ):
        return self.uiObject.lower() == 'textbox'

    def isTextArea( self ):
        return self.uiObject.lower() == 'textarea'

    def isPassword( self ):
        return self.uiObject.lower() == 'password'

    def isChoice( self ):
        return self.uiObject.lower() == 'choice'

    def hasLabel( self ):
        return self.__config.get( 'label', '' ) != ''

    @property
    def choice( self ):
        return self.__choice

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

        elif self.__sqlType == 'RECORD':
            return ''

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
            if self.__interface:
                return '{}Record'.format( self.__interface )

            else:
                return 'var'

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
                    result += ', db.ForeignKey( "{0}" )'.format( attr.split( ' ' )[ 2 ] )

                elif attr.startswith( 'DEFAULT' ):
                    result += ', default = "{0}"'.format( attr.split( ' ' )[ 1 ] )

                else:
                    print( 'Extra unknown attributes found: {0}'.format( attr ),
                           file = sys.stderr )
        else:
            result += 'db.relationship( "{0}", backref = "{1}", lazy = True'.\
                        format( self.__interface, self.__tableName )

        result += ' )'
        return result

    @property
    def nestedCls( self ):
        return self.__interface

    @property
    def validators( self ):
        result = '[ '
        if 'NOT NULL' in self.__attrs:
            result += 'Validators.required, '

        if self.__length > 0:
            result += 'Validators.maxLength( {0} ), '.format( self.__length )

        result += ' ]'
        return result
