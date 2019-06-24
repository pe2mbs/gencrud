from pytemplate.objects.actions.action import ( TemplateAction,
                                                DEFAULT_DELETE_ACTION,
                                                DEFAULT_EDIT_ACTION,
                                                DEFAULT_NEW_ACTION )


class TemplateActions( object ):
    def __init__( self, objname, cfg ):
        self.__name = objname
        self.__actions = []
        self.__cfg = cfg
        for action in cfg:
            self.__actions.append( TemplateAction( objname, **action ) )

        if not self.has( 'new' ):
            self.__actions.append( DEFAULT_NEW_ACTION.clone( objname ) )

        if not self.has( 'edit' ):
            self.__actions.append( DEFAULT_EDIT_ACTION.clone( objname ) )

        if not self.has( 'delete' ):
            self.__actions.append( DEFAULT_DELETE_ACTION.clone( objname ) )

        return

    def __iter__( self ):
        return iter( self.__actions )

    def has( self, key ):
        for action in self.__actions:
            if action.name == key:
                return True

        return False

    def get( self, key ):
        for action in self.__actions:
            if action.name == key:
                return action

        raise Exception( "Missing {} in actions of {}".format( key, self.__name ) )

    def getCustomButtons( self ):
        result = []
        for action in self.__actions:
            if action.name not in ( 'new', 'edit', 'delete' ):
                result.append( action )

        return result

    def getHeaderButtons( self ):
        result = []
        for action in self.__actions:
            if action.position == 'header' and action.type != 'none':
                result.append( action )

        return result

    def getCellButtons( self ):
        result = []
        for action in self.__actions:
            if action.position == 'cell' and action.type != 'none':
                result.append( action )

        return result

    def getRowAction( self ):
        for action in self.__actions:
            if action.position == 'row' and action.type != 'none':
                return action

        return None

    def getFooterButtons( self ):
        result = []
        for action in self.__actions:
            if action.position == 'footer' and action.type != 'none':
                result.append( action )

        return result

    def valid( self, name, _type ):
        for action in self.__actions:
            if action.name == name and action.type == _type:
                return action.position != 'none'

        return False