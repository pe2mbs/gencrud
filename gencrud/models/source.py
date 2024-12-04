import typing as t
from pydantic import BaseModel, Field, AliasChoices


class ISourceLocation( BaseModel ):
    base:       t.Optional[ str ]           = None
    python:     str
    angular:    str
    unittest:   str
    helppages:  str                         = Field( None, validation_alias = AliasChoices( 'helppages',
                                                                                            'help-pages' ) )


class TSourceTemplates( ISourceLocation ):
    common:     ISourceLocation

