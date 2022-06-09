import enum
from gencrud.config.base import TemplateBase
from gencrud.constants import *


class ElementType( enum.Enum ):
    DIALOG      = 1
    COMPONENT   = 2
    SERVICE     = 3
    MODULE      = 4


class InjectionElementTemplate( TemplateBase ):
    def __init__( self, parent, _type, cfg: dict ):
        TemplateBase.__init__( self, parent )
        self.__config   = cfg
        self.__type     = _type
        return

    @property
    def type( self ) -> ElementType:
        return self.__type

    def hasClass( self ):
        return C_CLASS in self.__config

    @property
    def cls( self ):
        return self.__config.get( C_CLASS )

    @property
    def file( self ):
        return self.__config.get( C_FILE )

    @property
    def export( self ):
        return self.__config.get( C_EXPORT, False )


class InjectionBlockTemplate( TemplateBase ):
    def __init__( self, parent, cfg: dict ):
        TemplateBase.__init__( self,parent )
        self.__config = cfg
        self.__components = []
        for elem in self.__config.get( C_DIALOGS, [] ):
            self.__components.append( InjectionElementTemplate( self, ElementType.DIALOG, elem ) )

        for elem in self.__config.get( C_COMPONENTS, [] ):
            self.__components.append( InjectionElementTemplate( self, ElementType.COMPONENT, elem ) )

        for elem in self.__config.get( C_SERVICES, [] ):
            self.__components.append( InjectionElementTemplate( self, ElementType.SERVICE, elem ) )

        for elem in self.__config.get( C_MODULES, [] ):
            self.__components.append( InjectionElementTemplate( self, ElementType.MODULE, elem ) )

        return

    @property
    def declaredClasses( self ):
        return [ obj.cls for obj in self.__components ]

    def hasDeclarations( self ):
        return len( self.declarations ) > 0

    @property
    def declarations( self ):
        return ",\n".join( [ obj.cls for obj in self.__components if obj.type in ( ElementType.DIALOG, ElementType.COMPONENT ) ] )

    def hasExports( self ):
        return len( self.exports ) > 0

    @property
    def exports( self ):
        return ",\n".join( [ obj.cls for obj in self.__components if obj.export ] )

    def hasImports( self ):
        return len( self.imports ) > 0

    @property
    def imports( self ):
        return ",\n".join( [ obj.cls for obj in self.__components if obj.type == ElementType.MODULE ] )

    def hasEntryComponents( self ):
        return len( self.entryComponents ) > 0

    @property
    def entryComponents( self ):
        return ",\n".join( [ obj.cls for obj in self.__components if obj.type == ElementType.DIALOG ] )

    def hasProviders( self ):
        return len( self.providers ) > 0

    @property
    def providers( self ):
        return ",\n".join( [ obj.cls for obj in self.__components if obj.type == ElementType.SERVICE ] )

    def needDeclareImports( self ):
        return len( self.__components ) > 0

    @property
    def declareImports( self ):
        return "\n".join( [ "import {{ {} }} from '{}';".format( obj.cls, obj.file ) for obj in self.__components ] )

    #
    # def hasEntryComponents( self ):
    #     return self.hasDialog()
    #
    # @property
    # def entryComponents( self ):
    #     declare = [ ]
    #     if self.hasDialog():
    #         declare.append( self.dialogComponent() )
    #
    #     if len( declare ) > 0:
    #         return ", ".join( declare )
    #
    #     return ""
    #
    # def hasExports( self ):
    #     return self.hasDialog() or self.hasScreen() or self.hasProviders()
    #
    # @property
    # def exports( self ):
    #     declare = []
    #     if self.hasDialog():
    #         declare.append( self.dialogComponent() )
    #
    #     if self.hasScreen():
    #         declare.append( self.screenComponent() )
    #
    #     if self.hasImports():
    #         declare.append( self.imports )
    #
    #     if len( declare ) > 0:
    #         return ", ".join( declare )
    #
    #     return ""
    #
    # def hasScreen( self ):
    #     return C_SCREEN in self.__config
    #
    # def screenComponent( self ):
    #     return self.__config.get( C_SCREEN, None )
    #
    # def hasDialog( self ):
    #     return C_DIALOG in self.__config
    #
    # def dialogComponent( self ):
    #     return self.__config.get( C_DIALOG, None )
    #
    # def hasProviders( self ):
    #     return C_PROVIDERS in self.__config
    #
    # @property
    # def providers( self ):
    #     declare = [ ]
    #     if self.hasProviders():
    #         for provider in self.__config.get( C_PROVIDERS, [] ):
    #             declare.append( provider )
    #
    #     if len( declare ) > 0:
    #         return ", ".join( declare )
    #
    #     return ""
    #
    # def hasImports( self ):
    #     return C_IMPORTS in self.__config
    #
    # @property
    # def imports( self ):
    #     declare = []
    #     if self.hasImports():
    #         for filename, objectName in self.__config.get( C_IMPORTS, {} ).items():
    #             declare.append( objectName )
    #
    #     if len( declare ) > 0:
    #         return ", ".join( declare )
    #
    #     return ""



class InjectionTemplate( TemplateBase ):
    def __init__( self,parent, cfg ):
        TemplateBase.__init__( self, parent )
        self.__config   = cfg
        self.__moduleTs = InjectionBlockTemplate( self, self.__config.get( 'module.ts', {} ) )
        return

    def hasModuleTs( self ):
        return 'module.ts' in self.__config

    @property
    def moduleTs( self ):
        return self.__moduleTs
