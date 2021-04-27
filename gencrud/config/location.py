import os
from gencrud.constants import *
from gencrud.config.base import TemplateBase


class LocationTemplateClass( TemplateBase ):
    def __init__( self, parent, cfg, source, common = None ):
        TemplateBase.__init__( self, parent )
        self.__type     = source
        self.__config   = cfg.get( self.platform, cfg ).get( source, {} )
        rootPath = os.environ.get( 'GENCRUD_TEMPLATES', None )
        if rootPath is None:
            rootPath = os.environ.get( 'GENCRUD', None )
            if rootPath is not None:
                rootpath = os.path.join( rootPath, 'templates' )

            else:
                rootpath = os.path.join( os.path.dirname( __file__ ), '..', source )

            self.__base     = self.__config.get( C_BASE, os.path.abspath( rootpath ) )

        if common is not None:
            self.__common = LocationTemplateClass( self, self.__config, common )

        else:
            self.__common = None

        return

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

    @property
    def common( self ) -> object:
        return self.__common

    def __str__(self):
        return "<LocationTemplateClass {} python={}\n{}angular={}>".format( self.__type,
                                                                            self.python,
                                                                            " " * 21,
                                                                            self.angular )


class TemplateLocation( LocationTemplateClass ):
    def __init__( self, parent, cfg ):
        LocationTemplateClass.__init__( self, parent, cfg, C_TEMPLATE, 'common' )
        return


class SourceLocation( LocationTemplateClass ):
    def __init__( self, parent, cfg ):
        LocationTemplateClass.__init__( self, parent, cfg, C_SOURCE )
        return
