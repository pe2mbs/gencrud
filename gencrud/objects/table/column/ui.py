#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2019 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation; either version 2 of the
#   License, or (at your option) any later version.
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
from gencrud.objects.table.column.service import TemplateService
import gencrud.util.utils

class TemplateUi( object ):
    def __init__( self, parent, **cfg ):
        self.__parent   = parent
        self.__cfg = cfg
        if 'service' in cfg:
            self.__service = TemplateService( **cfg[ 'service' ] )

        else:
            self.__service = None

        return

    @property
    def uiObject( self ):
        return self.__cfg.get( 'type', 'textbox' )

    @property
    def rows( self ):
        return self.__cfg.get( 'rows', 4 )

    @property
    def cols( self ):
        return self.__cfg.get( 'cols', 80 )

    @property
    def min( self ):
        return self.__cfg.get( 'min', 0 )

    @property
    def max( self ):
        return self.__cfg.get( 'max', 100 )

    def hasPrefix( self ):
        return 'prefix' in self.__cfg

    @property
    def prefixType( self ):
        return self.__cfg.get( 'prefix-type', 'text' )

    @property
    def prefix( self ):
        return self.__cfg.get( 'prefix', '' )

    def hasSuffix( self ):
        return 'suffix' in self.__cfg

    @property
    def suffixType( self ):
        return self.__cfg.get( 'suffix-type', 'text' )

    @property
    def suffix( self ):
        return self.__cfg.get( 'suffix', '' )

    def isTextbox( self ):
        return self.uiObject.lower() == 'textbox'

    def isCheckbox( self ):
        return self.uiObject.lower() == 'checkbox'

    def isTextArea( self ):
        return self.uiObject.lower() == 'textarea'

    def isPassword( self ):
        return self.uiObject.lower() == 'password'

    def isNumber( self ):
        return self.uiObject.lower() == 'number'

    def isChoice( self ):
        return self.uiObject.lower() == 'choice'

    def isCombobox( self ):
        return self.uiObject.lower() == 'combobox' or self.uiObject.lower() == 'combo'

    def isDate( self ):
        return self.uiObject.lower() == 'datepicker' or self.uiObject.lower() == 'date'

    def isDateTime( self ):
        return self.uiObject.lower() == 'datetimepicker' or self.uiObject.lower() == 'datetime'

    def isTime( self ):
        return self.uiObject.lower() == 'timepicker' or self.uiObject.lower() == 'time'

    def isLabel( self ):
        return self.uiObject.lower() == 'label'

    def isSlider( self ):
        return self.uiObject.lower() == 'slider'

    def isSliderToggle( self ):
        return self.uiObject.lower() == 'slidertoggle'

    def buildInputElement( self, table, field, label, options = None ):
        if options is None:
            options = []

        type2component = {
            'label':            'pyt-label-box',
            'textbox':          'pyt-text-input-box',
            'text':             'pyt-text-input-box',
            'checkbox':         'pyt-checkbox-input-box',
            'password':         'pyt-password-input-box',
            'textarea':         'pyt-textarea-input-box',
            'number':           'pyt-number-input-box',
            'email':            'pyt-email-input-box',
            'choice':           'pyt-choice-input-box',
            'combobox':         'pyt-combo-input-box',
            'combo':            'pyt-combo-input-box',
            'slider':           'pyt-slider-input-box',
            'slidertoggle':     'pyt-slidertoggle-input-box',
            'date':             'pyt-date-input-box',
            'time':             'pyt-time-input-box',
            'datetime':         'pyt-datetime-input-box',
            'datepicker':       'pyt-datepicker-input-box',
            'timepicker':       'pyt-timepicker-input-box',
            'datetimepicker':   'pyt-datetimepicker-input-box'
        }
        if 'hint' in  self.__cfg:
            options.append( 'hint="{0}"'.format( self.__cfg[ 'hint' ] ) )

        options.append( 'error="{0}"'.format( self.error.lower() ) )

        if self.hasPrefix():
            options.append( 'prefix="{0}" prefix-type="{1}"'.format( self.prefix, self.prefixType ) )

        if self.hasSuffix():
            options.append( 'suffix="{0}" prefix-type="{1}"'.format( self.suffix, self.suffixType ) )

        if self.isCombobox() or self.isChoice():
            if self.__service is None:
                options.append( '[items]="{}List"'.format( self.__parent.name ) )

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

        if 'disabled' in self.__cfg:
            options.append( 'disabled="{0}"'.format( self.disabled ) )

        if 'color' in self.__cfg:
            options.append( 'color="{0}"'.format( self.color ) )

        if self.isLabel():
            options.append( 'format="{0}"'.format( self.format ) )
            options.append( 'pipe="{0}"'.format( self.pipe ) )

        options.append( 'debug="{0}"'.format( str( self.__cfg.get( 'debug', False ) ) ).lower() )

        return '''<{tag} id="{table}.{id}" placeholder="{placeholder}" {option} formControlName="{field}"></{tag}>'''.\
                format( tag = type2component[ self.__cfg.get( 'type', 'textbox' ) ],
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

    @property
    def interval( self ):
        return self.__cfg.get( 'interval', 1 )

    @property
    def vertical( self ):
        return str( self.__cfg.get( 'vertical', False ) ).lower()

    @property
    def disabled( self ):
        return str( self.__cfg.get( 'disabled', False ) ).lower()

    @property
    def pipe( self ):
        return str( self.__cfg.get( 'pipe', '' ) ).lower()

    @property
    def format( self ):
        return str( self.__cfg.get( 'format', 'text' ) )

    @property
    def invert( self ):
        return str( self.__cfg.get( 'invert', False ) ).lower()

    @property
    def step( self ):
        return self.__cfg.get( 'step', 1 )

    @property
    def thumbLabel( self ):
        return str( self.__cfg.get( 'thumbLabel', True ) ).lower()

    @property
    def color( self ):
        return str( self.__cfg.get( 'color', 'primary' ) ).lower()

    @property
    def checked( self ):
        return str( self.__cfg.get( 'checked', False ) ).lower()

    @property
    def labelPosition( self ):
        return str( self.__cfg.get( 'labelPosition', 'after' ) ).lower()

    @property
    def error( self ):
        return str( self.__cfg.get( 'error', True ) ).lower()

    def hasResolveList( self ):
        return 'resolve-list' in self.__cfg or 'resolveList' in self.__cfg

    def typescriptResolveList( self ):
        if 'resolveList' in self.__cfg:
            resolveList = self.__cfg[ 'resolveList' ]

        else:
            resolveList = self.__cfg.get( 'resolve-list',[ ] )

        if isinstance( resolveList, dict ):
            # Short hand resolveList, need to convert
            newResolveList = []
            for item in resolveList.keys():
                newResolveList.append( {
                    'label': resolveList[ item ],
                    'value': item
                })


        else:
            newResolveList = resolveList

        ## result = [ "{}: '{}'".format( item[ 'value' ], item[ 'label' ] ) for item in resolveList ]
        return "{}".format( json.dumps( newResolveList, indent = 12 ) )

    @property
    def resolveList( self ):
        if 'resolveList' in self.__cfg:
            resolveList = self.__cfg[ 'resolveList' ]

        else:
            resolveList = self.__cfg.get( 'resolve-list', [] )

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
                result[ item[ 'value' ] ] = item[ 'label' ]

            elif isinstance( item, ( str, int, float ) ):  # key
                result[ item ] = resolveList[ item ]

            else:
                raise Exception( "Invalid format in resolve-list" )

        return json.dumps( result ).replace( "'", "\'" ).replace( '"', "'" )

    def createResolveConstants( self ):
        def normalizeConstant( value ):
            last = ''
            result = ''
            if isinstance( value, ( int, float ) ):
                return normalizeConstant( str( value ) )

            for ch in value:
                if ch.isalnum():
                    result += ch
                    last = ch

                elif last != ' ':
                    result += '_'
                    last = ' '

            if result[0].isdigit():
                result = '_' + result

            return result

        lines = []
        if self.hasResolveList():
            constant_format = self.__cfg.get( 'constant-format', '"{0:50} = {1}".format( label, value )' )
            if 'resolveList' in self.__cfg:
                resolveList = self.__cfg.get( 'resolveList', {} )

            else:
                resolveList = self.__cfg.get( 'resolve-list', {} )

            for item in resolveList:
                try:
                    varables = { 'field': normalizeConstant( self.__parent.name ),
                                 'table': normalizeConstant( self.__parent.tableName ) }
                    if isinstance( resolveList, ( list, tuple ) ) and isinstance( item, dict ):
                        varables[ "label" ] = normalizeConstant( item[ 'label' ] )
                        varables[ "value" ] = item[ 'value' ]

                    elif isinstance( item, ( str, int, float ) ):   # key
                        varables[ "label" ] = normalizeConstant( resolveList[ item ] )
                        varables[ "value" ] = item

                    else:
                        raise Exception( "Invalid format in resolve-list" )

                    result = eval( constant_format, globals(), varables )
                    if result not in lines:
                        lines.append( result )

                except Exception as exc:
                    logging.error( traceback.format_exc() )
                    raise Exception( "There is an error in the 'constant-format' expression" ) from None

        return lines



