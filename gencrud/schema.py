#
#   This is the JSON schema for the templates
#
GENCRUD_SCHEME = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "GenCrud",
    "type": "object",
    "required": [ 'source', 'application', 'objects' ],
    "additionalProperties": False,
    "properties": {
        'source': {
            'type': 'object',
            "additionalProperties": False,
            'properties': {
                'base': {
                    'type': 'string',
                    'optional': True
                },
                'python': {
                    'type': 'string'
                },
                'angular': {
                    'type': 'string'
                },
                'unittest': {
                    'type': 'string',
                    'optional': True
                }
            }
        },
        'templates': {
            'type': 'object',
            "optional": True,
            "additionalProperties": False,
            'properties': {
                'base': {
                    'type': 'string',
                    'optional': True
                },
                'python': {
                    'type': 'string',
                },
                'angular': {
                    'type': 'string',
                },
                'unittest': {
                    'type': 'string',
                    'optional': True
                },
                'common': {
                    'type': 'object',
                    "additionalProperties": False,
                    'properties': {
                        'base': {
                            'type': 'string',
                            'optional': True
                        },
                        'python': {
                            'type': 'string',
                        },
                        'angular': {
                            'type': 'string',
                        },
                        'unittest': {
                            'type': 'string',
                            'optional': True
                        }
                    }
                }
            }
        },
        'application': {
            'type': 'string'
        },
        'nogen': {
            'type': 'boolean'
        },
        'references': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'app-module': {
                    'type': 'object',
                    'additionalProperties': False,
                    'properties': {
                        'filename': { 'type': 'string' },
                        'class':  { 'type': 'string' },
                        'module':  { 'type': 'string' },
                    }
                },
                'app-routing': {
                    'type': 'object',
                    'additionalProperties': False,
                    'properties': {
                        'filename':  { 'type': 'string' },
                        'class':  { 'type': 'string' },
                        'module': { 'type': 'string' },
                    }
                }
            }
        },
        'options': {
            'type': 'object',
            "additionalProperties": False,
            'properties': {
                'ignore-case-db-ids': {
                    'type': 'boolean'
                },
                'overwrite': {
                    'type': 'boolean'
                },
                'use-module': {
                    'type': 'boolean'
                }
            }
        },
        'objects': {
            'type': 'array',
            'items': {
                "required": [ 'name', 'title', 'class', 'uri', 'actions', 'table' ],
                'type': 'object',
                "additionalProperties": False,
                'properties': {
                    'name': {
                        'type': 'string'
                    },
                    'autoupdate':  {
                        'type': 'integer'
                    },
                    'title': {
                        'type': 'string'
                    },
                    'remark': {
                        'type': 'string'
                    },
                    'class': {
                        'type': 'string'
                    },
                    'uri': {
                        'type': 'string'
                    },
                    'action-width': {
                        'type': 'string'
                    },
                    'modules': {
                        'type': 'array',
                        "items": {
                            'type': 'object',
                            'required': [ 'class', 'path' ],
                            "additionalProperties": False,
                            'properties': {
                                'class': {
                                    'type': 'string',
                                },
                                'path': {
                                    'type': 'string',
                                },
                                'module': {
                                    'type': 'string',
                                }
                            }
                        }
                    },
                    'mixin': {
                        'type': 'object',
                        "additionalProperties": False,
                        'properties': {
                            'angular': {
                                'type': 'object',
                                "additionalProperties": False,
                                'properties': {
                                    'module': {
                                        'type': 'object',
                                        'required': [ 'class', 'file' ],
                                        "additionalProperties": False,
                                        'properties': {
                                            'class': {
                                                'type': 'string',
                                            },
                                            'file': {
                                                'type': 'string',
                                            }
                                        }
                                    },
                                    'component.dialog': {
                                        'type': 'object',
                                        'required': [ 'class', 'file' ],
                                        "additionalProperties": False,
                                        'properties': {
                                            'class': {
                                                'type': 'string',
                                            },
                                            'file': {
                                                'type': 'string',
                                            },
                                        }
                                    },
                                    'screen.component': {
                                        'type': 'object',
                                        'required': [ 'class', 'file' ],
                                        "additionalProperties": False,
                                        'properties': {
                                            'class': {
                                                'type': 'string',
                                            },
                                            'file': {
                                                'type': 'string',
                                            }
                                        }
                                    },
                                    'table.component': {
                                        'required': [ 'class', 'file' ],
                                        'type': 'object',
                                        "additionalProperties": False,
                                        'properties': {
                                            'class': {
                                                'type': 'string',
                                            },
                                            'file': {
                                                'type': 'string',
                                            }
                                        }
                                    }
                                }
                            },
                            'python': {
                                'type': 'object',
                                "additionalProperties": False,
                                'properties': {
                                    'model': {
                                        'type': 'object',
                                        "additionalProperties": False,
                                        'properties': {
                                            'class': { 'type': 'string' },
                                            'filename': { 'type': 'string' },
                                        }
                                    },
                                    'schema': {
                                        'type': 'object',
                                        "additionalProperties": False,
                                        'properties': {
                                            'class': {'type': 'string'},
                                            'filename': {'type': 'string'},
                                        }
                                    },
                                    'view': {
                                        'type': 'object',
                                        "additionalProperties": False,
                                    }
                                }
                            }
                        }
                    },
                    'ignore_templates': { 'type': 'array' },
                    'injection': {
                        'type': 'object',
                        'properties': {
                            'module.ts': {
                                'type': 'object',
                                'properties': {
                                    'dialog': {
                                        'type': 'object',
                                        'properties': {
                                            'class': { 'type': 'string' },
                                            'file': { 'type': 'string' }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'route': { 'type': 'string' },
                    'actions': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'required': [ 'name', 'type' ],
                            "additionalProperties": False,
                            'properties': {
                                'name': {
                                    'type': 'string',
                                },
                                'label': {
                                    'type': 'string',
                                },
                               'type': {
                                    'enum': [ 'screen', 'dialog', 'api', 'function', 'directive', 'none' ],
                                },
                                'icon': {
                                    'type': 'string',
                                },
                                'position': {
                                    'enum': [ 'row', 'header', 'footer', 'cell', 'none', 'screen', 'sidebar' ],
                                },
                                'uri': {
                                    'type': 'string'
                                },
                                'function': {
                                    'type': 'string'
                                },
                                'directive': {
                                    'type': 'string'
                                },
                                'index': {
                                    'type': 'integer'
                                },
                                'disabled': {
                                    'type': ['string', 'boolean']
                                },
                                'ngIf': {
                                    'type': 'string'
                                },
                                'params': {
                                    'type': 'object',
                                    "additionalProperties": True,
                                    'properties': {
                                        'id': {
                                            'type': 'string',
                                        },
                                        'value': {
                                            'type': 'string',
                                        },
                                    }
                                },
                                'route': {
                                    'type': 'object',
                                    "additionalProperties": False,
                                    'properties': {
                                        'class': {
                                            'type': 'string',
                                        },
                                        'name': {
                                            'type': 'string',
                                        },
                                        'module': {
                                            'type': 'string',
                                        },
                                        'route': {
                                            'type': 'string',
                                        },
                                        'params': {
                                            'type': 'object',
                                            'required': [ 'mode' ],
                                            'properties': {
                                                'mode': {
                                                    'type': 'string',
                                                },
                                                'id': {
                                                    'type': ["number", "string" ],
                                                },
                                                'value': {
                                                    'type': 'string',
                                                },
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'menu': {
                        'type': 'object',
                        'required': [ 'caption' ],
                        "additionalProperties": False,
                        'properties': {
                            'caption': {
                                'type': 'string',
                            },
                            'index': {
                                'type': 'integer'
                            },
                            'icon': {
                                'type': 'string',
                            },
                            'after': {
                                'type': 'string',
                            },
                            'before': {
                                'type': 'string',
                            },
                            'route': {
                                'type': 'string'
                            },
                            'menu': {
                                'type': 'object',
                                'required': [ 'caption' ],
                                "additionalProperties": False,
                                'properties': {
                                    'caption': {
                                        'type': 'string',
                                    },
                                    'index': {
                                        'type': 'integer'
                                    },
                                    'icon': {
                                        'type': 'string',
                                    },
                                    'after': {
                                        'type': 'string',
                                    },
                                    'before': {
                                        'type': 'string',
                                    },
                                    'route': {
                                        'type': 'string'
                                    },
                                    'menu': {
                                        'type': 'object',
                                        'required': [ 'caption' ],
                                        "additionalProperties": False,
                                        'properties': {
                                            'caption': {
                                                'type': 'string'
                                            },
                                            'index': {
                                                'type': 'integer'
                                            },
                                            'icon': {
                                                'type': 'string'
                                            },
                                            'after': {
                                                'type': 'string'
                                            },
                                            'before': {
                                                'type': 'string'
                                            },
                                            'route': {
                                                'type': 'string'
                                            },
                                            'menu': {
                                                'type': 'object'
                                            }
                                        }
                                    }
                                }
                            },
                        }
                    },
                    'table': {
                        'type': 'object',
                        'required': [ 'name', 'columns' ],
                        "additionalProperties": False,
                        'properties': {
                            'name': {
                                'type': 'string',
                            },
                            'secondary-key': {
                                'type': 'string',
                                "optional": True
                            },
                            'unique-key': { 'type': 'string' },
                            'viewSort': {
                                'type': 'object',
                                'required': [ 'field', 'direction' ],
                                "additionalProperties": False,
                                'properties': {
                                    'field': {
                                        'type': 'string'
                                    },
                                    'direction': {
                                        'enum': [ 'desc', 'asc' ]
                                    },
                                }
                            },
                            'hint': {
                                'type': 'string',
                            },
                            'tabs': {
                                'type': 'object',
                                'required': [ 'labels' ],
                                "additionalProperties": False,
                                'properties': {
                                    'labels': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'string'
                                        }
                                    },
                                    'tab': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'required': [ 'label', 'component', 'params' ],
                                            "additionalProperties": False,
                                            'properties': {
                                                'label': {
                                                    'type': 'string',
                                                },
                                                'component': {
                                                    'type': 'string',
                                                },
                                                'params': {
                                                    'type': 'object',
                                                    'required': [ 'id', 'value' ],
                                                    "additionalProperties": False,
                                                    'properties': {
                                                        'id': {
                                                            'type': 'string',
                                                        },
                                                        'value': {
                                                            'type': 'string',
                                                        },
                                                        'caption': {
                                                            'type': 'boolean',
                                                        },
                                                        'displayedColumns': {
                                                            'type': 'string',
                                                        },
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            'columns': {
                                'type': 'array',
                                'items': {
                                    "type": "object",
                                    "required": [ 'field' ],
                                    "additionalProperties": False,
                                    "properties": {
                                        'field': {
                                            'type': 'string'
                                        },
                                        'hint': {
                                            'type': 'string',
                                        },
                                        'readonly': {
                                            'type': 'boolean'
                                        },
                                        "frontend": {
                                            'type': 'boolean'
                                        },
                                        "remark": {
                                            'type': 'string'
                                        },
                                        'name': {
                                            'type': 'string'
                                        },
                                        'unique': {
                                            'type': 'boolean'
                                        },
                                        'unique-key': {
                                            'type': 'string'
                                        },
                                        'label': {
                                            'type': 'string'
                                        },
                                        'ui': {
                                            'type': 'object',
                                            'required': [ 'type' ],
                                            "additionalProperties": False,
                                            'properties': {
                                                'type': {
                                                    "enum": [ 'textbox', 'editor', 'number', 'choice', 'choice-auto-complete',
                                                              'textarea', 'checkbox', 'password', 'date', 'time', 'datetime',
                                                              'label' ]
                                                },
                                                'format': {
                                                    'type': 'string'
                                                },
                                                'width': {
                                                    'type': 'integer'
                                                },
                                                'group': {
                                                    'type': 'string'
                                                },
                                                'ngIf': {
                                                    'type': 'string'
                                                },
                                                'hint': {
                                                    'type': 'string'
                                                },
                                                'pipe': {
                                                    'enum': [ 'date', 'datetime', 'time' ]
                                                },
                                                'cols': { 'type': 'integer', },
                                                'rows': { 'type': 'integer', },
                                                'resolve-list': {
                                                    'type': 'object',
                                                },
                                                'service': {
                                                    'type': 'object',
                                                    "additionalProperties": False,
                                                    'properties': {
                                                        'name': {
                                                            'type': 'string',
                                                        },
                                                        'path': {
                                                            'type': 'string',
                                                        },
                                                        'base-class': {
                                                            'type': 'string',
                                                        },
                                                        'class': {
                                                            'type': 'string',
                                                        },
                                                        'value': {
                                                            'type': 'string',
                                                        },
                                                        'label': {
                                                            'type': 'string',
                                                        },
                                                    }
                                                },
                                                'attributes': {
                                                    'type': 'object',
                                                    "additionalProperties": False,
                                                    'properties': {
                                                        'language': {
                                                            'enum': [ 'markdown',  'json', 'python', 'yaml', 'xml', 'sql', 'xpath' ]
                                                        },
                                                        'height': {
                                                            'type': 'string',
                                                        },
                                                        'minimap': {
                                                            'type': 'string',
                                                        },
                                                        'heightAdjust': {
                                                            'type': 'string',
                                                        },
                                                        'decodeFunc': {
                                                            'type': 'string',
                                                        },
                                                        'encodeFunc': {
                                                            'type': 'string',
                                                        },
                                                        'onSaveClick': {
                                                            'type': 'string',
                                                        }
                                                    }
                                                },
                                                'actions': {
                                                    'type': 'array',
                                                    'items': {
                                                        'type': 'object',
                                                        'required': [ 'name', 'icon', 'position' ],
                                                        "additionalProperties": False,
                                                        'properties': {
                                                            'name': {
                                                                'type': 'string'
                                                            },
                                                            'icon': {
                                                                'type': 'string'
                                                            },
                                                            'position': {
                                                                'enum': [ 'row', 'left', 'right' ],
                                                            },
                                                            'function': {
                                                                'type': 'string'
                                                            },
                                                        }
                                                    }
                                                },
                                            }
                                        },
                                        'listview': {
                                            'type': 'object',
                                            "additionalProperties": False,
                                            'required': [ 'width', 'index' ],
                                            'properties': {
                                                'width': {
                                                    'type': 'string'
                                                },
                                                'index': {
                                                    'type': 'integer'
                                                },
                                                'sort': {
                                                    'type': 'boolean'
                                                },
                                                'filter': {
                                                    'type': 'boolean'
                                                }
                                            }
                                        },
                                        'tab': {
                                            'type': 'object',
                                            "additionalProperties": False,
                                            'required': [ 'label', 'index' ],
                                            'properties': {
                                                'label': {
                                                    'type': 'string'
                                                },
                                                'index': {
                                                    'type': 'integer'
                                                }
                                            }
                                        },
                                        'test-data': {
                                            'type': 'object',
                                            "optional": True,
                                            "additionalProperties": False,
                                            'properties': {
                                                'value': {
                                                    'type': ['string', 'boolean', 'integer', 'number', 'object', 'null'],
                                                    "optional": True,
                                                },
                                                'values': {
                                                    'type': 'array',
                                                    "optional": True,
                                                    'items': {
                                                        'type': ['string', 'boolean', 'integer', 'number', 'object', 'null'],
                                                    }
                                                }
                                            }
                                        },
                                        'siblings': {
                                            'type': 'array',
                                            'items': {
                                                "type": "object",
                                                "required": [ 'label' ],
                                                "additionalProperties": False,
                                                "properties": {
                                                    'hint': {
                                                        'type': 'string',
                                                    },
                                                    'readonly': {
                                                        'type': 'boolean'
                                                    },
                                                    "remark": {
                                                        'type': 'string'
                                                    },
                                                    'label': {
                                                        'type': 'string'
                                                    },
                                                    'ui': {
                                                        'type': 'object',
                                                        'required': [ 'type' ],
                                                        "additionalProperties": False,
                                                        'properties': {
                                                            'type': {
                                                                "enum": [ 'textbox', 'editor', 'number', 'choice', 'choice-auto-complete',
                                                                        'textarea', 'checkbox', 'password', 'date', 'time', 'datetime',
                                                                        'label' ]
                                                            },
                                                            'format': {
                                                                'type': 'string'
                                                            },
                                                            'width': {
                                                                'type': 'integer'
                                                            },
                                                            'group': {
                                                                'type': 'string'
                                                            },
                                                            'ngIf': {
                                                                'type': 'string'
                                                            },
                                                            'hint': {
                                                                'type': 'string'
                                                            },
                                                            'pipe': {
                                                                'enum': [ 'date', 'datetime', 'time' ]
                                                            },
                                                            'cols': { 'type': 'integer', },
                                                            'rows': { 'type': 'integer', },
                                                            'resolve-list': {
                                                                'type': 'object',
                                                            },
                                                            'service': {
                                                                'type': 'object',
                                                                "additionalProperties": False,
                                                                'properties': {
                                                                    'name': {
                                                                        'type': 'string',
                                                                    },
                                                                    'path': {
                                                                        'type': 'string',
                                                                    },
                                                                    'base-class': {
                                                                        'type': 'string',
                                                                    },
                                                                    'class': {
                                                                        'type': 'string',
                                                                    },
                                                                    'value': {
                                                                        'type': 'string',
                                                                    },
                                                                    'label': {
                                                                        'type': 'string',
                                                                    },
                                                                }
                                                            },
                                                            'attributes': {
                                                                'type': 'object',
                                                                "additionalProperties": False,
                                                                'properties': {
                                                                    'language': {
                                                                        'enum': [ 'markdown',  'json', 'python', 'yaml', 'xml', 'sql', 'xpath' ]
                                                                    },
                                                                    'height': {
                                                                        'type': 'string',
                                                                    },
                                                                    'minimap': {
                                                                        'type': 'string',
                                                                    },
                                                                    'heightAdjust': {
                                                                        'type': 'string',
                                                                    },
                                                                    'decodeFunc': {
                                                                        'type': 'string',
                                                                    },
                                                                    'encodeFunc': {
                                                                        'type': 'string',
                                                                    },
                                                                    'onSaveClick': {
                                                                        'type': 'string',
                                                                    }
                                                                }
                                                            },
                                                            'actions': {
                                                                'type': 'array',
                                                                'items': {
                                                                    'type': 'object',
                                                                    'required': [ 'name', 'icon', 'position' ],
                                                                    "additionalProperties": False,
                                                                    'properties': {
                                                                        'name': {
                                                                            'type': 'string'
                                                                        },
                                                                        'icon': {
                                                                            'type': 'string'
                                                                        },
                                                                        'position': {
                                                                            'enum': [ 'row', 'left', 'right' ],
                                                                        },
                                                                        'function': {
                                                                            'type': 'string'
                                                                        },
                                                                    }
                                                                }
                                                            },
                                                        }
                                                    },
                                                    'listview': {
                                                        'type': 'object',
                                                        "additionalProperties": False,
                                                        'required': [ 'width', 'index' ],
                                                        'properties': {
                                                            'width': {
                                                                'type': 'string'
                                                            },
                                                            'index': {
                                                                'type': 'integer'
                                                            },
                                                            'sort': {
                                                                'type': 'boolean'
                                                            },
                                                            'filter': {
                                                                'type': 'boolean'
                                                            }
                                                        }
                                                    },
                                                    'tab': {
                                                        'type': 'object',
                                                        "additionalProperties": False,
                                                        'required': [ 'label', 'index' ],
                                                        'properties': {
                                                            'label': {
                                                                'type': 'string'
                                                            },
                                                            'index': {
                                                                'type': 'integer'
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        },

                                        # TODO: These need to be removed
                                        'default': {
                                            'type': 'string'
                                        },
                                        'autoupdate': {
                                            'type': 'string'
                                        },
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
