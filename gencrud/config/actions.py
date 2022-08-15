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
from gencrud.config.action import (TemplateAction,
                                   DEFAULT_DELETE_ACTION,
                                   DEFAULT_EDIT_ACTION,
                                   DEFAULT_NEW_ACTION)
from gencrud.constants import *
from gencrud.config.base import TemplateBase

logger = logging.getLogger()


class TemplateActions( TemplateBase ):
    def __init__( self, parent, objname, cfg ):
        TemplateBase.__init__( self, parent )
        self.__name = objname
        self.__actions = []
        self.__cfg = cfg
        for action in cfg:
            self.__actions.append( TemplateAction( self.parent, objname, **action ) )
        # Disabled for now, user should specify all actions manually
        if not self.has( C_NEW ):
            self.__actions.append( DEFAULT_NEW_ACTION.clone( objname ) )
        if not self.has( C_EDIT ):
            self.__actions.append( DEFAULT_EDIT_ACTION.clone( objname ) )
        if not self.has( C_DELETE ):
            self.__actions.append( DEFAULT_DELETE_ACTION.clone( objname ) )
        return

    def __iter__( self ):
        return iter( self.__actions )

    def __len__( self ):
        return len( self.__actions )

    def __getitem__(self, item):
        return self.__actions[item]

    @property
    def unique( self ):
        labelList = []
        resultList = []
        for action in self.__actions:
            if action.name in ( 'new', 'edit' ):
                if 'newedit' + action.type in labelList:
                    continue

                labelList.append( 'newedit' + action.type )

            else:
                if action.name + action.type in labelList:
                    continue

                labelList.append( action.name + action.type )

            resultList.append( action )

        return iter( resultList )

    def has( self, key ):
        for action in self.__actions:
            if action.name == key:
                return True

        return False

    def isDialog( self, name ):
        return self.get( name ).isDialog()

    def isScreen( self, name ):
        return self.get( name ).isScreen()

    def get( self, key ):
        for action in self.__actions:
            if action.name == key:
                return action

        raise Exception( "Missing {} in actions of {}".format( key, self.__name ) )

    def getCustomButtons( self ):
        result = []
        for action in self.__actions:
            if action.name not in ( C_NEW, C_EDIT, C_DELETE ):
                result.append( action )

        return result

    def getHeaderButtons( self ):
        result = []
        for action in self.__actions:
            if action.position == C_HEADER and action.type != C_NONE:
                result.append( action )

        return result

    def hasRowButtons( self ):
        # Downward compatibility
        return self.hasCellButtons()

    def hasCellButtons( self ):
        for action in self.__actions:
            if action.position in ( C_CELL, C_ROW ) and action.type != C_NONE and action.hasIcon():
                return True

        return False

    def getCellButtons( self ):
        result = []
        for action in self.__actions:
            if action.position in ( C_CELL, C_ROW ) and action.type != C_NONE and action.hasIcon():
                result.append( action )

        return result

    def getRowButtons( self ):
        result = []
        for action in self.__actions:
            if action.position == C_ROW and action.type != C_NONE:
                result.append( action )

        return result

    def isRowActionFunction( self ):
        for action in self.__actions:
            if action.position == C_ROW and action.type != C_NONE:
                logger.info( "getRowAction() => {}".format( action ) )
                return action.function != ''

        return False

    def getRowRouterLink( self ):
        for action in self.__actions:
            if action.position == C_ROW and action.type != C_NONE:
                logger.info( "getRowAction() => {}".format( action ) )
                if action.isAngularRoute():
                    # return 'routerLink="/{}/{}" {}'.format( self.__name, action.route.name, action.route.routeParams() )
                    route = "/".join( [ self.parent.name, action.name ] )
                    ACTION_STR = '''({on})="router.navigate( ['/{route}'], {params} )"'''
                    params = action.route.routeParams()

                elif action.function != '':
                    ACTION_STR = '({on})="{function}"'
                    route = ''
                    params = ''

                elif action.type == C_SCREEN:
                    route = "/".join( [ self.__name, action.name ] )
                    ACTION_STR = '''({on})="router.navigate( ['/{route}'], {params} )"'''
                    params = action.routeParams()

                else:

                    raise Exception( "Missing function or route declaration" )

                return ACTION_STR.format( function = action.function,
                                          on = action.on,
                                          route = route,
                                          params = params )

        return ''

    def getFooterButtons( self ):
        result = []
        for action in self.__actions:
            if action.position == C_FOOTER and action.type != C_NONE:
                result.append( action )

        return result

    def invalid( self, name ):
        for action in self.__actions:
            if action.name == name:
                if action.type == C_NONE:
                    return True

                return action.position == C_NONE

        return False

    def valid( self, name, _type ):
        for action in self.__actions:
            if action.name == name and action.type == _type:
                return action.position != C_NONE

        return False

    def getScreenActions( self ):
        return sorted( [ action for action in self.__actions if action.type == 'screen' and action.position == 'sidebar' ],
                       key = lambda k: k.get( 'index', 0 ) )

    @property
    def module( self ):
        return self.parent.module

    def __repr__( self ):
        return "<TemplateActions {}>".format( ", ".join( action.name for action in self.__actions ) )
