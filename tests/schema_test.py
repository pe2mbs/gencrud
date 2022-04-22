import yaml
import json
import jsonschema
from gencrud.schema import GENCRUD_SCHEME
import os


def test():
    filename = os.path.join(os.getcwd(), 'tests', 'input', 'te_format.yaml')

    with open( filename, 'r' ) as stream:
        data = yaml.load( stream, Loader=yaml.Loader )

    try:
        jsonschema.Draft7Validator( GENCRUD_SCHEME )
        jsonschema.validate( instance = data, schema = GENCRUD_SCHEME )

    except jsonschema.SchemaError as exc:
        print( exc )
        raise SystemExit

    except jsonschema.ValidationError as exc:
        print( exc )
        raise SystemExit

    assert True
