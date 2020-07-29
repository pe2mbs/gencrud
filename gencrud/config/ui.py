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
import traceback
import json
from gencrud.config.base import TemplateBase
from gencrud.config.service import TemplateService
from gencrud.constants import *


class TemplateUi( TemplateBase ):
    def __init__( self, parent, **cfg ):
        TemplateBase.__init__( self, parent )
        self.__cfg = cfg
        if C_SERVICE in cfg:
            self.__service = TemplateService( **cfg[ C_SERVICE ] )

        else:
            self.__service = None

        return

    @property
    def field( self ):
        return self.parent

    @property
    def table( self ):
        return self.parent.table

    @property
    def object( self ):
        return self.table.object

    @property
    def uiObject( self ):
        return self.__cfg.get( C_TYPE, C_TEXTBOX )

    @property
    def type( self ):
        return self.__cfg.get( C_TYPE, None )

    @property
    def label( self ):
        return self.__cfg.get( C_LABEL, self.parent.label )

    @property
    def hint( self ):
        return self.__cfg.get( C_HINT, None )

    @property
    def rows( self ):
        return self.__cfg.get( C_ROWS, 4 )

    @property
    def cols( self ):
        return self.__cfg.get( C_COLS, 80 )

    @property
    def min( self ):
        return self.__cfg.get( C_MIN, 0 )

    @property
    def max( self ):
        return self.__cfg.get( C_MAX, 100 )

    # def hasPrefix( self ):
    #     return C_PREFIX in self.__cfg

    @property
    def prefixType( self ):
        return self.__cfg.get( C_PREFIX_TYPE, C_TEXT )

    @property
    def prefix( self ):
        return self.__cfg.get( C_PREFIX, '' )

    # def hasSuffix( self ):
    #     return C_SUFFIX in self.__cfg

    @property
    def suffixType( self ):
        return self.__cfg.get( C_SUFFIX_TYPE, C_TEXT )

    @property
    def suffix( self ):
        return self.__cfg.get( C_SUFFIX, '' )

    @property
    def interval( self ):
        return self.__cfg.get( C_INTERVAL, 1 )

    @property
    def vertical( self ):
        return str( self.__cfg.get( C_VERTICAL, False ) ).lower()

    @property
    def disabled( self ):
        return str( self.__cfg.get( C_DISABLED, self.parent.disabled ) ).lower()

    @property
    def readonly( self ):
        return str( self.__cfg.get( C_READ_ONLY, self.parent.readonly ) ).lower()

    @property
    def pipe( self ):
        return str( self.__cfg.get( C_PIPE, '' ) ).lower()

    @property
    def format( self ):
        return str( self.__cfg.get( C_FORMAT, C_TEXT ) )

    @property
    def invert( self ):
        return str( self.__cfg.get( C_INVERT, False ) ).lower()

    @property
    def step( self ):
        return self.__cfg.get( C_STEP, 1 )

    @property
    def thumbLabel( self ):
        return str( self.__cfg.get( C_THUMB_LABEL, True ) ).lower()

    @property
    def color( self ):
        return str( self.__cfg.get( C_COLOR, C_COLOR_PRIMARY ) ).lower()

    @property
    def checked( self ):
        return str( self.__cfg.get( C_CHECKED, False ) ).lower()

    @property
    def labelPosition( self ):
        return str( self.__cfg.get( C_LABEL_POSITION, C_AFTER ) ).lower()

    @property
    def error( self ):
        return str( self.__cfg.get( C_ERROR, True ) ).lower()

    def get( self, property, default = None ):
        return self.__cfg.get( property, default )

    def isTextbox( self ):
        return self.uiObject.lower() == C_TEXTBOX

    def isCheckbox( self ):
        return self.uiObject.lower() == C_CHECKBOX

    def isTextArea( self ):
        return self.uiObject.lower() == C_TEXTAREA

    def isPassword( self ):
        return self.uiObject.lower() == C_PASSWORD

    def isNumber( self ):
        return self.uiObject.lower() == C_NUMBER

    def isChoice( self ):
        return self.uiObject.lower() == C_CHOICE

    def isEmail( self ):
        return self.uiObject.lower() == C_EMAIL

    def isCombobox( self ):
        return self.uiObject.lower() == C_COMBOBOX or self.uiObject.lower() == C_COMBO

    def isDate( self ):
        return self.uiObject.lower() == C_DATE_PICKER or self.uiObject.lower() == C_DATE

    def isDateTime( self ):
        return self.uiObject.lower() == C_DATE_TIME_PICKER or self.uiObject.lower() == C_DATE_TIME

    def isTime( self ):
        return self.uiObject.lower() == C_TIME_PICKER or self.uiObject.lower() == C_TIME

    def isLabel( self ):
        return self.uiObject.lower() == C_LABEL

    def isSlider( self ):
        return self.uiObject.lower() == C_SLIDER

    def isSliderToggle( self ):
        return self.uiObject.lower() == C_SLIDER_TOGGLE

    def isSet( self, property ):
        return property in self.__cfg or self.parent.isSet( property )

    def buildInputElement( self, table, field, label, options = None ):
        if options is None:
            options = []

        type2component = {
            C_LABEL:                'pyt-label-box',
            C_TEXTBOX:              'pyt-text-input-box',
            C_TEXT:                 'pyt-text-input-box',
            C_CHECKBOX:             'pyt-checkbox-input-box',
            C_PASSWORD:             'pyt-password-input-box',
            C_TEXTAREA:             'pyt-textarea-input-box',
            C_NUMBER:               'pyt-number-input-box',
            C_EMAIL:                'pyt-email-input-box',
            C_CHOICE:               'pyt-choice-input-box',
            C_COMBOBOX:             'pyt-combo-input-box',
            C_COMBO:                'pyt-combo-input-box',
            C_SLIDER:               'pyt-slider-input-box',
            C_SLIDER_TOGGLE:        'pyt-slidertoggle-input-box',
            C_DATE:                 'pyt-date-input-box',
            C_TIME:                 'pyt-time-input-box',
            C_DATE_TIME:            'pyt-datetime-input-box',
            C_DATE_PICKER:          'pyt-datepicker-input-box',
            C_TIME_PICKER:          'pyt-timepicker-input-box',
            C_DATE_TIME_PICKER:     'pyt-datetimepicker-input-box'
        }
        if C_HINT in  self.__cfg:
            options.append( 'hint="{0}"'.format( self.__cfg[ C_HINT ] ) )

        options.append( 'error="{0}"'.format( self.error.lower() ) )

        if self.isSet( 'prefix-type' ) or self.isSet( 'prefix' ):
            options.append( 'prefix="{0}" prefix-type="{1}"'.format( self.prefix, self.prefixType ) )

        if self.isSet( 'suffix-type' ) or self.isSet( 'suffix' ):
            options.append( 'suffix="{0}" suffix-type="{1}"'.format( self.suffix, self.suffixType ) )

        if self.isCombobox() or self.isChoice():
            if self.__service is None:
                options.append( '[items]="{}List"'.format( self.parent.name ) )

            else:
                options.append( '[items]="{}List"'.format( self.__service.name ) )

        elif self.isTextArea():
            options.append( 'rows="{0}" cols="{1}"'.format( self.rows, self.cols ) )

        elif self.isCheckbox():
            options.append( 'labelPosition="{0}"'.format( self.labelPosition ) )

        elif self.isSlider():
            options.append( 'min="{0}" max="{1}"'.format( self.min, self.max ) )
            options.append( 'interval="{0}"'.format( self.interval ) )
            options.append( 'vertical="{0}"'.format( self.vertical ) )
            options.append( 'invert="{0}"'.format( self.invert ) )
            options.append( 'step="{0}"'.format( self.step ) )
            options.append( 'thumbLabel="{0}"'.format( self.thumbLabel ) )
            options.append( 'labelPosition="{0}"'.format( self.labelPosition ) )

        if C_DISABLED in self.__cfg:
            options.append( 'disabled="{0}"'.format( self.disabled ) )

        if self.field.isPrimaryKey():
            options.append( 'readonly="true"' )

        elif C_READ_ONLY in self.__cfg or self.field.readonly:
            options.append( 'readonly="{0}"'.format( self.readonly ) )

        if C_COLOR in self.__cfg:
            options.append( 'color="{0}"'.format( self.color ) )

        if self.isLabel():
            options.append( 'format="{0}"'.format( self.format ) )
            options.append( 'pipe="{0}"'.format( self.pipe ) )

        if self.isDate() or self.isTime() or self.isDateTime():
            options.append( 'format="{0}"'.format( self.format ) )

        if C_DEBUG in self.__cfg:
            options.append( 'debug="{0}"'.format( str( self.__cfg.get( C_DEBUG, False ) ) ).lower() )

        return '''<{tag} id="{table}.{id}" placeholder="{placeholder}" {option} formControlName="{field}"></{tag}>'''.\
                format( tag = type2component[ self.uiObject ],
                        id = field,
                        table = table,
                        placeholder = label,
                        option = ' '.join( options ),
                        field = field )

    def hasService( self ):
        return self.__service is not None

    @property
    def service( self ):
        return self.__service

    def hasResolveList( self ):
        return C_RESOLVE_LIST in self.__cfg or C_RESOLVE_LIST_OLD in self.__cfg

    def typescriptResolveList( self ):
        if C_RESOLVE_LIST_OLD in self.__cfg:
            resolveList = self.__cfg[ C_RESOLVE_LIST_OLD ]

        else:
            resolveList = self.__cfg.get( C_RESOLVE_LIST, [ ] )

        if isinstance( resolveList, dict ):
            # Short hand resolveList, need to convert
            newResolveList = []
            for item in resolveList.keys():
                newResolveList.append( {
                    C_LABEL: resolveList[ item ],
                    C_VALUE: item
                })

        else:
            newResolveList = resolveList

        # result = [ "{}: '{}'".format( item[ 'value' ], item[ 'label' ] ) for item in resolveList ]
        return "{}".format( json.dumps( newResolveList, indent = 12 ) )

    @property
    def resolveList( self ):
        if C_RESOLVE_LIST_OLD in self.__cfg:
            resolveList = self.__cfg[ C_RESOLVE_LIST_OLD ]

        else:
            resolveList = self.__cfg.get( C_RESOLVE_LIST, [] )

        '''
        resolve-list:
        -   label:          Disabled
            value:          false
        -   label:          Enabled
            value:          true
        OR
        resolve-list:
        -   label:          Disabled
            value:          0
        -   label:          Enabled      
            value:          1
        OR
        resolve-list:
            0:              Disabled     
            1:              Disabled
        '''
        result = {}
        for item in resolveList:
            if isinstance( item, dict ):
                result[ item[ C_VALUE ] ] = item[ C_LABEL ]

            elif isinstance( item, ( str, int, float ) ):  # key
                result[ item ] = resolveList[ item ]

            else:
                raise Exception( "Invalid format in resolve-list" )

        return json.dumps( result ).replace( "'", "\'" ).replace( '"', "'" )

    @property
    def resolveListPy( self ):
        if C_RESOLVE_LIST_OLD in self.__cfg:
            resolveList = self.__cfg[ C_RESOLVE_LIST_OLD ]

        else:
            resolveList = self.__cfg.get( C_RESOLVE_LIST,[ ] )

        '''
        resolve-list:
        -   label:          Disabled
            value:          false
        -   label:          Enabled
            value:          true
        OR
        resolve-list:
        -   label:          Disabled
            value:          0
        -   label:          Enabled      
            value:          1
        OR
        resolve-list:
            0:              Disabled     
            1:              Disabled
        '''
        result = { }
        for item in resolveList:
            if isinstance( item,dict ):
                result[ item[ C_VALUE ] ] = item[ C_LABEL ]

            elif isinstance( item, ( str,int,float ) ):  # key
                result[ item ] = resolveList[ item ]

            else:
                raise Exception( "Invalid format in resolve-list" )

        return result

    def createResolveConstants( self ):
        def normalizeConstant( value ):
            last = ''
            constantName = ''
            if isinstance( value, ( int, float ) ):
                return normalizeConstant( str( value ) )

            for ch in value:
                if ch.isalnum():
                    constantName += ch
                    last = ch

                elif last != ' ':
                    constantName += '_'
                    last = ' '

            if constantName[0].isdigit():
                constantName = '_' + constantName

            return constantName

        lines = []
        if self.hasResolveList():
            constant_format = self.__cfg.get( C_CONSTANT_FORMAT, '"C_{0:50} = {1}".format( label.upper(), value )' )
            if C_RESOLVE_LIST_OLD in self.__cfg:
                resolveList = self.__cfg.get( C_RESOLVE_LIST_OLD, {} )

            else:
                resolveList = self.__cfg.get( C_RESOLVE_LIST, {} )

            for item in resolveList:
                try:
                    variables = { C_FIELD: normalizeConstant( self.parent.name ),
                                 C_TABLE: normalizeConstant( self.parent.tableName ) }
                    if isinstance( resolveList, ( list, tuple ) ) and isinstance( item, dict ):
                        variables[ C_LABEL ] = normalizeConstant( item[ C_LABEL ] )
                        variables[ C_VALUE ] = item[ C_VALUE ]

                    elif isinstance( item, ( str, int, float ) ):   # key
                        variables[ C_LABEL ] = normalizeConstant( resolveList[ item ] )
                        variables[ C_VALUE ] = item

                    else:
                        raise Exception( "Invalid format in resolve-list" )

                    result = eval( constant_format, globals(), variables )
                    if result not in lines:
                        lines.append( result )

                except Exception:
                    logging.error( traceback.format_exc() )
                    raise Exception( "There is an error in the 'constant-format' expression" ) from None

        return lines

