import typing as t
from pydantic import BaseModel, model_validator
from gencrud.models.front_back import IFrontBackend
from gencrud.models.table import IObjects
from gencrud.models.options import IOptions
from gencrud.models.source import ISourceLocation, TSourceTemplates


class IIncludeTemplate( BaseModel ):
    version:        int
    options:        IOptions
    application:    t.Optional[ str ]       = None
    source:         ISourceLocation
    templates:      TSourceTemplates
    interface:      IFrontBackend


class ITemplate( IIncludeTemplate ):
    defaults:       IIncludeTemplate
    objects:        t.List[ IObjects ]
    nogen:          t.Optional[ bool ]      = False

    @model_validator(mode='before')
    @classmethod
    def correctModel(cls, self: t.Any) -> t.Any:
        self[ 'version' ]     = self.get( 'defaults', {} ).get( 'version' )
        self[ 'options' ]     = self.get( 'defaults', {} ).get( 'options' )
        self[ 'application' ] = self.get( 'defaults', {} ).get( 'application' )
        self[ 'source' ]      = self.get( 'defaults', {} ).get( 'source' )
        self[ 'templates' ]   = self.get( 'defaults', {} ).get( 'templates' )
        self[ 'interface' ]   = self.get( 'defaults', {} ).get( 'interface' )
        return self