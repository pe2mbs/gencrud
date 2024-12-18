import typing as t
from pydantic import BaseModel, Field, AliasChoices
from gencrud.models.actions import IActionParams


class ITabParams( BaseModel ):
    # Extra allowed !!!
    caption:    t.Optional[ bool ]          = True
    id:         t.Optional[ str ]           = None
    value:      t.Optional[ str ]           = None


class ITabComponent( BaseModel ):
    label:          str
    component:      str
    cls:            t.Optional[ str ]               = None
    name:           t.Optional[ str ]               = None
    file:           t.Optional[ str ]               = None
    params:         t.Optional[ ITabParams ]        = None


class IScreenTabs( BaseModel ):
    labels:         t.List[ str ]
    tab:            t.Optional[ t.List[ ITabComponent ] ]   = None


class IFieldTab( BaseModel ):
    label:          str
    index:          int
