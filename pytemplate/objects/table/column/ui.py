
from pytemplate.objects.table.column.service import TemplateService

class TemplateUi( object ):
    def __init__( self, **cfg ):
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
        return self.uiObject.lower() == 'datepicker'

    def isDateTime( self ):
        return self.uiObject.lower() == 'datetimepicker'

    def isTime( self ):
        return self.uiObject.lower() == 'timepicker'

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

        options.append( 'error="{0}"'.format( self.error ) )

        if self.hasPrefix():
            options.append( 'prefix="{0}" prefix-type="{1}"'.format( self.prefix, self.prefixType ) )

        if self.hasSuffix():
            options.append( 'suffix="{0}" prefix-type="{1}"'.format( self.suffix, self.suffixType ) )

        if self.isCombobox() or self.isChoice():
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

        if 'debug' in self.__cfg:
            options.append( 'debug="{0}"'.format( self.__cfg[ 'debug' ] ) )

        return '''<{tag} id="{table}.{id}" placeholder="{placeholder}"{option} formControlName="{field}"></{tag}>'''.\
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
        return str( self.__cfg.get( 'labelPosition', 'before' ) ).lower()

    @property
    def error( self ):
        return str( self.__cfg.get( 'error', True ) ).lower()
