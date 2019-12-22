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
import json
from gencrud.objects.actions.action import (TemplateAction,
                                            DEFAULT_DELETE_ACTION,
                                            DEFAULT_EDIT_ACTION,
                                            DEFAULT_NEW_ACTION)

logger = logging.getLogger()


class TemplateActions( object ):
    def __init__( self, parent, objname, cfg ):
        self.__parent = parent
        self.__name = objname
        self.__actions = []
        self.__cfg = cfg
        for action in cfg:
            self.__actions.append( TemplateAction( self.__parent, objname, **action ) )

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

    def getRowDblClick( self ):
        for action in self.__actions:
            if action.position == 'row' and action.type != 'none':
                logger.info( "getRowAction() => {}".format( action ) )
                if action.function != '':
                    return '(dblclick)="{}"'.format( action.function )

        return ''

    def isRowActionFunction( self ):
        for action in self.__actions:
            if action.position == 'row' and action.type != 'none':
                logger.info( "getRowAction() => {}".format( action ) )
                return action.function != ''

        return False

    def getRowRouterLink( self ):
        for action in self.__actions:
            if action.position == 'row' and action.type != 'none':
                logger.info( "getRowAction() => {}".format( action ) )
                if action.function == '':
                    return 'routerLink="/{}/{}" {}'.format( self.__name, action.route.name, action.route.routeParams() )

        return ''

    def hasRowButtons( self ):
        for action in self.__actions:
            if action.position == 'row' and action.type != 'none':
                return True

        return False

    def getFooterButtons( self ):
        result = []
        for action in self.__actions:
            if action.position == 'footer' and action.type != 'none':
                result.append( action )

        return result

    def invalid( self, name ):
        for action in self.__actions:
            if action.name == name:
                if action.type == 'none':
                    return True

                return action.position == 'none'

        return False

    def valid( self, name, _type ):
        for action in self.__actions:
            if action.name == name and action.type == _type:
                return action.position != 'none'

        return False

    def __repr__( self ):
        return "<TemplateActions {}>".format( ", ".join( action.name for action in self.__actions ) )