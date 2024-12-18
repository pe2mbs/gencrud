from gencrud.schema.schema_v1 import getTemplateV1
from gencrud.schema.schema_v2 import getTemplateV2      # uses the YAML coded schema for better readability.

SCHEMES = { 1: getTemplateV1(),
            2: getTemplateV2() }


def getSchema( version: int = 1 ):
    return SCHEMES[ version ]
