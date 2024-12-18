import typing as t
from pydantic import BaseModel, Field, AliasChoices, ConfigDict


class IActionParams( BaseModel ):
    # Extra allowed !!!
    model_config = ConfigDict( extra  = 'allow' )
    mode:       t.Optional[ t.Literal[ 'new', 'edit', 'filter', 'api', 'add' ] ]    = None
    id:         t.Optional[ str ]           = None
    value:      t.Optional[ str ]           = None


class IActionRoute( BaseModel ):
    cls:        str                 = Field( validation_alias=AliasChoices('cls','class') )
    params:     IActionParams


class IScreenActions( BaseModel ):
    name:       str
    type:       t.Literal[ 'none', 'screen', 'dialog', 'button', 'api', 'function' ]
    position:   t.Optional[ t.Literal[ 'none', 'cell', 'row', 'sidebar', 'header', 'footer' ] ]     = None
    label:      t.Optional[ str ]                       = None
    icon:       t.Optional[ str ]                       = None
    help:       t.Optional[ str ]                       = None
    route:      t.Optional[ IActionRoute ]              = None
    function:   t.Optional[ str ]                       = None
    index:      t.Optional[ int ]                       = 0
    directive:  t.Optional[ str ]                       = None
    params:     t.Optional[ IActionParams ]             = None