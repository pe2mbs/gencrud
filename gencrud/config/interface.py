from gencrud.config.base import TemplateBase
from gencrud.config.source import TemplateSourcePython
from gencrud.constants import *
#   interface:
#       backend:
#           target:         VirtualTableDemo
#           class:          VirtualTable
#           file:           webapp2.commin.virual_table
#           # This overrides the template in the main configuration
#           templates:
#               python:     examples\templates_v10\templates\virtual\py


class InterfaceBackend( TemplateBase ):
    def __init__( self, parent, **cfg ):
        TemplateBase.__init__( self, parent )
        self.__cfg = cfg
        return

    @property
    def TargetClass( self ):
        return self.__cfg.get( C_TARGET_CLASS, None )

    @property
    def Cls( self ):
        return self.__cfg.get( C_CLASS, None )

    @property
    def File( self ):
        return self.__cfg.get( C_FILE, None )

    @property
    def Templates( self ):
        obj = TemplateSourcePython( **self.__cfg.get( C_TEMPLATES, {} ) )
        if not obj.hasBaseFolder() and not obj.isTemplateFolderAbs():
            # the the correct BASE folder
            obj.set( C_BASE, self.Root.Templates.templateBaseFolder )

        return obj


class Interface( TemplateBase ):
    def __init__( self, parent, **cfg ):
        TemplateBase.__init__(self, parent)
        self.__cfg = cfg
        return

    def hasBackend(self):
        return self.__cfg.get( C_BACKEND, None ) is not None

    @property
    def Backend(self):
        return InterfaceBackend( self, **self.__cfg.get( C_BACKEND, None ) )

    # TODO: These are not yet supported
    # def hasFrondend(self):
    #     return self.__cfg.get( C_FRONTEND, None) is not None
    #
    # @property
    # def Frontend(self):
    #     return InterfaceFrontend( self, **self.__cfg.get( C_FRONTEND, None ) )

