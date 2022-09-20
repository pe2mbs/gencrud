#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2020 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#   Library General Public License for more details.
#
#   You should have received a copy of the GNU Library General Public
#   License GPL-2.0-only along with this library; if not, write to the
#   Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301 USA
#
C_APPLICATION           = 'application'
C_FILE                  = 'file'
C_FILENAME              = 'filename'
C_FILTER                = 'filter'
C_BASECLASS             = 'base-class'
C_CLASS                 = 'class'
C_MODULE                = 'module'
C_GROUP                 = 'group'
C_MODULES               = 'modules'
C_OPTIONS               = 'options'
C_REFERENCES            = 'references'
C_OBJECTS               = 'objects'
C_OBJECT                = 'object'
C_CONTROLS              = 'controls'
C_ROOT                  = 'root'
C_AUTO_UPDATE           = 'autoupdate'
C_NO_GENERATE           = 'nogen'
C_USE_MODULE            = 'use-module'
C_BACKUP                = 'backup'
C_IGNORE_CASE_DB_IDS    = 'ignore-case-db-ids'
C_OVERWRITE             = 'overwrite'
C_LAZY_LOADING          = 'lazy-loading'
C_SORT                  = 'sort'

C_APP_MODULE            = 'app-module'
C_APP_ROUTING           = 'app-routing'

C_SOURCE                = 'source'
C_BASE                  = 'base'
C_PYTHON                = 'python'
C_COMMON                = 'common'
C_TEMPLATES_DIR         = 'templates'
C_ANGULAR               = 'angular'
C_TYPESCRIPT            = 'typescript'
C_TEMPLATE              = 'template'
C_UNITTEST              = 'unittest'

C_PLATFORM_LINUX        = 'linux'
C_PLATFORM_WINDOS       = 'windows'
C_PLATFORM_OSX          = 'osx'
C_PLATFORMS             = ( C_PLATFORM_LINUX, C_PLATFORM_WINDOS, C_PLATFORM_OSX )

C_VERSION               = 'version'
C_VERSION_DEFAULT       = 2
C_MENU                  = 'menu'
C_ACTIONS               = 'actions'
C_ACTION                = 'action'
C_TABLE                 = 'table'
C_CASCADE               = 'cascade'
C_EXTRA                 = 'extra'
C_TITLE                 = 'title'
C_NAME                  = 'name'
C_URI                   = 'uri'
C_URL                   = 'url'
C_ACTION_WIDTH          = 'action-width'
C_INDEX                 = 'index'
C_CAPTION               = 'caption'
C_ICON                  = 'icon'
C_ROUTE                 = 'route'
C_COMPONENT             = 'component'
C_TYPE                  = 'type'
C_WHERE                 = 'where'
C_PATH                  = 'path'
C_IMPORTS               = 'imports'
C_INJECTION             = 'injection'
C_PROVIDERS             = 'providers'
C_POSITION              = 'position'
C_NONE                  = 'none'
C_LABEL                 = 'label'
C_LABELS                = 'labels'
C_PARAMS                = 'params'
C_ON                    = 'on'
C_FUNCTION              = 'function'

C_EXPORT                = 'export'
C_DIALOGS               = 'dialogs'
C_DIALOG                = 'dialog'
C_COMPONENTS            = 'components'
C_SERVICES              = 'services'
C_SCREEN                = 'screen'
C_LIST                  = 'list'
C_API                   = 'api'
C_DIRECTIVE             = 'directive'

C_CELL                  = 'cell'
C_ROW                   = 'row'
C_FOOTER                = 'footer'
C_HEADER                = 'header'

C_CLICK                 = 'click'
C_DBLCLICK              = 'dblclick'
C_DOUBLE_CLICK          = 'dblclick'
C_MIXIN                 = 'mixin'

C_LEFT                  = 'left'
C_RIGHT                 = 'right'
C_SIDEBAR               = 'sidebar'

C_ACTION_TYPES          = ( C_DIALOG, C_SCREEN, C_LIST, C_API, C_DIRECTIVE, C_NONE )
C_ACTION_POSITIONS      = ( C_CELL, C_HEADER, C_FOOTER, C_ROW, C_NONE, C_SCREEN, C_LEFT, C_RIGHT, C_SIDEBAR )
C_ACTION_ATTRIBUTES     = ( C_FUNCTION,
                            C_NAME,
                            C_LABEL,
                            C_ICON,
                            C_SOURCE,
                            C_POSITION,
                            C_TYPE,
                            C_URI,
                            C_ROUTE,
                            C_PARAMS,
                            C_ON )
