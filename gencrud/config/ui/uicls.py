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
import typing as t

from gencrud.config.action import TemplateAction
from gencrud.config.actions import TemplateActions
from gencrud.config.base import TemplateBase
from gencrud.config.service import TemplateService
from gencrud.constants import *
from gencrud.util.validators import Validator, ValidatorType
from gencrud.config.ui.monaco import TemplateMonaco


class TypeComponents( object ):
    # TODO; remove flex
    _Component = {
        C_LABEL: { 'tag': 'gc-label' },
        C_TEXTBOX: { 'tag': 'gc-text-input' },
        C_TEXT: { 'tag': 'gc-text-input' },
        C_CHECKBOX: { 'tag': 'gc-checkbox-input' },
        C_PASSWORD: { 'tag': 'gc-password-input' },
        C_TEXTAREA: { 'tag': 'gc-textarea-input', 'fxflex': '98' },
        C_EDITOR: { 'tag': 'gc-monaco-editor', 'fxflex': '98' },
        C_NUMBER: { 'tag': 'gc-number-input' },
        C_EMAIL: { 'tag': 'gc-mail-input' },
        C_CHOICE: { 'tag': 'gc-choice-input' },
        C_CHOICE_BASE: { 'tag': 'gc-choice-base-input' },
        C_CHOICE_AUTO: { 'tag': 'gc-choice-autocomplete-input' },
        C_COMBOBOX: { 'tag': 'gc-combo-input' },
        C_COMBO: { 'tag': 'gc-combo-input' },
        C_SLIDER: { 'tag': 'gc-slider-input', 'fxflex': '30px' },
        C_SLIDER_TOGGLE: { 'tag': 'gc-slidertoggle-input', 'fxflex': '30px' },
        C_DATE: { 'tag': 'gc-date-input' },
        C_TIME: { 'tag': 'gc-time-input' },
        C_DATE_TIME: { 'tag': 'gc-datetime-input' },
        C_DATE_PICKER: { 'tag': 'gc-datepicker-input' },
        C_TIME_PICKER: { 'tag': 'gc-timepicker-input' },
        C_DATE_TIME_PICKER: { 'tag': 'gc-datetimepicker-input' } }

    def getComponentTag( self, component ):
        if component in TypeComponents._Component:
            return TypeComponents._Component[ component ].get( 'tag' )

        raise Exception( "Unknown component '{}' allowed: {}".format( component, ', '.join( list( TypeComponents._Component.keys() ) ) ) )

    def getFlex( self, component ):
        if component in TypeComponents._Component:
            c = TypeComponents._Component[ component ]
            if c.get( 'fxflex' ) is not None:
                return 'fxFlex="{}"'.format( c.get( 'fxflex' ) )

            return ""

        raise Exception( "Unknown component '{}' allowed: {}".format( component, ', '.join( list( TypeComponents._Component.keys() ) ) ) )


