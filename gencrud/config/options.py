from gencrud.constants import *
import gencrud.util.utils
from gencrud.config.base import TemplateBase


class TemplateOptions( TemplateBase ):
    def __init__( self, **cfg ) -> None:
        TemplateBase.__init__( self, None )
        self.__config = cfg
        return

    @property
    def useModule( self ) -> bool:
        # This override/set commandline options from the template defintion.
        return self.__config.get( C_USE_MODULE, gencrud.util.utils.useModule )

    @property
    def backupFiles( self ) -> bool:
        # This override/set commandline options from the template defintion.
        return self.__config.get( C_BACKUP, gencrud.util.utils.backupFiles )

    @property
    def ignoreCaseDbIds( self ) -> bool:
        # This override/set commandline options from the template defintion.
        return self.__config.get( C_IGNORE_CASE_DB_IDS, gencrud.util.utils.ignoreCaseDbIds )

    @property
    def overWriteFiles( self ) -> bool:
        # This override/set commandline options from the template defintion.
        return self.__config.get( C_OVERWRITE, gencrud.util.utils.overWriteFiles )

    @property
    def lazyLoading( self ) -> bool:
        # This override/set commandline options from the template defintion.
        return self.__config.get( C_LAZY_LOADING, gencrud.util.utils.lazyLoading )

    @property
    def generateFrontend( self ) -> bool:
        # This override/set commandline options from the template defintion.
        return self.__config.get( C_GENERATE_FRONTEND, True )

    @property
    def generateBackend( self ) -> bool:
        # This override/set commandline options from the template defintion.
        return self.__config.get( C_GENERATE_BACKEND, True )
