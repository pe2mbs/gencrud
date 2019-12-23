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

class TemplateTab( object ):
    def __init__( self, parent, **cfg ):
        self.__parent   = parent
        self.__cfg = cfg
        return

    @property
    def index( self ):
        return self.__cfg.get( 'index', None )

    @property
    def label( self ):
        return self.__cfg.get( 'label', None )


class TemplateTabs( object ):
    def __init__( self, parent, **cfg ):
        self.__parent   = parent
        self.__cfg      = cfg
        self.__fields   = { l: [] for l in self.labels }
        self.__comps    = { l: None for l in self.labels }
        self.__params   = { l: None for l in self.labels }
        for col in self.__parent.columns:
            if col.hasTab:
                self.__fields[ col.tab.label ].append( col )

        for key in self.__fields.keys():
            self.__fields[ key ].sort( key = lambda x: x.tab.index, reverse = False )

        for tab in self.__cfg.get( 'tab', [] ):
            self.__comps[ tab.get( 'label', None ) ] = tab.get( 'component', None )
            self.__params[ tab.get( 'label', None ) ] = tab.get( 'params', {} )

        return

    @property
    def labels( self ):
        if isinstance( self.__cfg, ( list, tuple ) ):
            return self.__cfg

        return self.__cfg.get( 'labels', None )

    @property
    def tabTag( self ):
        return self.__cfg.get( 'tabtag', 'mat-tab' )

    @property
    def contentTag( self ):
        return self.__cfg.get( 'contenttag', None )

    @property
    def groupTag( self ):
        return self.__cfg.get( 'grouptag', 'mat-tab-group' )

    def fieldsFor( self, label ):
        result = self.__fields[ label ]
        return result

    def hasComponent( self, label ):
        value = self.__comps.get( label, None )
        return isinstance( value, str )

    def component( self, label ):
        value = self.__comps.get( label, '' )
        return value

    def params( self, label ):
        result = ''
        for key, value in self.__params[ label ].items():
            result += '[{}]="{}" '.format( key, value )
            if key == 'value':
                result += '*ngIf="{}" '.format( value )

        return result

