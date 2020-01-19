from mako.template import Template
from gencrud.config.dynamic.property import ControlProperty


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
