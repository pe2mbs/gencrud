from gencrud.config.base import TemplateBase
from gencrud.constants import *
import posixpath

class AngularModule( TemplateBase ):
    def __init__( self,parent, **cfg ):
        TemplateBase.__init__( self,parent )
        self.__config = cfg
        return

    @property
    def path( self ):
        return self.__config.get( C_PATH, self.get_default( C_PATH ) )

    @property
    def cls( self ):
        return self.__config.get( C_CLASS, self.get_default( C_MODULE ) )

    @property
    def module( self ):
        return self.__config.get( C_MODULE, "module" )

    @property
    def importPath( self ):
        if '.' in self.path or '/' in self.path:
            # seems to be a full path
            path = posixpath.join( self.path, self.module )

        else:
            # Another module should be one level up in the filesystem
            path = posixpath.join( "..", self.path, self.module )

        return path

    # "import {{ {modCls} }} from '{path}';".format( modCls = mod.module, path = path ) )


class AngularModules( TemplateBase ):
    def __init__( self, parent, cfg ):
        TemplateBase.__init__( self, parent )
        self.__config       = []
        for i in cfg:
            self.__config.append( AngularModule( self, **i ) )

        return

    def __iter__( self ):
        return iter( self.__config )

    @property
    def items(self):
        return self.__config
