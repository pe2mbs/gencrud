from gencrud.constants import *


class TemplateAngularModule( object ):
    def __init__( self, default_filename, default_class, default_module = None, **cfg ):
        self.__filename = default_filename
        self.__class = default_class
        self.__module = default_module or default_class
        self.__config = cfg
        return

    @property
    def filename( self ) -> str:
        return self.__config.get( C_FILENAME, self.__filename )

    @property
    def cls( self ) -> str:
        return self.__config.get( C_CLASS, self.module if self.__class is None else self.__class )

    @property
    def module( self ) -> str:
        return self.__config.get( C_MODULE, self.__module )