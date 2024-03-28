from gencrud.config.base import TemplateBase
from gencrud.constants import *


class Interface( TemplateBase ):
    def __init__( self, parent, **cfg ):
        TemplateBase.__init__(self, parent)
        self.__cfg = cfg
        return

    @property
    def Backend(self) -> str:
        return self.__cfg.get( C_BACKEND, None )

    @property
    def Frontend(self) -> str:
        return self.__cfg.get( C_FRONTEND, None )

    @property
    def Module(self) -> str:
        return self.__cfg.get( C_MODULE, None )

    @property
    def Package( self ) -> str:
        return self.Backend.replace('/','.').replace('\\','.')