C_ACTION_ON_ACTIONS     = ( C_CLICK,
                            C_DOUBLE_CLICK )

C_HINT                  = 'hint'
C_COLOR                 = 'color'
C_COLOR_PRIMARY         = 'primary'

C_CSS                   = 'css'

C_NEW                   = 'new'
C_EDIT                  = 'edit'
C_DELETE                = 'delete'

C_COLUMNS               = 'columns'

C_TABS                  = 'tabs'
C_TAB                   = 'tab'
C_TAB_TAG               = 'tabtag'
C_TAB_CONTENT_TAG       = 'contenttag'
C_TAB_GROUP_TAG         = 'grouptag'
C_MIXIN                 = 'mixin'
C_VIEW_SORT             = 'viewSort'
C_VIEW_SIZE             = 'viewSize'
C_UNIQUE_KEY            = 'unique-key'
C_UNIQUE                = 'unique'
C_SECONDARY_KEY         = 'secondary-key'

C_ASCENDING             = 'asc'
C_DESENDING             = 'desc'
C_DIRECTIONS            = ( C_ASCENDING, C_DESENDING, '' )

C_FIELD                 = 'field'
C_DIRECTION             = 'direction'

C_MODEL                 = 'model'
C_SCHEMA                = 'schema'
C_VIEW                  = 'view'

C_SERVICE               = 'service'


C_ROWS                  = 'rows'
C_COLS                  = 'cols'
C_MIN                   = 'min'
C_MINIMAL               = 'minimal'
C_MAX                   = 'max'
C_MAXIMAL               = 'maximal'

C_PREFIX                = 'prefix'
C_PREFIX_TYPE           = 'prefix-type'
C_SUFFIX                = 'suffix'
C_SUFFIX_TYPE           = 'suffix-type'

C_TEXTBOX               = 'textbox'
C_TEXT                  = 'text'
C_CHECKBOX              = 'checkbox'
C_PASSWORD              = 'password'
C_TEXTAREA              = 'textarea'
C_EDITOR                = 'editor'
C_NUMBER                = 'number'
C_EMAIL                 = 'email'
C_CHOICE                = 'choice'
C_CHOICE_AUTO           = 'choice-auto-complete'
C_COMBOBOX              = 'combobox'
C_COMBO                 = 'combo'
C_SLIDER                = 'slider'
C_SLIDER_TOGGLE         = 'slidertoggle'
C_DATE                  = 'date'
C_TIME                  = 'time'
C_DATE_TIME             = 'datetime'
C_DATE_PICKER           = 'datepicker'
C_TIME_PICKER           = 'timepicker'
C_DATE_TIME_PICKER      = 'datetimepicker'
C_INTERVAL              = 'interval'
C_DISABLED              = 'disabled'
C_VERTICAL              = 'vertical'
C_PIPE                  = 'pipe'
C_FORMAT                = 'format'
C_INVERT                = 'invert'
C_STEP                  = 'step'
C_THUMB_LABEL           = 'thumbLabel'
C_CHECKED               = 'checked'
C_ERROR                 = 'error'
C_LABEL_POSITION        = 'labelPosition'
C_RESOLVE_LIST          = 'resolve-list'
C_RESOLVE_LIST_OLD      = 'resolveList'
C_VALUE                 = 'value'
C_VALUES                = 'values'
C_CONSTANT_FORMAT       = 'constant-format'
C_AFTER                 = 'after'
C_BEFORE                = 'before'

C_DEBUG                 = 'debug'
C_SIBLINGS              = 'siblings'
C_ISSIBLING             = 'isSibling'

C_FIELD_NAME            = 'field-name'
C_LAZY                  = 'lazy'
C_WIDTH                 = 'width'
C_UI                    = 'ui'
C_LIST_VIEW             = 'listview'
C_TEST_DATA             = 'test-data'
C_RELATION_SHIP         = 'relationship'
C_AUTO_UPDATE           = 'autoupdate'
C_DEFAULT               = 'default'
C_DEFAULTS              = 'defaults'
C_INIT                  = 'init'
C_INITIAL_VALUE         = 'initialValue'
C_READ_ONLY             = 'readonly'

C_GENERATE_FRONTEND     = 'generate-frontend'
C_GENERATE_BACKEND      = 'generate-backend'
C_GENERATE_TESTS        = 'generate-tests'

C_GENCRUD_TEMPLATES     = 'GENCRUD_TEMPLATES'
C_GENCRUD               = 'GENCRUD'

C_NOTAB                 = 'notab'
C_NOGROUP               = 'nogroup'
