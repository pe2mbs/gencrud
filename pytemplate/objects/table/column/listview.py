import logging
import json

logger = logging.getLogger()


class TemplateListView( object ):
    def __init__( self, parent, **cfg ):
        self.__parent   = parent
        self.__cfg      = cfg
        return

    @property
    def width( self ):
        if 'width' not in self.__cfg:
            return self.__parent.css.width

        return self.__cfg.get( 'width', None )

    @property
    def index( self ):
        if 'index' not in self.__cfg:
            return self.__parent.index

        return self.__cfg.get( 'index', None )
