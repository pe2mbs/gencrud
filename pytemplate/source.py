import os
import logging
import pytemplate.util.utils
import pathlib
from pytemplate.util.exceptions import MissingTemplate

logger = logging.getLogger()


class TemplateSource( object ):
    def __init__( self, type, current_path, **cfg ):
        if 'templates' in cfg:
            if pathlib.Path( cfg[ 'templates' ][ type ] ).is_absolute():
                self.__template = os.path.abspath( cfg[ 'templates' ][ type ] )

            else:
                self.__template = os.path.abspath( os.path.join( current_path, cfg[ 'templates' ][ type ] ) )

        else:
            self.__template = os.path.abspath( os.path.join( os.path.dirname( __file__ ), 'templates', type ) )

        logger.info( 'Template folder: {0}'.format( self.__template ) )
        cnt = 0
        for templ_file in os.listdir( self.__template ):
            if os.path.splitext( templ_file )[ 1 ] == '.templ':
                cnt += 1

        if cnt == 0:
            raise MissingTemplate( self.__template )

        if pathlib.Path( cfg[ 'source' ][ type ] ).is_absolute():
            self.__source   = os.path.abspath( cfg[ 'source' ][ type ] )

        else:
            self.__source   = os.path.abspath( os.path.join( current_path, cfg[ 'source' ][ type ] ) )

        return

    @property
    def source( self ):
        return self.__source

    @property
    def template( self ):
        return self.__template

