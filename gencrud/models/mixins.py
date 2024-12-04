import typing as t
from pydantic import BaseModel, Field, AliasChoices


class IMixinObject( BaseModel ):
    cls:                str                                     = Field( validation_alias=AliasChoices('cls','class') )
    file:               str


class IAngularMixins( BaseModel ):
    table_component:    t.Optional[ IMixinObject ]              = None
    screen_component:   t.Optional[ IMixinObject ]              = None


class IPythonMixins( BaseModel ):
    view:               t.Optional[ IMixinObject ]              = None
    schm:               t.Optional[ IMixinObject ]              = Field( None, validation_alias= AliasChoices('schm','schema'))
    model:              t.Optional[ IMixinObject ]              = None


class IMixinModules( BaseModel ):
    angular:            t.Optional[ IAngularMixins ]            = None
    python:             t.Optional[ IPythonMixins ]             = None


class IGuardService( IMixinObject ):
    pass


class IDeclare( BaseModel ):
    module:             t.Optional[ t.List[ IMixinObject ] ]    = None
    component:          t.Optional[ t.List[ IMixinObject ] ]    = None