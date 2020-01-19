
class TemplateBase( object ):
    def __init__( self, parent ):
        self.__parent = parent
        return

    @property
    def parent( self ):
        return self.__parent

