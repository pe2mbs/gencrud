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


class PositionInterface( object ):
    def __init__( self, start = 0, end = 0 ):
        self.__start    = start
        self.__end      = end
        return

    @property
    def start( self ):
        return self.__start

    @start.setter
    def start( self, value ):
        self.__start = value
        return

    @property
    def end( self ):
        return self.__end

    @end.setter
    def end( self, value ):
        self.__end = value
        return

    def range( self ):
        return range( self.__start, self.__end )

    def dump( self, caption ):
        print( '{0}\n- start: {1} end {2}'.format( caption, self.__start, self.__end ) )
        return
