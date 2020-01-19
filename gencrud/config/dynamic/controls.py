from gencrud.config.dynamic.control import TemplateDymanicControl


class DymanicControls( object ):
    def __init__( self, controls ):
        self.__cfg = controls
        self.__controls = {}
        self.parse()
        return

    def parse( self ):
        for name, value in self.__cfg.items():
            # all types shall be in lowercase
            if any( c.islower() for c in name ):
                # Add new control
                self.__controls[ name ] = TemplateDymanicControl( self,
                                              name,
                                              arguments = value[ 'properties' ],
                                              htmlTemplate = value[ 'html' ] )

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

