# -*- coding: utf-8 -*-
"""Main webapp application package."""
#
# Main webapp application package
# Copyright (C) 2018-2020 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>
#
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License GPL-2.0-only
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
import os


class InvalidModel( Exception ):
    pass


def keysToString( keys ):
    if len( keys ) > 1:
        return ', '.join( [ value for value in keys[ : -1 ] ] ) + ' and ' + keys[ -1 ]

    if len( keys ) == 1:
        return keys[ 0 ]

    return "?"


class DbExporterInporters( dict ):
    def __init__( self, d ):
        for key, value in d.items():
            self[ key ] = value

        return

    def hasClear2String( self ):
        result = [ ]
        for key,value in self.items():
            if value.CLEAR:
                result.append( key.upper() )

        return keysToString( result )

    def keysUpperCase( self ):
        return [ k.upper() for k in self.keys() ]

    def keysToString( self ):
        return keysToString( self.keysUpperCase() )


def CommandBanner( *args ):
    l = 76
    for line in args:
        if len( line ) > l:
            l = len( line )

    print( "+{}+".format( "-" * (l+2) ) )
    for line in args:
        print( "| {:{}} |".format( line, l ) )

    print( "+{}+".format( "-" * (l+2) ) )
    return


def ResolveRootPath( path ):
    if path == '':
        path = os.path.abspath( os.path.join( os.path.dirname( __file__ ), '..', '..' ) )

    elif path == '.':
        path = os.path.abspath( path )

    return os.path.abspath( path )
