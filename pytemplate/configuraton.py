import os
import pathlib
from pytemplate.objects.object import TemplateObject
from pytemplate.source import TemplateSource
from pytemplate.util.folders import findpath
from pytemplate.util.exceptions import MissingSourceFolder

class TemplateConfiguration( object ):
    def __init__( self, **cfg ):
        self.__config   = cfg
        current_path = os.getcwd()
        python_path = cfg[ 'source' ][ 'python' ]
        angular_path = cfg[ 'source' ][ 'angular' ]
        if python_path.startswith( '.' ) and angular_path.startswith( '.' ):
            if current_path.endswith( python_path[1:] ):
                # We are on the python folder
                current_path = findpath( angular_path )

                pass

            elif current_path.endswith( angular_path[1:] ):
                # We are on the Angular folder
                current_path = findpath( python_path )

            elif ( os.path.isdir( os.path.join( current_path, python_path ) ) and
                   os.path.isdir( os.path.join( current_path, angular_path ) ) ):
                # we are on the project root folder
                pass

            else:
                raise MissingSourceFolder( python_path, angular_path )

        else:
            if os.path.isdir( python_path ) and os.path.isdir( angular_path ):
                # We have a full path and they exist
                pass

            else:
                raise MissingSourceFolder( python_path, angular_path )

        self.__python   = TemplateSource( 'python', current_path, **self.__config )
        self.__angular  = TemplateSource( 'angular', current_path, **self.__config )
        self.__objects  = []
        for obj in cfg[ 'objects' ]:
            #print( obj )
            self.__objects.append( TemplateObject( **obj ) )

        return

    @property
    def python( self ):
        return self.__python

    @property
    def angular( self ):
        return self.__angular

    @property
    def objects( self ):
        return self.__objects

    def __iter__( self ):
        return iter( self.__objects )

    @property
    def application( self ):
        return self.__objects[ 0 ].application
