import io
import yaml
import json
from gencrud.schema.schema_v1 import _GENCRUD_SCHEME_V1 # JSON/DICT
from gencrud.schema.schema_v2 import _GENCRUD_SCHEME_V2_YAML


def exportSchema( version, filename ):
    if version == 1:
        schema = _GENCRUD_SCHEME_V1

    elif version == 2:
        schema = yaml.load( io.StringIO( _GENCRUD_SCHEME_V2_YAML ), Loader=yaml.Loader )

    else:
        raise ValueError("version error")

    for ext in ( ".jsons", ".yamls" ):
        _filename = f"{filename}{ext}"
        with open( _filename, 'w' ) as stream:
            if ext == '.jsons':
                json.dump( schema, stream )

            elif ext == '.yamls':
                yaml.dump( schema, stream )


    return