class TemplateUi( TemplateBase ):
    def __init__( self, parent, **cfg ):
        TemplateBase.__init__( self, parent )
        self.__components = TypeComponents()
        self.__cfg = cfg
        if C_SERVICE in cfg:
            self.__service = TemplateService( parent=self, **cfg[ C_SERVICE ] )

        else:
            self.__service = None

        if C_ACTIONS in cfg:
            self.__actions = TemplateActions( self, "name", cfg[ C_ACTIONS ], includeDefault=False )

        else:
            self.__actions = []

        self.__group = self.__cfg.get( C_GROUP, None )
        self.__monaco = None
        if C_MONACO_EDITOR in self.__cfg:
            self.__monaco = TemplateMonaco( self, **self.__cfg.get( C_MONACO_EDITOR ) )

        return

    @property
    def field( self ) -> 'TemplateColumn':
        return self.parent

    @property
    def table( self ):
        return self.parent.table

    @property
    def object( self ) -> 'TemplateObject':
        return self.table.object

    @property
    def uiObject( self ):
        return self.__cfg.get( C_TYPE, C_TEXTBOX ).lower()

    @property
    def type( self ) -> str:
        return self.__cfg.get( C_TYPE, None )

    @property
    def group( self ):
        return self.__group

    def hasGroup( self ) -> bool:
        return self.__group is not None

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

    def hasAttributes( self ):
        return 'attributes' in self.__cfg

    @property
    def attributes( self ):
        return self.__cfg.get( 'attributes', { } )

    @property
    def prefixType( self ):
        return self.__cfg.get( C_PREFIX_TYPE, C_TEXT )

    @property
    def prefix( self ):
        return self.__cfg.get( C_PREFIX, '' )

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
        return str( self.__cfg.get( C_FORMAT ) )

    @property
    def timezone( self ) -> str:
        return self.__cfg.get( C_TIMEZONE, 'UTC' )

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

    @property
    def serviceLabel( self ):
        if self.__service is not None:
            return self.__service.label
        return None

    @property
    def width( self ) -> int:
        return self.get( C_WIDTH, 100 )

    def get( self, property, default = None ):
        return self.__cfg.get( property, default )

    def isUiType( self, *args ):
        return self.uiObject in args

    # deprecated
    def isChoice( self ):
        return self.uiObject in ( C_CHOICE, C_CHOICE_AUTO ) #, C_CHOICE_BASE )

    # deprecated
    def isCombobox( self ):
        return self.uiObject in ( C_COMBOBOX, C_COMBO )

    def isSet( self, property ):
        return property in self.__cfg or self.parent.isSet( property )

    def buildInputElement( self, table, field, label, options = None, mixin = "", validators: t.List[Validator] = [], tab: bool = False ):
        if options is None:
            options = []
        
        if self.hasNgIf():
            options.append( '*ngIf="{}"'.format( self.ngIf ) )

        if C_HINT in  self.__cfg:
            options.append( 'hint="{0}"'.format( self.__cfg[ C_HINT ] ) )

        options.append( '[error]="{0}"'.format( self.error.lower() ) )
        if self.isSet( 'prefix-type' ) or self.isSet( 'prefix' ):
            options.append( 'prefix="{0}" prefix-type="{1}"'.format( self.prefix, self.prefixType ) )

        if self.isSet( 'suffix-type' ) or self.isSet( 'suffix' ):
            options.append( 'suffix="{0}" suffix-type="{1}"'.format( self.suffix, self.suffixType ) )

        def createActionButtons( actions: list, service: t.Optional[ TemplateService] = None ) -> list:
            _options = []
            for action in actions:
                buttonFields = []
                buttonFields.append(f"field: '{action.parent.parent.name}'")

                if action.icon is not None:
                    buttonFields.append(f"icon: '{action.icon}'")

                if action.mode is not None:
                    buttonFields.append(f"mode: '{action.mode}'")

                # if action.disabled is not None:
                #     buttonFields.append(f"disabled: {action.disabled}")

                if action.function not in ( None, '' ):
                    buttonFields.append( f"function: {action.function}" )

                else:
                    if isinstance( service, TemplateService ):
                        buttonFields.append(f"route: '{service.module}/{service.name}/edit'")

                    elif action.route in (None, ''):
                        buttonFields.append(f"route: '{self.object.route}/edit'")

                    else:
                        buttonFields.append(f"route: '{ action.route }'")

                _options.append(f'[{action.position}ActionButton]="{{ {", ".join(buttonFields)} }}"')

            return _options

        if self.isUiType( C_COMBO, C_CHOICE, C_CHOICE_AUTO, C_TEXTBOX, C_LABEL ):        # C_CHOICE_BASE
            if self.__service is None and self.hasResolveList() and not self.isUiType( C_TEXTBOX ): # choice is backend rendered and does not take items list
                options.append( '[items]="{}List"'.format( self.parent.name ) )

            else:
                if self.__service is not None:
                    options.append( 'serviceName="{}"'.format( self.__service.name ) )
                    if not self.isUiType( C_TEXTBOX ):
                        if not self.isUiType( C_CHOICE ):
                            options.append( '[items]="{}List"'.format( self.__service.name ) )
                        else:
                            # TODO: fix this part since it assumes Sercive explicitly as the name
                            options.append( '[service]="{}Service"'.format( self.__service.name ) )
                            options.append( 'valueField="{}"'.format( self.__service.value ) )
                            options.append( 'labelField="{}"'.format( self.__service.label ) )

                        # apply (backend) filter if specified
                        if self.service.hasFilter():
                            filterDictString = ", ".join([key + ": " + value for key, value in self.service.filter.items()])
                            options.append( '[filterDict]="{ ' + filterDictString + '}"' )

        elif self.isUiType( C_TEXTAREA ):
            options.append( 'rows="{0}" cols="{1}"'.format( self.rows, self.cols ) )

        elif self.isUiType( C_CHECKBOX ):
            options.append( 'labelPosition="{0}"'.format( self.labelPosition ) )

        elif self.isUiType( C_SLIDER ):
            options.append( 'min="{0}" max="{1}"'.format( self.min, self.max ) )
            options.append( 'interval="{0}"'.format( self.interval ) )
            options.append( 'vertical="{0}"'.format( self.vertical ) )
            options.append( 'invert="{0}"'.format( self.invert ) )
            options.append( 'step="{0}"'.format( self.step ) )
            options.append( 'thumbLabel="{0}"'.format( self.thumbLabel ) )
            options.append( 'labelPosition="{0}"'.format( self.labelPosition ) )

        if C_DISABLED in self.__cfg:
            options.append( '[disabled]="{0}"'.format( self.__cfg[C_DISABLED] ) )

        if self.field.isPrimaryKey():
            options.append( '[readonly]="true"' )

        elif C_READ_ONLY in self.__cfg or self.field.readonly:
            options.append( '[readonly]="{0}"'.format( self.readonly ) )

        if C_COLOR in self.__cfg:
            options.append( 'color="{0}"'.format( self.color ) )

        if self.pipe != '':
            if self.isUiType( C_LABEL ):
                options.append( 'format="{0}"'.format( self.format ) )
                options.append( 'pipe="{0}"'.format( self.pipe ) )
                if self.timezone != 'UTC':
                    options.append( 'timezone="{0}"'.format(self.timezone))

            elif self.isUiType( C_DATE, C_DATE_PICKER, C_DATE_TIME, C_DATE_TIME_PICKER, C_TIME, C_TIME_PICKER ):
                options.append( 'format="{0}"'.format( self.format ) )
                options.append( 'pipe="{0}"'.format( self.pipe ) )
                if self.timezone != 'UTC':
                    options.append( 'timezone="{0}"'.format(self.timezone))

        if self.hasDetailButton():
            s = self.detailButton()
            if isinstance( s, dict ):
                route = s.get( 'route', None )
                if route is not None:
                    options.append( 'detail_button="{}"'.format( route ) )
                    options.append( 'detail_id="{}"'.format( s.get( 'id', None ) ) )

        if C_DEBUG in self.__cfg:
            options.append( '[debug]="{0}"'.format( str( self.__cfg.get( C_DEBUG, False ) ) ).lower() )

        if self.hasMonaco():
            # Check if we are on a tab
            if tab:
                options.append( 'monacoMatTab' )
                options.append( 'height="auto"')

            # Set the minimap and language, default minimap = false, language = 'text'
            options.append( f'[minimap]="{ self.Monaco.Minimap }"' )
            options.append( f'language="{ self.Monaco.Language }"' )
            options.append( f'theme="{ self.Monaco.Theme }"')
            # Do we have a action bar defined ?
            if self.Monaco.hasActionBar():
                # Add the actionbar and monacoConfig elements
                options.append( f'[actionbar]="getActionBar_{ field }()"' )
                options.append( f'[monacoConfig]="getEditorConfig_{ field }()"' )

        ng_context = ''
        for action in self.__actions:
            action: TemplateAction
            ng_context += action.createFieldAction( field, self.__service ) + "\n"

        result = '<{tag} id="{table}.{field}" placeholder="{placeholder}" {option} formControlName="{field}"{mixin}>{ng_context}</{tag}>'.\
                format( tag         = self.__components.getComponentTag( self.uiObject ),
                        table       = self.table.name,
                        name        = self.parent.name,
                        placeholder = label,
                        option      = ' '.join( options ),
                        field       = field,
                        ng_context  = ng_context,
                        mixin       = " " + mixin if len(mixin) > 0 else "" )
        if self.hasMonaco():
            if self.Monaco.hasHeight() and self.Monaco.Height != 'auto':
                result = f'<div style="{ self.Monaco.Height }">{ result }</div>'

        if validators != None and len(validators) > 0:
            errorHandler = ""
            for validator in validators:
                if validator.validatorType in ( ValidatorType.REQUIRED, ValidatorType.MAXLENGTH, ValidatorType.MINLENGTH ):
                    result += f'\n <span class="form-error" *ngIf="{field}?.errors && '

                if validator.validatorType == ValidatorType.REQUIRED:
                    result += f'{field}?.hasError(\'required\')">{label} is a required field</span>'

                elif validator.validatorType == ValidatorType.MAXLENGTH:
                    result += f'{field}?.hasError(\'maxlength\')">Maximum size limit ({validator.value}) exceeded for {label} field</span>'

                elif validator.validatorType == ValidatorType.MINLENGTH:
                    result += f'{field}?.hasError(\'minlength\')">Minimum size limit ({validator.value}) not reached for {label} field</span>'

        return result

    def hasNgIf( self ):
        return 'ngif' in self.__cfg

    @property
    def ngIf( self ):
        return self.__cfg.get( 'ngif', '' )

    def hasService( self ):
        return self.__service is not None

    def hasServiceBaseClass( self ):
        return self.__service is not None and self.__service.hasBaseClass()

    @property
    def service( self ):
        return self.__service

    def defaultResolveList( self ):
        if self.isUiType( C_CHECKBOX ):
            return { True: "Yes", False: "No" }

        return []

    def hasResolveList( self ):
        result = C_RESOLVE_LIST in self.__cfg or C_RESOLVE_LIST_OLD in self.__cfg
        if not result and self.isUiType( C_CHECKBOX ):
            return True

        return result

    def typescriptResolveList( self ):
        if C_RESOLVE_LIST_OLD in self.__cfg:
            resolveList = self.__cfg[ C_RESOLVE_LIST_OLD ]

        else:
            resolveList = self.__cfg.get( C_RESOLVE_LIST, self.defaultResolveList() )

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
        result = "{}".format( json.dumps( newResolveList, indent = 4 ) )
        return result.replace( ' ', '' ).replace(':', ': ').replace(",", ", ")
        # return result.replace( '\n', '\n{}'.format( " " * 4 ) )

    @property
    def resolveList( self ):
        if C_RESOLVE_LIST_OLD in self.__cfg:
            resolveList = self.__cfg[ C_RESOLVE_LIST_OLD ]

        else:
            resolveList = self.__cfg.get( C_RESOLVE_LIST, self.defaultResolveList() )

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
            resolveList = self.__cfg.get( C_RESOLVE_LIST, self.defaultResolveList() )

        '''
        resolve-list:
        -   label:          Disabled
            value:          false
        -   label:          Enabled
            value:          true
        OR
        resolve-list:
            0:              Disabled     
            1:              Disabled
        '''
        result = { }
        if isinstance( resolveList, ( list, tuple ) ):
            for item in resolveList:
                if isinstance( item,dict ):
                    result[ item[ C_VALUE ] ] = item[ C_LABEL ]

                elif isinstance( item, ( str, int, float ) ):  # key
                    result[ item ] = resolveList[ item ]

                else:
                    raise Exception( "Invalid format in resolve-list" )

        elif isinstance( resolveList, dict ):
            return resolveList

        else:
            raise Exception( "Invalid resolve-list, needs to be a dictionary or a list with value/label attributes" )

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
            constant_format = self.__cfg.get( C_CONSTANT_FORMAT, '"C_{field}_{label:50} = {value}".format( label = label.upper(), value = value, field = field.upper() )' )
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

    def hasDetailButton( self ):
        return 'detail-button' in self.__cfg

    def detailButton( self ):
        return self.__cfg.get( 'detail-button', {} )

    def nullSafeAngularObject( self, inputString, startIndex = 1):
        if inputString is None:
            return None
        else:
            components = inputString.split(".")
            result = ""
            for i in range(startIndex, len(components) + 1):
                result += ".".join(components[:i]) + " != null && "
            return result[:-4] + " ? " + inputString + " : null"

    def hasMonaco( self ) -> bool:
        return self.__monaco is not None

    @property
    def Monaco( self ) -> TemplateMonaco:
        return self.__monaco
