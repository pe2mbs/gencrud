#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2020 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#   Library General Public License for more details.
#
#   You should have received a copy of the GNU Library General Public
#   License GPL-2.0-only along with this library; if not, write to the
#   Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301 USA
#
import logging
from nltk.tokenize import word_tokenize
from gencrud.config.listview import TemplateListView
from gencrud.config.relation import TemplateRelation
from gencrud.config.testdata import TemplateTestData
from gencrud.config.ui import TemplateUi
from gencrud.config.tab import TemplateTab
from gencrud.config.base import TemplateBase
from gencrud.util.exceptions import InvalidSetting
from gencrud.constants import *
from gencrud.util.validators import Validator, ValidatorType
import gencrud.util.utils as root
from gencrud.util.exceptions import MissingAttribute
logger = logging.getLogger()


class TemplateColumn( TemplateBase ):
    TS_TYPES_FROM_SQL = { 'CHAR': 'string',
                          'VARCHAR': 'string',
                          'INT': 'number',
                          'BIGINT': 'number',
                          'FLOAT': 'number',
                          'REAL': 'number',
                          'BOOLEAN': 'boolean',
                          'TIMESTAMP': 'Date',
                          'DATETIME': 'Date',
                          'DATE': 'Date',
                          'TIME': 'Date',
                          'INTERVAL': 'Interval',
                          'BLOB': 'string',
                          'NUMERIC': 'string',
                          'DECIMAL': 'string',
                          'CLOB': 'string',
                          'TEXT': 'string' }

    PY_TYPES_FROM_SQL = { 'CHAR': 'API.db.String',
                          'VARCHAR': 'API.db.String',
                          'INT': 'API.db.Integer',
                          'BIGINT': 'API.db.BigInteger',
                          'BOOLEAN': 'API.db.Boolean',
                          'BOOL': 'API.db.Boolean',
                          'TIMESTAMP': 'API.db.DateTime',
                          'DATETIME': 'API.db.DateTime',
                          'DATE': 'API.db.Date',
                          'FLOAT': 'API.db.Float',
                          'REAL': 'API.db.Float',
                          'INTERVAL': 'API.db.Interval',
                          'BLOB': 'API.db.LargeBinary',
                          'NUMERIC': 'API.db.Numeric',
                          'DECIMAL': 'API.db.Numeric',
                          'CLOB': 'API.db.LONGTEXT',
                          'TEXT': 'API.db.LONGTEXT',
                          'TIME': 'API.db.Time' }

    NATIVE_PY_TYPES_FROM_SQL = { 'CHAR': 'str',
                          'VARCHAR': 'str',
                          'INT': 'int',
                          'BIGINT': 'int',
                          'BOOLEAN': 'bool',
                          'BOOL': 'bool',
                          'TIMESTAMP': 'str',
                          'DATETIME': 'str',
                          'DATE': 'str',
                          'FLOAT': 'float',
                          'REAL': 'float',
                          'INTERVAL': 'tuple',
                          'BLOB': 'bytes',
                          'NUMERIC': 'float',
                          'DECIMAL': 'int',
                          'CLOB': 'str',
                          'TEXT': 'str',
                          'TIME': 'str' }

    SCHEMA_TYPES_FROM_SQL = { 'CHAR': 'String',
                          'VARCHAR': 'String',
                          'INT': 'Integer',
                          'BIGINT': 'Integer',
                          'BOOLEAN': 'Boolean',
                          'BOOL': 'Boolean',
                          'TIMESTAMP': 'DateTime',
                          'DATETIME': 'DateTime',
                          'DATE': 'Date',
                          'FLOAT': 'Float',
                          'REAL': 'Float',
                          'INTERVAL': 'Integer',
                          'BLOB': 'String',
                          'NUMERIC': 'Decimal',
                          'DECIMAL': 'Decimal',
                          'CLOB': 'String',
                          'TEXT': 'String',
                          'TIME': 'Time' }

    def __init__( self, parent, table_name, **cfg ):
        """
            field:              D_ROLE_ID       INT         AUTO_NUMBER  PRIMARY KEY

        :param cfg:
        :return:
        """
        TemplateBase.__init__( self, parent )
        self.__tableName    = table_name
        self.__config       = cfg
        self.__field        = ''
        self.__testdata     = None
        self.__sqlType      = ''
        self.__length       = 0
        self.__relationShip = None
        self.__choice       = None
        self.__attrs        = []
        self.__ui           = None
        self.__leadIn       = []
        self.__dbField      = ''
        self.unique         = False
        self._isSibling      = cfg.get( C_ISSIBLING, False)
        self._siblings       = []
        if C_FIELD not in self.__config:
            raise MissingAttribute( C_TABLE, C_FIELD )

        field_data = cfg.get( C_FIELD, '' )
        tokens = [ x for x in word_tokenize( field_data ) ]
        self.__dbField  = self.__field = tokens[ 0 ]
        self.__sqlType  = tokens[ 1 ]
        if self.__sqlType not in self.TS_TYPES_FROM_SQL:
            raise InvalidSetting( C_FIELD, self.__tableName, self.__field, expected = self.TS_TYPES_FROM_SQL )

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
        # UNIQUE
        # FOREIGN KEY <reference>
        while offset < len( tokens ):
            if tokens[ offset ] == 'NULL':
                self.__attrs.append( 'NULL' )

            elif tokens[ offset ] == 'NOT':
                offset += 1
                if tokens[ offset ] == 'NULL':
                    self.__attrs.append( 'NOT NULL' )

                else:
                    raise InvalidSetting( C_FIELD, 'attr: "NOT ' + tokens[ offset ] + '"', self.__field )

            elif tokens[ offset ] == 'DEFAULT':
                self.__attrs.append( 'DEFAULT {0}'.format( tokens[ offset + 1 ] ) )

            elif tokens[ offset ] == 'PRIMARY':
                self.__attrs.append( 'PRIMARY KEY' )

            elif tokens[ offset ] == 'AUTO':
                self.__attrs.append( 'AUTO NUMBER' )

            elif tokens[ offset ] == 'UNIQUE':
                self.__attrs.append( 'UNIQUE' )

            elif tokens[ offset ] == 'FOREIGN':
                self.__attrs.append( 'FOREIGN KEY {0}'.format( tokens[ offset + 2 ] ) )
                offset += 1

            else:
                raise InvalidSetting( C_FIELD, 'attr: "' + tokens[ offset ] + '"', self.__field )

            offset += 2

        if C_UI in cfg and type( cfg[ C_UI ] ) is dict:
            self.__ui = TemplateUi( self, **cfg.get( C_UI, {} ) )

        if C_SIBLINGS in cfg and type( cfg[ C_SIBLINGS ] ) is list:
            for subConfig in cfg[ C_SIBLINGS ]:
                subConfig[ C_ISSIBLING ] = True
                # TODO: check necessity
                subConfig[ C_FIELD ] = cfg.get( C_FIELD, '' )
                self._siblings.append( TemplateColumn( parent, table_name, **subConfig ) )

        self.__relationShip = TemplateRelation( self, **self.__config.get( C_RELATION_SHIP, {} ) )
        self.__listview     = TemplateListView( self, **self.__config.get( C_LIST_VIEW, {} ) )
        self.__testdata     = TemplateTestData( self, **self.__config.get( C_TEST_DATA, {} ))

        if root.config.options.ignoreCaseDbIds:
            self.__dbField = self.__dbField.lower()

        if C_INDEX in cfg:
            logger.warning( "'index' in the 'field' defintion is OBSOLETE, use 'listview' -> 'index' +"
                            " in the 'field' definition." )

        return

    def hasAttribute( self,attr ):
        if attr in self.__attrs:
            return True

        if attr in ( 'FOREIGN KEY', 'DEFAULT' ):
            for item in self.__attrs:
                if item[ :len( attr ) ] == attr:
                    return True

        return False

    @property
    def table( self ):
        return self.parent

    @property
    def object( self ):
        return self.table.object

    @property
    def isSibling( self ):
        return self._isSibling

    @property
    def siblings( self ):
        return self._siblings

    @property
    def leadIn( self ) -> list:
        return self.__leadIn

    @property
    def hasAutoUpdate( self ) -> bool:
        return C_AUTO_UPDATE in self.__config

    @property
    def autoUpdate( self ):
        if C_AUTO_UPDATE in self.__config:
            logger.debug( "AUTO UPDATE {}".format( self.__config[ C_AUTO_UPDATE ] ) )

            autoValue = self.__config[ C_AUTO_UPDATE ]
            if '(' in autoValue:
                # Python callable
                if '.' not in autoValue:
                    autoValue = 'common.{}'.format(autoValue)

                module_name, _ = autoValue.rsplit('.', 1 )
                import_statement = 'import {}'.format( module_name )
                if module_name != 'common' and import_statement not in self.__leadIn:
                    self.__leadIn.append( import_statement )

            else:
                # A scalar
                pass

            logger.debug("AUTO UPDATE {}".format( autoValue ) )
            return autoValue

        return None

    @property
    def listview( self ):
        return self.__listview
    
    @property
    def testdata( self ):
        return self.__testdata

    def hasTestdata( self ):
        return C_TEST_DATA in self.__config

    def hasResolveList( self ) -> bool:
        return self.__ui is not None and self.__ui.hasResolveList()

    def hasService( self ) -> bool:
        return self.__ui is not None and self.__ui.hasService()

    def hasServiceBaseClass( self ) -> bool:
        return self.__ui is not None and self.__ui.hasServiceBaseClass()

    def __repr__(self):
        return "<TemplateColumn name='{}' label='{}'".format( self.name, self.label )

    def __eq__(self, other):
        return self.name == other.name

    def definedNotNull( self ) -> bool:
        return not self.sqlAttrs2Dict()[ 'nullable' ]

    def definedNull( self ) -> bool:
        return self.sqlAttrs2Dict()[ 'nullable' ]

    @property
    def tableName( self ) -> str:
        return self.__tableName

    @property
    def hasTab( self ) -> bool:
        return C_TAB in self.__config

    @property
    def tab( self ) -> TemplateTab:
        return TemplateTab( self, **self.__config.get( C_TAB, {} ) )

    @property
    def uniqueKey( self ) -> str:
        result = self.__config.get( C_UNIQUE, self.__config.get( C_UNIQUE_KEY, '' ) )
        if isinstance( result, bool ):
            result = "{}_IDX".format( self.name )

        return result

    def hasUniqueKey( self ) -> bool:
        return C_UNIQUE_KEY in self.__config or C_UNIQUE in self.__config

    def hasForeignKey( self ) -> bool:
        return any( 'FOREIGN KEY' in x for x in self.__attrs )
        # return 'FOREIGN KEY' in self.__attrs

    def hasRelationship( self ) -> bool:
        return self.hasForeignKey() and C_RELATION_SHIP in self.__config

    @property
    def relationship( self ):
        return self.__relationShip

    @property
    def name( self ) -> str:
        if self.isSibling:
            return self.__field + "_" + self.label.upper().replace(" ", "_")
        return self.__field

    @property
    def fieldName( self ) -> str:
        return self.__field

    def hasLabel( self ) -> bool:
        return self.__config.get( C_LABEL, '' ) != ''

    @property
    def label( self ) -> str:
        return self.__config.get( C_LABEL, '' )

    @property
    def frontend( self ):
        return self.__config.get( 'frontend', True )

    def isPrimaryKey( self ) -> bool:
        return 'PRIMARY KEY' in self.__attrs

    def hasForeign( self ) -> bool:
        return 'FOREIGN KEY' in self.__attrs

    @property
    def foreignReferenceID( self ) -> str:
        if self.__ui is not None and isinstance(self.__ui.serviceLabel, str):
            # remove the last item of the label string since that is the actual label but we want
            # the foreign key id of the row that contains the label. Also, remove the "_FK" at the end
            return self.__field + "_FK." +  ".".join(self.__ui.serviceLabel.split(".")[:-1])[:-3]
        return None

    @property
    def ui( self ):
        return self.__ui

    def minimal( self ) -> str:
        return self.__config.get( C_MINIMAL, '0' )

    def maximal( self ):
        if self.__sqlType == 'BIGINT':
            return self.__config.get( C_MAXIMAL, str( 2 ** 63 - 1 ) )

        elif self.__sqlType == 'NUMERIC' or self.__sqlType == 'DECIMAL':
            return self.__config.get( C_MAXIMAL, str( 2 ** ( self.__length * 8 ) - 1 ) )

        return self.__config.get( C_MAXIMAL, str( 2 ** 31 - 1 ) )

    @property
    def pType( self ) -> str:
        """
            BigInteger          = BIGINT
            Boolean             = BOOLEAN or SMALLINT
            Date                = DATE
            DateTime            = TIMESTAMP
            Enum
            Float               = FLOAT or REAL.
            Integer             = INT
            Interval            = INTERVAL
            CLOB
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
        if self.__sqlType in self.PY_TYPES_FROM_SQL:
            return self.PY_TYPES_FROM_SQL[ self.__sqlType ]

        raise Exception( 'Invalid SQL type: {0} for field {1}'.format( self.__sqlType, self.name ) )

    @property
    def nativePythonType( self ) -> str:
        if self.__sqlType in self.NATIVE_PY_TYPES_FROM_SQL:
            return self.NATIVE_PY_TYPES_FROM_SQL[ self.__sqlType ]

        raise Exception( 'Invalid SQL type: {0} for field {1}'.format( self.__sqlType, self.name ) )

    @property
    def tsType( self ) -> str:
        if self.__sqlType in self.TS_TYPES_FROM_SQL:
            return self.TS_TYPES_FROM_SQL[ self.__sqlType ]

        raise Exception( 'Invalid SQL type: {0}'.format( self.__sqlType ) )

    @property
    def schemaType( self ):
        if self.__sqlType in self.TS_TYPES_FROM_SQL:
            return self.SCHEMA_TYPES_FROM_SQL[ self.__sqlType ]

        raise Exception( 'Invalid SQL type: {0}'.format( self.__sqlType ) )

    def isNumericField( self ) -> bool:
        return self.TS_TYPES_FROM_SQL[ self.__sqlType ] == 'number'

    def isBooleanField( self ) -> bool:
        return self.TS_TYPES_FROM_SQL[ self.__sqlType ] == 'boolean'

    def isDateField( self ):
        return self.__sqlType == "DATE"

    def isTimeField( self ):
        return self.__sqlType == "TIME"

    def isDateTimeField( self ):
        return self.__sqlType in ( "DATETIME", 'TIMESTAMP' )

    def isString( self ):
        return self.TS_TYPES_FROM_SQL[ self.__sqlType ] == 'string'

    def sqlAttrs2Dict( self ):
        options = { 'autoincrement': False,
                    'primary_key': False,
                    'nullable': True,
                    'foreign_key': None,
                    'unique': False,
                    'default': None,
                  }
        for attr in self.__attrs:
            if 'AUTO NUMBER' in attr:
                options[ 'autoincrement' ] = True

            elif 'PRIMARY KEY' in attr:
                options[ 'primary_key'] = True
                options[ 'nullable'] = False

            elif 'NOT NULL' in attr:
                options[ 'nullable' ] = False

            elif 'UNIQUE' in attr:
                options[ 'unique' ] = True
                options[ 'nullable' ] = False

            elif attr.startswith( 'FOREIGN KEY' ):
                if root.config.options.ignoreCaseDbIds:
                    options[ 'foreign_key' ] = attr.split( ' ' )[ 2 ].lower()

                else:
                    options['foreign_key'] = attr.split(' ')[ 2 ]

            elif attr.startswith( 'DEFAULT' ):
                value = attr.split( ' ' )[ 1 ]
                if self.isNumericField():
                    options[ 'default' ] = value

                elif self.isBooleanField():
                    if value.lower() == ( "true", "1", "yes" ):
                        options[ 'default' ] = True

                    else:
                        options[ 'default' ] = False

                else:
                    options['default'] = '"{0}"'.format( value )

            elif attr.startswith( 'NULL' ):
                options[ 'nullable' ] = True

            else:
                logger.error( 'Extra unknown attributes found: {0}'.format( attr ) )

        return options

    def sqlAlchemyDef( self ) -> str:
        """
            https://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Column
        :return:
        """
        if root.config.options.ignoreCaseDbIds:
            result = 'API.db.Column( "{0}", {1}'.format( self.__dbField, self.pType )

        else:
            result = 'API.db.Column( {0}'.format( self.pType )

        if self.__length != 0:
            result += '( {0} )'.format( self.__length )

        for attr in self.__attrs:
            if 'AUTO NUMBER' in attr:
                result += ', autoincrement = True'

            elif 'PRIMARY KEY' in attr:
                result += ', primary_key = True'

            elif 'NOT NULL' in attr:
                result += ', nullable = False'

            elif 'UNIQUE' in attr:
                result += ', unique = True'

            elif attr.startswith( 'FOREIGN KEY' ):
                foreignKeyName = attr.split( ' ' )[ 2 ].lower() if root.config.options.ignoreCaseDbIds else attr.split( ' ' )[ 2 ]
                if 'NULL' in self.__attrs and 'NOT NULL' not in self.__attrs:
                    # TODO: maybe better to set to default if it is specified
                    result += ', API.db.ForeignKey( "{0}", ondelete = "SET NULL" )'.format( foreignKeyName )
                else:
                    result += ', API.db.ForeignKey( "{0}", ondelete = "CASCADE" )'.format( foreignKeyName )

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

            elif attr.startswith( 'NULL' ):
                result += ', nullable = True'

            else:
                logger.error( 'Extra unknown attributes found: {0}'.format( attr ) )

            defValue = self.DefaultValue()
            if defValue is not None:
                defValue, module_name, function = defValue
                if module_name is None:
                    # A scalar
                    result += ', default = {q}{val}{q}'.format( val = defValue,
                                                                q = '"' if type( defValue ) is str else "" )

                else:
                    # Python callable
                    # Need to inject the module
                    import_statement = 'import {}'.format( module_name )
                    if module_name != 'common' and import_statement not in self.__leadIn:
                        self.__leadIn.append( import_statement )

                    result += ', default = {mod}.{call}'.format( mod = module_name, call = function )

        if self.unique:
            result += ", unique = {}".format( self.unique )

        result += ' )'
        return result

    def DefaultValue( self ):
        if C_DEFAULT in self.__config:
            module_name = None
            function = None
            defValue = self.__config[ C_DEFAULT ]
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

            return defValue, module_name, function

        return None

    @property 
    def dbField( self ):
        return self.__dbField

    def serviceClass( self, modules: list, table: str ):
        for module in modules:
            if module.get("table") == table:
                return module.get("model")
        return None

    @property 
    def foreignKey ( self ):
        for attr in self.__attrs:
            if "FOREIGN KEY" in attr:
                return attr.split(" ")[-1]
        return None

    @property
    def initValue( self ):
        def initValueDefault():
            if self.isNumericField():
                return "0"

            elif self.isBooleanField():
                return "false"

            return "''"

        return self.__config.get( C_INITIAL_VALUE, initValueDefault() )

    @property
    def validators( self ):
        result = ""
        if not self.isPrimaryKey():
            if 'NOT NULL' in self.__attrs or self.hasForeign():
                result += 'Validators.required, '

            if self.__length > 0:
                result += 'Validators.maxLength( {0} ), '.format( self.__length )

        return '[ {} ] '.format( result )

    @property
    def validatorsList( self ):
        result = []
        if not self.isPrimaryKey():
            if 'NOT NULL' in self.__attrs or self.hasForeign():
                result.append(Validator(ValidatorType.REQUIRED, True))

            if self.__length > 0:
                result.append(Validator(ValidatorType.MAXLENGTH, self.__length))

        return result

    def angularUiInput( self, mixin="" ):
        if self.__ui is None:
            raise Exception( "Missing 'ui' group for column {} on table {}".format( self.__field,
                                                                                    self.__tableName ) )
        if root.config.controls is not None:
            return self.build()

        return self.__ui.buildInputElement( self.__tableName,
                                            self.name,
                                            self.__config.get( C_LABEL, '' ),
                                            mixin = mixin,
                                            validators=self.validatorsList )

    @property
    def readonly( self ) -> bool:
        return self.__config.get( C_READ_ONLY, False )

    @property
    def group( self ):
        if self.ui:
            return self.ui.group
        return None

    @property
    def disabled( self ) -> bool:
        return self.__config.get( C_DISABLED, False )

    def isSet( self, property ):
        return property in self.__config

    def build( self ):
        if self.__ui is None:
            return ''

        obj = root.config.controls.get( self.__ui.type )

        if obj is None:
            raise Exception( "Unknown control {} in {}".format( self.__ui.type, self.name ) )

        return obj.build( field = self,
                          table = self.table,
                          obj = self.object,
                          root = root.config )

