from mako.template import Template


class InvalidPropertyValue( Exception ):
    pass


class ControlProperty( object ):
    def __init__( self, name, type, default = None, allowed = None, **kwargs ):
        self.__name = name
        self.__value = None
        self.__type = None
        self.__default = None
        self.__allowed = []
        self.set(  type, default, allowed, **kwargs )
        return

    @property
    def name( self ):
        return self.__name

    @property
    def type( self ):
        return self.__type

    @property
    def default( self ):
        return self.__default

    @property
    def allowed( self ):
        return self.__allowed

    def set( self, type, default = None, allowed = None, **kwargs ):
        self.__type = type
        self.__default = default
        self.__allowed = allowed
        for name, setting in kwargs.items():
            setattr( self, name, setting )

        return

    def isSet( self ):
        return self.__value is not None

    @property
    def value( self ):
        if self.__value is None:
            return self.__default

        return self.__value

    @value.setter
    def value( self, val ):
        self.__value = val
        return

    def __int__(self):
        if self.__type == 'int':
            return int( self.value )

        raise InvalidPropertyValue( self.__name )

    def __str__(self):
        if self.__type in ( 'str', 'int' ):
            return str( self.value )

        elif self.__type == 'bool':
            return str( self.value ).lower()

        elif self.__type == 'list':
            if self.__value is list:
                return ','.join( self.__value )

            return ''

        raise InvalidPropertyValue( self.__name )

    def __bool__(self):
        if self.__type == 'bool':
            return

        raise InvalidPropertyValue( self.__name )

class TemplateDymanicControl( object ):
    def __init__( self, parent, name, arguments, htmlTemplate ):
        self.__parent = parent
        self.__name = name
        self.__htmlTemplate = htmlTemplate
        self.__attributes = []
        for name, properties in arguments.items():
            self.__attributes.append( name )
            setattr( self, name, ControlProperty( name, **properties ) )

        return

    @property
    def name( self ):
        return self.__name

    @property
    def htmlTemplate( self ):
        return self.__htmlTemplate

    @property
    def parent( self ):
        return self.__parent

    def set( self, arguments ):
        for name, attributes in arguments.items():
            if hasattr( self, name ):
                getattr( self, name ).set( **attributes )

            else:
                setattr( self, name, ControlProperty( name, **attributes ) )

        return

    def get( self, arguments ):
        return


    def dump( self ):
        for attr in self.__attributes:
            print( "{}.{} = {}".format( self.name, attr, getattr( self, attr ) ) )

        return

    def getOptions( self, ui = None ):
        options = []
        for attr in self.__attributes:
            value = None
            if ui.isSet( attr ):
                value = ui.get( attr )

            if value is None:
                value = getattr( self, attr )
                if not value.isSet():
                    continue

                value = str( value )

            if value is None:
                continue

            options.append( '{}="{}"'.format( attr, value ) )

        return ' '.join( options )

    def build( self, field, table, obj, root ):
        return Template( self.__htmlTemplate ).render( this = self,
                                                       field = field,
                                                       table = table,
                                                       obj = obj,
                                                       root = root )



class DymanicControls( object ):
    def __init__( self ):
        self.__controls = {}
        return

    def append( self, obj ):
        self.__controls[ obj.name ] = obj
        return

    def get( self, name ):
        if name in self.__controls:
            return self.__controls[ name ]

        return None

    def dump( self ):
        for name, control in self.__controls.items():
            print( "{} : ".format( name ) )
            control.dump()


def main():
    ctrls = DymanicControls()

    filename = '/home/mbertens/src/python/pytemplate/gencrud/templates/pyt-controls.yaml'
    with open( filename, 'r' ) as stream:
        cfg = yaml.load( stream, Loader = yaml.Loader )

    for name, value in cfg.items():
        if any(c.islower() for c in name):
            ctrls.append( TemplateDymanicControl( ctrls,
                                                  name,
                                                  arguments = value[ 'properties' ],
                                                  htmlTemplate = value[ 'html' ] ) )


    obj = ctrls.get( 'password' )
    obj.hint.value = "This is a TEST to set the dynamic property"
    obj.error.value = True

    obj.dump()
    obj.hint.value = None
    data = { 'hint':        { 'default': 'This is the second text', 'type': 'str' },
             'minLength':   { 'default': 8, 'type': 'int' },
             'maxLength':   { 'default': 32, 'type': 'int' },
             'allowed':     { 'default': [ 'lower', 'upper', 'digit' ], 'type': 'list' } }
    obj.set( data )
    obj.dump()
    obj.maxLength.value = 64
    obj.dump()

    inputFile = '/home/mbertens/src/angular/mat-table-crud/templates/systems.yaml'
    with open( inputFile, 'r' ) as stream:
        config = TemplateConfiguration( **yaml.load( stream ) )

    for obj in config:
        print( "Object name: {}".format( obj.name ) )
        for fld in obj.table:
            print( "Field name: {}".format( fld.name ) )
            print( fld.build( ctrls, config ) )


if __name__ == '__main__':
    import yaml
    import io
    import copy
    from gencrud.configuraton import TemplateConfiguration

    main()
