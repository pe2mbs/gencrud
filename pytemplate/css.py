


class TemplateCss( object ):
    def __init__( self, no_columns, **cfg ):
        self.noColumns = no_columns
        self.data = cfg
        return

    @property
    def width( self ):
        return self.data.get( 'width', int( 97 / self.noColumns ) )

