import yaml
import json
import jsonschema
from gencrud.schema import GENCRUD_SCHEME



def test():
    filename = r'C:\src\python\testrun-web\template\test_message\te_format.yaml'

    with open( filename, 'r' ) as stream:
        data = yaml.load( stream, Loader=yaml.Loader )

    print( json.dumps( data, indent= 4 ) )

    try:
        jsonschema.Draft7Validator( GENCRUD_SCHEME )
        jsonschema.validate( instance = data, schema = GENCRUD_SCHEME )

    except jsonschema.SchemaError as exc:
        print( exc )
        raise SystemExit

    except jsonschema.ValidationError as exc:
        print( exc )
        raise SystemExit


    return

if __name__ == '__main__':
    test()
