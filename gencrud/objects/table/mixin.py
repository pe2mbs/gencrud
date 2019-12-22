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

from gencrud.objects.table.python import PythonObject

class TemplateMixin( object ):
    def __init__( self, mixin ):
        self.__model    = PythonObject( mixin[ 'model' ] if mixin is not None and 'model' in mixin else None )
        self.__schema   = PythonObject( mixin[ 'schema' ] if mixin is not None and 'schema' in mixin else None )
        self.__view     = PythonObject( mixin[ 'view' ] if mixin is not None and 'view' in mixin else None )
        return

    @property
    def Model( self ):
        return self.__model

    @property
    def Schema( self ):
        return self.__schema

    @property
    def View( self ):
        return self.__view
