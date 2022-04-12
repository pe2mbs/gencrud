import os
from gencrud.constants import *
from gencrud.config.base import TemplateBase


class LocationTemplateClass( TemplateBase ):
    def __init__( self, parent, cfg, source, common = None, root_path = None ):
        TemplateBase.__init__( self, parent )
        self.__type     = source
        self.__config   = cfg.get( self.platform, cfg ).get( source, cfg )
        root_path = os.environ.get( 'GENCRUD_TEMPLATES', root_path )
        if root_path is None:
            root_path = os.environ.get( 'GENCRUD', None )
            if root_path is not None:
                root_path = os.path.join( rootPath, 'templates' )

            else:
                root_path = os.path.join( os.path.dirname( __file__ ), '..', source )

            self.__base     = self.__config.get( C_BASE, os.path.abspath( root_path ) )

        else:
            self.__base     = root_path

        if common is not None:
            self.__base = os.path.join( self.__base, common )

        return

    @property
    def base( self ) -> str:
        return self.__base

    @property
    def python( self ) -> str:
        path = self.__config.get( C_PYTHON, C_PYTHON )
        if path.startswith( os.path.sep ):
            return path

        return os.path.abspath( os.path.join( self.__base, path ) )

    @property
    def angular( self ) -> str:
        path = self.__config.get( C_ANGULAR, C_ANGULAR )
        if path.startswith( os.path.sep ):
            return path

        return os.path.abspath( os.path.join( self.__base, path ) )

    def __str__(self):
        return "<LocationTemplateClass {} python={}\n{}angular={}>".format( self.__type,
                                                                            self.python,
                                                                            " " * 21,
                                                                            self.angular )


class TemplateLocation( LocationTemplateClass ):
    def __init__( self, parent, cfg ):
        LocationTemplateClass.__init__( self, parent, cfg, C_TEMPLATE )
        self.__common = LocationTemplateClass( parent, cfg, C_TEMPLATE, common = 'common', root_path = self.base )
        return

    @property
    def common( self ) -> object:
        return self.__common

class SourceLocation( LocationTemplateClass ):
    def __init__( self, parent, cfg ):
        LocationTemplateClass.__init__( self, parent, cfg, C_SOURCE )
        return
