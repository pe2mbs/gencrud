import typing as t
from pydantic import BaseModel, Field, AliasChoices


class ISqlField( BaseModel ):
    name:           str
    type:           t.Literal[ 'INT', 'CHAR', 'VARCHAR', 'BLOB', 'CLOB', 'BOOL', 'BOOLEAN', 'DATE', 'TIME', 'DATETIME',
                               'TIMESTAMP', 'JSON', 'JSON', 'GZIP_JSON', 'GZIP_DATA' ]
    size:           t.Optional[ int ]   = Field( None, validation_alias= AliasChoices( 'size', 'length' ) )
    autonumber:     t.Optional[ bool ]  = Field( False, validation_alias= AliasChoices( 'autonumber', 'auto-number' ) )
    primarykey:     t.Optional[ bool ]  = Field( None, validation_alias= AliasChoices( 'primarykey', 'primary-key' ) )
    not_null:       t.Optional[ bool ]  = Field( None, validation_alias= AliasChoices( 'not_null', 'not-null' ) )
    def_value:      t.Optional[ t.Union[ str, int, float, bool ] ] = Field( None,
                                                                            validation_alias= AliasChoices( 'def_value',
                                                                                                            'default' ))
    foreign_key:    t.Optional[ str ]   = Field( None, validation_alias= AliasChoices( 'foreign_key',
                                                                                       'foreignkey',
                                                                                       'foreign-key' ) )
