#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2019 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation; either version 2 of the
#   License, or (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#   Library General Public License for more details.
#
#   You should have received a copy of the GNU Library General Public
#   License GPL-2.0-only along with this library; if not, write to the
#   Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301 USA
#
import logging
from gencrud.util.typescript import TypeScript
from gencrud.util.exceptions import InvalidSetting
from gencrud.objects.actions.route import RouteTemplate

logger = logging.getLogger()

TYPES       = ( 'dialog', 'screen', 'list', 'api', 'none' )
POSITIONS   = ( 'cell', 'header', 'footer', 'row', 'none' )
ATTRIBUTES  = ( 'function', 'name', 'label', 'icon', 'source', 'position', 'type', 'uri', 'route', 'param', 'on' )
ON_ACTIONS  = ( 'click', 'dblclick' )

class TemplateAction( object ):
    def __init__( self, parent, obj_name, **cfg ):
        self.__parent = parent
        self.__name = obj_name
        self.__cfg = cfg
        return

    @property
    def name( self ):
        result = self.__cfg.get( 'name', None )
        if result is None:
            raise InvalidSetting( 'name', 'action', self.name )

        return result

    @property
    def type( self ):
        result = self.__cfg.get( 'type', TYPES[ -1 ] )
        if result not in TYPES:
            raise InvalidSetting( 'name', 'action', self.name )

        return result

    @property
    def position( self ):
        result = self.__cfg.get( 'position', POSITIONS[ -1 ] )
        if result not in POSITIONS:
            raise InvalidSetting( 'position', 'action', self.name )

        return result

    @property
    def on( self ):
        value = self.__cfg.get( 'on', 'dblclick' if self.position == 'row' else 'click' )
        if value not in ON_ACTIONS:
            raise Exception( "invalid 'on' value, must be one of {}".format( ', '.join( ON_ACTIONS ) ) )

        return value

    @property
    def label( self ):
        return self.__cfg.get( 'label', '' )

    @property
    def icon( self ):
        return self.__cfg.get( 'icon', '' )

    @property
    def function( self ):
        return self.__cfg.get( 'function', '' )

    def set( self, attr, value ):
        if attr not in ATTRIBUTES:
            raise Exception( "Invalid attribute '{}' for Action with value '{}'".format( attr, value ) )

        self.__cfg[ attr ] = value
        return

    @property
    def source( self ):
        return self.__cfg.get( 'source', '' )

    @property
    def uri( self ):
        return self.__cfg.get( 'uri', '' )

    def isAngularRoute( self ):
        return 'route' in self.__cfg

    @property
    def hint( self ):
        return self.__cfg.get( 'hint', '' )

    @property
    def color( self ):
        return self.__cfg.get( 'color', 'primary' )

    @property
    def css( self ):
        return self.__cfg.get( 'css', '' )

    @property
    def route( self ):
        return RouteTemplate( self, **self.__cfg.get( 'route', None ) ) if self.isAngularRoute() else {}

    @property
    def params( self ):
        return self.__cfg.get( 'params', {} )

    def routeParams( self ):
        params = self.params
        if len( params ) > 0:
            items = {}
            for key, value in params.items():
                items[ key ] = value
            # (click) = "router.navigate( [ '/tr/edit', { queryParams: { id: 'TR_ID', mode: 'edit', value: row.TR_ID } } ] )"
            return '{{ queryParams: {} }}'.format( TypeScript().build( items ) )

        return ''

    #
    #   Internal functions and properies to gencrud
    #
    def hasApiFunction( self ):
        return 'function' in self.__cfg

    def clone( self, obj_name ):
        return TemplateAction( self.__parent,
                               obj_name,
                               name = self.name,
                               label = self.label,
                               type = self.type,
                               icon = self.icon,
                               position = self.position,
                               function = self.function )

    def buttonObject( self ):
        tooltip = ''
        if self.type == 'none':
            return ''

        button_type = 'mat-raised-button'
        content = self.label
        if self.icon != '':
            button_type = 'mat-icon-button'
            content = '<mat-icon aria-label="{label}">{icon}</mat-icon>'.format( label = self.label,
                                                                                 icon = self.icon )

            tooltip = 'matTooltip = "{}"'.format( self.label )
        else:
            if self.hint != '':
                tooltip = 'matTooltip = "{}"'.format( self.hint )

        function = ''
        if self.function == '' and self.uri != '':
            param = TypeScript().build( self.params )
            function = "dataService.genericPut( '{uri}', {param} )".format( uri = self.uri,
                                                                              param = param )

        else:
            function = self.function

        button = '<span class="spacer"></span>'
        logger.info( "function: {}\nroute: {}".format( function, "/".join( [ self.__parent.name if self.__parent is not None else '',
                                                                             self.route.name if isinstance( self.route, RouteTemplate ) else '?' ] ) ) )
        cls = ''
        if self.css != '':
            cls = 'class="{}"'.format( self.css )

        if function != '':
            BUTTON_STR = '''<button {cls} {button} {tooltip} color="{color}" ({on})="{function}" id="{objname}.{name}">{content}</button>'''
            route = ''
            params = ''

        elif self.isAngularRoute():
            BUTTON_STR = '''<a {cls} {button} {tooltip} color="{color}" ({on})="router.navigate( ['/{route}'], {params} )" id="{objname}.{name}">{content}</a>'''
            route = "/".join( [ self.__parent.name, self.route.name ] )
            params = self.routeParams()

        elif self.type == 'screen' and self.name in ( 'new', 'edit' ):
            BUTTON_STR = '''<a {cls} {button} {tooltip} color="{color}" ({on})="router.navigate( ['/{route}'], {params} )" id="{objname}.{name}">{content}</a>'''
            route = "/".join( [ self.__parent.name, self.name ] )
            params = {}

        else:
            raise Exception( 'Missing function or route for {}'.format( self ) )

        return button + BUTTON_STR.format( button = button_type,
                                           route = route,
                                           cls = cls,
                                           params = params,
                                           color = self.color,
                                           function = function,
                                           tooltip = tooltip,
                                           on = self.on,
                                           objname = self.__name,
                                           name = self.name,
                                           content = content )

    def __repr__(self):
        return "<TemplateAction *{}* name = '{}', label = '{}', type = {}, icon = {}, position = {}, function = '{}' route = {}>".format(
            self.__name, self.name, self.label, self.type, self.icon, self.position, self.function, self.route
        )


DEFAULT_NEW_ACTION      = TemplateAction( None,
                                          'internal_action',
                                          name = 'new',
                                          label = 'Add a new record',
                                          type = 'dialog',
                                          icon = 'add',
                                          position = 'header',
                                          function = 'addRecord()' )
DEFAULT_DELETE_ACTION   = TemplateAction( None,
                                          'internal_action',
                                          name = 'delete',
                                          label = 'Delete a record',
                                          type = 'dialog',
                                          icon = 'delete',
                                          position = 'cell',
                                          function = 'deleteRecord( i, row )' )
DEFAULT_EDIT_ACTION     = TemplateAction( None,
                                          'internal_action',
                                          name = 'edit',
                                          label = 'Edit a record',
                                          type = 'dialog',
                                          position = 'row',
                                          function = 'editRecord( i, row )' )
