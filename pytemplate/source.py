import os

import pytemplate.util.utils


class TemplateSource( object ):
    def __init__( self, type, **cfg ):
        if 'templates' in cfg:
            self.__template = os.path.abspath( cfg[ 'templates' ][ type ] )

        else:
            self.__template = os.path.abspath( os.path.join( os.path.dirname( __file__ ), 'templates', type ) )

        if pytemplate.util.utils.verbose:
            print( 'Template folder: {0}'.format( self.__template ) )

        cnt = 0
        for templ_file in os.listdir( self.__template ):
            if os.path.splitext( templ_file )[ 1 ] == '.templ':
                cnt += 1

        if cnt == 0:
            raise Exception( 'No templates found in {0}'.format( self.__template ) )

        self.__source   = os.path.abspath( cfg[ 'source' ][ type ] )
        return

    @property
    def source( self ):
        return os.path.abspath( os.path.normpath( self.__source ) )

    @property
    def template( self ):
        return os.path.abspath( os.path.normpath( self.__template ) )

