import typing as t
from pydantic import BaseModel, Field, AliasChoices


class IExtraTemplates( BaseModel ):
    route:                      str
    subroute:                   str                         = Field( None, validation_alias=AliasChoices('subroute','sub-route'))
    module:                     str

class IFrontend( BaseModel ):
    path:                       str
    templates:                  IExtraTemplates
    cls:                        str                         = Field( None, validation_alias=AliasChoices('cls','class'))
    file:                       str

class IBackend( BaseModel ):
    package:                    str
    module:                     str

class IFrontBackend( BaseModel ):
    frontend:                   IFrontend
    backend:                    IBackend
