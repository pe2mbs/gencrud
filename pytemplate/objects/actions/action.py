
from pytemplate.util.utils import InvalidSetting


class TemplateAction( object ):
    def __init__( self, obj_name, **cfg ):
        self.__name = obj_name
        self.__cfg = cfg
        return

    def clone( self, obj_name ):
        return TemplateAction( obj_name,
                               name = self.name,
                               label = self.label,
                               type = self.type,
                               icon = self.icon,
                               position = self.position,
                               function = self.function )


    @property
    def name( self ):
        result = self.__cfg.get( 'name', None )
        if result is None:
            raise InvalidSetting( 'name', 'action', self.name )

        return result

    @property
    def type( self ):
        result = self.__cfg.get( 'type', 'dialog' )
        if result not in ( 'dialog', 'screen', 'list', 'none' ):
            raise InvalidSetting( 'name', 'action', self.name )

        return result

    @property
    def position( self ):
        result = self.__cfg.get( 'position', 'cell' )
        if result not in ( 'cell', 'header', 'footer', 'row' ):
            raise InvalidSetting( 'position', 'action', self.name )

        return result

    @property
    def label( self ):
        return self.__cfg.get( 'label', '' )

    @property
    def icon( self ):
        return self.__cfg.get( 'icon', '' )

    @property
    def position( self ):
        return self.__cfg.get( 'position', 'row' )

    @property
    def function( self ):
        return self.__cfg.get( 'function', '' )

    @property
    def source( self ):
        return self.__cfg.get( 'source', '' )

    @property
    def uri( self ):
        return self.__cfg.get( 'uri', '' )

    @property
    def param( self ):
        return self.__cfg.get( 'param', [] )

    def buttonObject( self ):
        if self.type == 'none':
            return ''

        button = 'mat-raised-button'
        content = self.label
        if self.icon != '':
            button = 'mat-icon-button'
            content = '<mat-icon aria-label="{label}">{icon}</mat-icon>'.format( label = self.label,
                                                                                 icon = self.icon )
        function = self.function
        if self.function == '' and self.uri != '':
            params = []
            for key, value in self.param:
                params.append( "'{}=' + {}".format( key, value ) )

            param = '&'.join( params )
            if len( param ) > 0:
                param = '?' + param

            function = "genericPut( '{uri}', '{param}' )".format( uri = self.uri,
                                                                   param = param )

        button = '''<span class="spacer"></span>
            <button {button}
                    color="primary"
                    (click)="{function}"
                    id="{objname}.{name}">
                {content}
            </button>'''.format( button = button,
                                 function = function,
                                 objname = self.__name,
                                 name = self.name,
                                 content = content )

        return button




DEFAULT_NEW_ACTION      = TemplateAction( 'internal_action',
                                          name = 'new',
                                          label = 'Add a new record',
                                          type = 'dialog',
                                          icon = 'add',
                                          position = 'header',
                                          function = 'addNew()' )
DEFAULT_DELETE_ACTION   = TemplateAction( 'internal_action',
                                          name = 'delete',
                                          label = 'Delete a record',
                                          type = 'dialog',
                                          icon = 'delete',
                                          position = 'cell',
                                          function = 'deleteItem( i, row )' )
DEFAULT_EDIT_ACTION     = TemplateAction( 'internal_action',
                                          name = 'edit',
                                          label = 'Edit a record',
                                          type = 'dialog',
                                          position = 'row',
                                          function = 'startEdit( i, row )' )
