import typing as t
from pydantic import BaseModel, Field, AliasChoices
from gencrud.models.sql import ISqlField
from gencrud.models.tabs import IFieldTab


class IActionButton( BaseModel ):
    name:           t.Literal[ 'edit', 'open' ]
    icon:           str
    position:       t.Literal[ 'prefix', 'suffix' ]
    disabled:       t.Optional[ str ]                   = None
    function:       t.Optional[ str ]                   = None


class IService( BaseModel ):
    name:           str
    module:         str
    cls:            str                                     = Field( validation_alias=AliasChoices('cls','class') )
    value:          str
    label:          t.Union[ str, t.List[ str ] ]


class IMonacoActionBar( BaseModel ):
    tooltip:        str
    action:         str
    icon:           str


class IMonacoEditor( BaseModel ):
    language:       str
    minimap:        t.Optional[ bool ]                      = False
    theme:          t.Optional[ str ]                       = 'vs'
    function:       t.Optional[ str ]                       = None
    file:           t.Optional[ str ]                       = None
    actionbar:      t.Optional[ t.List[ IMonacoActionBar ] ]= None


class IUserInterface( BaseModel ):
    type:           t.Literal[ 'label', 'textbox', 'choice', 'checkbox', 'password', 'textarea', 'editor',
                                'number', 'email', 'combobox', 'slider', 'slidertoggle' ]
    group:          t.Optional[ str ]                       = None
    width:          t.Optional[ str ]                       = None
    service:        t.Optional[ IService ]                  = None
    actions:        t.Optional[ t.List[ IActionButton ] ]   = None
    monaco:         t.Optional[ IMonacoEditor ]             = None
    resolve_list:   t.Optional[ t.Mapping[ str, str ] ]     = None


class IListView( BaseModel ):
    index:          int
    width:          str
    sort:           t.Optional[ bool ]                      = False
    filter:         t.Optional[ bool ]                      = False


class IScreenField( BaseModel ):
    field:          t.Union[ str, ISqlField ]
    label:          t.Optional[ str ]                       = None
    hint:           t.Optional[ str ]                       = None
    help:           t.Optional[ str ]                       = None
    # TODO: This needs a change in gencrud, support function for readonly attribute
    readonly:       t.Optional[ t.Union[ bool, str ] ]      = False
    unique:         t.Optional[ bool ]                      = False
    frontend:       t.Optional[ bool ]                      = True
    ui:             t.Optional[ IUserInterface ]            = None
    listview:       t.Optional[ IListView ]                 = None
    tab:            t.Optional[ IFieldTab ]                 = None
