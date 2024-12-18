import typing as t
from pydantic import BaseModel, Field, AliasChoices


class IOptions( BaseModel ):
    ignore_case_db_ids:     t.Optional[ bool ]  = Field( True, validation_alias = AliasChoices( 'ignore_case_db_ids',
                                                                                                'ignore-case-db-ids' ) )
    overwrite:              t.Optional[ bool ]  = True
    use_module:             t.Optional[ bool ]  = Field( True, validation_alias = AliasChoices( 'use_module',
                                                                                                'use-module' ) )
    generate_frontend:      t.Optional[ bool ]  = Field( True, validation_alias = AliasChoices( 'generate_frontend',
                                                                                                'generate-frontend' ) )
    generate_backend:       t.Optional[ bool ]  = Field( True, validation_alias = AliasChoices( 'generate_backend',
                                                                                                'generate-backend' ) )
    generate_tests:         t.Optional[ bool ]  = Field( False, validation_alias = AliasChoices( 'generate_tests',
                                                                                                 'generate-tests' ) )
    generate_help_pages:    t.Optional[ bool ]  = Field( False, validation_alias = AliasChoices( 'generate_help_pages',
                                                                                                 'generate-help-pages'))
    use_prettier:           t.Optional[ bool ]  = Field( False, validation_alias = AliasChoices( 'use_prettier',
                                                                                                 'use-prettier' ) )
    prettier_style:         t.Optional[ str ]   = Field( None, validation_alias = AliasChoices( 'prettier_style',
                                                                                                'prettier-style' ) )
    use_yapf:               t.Optional[ bool ]  = Field( False, validation_alias = AliasChoices( 'use_yapf',
                                                                                                 'use-yapf' ) )
    yapf_style:             t.Optional[ str ]   = Field( None, validation_alias = AliasChoices( 'yapf_style',
                                                                                                'yapf-style' ) )
