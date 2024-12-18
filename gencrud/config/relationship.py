from gencrud.config.base import TemplateBase


class TemplateRelationShip( TemplateBase ):
    def __init__( self, parent, **relationship ):
        super().__init__( parent )
        self.__name = relationship[ 'name' ]
        self.__model = relationship[ 'model' ]
        self.__populates = relationship[ 'populates' ]
        self.__cascade = relationship.get( 'cascade' )
        self.__singleParent = relationship.get('single-parent')
        return

    def _getCascade( self ) -> str:
        cascade = ''
        if isinstance( self.__cascade, str ):
            cascade = f", cascade = '{ self.__cascade }'"

        return cascade

    def modelRelationShip( self ) -> str:
        extra = ''
        if self.__singleParent:
            extra = ", single_parent = True"

        return f"{self.__name} = API.db.relationship( '{ self.__model }', back_populates = '{ self.__populates }'{ self._getCascade() }{ extra } )"

    def __repr__( self ):
        cascade = ''
        if isinstance(self.__cascade, str):
            cascade = f", cascade = '{self.__cascade}'"

        return f"<RelationShip name='{self.__name}' model='{ self.__model }' back_populates='{ self.__populates }'{ self._getCascade() }>"