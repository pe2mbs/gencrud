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
from gencrud.util.exceptions import MissingAttribute


class TemplateService( TemplateBase ):
    def __init__( self, **cfg ):
        TemplateBase.__init__( self, None )
        self.__config = cfg
        if C_NAME not in self.__config:
            raise MissingAttribute( C_SERVICE, C_NAME )

        if C_VALUE not in self.__config:
            raise MissingAttribute( C_SERVICE, C_VALUE )

        if C_LABEL not in self.__config:
            raise MissingAttribute( C_SERVICE, C_LABEL )

        if C_CLASS not in self.__config:
            raise MissingAttribute( C_SERVICE, C_CLASS )

        self.__fieldLabel = ''
        return

    @property
    def fieldLabel( self ):
        return self.__fieldLabel

    @fieldLabel.setter
    def fieldLabel( self, value ):
        self.__fieldLabel = value
        return

    @property
    def dictionary( self ) -> dict:
        return self.__config

    @property
    def name( self ):
        return self.__config.get( C_NAME, None )

    @property
    def value( self ):
        return self.__config.get( C_VALUE, None )

    @property
    def label( self ):
        label = self.__config.get( C_LABEL, None )
        return self.__config.get( C_LABEL, None )

    @property
    def resolveLabel( self ):
        # in case a foreign key label is taken, only the actual label name
        # is retrieved, i.e., SOME_LABEL instead of SOME_ID_FK.SOME_LABEL
        label = self.__config.get( C_LABEL, None )
        if label != None:
            return label.split(".")[-1]
        return None

    @property
    def baseClass( self ):
        # in case a base class is explicitly provided, e.g., when a foreign key is used,
        # we will take that one
        if C_BASECLASS in self.__config:
            return self.__config.get( C_BASECLASS )
        return self.__config.get( C_CLASS, None )

    def hasBaseClass( self ):
        return C_BASECLASS in self.__config

    @property
    def cls( self ):
        value = self.__config.get( C_CLASS, None )
        if value.endswith( 'Service' ):
            return value

        return '{}DataService'.format( value )

    @property
    def path( self ):
        if C_PATH in self.__config:
            return self.__config[ C_PATH ]

        return '../{}/service'.format( self.__config[ C_NAME ] )

    def hasInitial( self ):
        return 'initial' in self.__config

    @property
    def initial( self ):
        return dict2typeScript( self.__config[ 'initial' ] )

    def hasFinal( self ):
        return 'final' in self.__config

    @property
    def final( self ):
        return dict2typeScript( self.__config[ 'final' ] )

    def __repr__(self):
        return "<Service name={} path={} label={} value={}".format( self.name, self.path, self.label, self.value )

    def uniqueName( self, *args ):
        return ( "_".join( [ self.name, self.label ] + list( args ) ) ).replace( ',', '_' ).replace( ';', '_' ).replace( '-', '_' )

    def mapperName( self ):
        return "_".join( [ self.name, self.cls, self.label, self.value ] ).replace( ',', '_' ).replace( ';', '_' ).replace( '-', '_' )


def list2typeScript( array ):
    result = []
    for item in array:
        if isinstance( item, dict ):
            result.append( dict2typeScript( item ) )

        elif isinstance( item, ( list, tuple )  ):
            result.append( list2typeScript( item ) )

        elif isinstance( item, bool ):
            result.append( '{}'.format( 'true' if item else 'false' ) )

        else:
            result.append( '{}'.format( item ) )

    return ', '.join( result )


def dict2typeScript( dictionary ):
    result = []
    for key, value in dictionary.items():
        if isinstance( value, str ):
            result.append( '{}: "{}"'.format( key, value ) )

        elif isinstance( value, ( list, tuple )  ):
            result.append( list2typeScript( value ) )

        elif isinstance( value, dict ):
            result.append( dict2typeScript( value ) )

        elif isinstance( value, bool ):
            result.append( '{}: {}'.format( key, 'true' if value else 'false' ) )

        else:
            result.append( '{}: {}'.format( key,value ) )

    return "{{ {} }}".format( ', '.join( result ) )
