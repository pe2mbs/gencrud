import typing as t
from pydantic import BaseModel, Field, AliasChoices
from gencrud.models.actions import IScreenActions
from gencrud.models.help import IHelpGeneral
from gencrud.models.mixins import IMixinModules, IGuardService, IDeclare
from gencrud.models.screen import IScreenField
from gencrud.models.tabs import IScreenTabs


class ITable( BaseModel ):
    name:           str
    # This should not be optional
    secondary_key:  t.Optional[ str ]                       = Field( None, validation_alias = AliasChoices( 'secondary_key',
                                                                                                      'secondary-key' ))
    columns:        t.List[ IScreenField ]
    tabs:           t.Optional[ IScreenTabs ]               = None


class IMenu( BaseModel ):
    caption:        str
    icon:           t.Optional[ str ]                       = None
    route:          t.Optional[ str ]                       = None
    after:          t.Optional[ str ]                       = None
    before:         t.Optional[ str ]                       = None
    menu:           t.Optional[ 'IMenu' ]                   = None


class IViewSort( BaseModel ):
    field:          str
    direction:      t.Literal[ 'desc', 'asc' ]


class IObjects( BaseModel ):
    name:           str
    title:          str
    # When omitted the name attribute is used as the class name using the title function
    cls:            t.Optional[ str ]                       = Field( None, validation_alias=AliasChoices('cls','class') )
    uri:            str
    route:          str
    table:          ITable
    remark:         t.Optional[ str ]                       = None
    guard:          t.Optional[ IGuardService ]             = None
    actions:        t.Optional[ t.List[ IScreenActions ] ]  = []
    mixin:          t.Optional[ IMixinModules ]             = None
    help:           t.Optional[ IHelpGeneral ]              = None
    menu:           t.Optional[ IMenu ]                     = None
    declare:        t.Optional[ IDeclare ]                  = None
    viewsort:       t.Optional[ IViewSort ]                 = None