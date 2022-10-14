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
from gencrud.constants import *
from gencrud.config.base import TemplateBase
import logging


logger = logging.getLogger()


class TemplateTab( TemplateBase ):
    def __init__( self, parent, **cfg ):
        TemplateBase.__init__( self, parent )
        self.__cfg = cfg
        return

    @property
    def index( self ):
        return self.__cfg.get( C_INDEX, 0 ) # or None

    @property
    def label( self ):
        return self.__cfg.get( C_LABEL, None )

    def __repr__(self):
        return "<TemplateTab label='{}' index={} parent='{}'>".format( self.label,
                                                                       self.index,
                                                                       self.parent )

class TemplateTabs( TemplateBase ):
    def __init__( self, parent, **cfg ):
        TemplateBase.__init__( self, parent )
        self.__cfg      = cfg
        self.__fields   = { l: [] for l in (self.labels + [C_NOTAB]) }
        self.__comps    = { l: None for l in self.labels }
        self.__params   = { l: None for l in self.labels }
        for col in self.parent.columns:
            if col.hasTab:
                logging.info( col.tab )
                self.__fields[ col.tab.label ].append( col )
            else:
                self.__fields[ C_NOTAB ].append( col )
            for sibling in col.siblings:
                if sibling.hasTab:
                    logging.info( sibling.tab )
                    self.__fields[ sibling.tab.label ].append( col )
                else:
                    self.__fields[ C_NOTAB ].append( sibling )

        for key in self.__fields.keys():
            self.__fields[ key ].sort( key = lambda x: x.tab.index, reverse = False )

        for tab in self.__cfg.get( C_TAB, [] ):
            self.__comps[ tab.get( C_LABEL, None ) ] = tab.get( C_COMPONENT, None )
            self.__params[ tab.get( C_LABEL, None ) ] = tab.get( C_PARAMS, {} )

        return

    @property
    def labels( self ):
        if isinstance( self.__cfg, ( list, tuple ) ):
            return self.__cfg

        return self.__cfg.get( C_LABELS, [] )

    @property
    def tabTag( self ):
        return self.__cfg.get( C_TAB_TAG, 'mat-tab' )

    @property
    def contentTag( self ):
        return self.__cfg.get( C_TAB_CONTENT_TAG, 'mat-card' )

    @property
    def groupTag( self ):
        return self.__cfg.get( C_TAB_GROUP_TAG, 'mat-tab-group' )

    def fieldsFor( self, label ):
        if label == None:
            return self.__fields[ "notab" ]
        return self.__fields[ label ]

    def hasComponent( self, label ):
        value = self.__comps.get( label, None )
        return isinstance( value, str )

    def component( self, label ):
        value = self.__comps.get( label, '' )
        return value

    def variable2typescript( self, value ):
        if isinstance( value, bool ):
            value = str( value ).lower()

        return value

    def params( self, label, mode = None ):
        result = ''
        for key, value in self.__params[ label ].items():
            value = str(self.variable2typescript( value )).replace("'", "").replace("\"", "") if \
                "[" not in str(value) else str(self.variable2typescript( value )) 
            if key in ( 'value', 'displayedColumns' ):
                result += '[{}]="{}" '.format( key, value )

            else:
                result += '{}="{}" '.format( key, value )

            if key == C_VALUE:
                if '.' in value:
                    this, _ = value.split( '.', 1 )
                    value = "{} && {}".format( this, value )

                result += '*ngIf="{}" '.format( value )

        if isinstance(mode, str):
            result += ' mode="{}" '.format( mode )

        return result
