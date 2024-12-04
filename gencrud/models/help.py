import typing as t
from pydantic import BaseModel, Field, AliasChoices


class IHelpGeneral( BaseModel ):
    title:      str
    table:      str
    screen:     str
