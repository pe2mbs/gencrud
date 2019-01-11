
from pytemplate.service import TemplateService

class TemplateUi( object ):
    def __init__( self, **cfg ):
        self.__cfg = cfg
        if self.isChoice() or self.isCombobox():
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

    def prefixType( self ):
        return self.__cfg.get( 'prefix-type', 'text' )

    def prefix( self ):
        return self.__cfg.get( 'prefix', '' )

    def hasSuffix( self ):
        return 'suffix' in self.__cfg

    def suffixType( self ):
        return self.__cfg.get( 'suffix-type', 'text' )

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
        if self.isCombobox() or self.isChoice():
            options.append( '[items]="{}List"'.format( self.__service.name ) )

        elif self.isTextArea():
            options.append( 'rows="{0}" cols="{1}"'.format( self.rows, self.cols ) )

        elif self.isSlider():
            options.append( 'min="{0}" max="{1}"'.format( self.min, self.max ) )
            if 'interval' in self.__cfg:
                options.append( 'interval="{0}"'.format( self.__cfg[ 'interval' ] ) )

            if 'displayWith' in self.__cfg:
                options.append( 'displayWith="{0}"'.format( self.__cfg[ 'displayWith' ] ) )


        return '''<{tag} id="{table}.{id}" placeholder="{placeholder}"{option} formControlName="{field}"></{tag}>'''.\
                format( tag = type2component[ self.__cfg.get( 'type', 'textbox' ) ],
                        id = field,
                        table = table,
                        placeholder = label,
                        option = ' '.join( options ),
                        field = field )

    @property
    def service( self ):
        return self.__service
