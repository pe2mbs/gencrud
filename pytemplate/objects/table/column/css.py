import logging

logger = logging.getLogger()


class TemplateCss( object ):
    def __init__( self, no_columns, **cfg ):
        self.noColumns = no_columns
        self.data = cfg

        if 'width' in cfg:
            logger.warning( "the propery 'width' in 'css' is OBSOLETE, use 'listview' -> 'width' in the field definition." )

        return

    # OBSOLETE: use the columns.listview.width
    @property
    def width( self ):
        return self.data.get( 'width', int( 97 / self.noColumns ) )

    @property
    def cls( self ):
        return self.data.get( 'class', '' )