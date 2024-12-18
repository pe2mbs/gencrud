import os.path
import glob
import yaml
import yaml_include
from pydantic_core._pydantic_core import ValidationError
from gencrud.models.template import ITemplate


location = os.path.join( "C:\\", "src", "python", "testrun-web", "template" )


def scanFolder( folder: str ):
    scan = os.path.join( folder, "**" )
    for filepath in glob.glob( scan, recursive = False ):
        basepath, filename = os.path.split( filepath )
        if filename.startswith( 'templates' ) or filename in ('old', 'include'):
            continue

        elif os.path.isdir( filepath ):
            scanFolder( filepath )

        elif filepath.endswith( '.yaml' ):
            print( f"Filename: { filepath }" )
            yaml.add_constructor( "!include", yaml_include.Constructor( base_dir = basepath ) )
            with open( filepath, 'r' ) as stream:
                data = yaml.load( stream, Loader = yaml.Loader )

            del yaml.Loader.yaml_constructors[ "!include" ]
            try:
                tempplate = ITemplate( **data )

            except BaseException as exc:
                print(exc)
                exit( -1 )


if __name__ == '__main__':
    print( location )
    scanFolder( location )