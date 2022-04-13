#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2020 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation.
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
from gencrud.config.route import RouteTemplate
from gencrud.constants import *
from gencrud.config.base import TemplateBase

logger = logging.getLogger()


class TemplateAction( TemplateBase ):
    def __init__( self, parent, obj_name, **cfg ):
        TemplateBase.__init__( self, parent )
        self.__name = obj_name
        self.__cfg = cfg
        return

    @property
    def module( self ):
        return self.parent.module

    @property
    def name( self ):
        result = self.__cfg.get( C_NAME, None )
        if result is None:
            raise InvalidSetting( C_NAME, C_ACTION, self.name )

        return result

    @property
    def type( self ):
        result = self.__cfg.get( C_TYPE, C_ACTION_TYPES[ -1 ] )
        if result not in C_ACTION_TYPES:
            raise InvalidSetting( C_TYPE, C_ACTION, self.name )

        return result

    @property
    def position( self ):
        result = self.__cfg.get( C_POSITION, C_ACTION_POSITIONS[ -1 ] )
        if result not in C_ACTION_POSITIONS:
            raise InvalidSetting( C_POSITION, C_ACTION, self.name )

        return result

    @property
    def on( self ):
        value = self.__cfg.get( C_ON, C_DOUBLE_CLICK if self.position == C_ROW else C_CLICK )
        if value not in C_ACTION_ON_ACTIONS:
            raise Exception( "invalid 'on' value, must be one of {}".format( ', '.join( C_ACTION_ON_ACTIONS ) ) )

        return value

    @property
    def label( self ):
        return self.__cfg.get( C_LABEL, "{}{}".format( self.name[0].upper(), self.name[1:].lower() ) )

    @property
    def icon( self ):
        return self.__cfg.get( C_ICON, '' )

    @property
    def function( self ):
        return self.__cfg.get( C_FUNCTION, '' )

    def set( self, attr, value ):
        if attr not in C_ACTION_ATTRIBUTES:
            raise Exception( "Invalid attribute '{}' for Action with value '{}'".format( attr, value ) )

        self.__cfg[ attr ] = value
        return

    def get( self, attr, default = None ):
        return self.__cfg.get( attr, default )

    @property
    def source( self ) -> str:
        return self.__cfg.get( C_SOURCE, '' )

    @property
    def uri( self ) -> str:
        return self.__cfg.get( C_URI, '' )

    @property
    def disabled( self ) -> str:
        return self.__cfg.get( 'disabled', 'false' )

    def hasDisabed( self ) -> bool:
        return 'disabled' in self.__cfg

    def isAngularRoute( self ) -> bool:
        return C_ROUTE in self.__cfg

    @property
    def hint( self ) -> str:
        return self.__cfg.get( C_HINT, '' )

    @property
    def color( self ) -> str:
        return self.__cfg.get( C_COLOR, 'primary' )

    @property
    def css( self ) -> str:
        return self.__cfg.get( C_CSS, '' )

    @property
    def route( self ) -> RouteTemplate:
        return RouteTemplate( self, **self.__cfg.get( C_ROUTE, None ) ) if self.isAngularRoute() else None

    @property
    def params( self ):
        return self.__cfg.get( C_PARAMS, {} )

    def routeParams( self ) -> str:
        params = self.params
        if len( params ) > 0:
            items = {}
            for key, value in params.items():
                items[ key ] = value

            return '{{ queryParams: {} }}'.format( items )

        return '{ }'

    #
    #   Internal functions and properies to gencrud
    #
    def hasApiFunction( self ) -> bool:
        return C_FUNCTION in self.__cfg

    def clone( self, obj_name ):
        return TemplateAction( self.parent,
                               obj_name,
                               name = self.name,
                               label = self.label,
                               type = self.type,
                               icon = self.icon,
                               position = self.position,
                               function = self.function )

    def hasNgIf( self ):
        return "ngIf" in self.__cfg
    
    @property
    def ngIf( self ):
        if self.hasNgIf():
            return '*ngIf="{}"'.format( self.__cfg.get( 'ngIf', '' ) )

        return ''

    def buttonObject( self ) -> str:
        tooltip = ''
        if self.type == C_NONE:
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

        if self.function == '' and self.uri != '':
            param = TypeScript().build( self.params )
            function = "dataService.genericPut( '{uri}', {param} )".format( uri = self.uri,
                                                                              param = param )

        else:
            function = self.function

        button = '<span class="spacer"></span>'
        logger.info( "function: {}\nroute: {}".format( function, "/".join( [ self.parent.name if self.parent is not None else '',
                                                                             self.route.name if isinstance( self.route, RouteTemplate ) else '?' ] ) ) )
        cls = ''
        if self.css != '':
            cls = 'class="{}"'.format( self.css )

        if function != '':
            BUTTON_STR = '''<button {cls} {condition} {button} {tooltip} color="{color}" ({on})="{function}" id="{objname}.{name}">{content}</button>'''
            route = ''
            params = ''

        elif self.isAngularRoute():
            BUTTON_STR = '''<a {cls} {condition} {button} {tooltip} color="{color}" ({on})="router.navigate( ['/{route}'], {params} )" id="{objname}.{name}" angular_route="true">{content}</a>'''
            if isinstance( self.route.route, str ):
                if self.route.route.startswith( '/' ):
                    route = self.route.route[1:]

                else:
                    route = self.route.name[1:]

            else:
                route = "/".join( [ self.parent.name, self.route.name ] )

            params = self.route.routeParams()

        elif self.type == 'screen' and self.name in ( 'new', 'edit' ):
            BUTTON_STR = '''<a {cls} {condition} {button} {tooltip} color="{color}" ({on})="router.navigate( ['/{route}'], {params} )" id="{objname}.{name}" screen_route="true">{content}</a>'''
            if self.route.name.startswith( '/' ):
                route = self.route.name[1:]

            else:
                route = "/".join( [ self.parent.name, self.name ] )

            params = '{ }'

        else:
            raise Exception( 'Missing function or route for {}'.format( self ) )

        condition = ''
        if self.hasNgIf():
            condition = self.ngIf

        return button + BUTTON_STR.format( button = button_type,
                                           route = route,
                                           cls = cls,
                                           condition = condition,
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

    def screenObject( self ):
        if self.__cfg.get( 'directive', None ) is not None:
            params = " ".join( [ '[{}]="{}"'.format( par, val ) for par, val in self.__cfg.get( 'params', {} ).items() ] )
            if self.hasDisabed():
                params += ' [disabled]="{}"'.format( self.disabled )
            return '<{directive} name="{name}" tooltip="{label}" {control}></{directive}>'.format( **self.__cfg, control = params )

        return ""


DEFAULT_NEW_ACTION      = TemplateAction( None,
                                          'internal_action',
                                          name = C_NEW,
                                          label = 'Add a new record',
                                          type = C_SCREEN,
                                          icon = 'add',
                                          position = C_HEADER,
                                          function = 'addRecord()' )
DEFAULT_DELETE_ACTION   = TemplateAction( None,
                                          'internal_action',
                                          name = C_DELETE,
                                          label = 'Delete a record',
                                          type = C_DIALOG,
                                          icon = 'delete',
                                          position = C_CELL,
                                          function = 'deleteRecord( i, row )' )
DEFAULT_EDIT_ACTION     = TemplateAction( None,
                                          'internal_action',
                                          name = C_EDIT,
                                          label = 'Edit a record',
                                          type = C_SCREEN,
                                          position = C_ROW,
                                          function = 'editRecord( i, row )' )
