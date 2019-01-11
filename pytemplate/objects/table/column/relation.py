


class TemplateRelation( object ):
    def __init__( self, field, **cfg ):
        self.__field        = field
        self.__cfg          = cfg
        return

    @property
    def name( self ):
        return self.__cfg.get( 'name', None )

    @property
    def fieldName( self ):
        return self.__cfg.get( 'field-name', self.__field.name + '_REL' )

    @property
    def cls( self ):
        return self.__cfg.get( 'class', None )

    @property
    def tableName( self ):
        return self.__field.tableName

    @property
    def lazy( self ):
        return self.__cfg.get( 'lazy', 'True' )