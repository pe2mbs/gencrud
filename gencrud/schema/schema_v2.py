import io
import yaml


_GENCRUD_SCHEME_V2_YAML = """---
'$schema': http://json-schema.org/draft-07/schema#
title: GenCrud
type: object
required: 
-   source
-   interface
-   objects
additionalProperties: true
properties:
    source:
        type: object
        additionalProperties: false
        properties:
            base:
                type: string
                optional: true
            python:
                type: string
            angular:
                type: string
            unittest:
                type: string
                optional': true
            ext-models:
                type: string
                optional: true
            help-pages:
                type: string
                optional: true
    templates:
        type: object
        optional: true
        additionalProperties: false
        properties:
            base:
                type: string
                optional: true
            python:
                type: string
            angular:
                type: string
            unittest:
                type: string
                optional: true
            ext-models:
                type: string
                optional: true
            help-pages:
                type: string
                optional: true
            common:
                type: object
                additionalProperties: false
                properties:
                    base:
                        type: string
                        optional: true
                    python:
                        type: string
                    angular:
                        type: string
                    unittest:
                        type: string
                        optional: true
                    ext-models:
                        type: string
                        optional: true
                    help-pages:
                        type: string
                        optional: true                       
    application:
        type: string
    interface:
        # When defining an interface instead of 'application'   
        type: object
        additionalProperties: false
        required: 
        -   backend  
        -   frontend  
        properties:
            backend:
                type: object
                additionalProperties: false
                properties:
                    path:
                        type: string   
                    module:
                        type: string                                         
                    package:
                        type: string                                         
            frontend:
                type: object
                additionalProperties: false
                required: 
                -   path  
                properties:
                    path:
                        type: string
                    class:
                        type: string
                    file:
                        type: string  
                    templates:
                        type: object
                        additionalProperties: false
                        required: 
                        -   route  
                        -   sub-route
                        -   module  
                        properties:
                            route:
                                type: string
                            sub-route:
                                type: string
                            module:
                                type: string                               
    nogen:
        type: boolean
    options:
        type: object
        additionalProperties: false
        properties:
            ignore-case-db-ids:
                type: boolean
            overwrite:            
                type: boolean
            use-module:           
                type: boolean
            generate-backend:
                type: boolean
            generate-frontend:
                type: boolean
            generate-tests:
                type: boolean
            generate-ext-models:
                type: boolean
            generate-help-pages:
                type: boolean
            use-prettier:
                type: boolean
            prettier-style:
                type: string
            use-yapf:
                type: boolean
            yapf-style:
                type: string
                default: pep8
    objects:
        type: array
        items:
            required: 
            -   name
            -   uri
            -   actions
            -   table
            -   route
            type: object
            additionalProperties: true
            properties:
                name:         
                    type: string
                autoupdate:   
                    type: integer
                title:        
                    type: string
                remark:       
                    type: string
                class:        
                    type: string
                uri:          
                    type: string
                action-width: 
                    type: string
                help:
                    type:   object
                    additionalProperties: false
                    properties:
                        title:  
                            type: string
                        table:
                            type: string
                        screen:
                            type: string
                        dialog:
                            type: string
                modules:
                    type: array
                    items:
                        type: object
                        required: 
                        -   class
                        -   path
                        additionalProperties: false
                        properties:
                            class:    
                                type: string
                            path:     
                                type: string
                            module:   
                                type: string
                mixin:
                    type: object
                    additionalProperties: false
                    properties:
                        angular:
                            type: object
                            additionalProperties: false
                            properties:
                                module:
                                    type: object
                                    required: 
                                    -   class
                                    -   file
                                    additionalProperties: false
                                    properties:
                                        class:
                                            type: string
                                        file:
                                            type: string
                                component.dialog:
                                    type: object
                                    required: 
                                    -   class
                                    -   file
                                    additionalProperties: false
                                    properties:
                                        class:
                                            type: string
                                        file:
                                            type: string
                                screen.component:
                                    type: object
                                    required:
                                    -   class
                                    -   file
                                    additionalProperties: false
                                    properties:
                                        class:
                                            type: string
                                        file:
                                            type: string
                                table.component:
                                    required: 
                                    -   class
                                    -   file
                                    type: object
                                    additionalProperties: false
                                    properties:
                                        class:
                                            type: string
                                        file:
                                            type: string
                        python:
                            type: object
                            additionalProperties: false
                            properties:
                                model:
                                    type: object
                                    additionalProperties: false
                                    properties:
                                        class: 
                                            type: string
                                        file: 
                                            type: string
                                schema:
                                    type: object
                                    additionalProperties: false
                                    properties:
                                        class:
                                            type: string
                                        file:
                                            type: string
                                view:
                                    type: object
                                    additionalProperties: false
                                    properties:
                                        class: 
                                            type: string
                                        file: 
                                            type: string
                ignore_templates: 
                    type: array
                providers:
                    type: array
                    items:
                        type: object
                        required: 
                        -   file
                        -   class
                        properties:
                            file:     
                                type: string
                            class:    
                                type: string
                injection:
                    type: object
                    properties:
                        module.ts:
                            type: object
                            properties:
                                dialog:
                                    type: object
                                    properties:
                                        class: 
                                            type: string
                                        file: 
                                            type: string
                route: 
                    type: string
                ignore-route:
                    type: boolean
                actions:
                    type: array
                    items:
                        type: object
                        required: 
                        -   name
                        -   type
                        additionalProperties: false
                        properties:
                            name:     
                                type: string
                            label:    
                                type: string
                            type:     
                                type: string
                                enum: 
                                -   screen
                                -   dialog
                                -   api
                                -   function
                                -   button
                                -   none
                            icon:     
                                type: string
                            help:
                                type: string
                            position: 
                                enum: 
                                -   row
                                -   header
                                -   footer
                                -   cell
                                -   none
                                -   screen
                                -   sidebar
                            uri:      
                                type: string
                            function: 
                                type: string
                            directive: 
                                type: string
                            class:
                                type: string
                            file:
                                type: string
                            index:    
                                type: integer
                            disabled: 
                                type: 
                                -   string
                                -   boolean
                            ngIf:     
                                type: string
                            params:
                                type: object
                                additionalProperties: true
                                properties:
                                    id:       
                                        type: string
                                    value:    
                                        type: string
                            route:
                                type: object
                                additionalProperties: false
                                properties:
                                    class: 
                                        type: string
                                    name: 
                                        type: string
                                    module: 
                                        type: string
                                    route: 
                                        type: string
                                    params:
                                        type: object
                                        required: 
                                        -   mode
                                        properties:
                                            mode:  
                                                type: string
                                            id:    
                                                type: 
                                                -   number
                                                -   string
                                            value: 
                                                type: string
                menu:
                    # At this moment we support only 3 levels.
                    type: object
                    required: 
                    -   caption
                    additionalProperties: false
                    properties:
                        caption:
                            type: string
                        icon:
                            type: string
                        after:
                            type: 
                            -   string
                            -   "null"
                        before:
                            type: 
                            -   string
                            -   "null"
                        route:
                            type: string
                        access:
                            type: string
                        menu:
                            type: object
                            required: 
                            -   caption
                            additionalProperties: false
                            properties:
                                caption:
                                    type: string
                                icon:
                                    type: string
                                after:
                                    type: 
                                    -   string
                                    -   "null"
                                before:
                                    type: 
                                    -   string
                                    -   "null"
                                route:
                                    type: string
                                access:
                                    type: string
                                menu:
                                    type: object
                                    required:
                                    -   caption
                                    additionalProperties: false
                                    properties:
                                        caption:
                                            type: string
                                        icon:
                                            type: string
                                        after:
                                            type: 
                                            -   string
                                            -   "null"
                                        before:
                                            type: 
                                            -   string
                                            -   "null"  
                                        route:
                                            type: string
                                        access:
                                            type: string  
                                        menu:
                                            type: object
                table:
                    type: object
                    required: 
                    -   name
                    -   columns
                    additionalProperties: true
                    properties:
                        engine:
                            type: object
                            required: 
                            -   module
                            -   connect
                            additionalProperties: true
                            properties:
                                module: 
                                    type: string
                                connect: 
                                    type: string
                        name:
                            type: string
                        secondary-key:
                            type: string
                            optional: true
                        unique-key: 
                            type: string
                        relationships:
                            type: array
                            items:
                                type: object
                                required:
                                -   name
                                -   model
                                -   populates
                                additionalProperties: false
                                properties:
                                    name:
                                        type:   string
                                    model:
                                        type:   string
                                    populates:
                                        type:   string
                                    cascade:    
                                        type:   string
                                    single-parent:
                                        type:   boolean
                        viewSort:
                            type: object
                            required: 
                            -   field
                            -   direction
                            additionalProperties: false
                            properties:
                                field:
                                    type: string
                                direction:
                                    enum: 
                                    -   desc
                                    -   asc
                        viewFilter:
                            type: array
                            items:
                                type: object
                                required: 
                                -   column
                                -   value
                                -   operator
                                additionalProperties: false
                                properties:
                                    column:
                                        type: string
                                    value:
                                        type: 
                                        -   integer
                                        -   string
                                    operator:
                                        type: string
                        hint:
                            type: string
                        tabs:
                            type: object
                            required: 
                            -   labels
                            additionalProperties: false
                            properties:
                                labels:
                                    type: array
                                    items:
                                        type: string
                                tab:
                                    type: array
                                    items:
                                        type: object
                                        required: 
                                        -   label
                                        -   component
                                        # -   name
                                        # -   file
                                        -   params
                                        additionalProperties: false
                                        properties:
                                            label:
                                                type: string
                                            component:
                                                type: string
                                            name:
                                                type: string
                                            class:
                                                type: string
                                            file:
                                                type: string
                                            help:
                                                type: string
                                            params:
                                                type: object
                                                required: 
                                                -   id
                                                -   value
                                                additionalProperties: false
                                                properties:
                                                    id:
                                                        type: string
                                                    value:
                                                        type: string
                                                    caption:
                                                        type: boolean
                                                    displayedColumns:
                                                        type: string
                        columns:
                            type: array
                            items:
                                type: object
                                required: 
                                -   field
                                additionalProperties: false
                                properties:
                                    field:
                                        type: string
                                    hint:
                                        type: string
                                    readonly:
                                        type: boolean
                                    frontend:
                                        type: boolean
                                    remark:
                                        type: string
                                    name:
                                        type: string
                                    unique:
                                        type: boolean
                                    unique-key:
                                        type: string
                                    label:
                                        type: string
                                    help:
                                        type: string
                                    ui:
                                        type: object
                                        required: 
                                        -   type
                                        additionalProperties: false
                                        properties:
                                            type:
                                                enum: 
                                                -   textbox
                                                -   editor
                                                -   number
                                                -   choice
                                                -   choice-auto-complete
#                                                -   choice-base
                                                -   textarea
                                                -   checkbox
                                                -   password
                                                -   date
                                                -   time
                                                -   datetime
                                                -   label
                                            format:
                                                type: string
                                            width:
                                                type: string
                                            group:
                                                type: string
                                            index:
                                                type: integer
                                            ngIf:
                                                type: string
                                            disabled:
                                                type: string
                                            hint:
                                                type: string
                                            pipe:
                                                enum: 
                                                -   date
                                                -   datetime
                                                -   time
                                            timezone:
                                                type:   string
                                            cols: 
                                                type: integer
                                            resolve-list:
                                                type: object
                                            service:
                                                type: object
                                                additionalProperties: false
                                                properties:
                                                    name:
                                                        type: string
                                                    path:
                                                        type: string
                                                    base-class:
                                                        type: string
                                                    class:
                                                        type: string
                                                    module:
                                                        type: string
                                                    value:
                                                        type: string
                                                    label:
                                                        type: string
                                                    filter:
                                                        type: object
                                                        optional: true
                                                        additionalProperties: true
                                            actions:
                                                type: array
                                                items:
                                                    type: object
                                                    required: 
                                                    -   name 
                                                    -   icon
                                                    -   position
                                                    additionalProperties: false
                                                    properties:
                                                        name:
                                                            type: string
                                                        icon:
                                                            type: string
                                                        position:
                                                            enum: 
                                                            -   prefix
                                                            -   suffix
                                                        route:
                                                            type: string
                                                        function:
                                                            type: string
                                                        ngIf:
                                                            type: string
                                                        disabled:
                                                            type: string
                                            monaco:
                                                type: object
                                                additionalProperties: false
                                                required: 
                                                -   language
                                                properties:
                                                    minimap:
                                                        type: boolean
                                                    language:
                                                        type: string
                                                    theme:
                                                        type: string
                                                    height:
                                                        type: string
                                                    function:
                                                        type: string
                                                    file:
                                                        type: string
                                                    actionbar:
                                                        type: array
                                                        items:
                                                            type: object
                                                            required: 
                                                            -   tooltip
                                                            -   action
                                                            -   icon
                                                            additionalProperties: false
                                                            properties:
                                                                tooltip:
                                                                    type: string
                                                                action:
                                                                    type: string
                                                                icon:
                                                                    type: string
                                            
                                    listview:
                                        type: object
                                        additionalProperties: false
                                        required: 
                                        -   width
                                        -   index
                                        properties:
                                            width:
                                                type: string
                                            index:
                                                type: integer
                                            sort:
                                                type: boolean
                                            filter:
                                                type: boolean
                                    tab:
                                        type: object
                                        additionalProperties: false
                                        required: 
                                        -   label
                                        -   index
                                        properties:
                                            label:
                                                type: string
                                            index:
                                                type: integer
                                    test-data:
                                        type: object
                                        optional: true
                                        additionalProperties: false
                                        properties:
                                            value:
                                                type: 
                                                -   string
                                                -   boolean
                                                -   integer
                                                -   number
                                                -   object
                                                optional: true
                                            values:
                                                type: array
                                                optional: true
                                                items:
                                                    type: 
                                                    -   string
                                                    -   boolean
                                                    -   integer
                                                    -   number
                                                    -   object
                                    siblings:
                                        type: array
                                        items:
                                            type: object
                                            required: 
                                            -   label
                                            additionalProperties: false
                                            properties:
                                                hint:
                                                    type: string
                                                readonly:
                                                    type: boolean
                                                remark:
                                                    type: string
                                                label:
                                                    type: string
                                                ui:
                                                    type: object
                                                    required: 
                                                    -   type
                                                    additionalProperties: false
                                                    properties:
                                                        type:
                                                            enum: 
                                                            -   textbox
                                                            -   editor
                                                            -   number
                                                            -   choice
                                                            -   choice-auto-complete
#                                                            -   choice-base
                                                            -   textarea
                                                            -   checkbox
                                                            -   password
                                                            -   date
                                                            -   time
                                                            -   datetime
                                                            -   label
                                                        format:
                                                            type: string
                                                        width:
                                                            type: string
                                                        group:
                                                            type: string
                                                        ngIf:
                                                            type: string
                                                        disabled:
                                                            type: string
                                                        hint:
                                                            type: string
                                                        pipe:
                                                            enum: 
                                                            -   date
                                                            -   datetime
                                                            -   time
                                                        timezone:
                                                            type:   string                                                            
                                                        cols: 
                                                            type: integer
                                                        rows: 
                                                            type: integer
                                                        resolve-list:
                                                            type: object
                                                        service:
                                                            type: object
                                                            additionalProperties: false
                                                            properties:
                                                                name:
                                                                    type: string
                                                                path:
                                                                    type: string
                                                                base-class:
                                                                    type: string
                                                                class:
                                                                    type: string
                                                                value:
                                                                    type: string
                                                                label:
                                                                    type: string
                                                                filter:
                                                                    type: object
                                                                    optional: true
                                                                    additionalProperties: true
                                                        actions:
                                                            type: array
                                                            items:
                                                                type: object
                                                                required: 
                                                                -   name
                                                                -   icon
                                                                -   position
                                                                additionalProperties: false
                                                                properties:
                                                                    name:
                                                                        type: string
                                                                    icon:
                                                                        type: string
                                                                    position:
                                                                        enum: 
                                                                        -   row
                                                                        -   left
                                                                        -   right
                                                                    function:
                                                                        type: string
                                                        monaco:
                                                            type: object
                                                            additionalProperties: false
                                                            required: 
                                                            -   language
                                                            properties:
                                                                minimap:
                                                                    type: boolean
                                                                language:
                                                                    type: string
                                                                height:
                                                                    type: string
                                                                theme:
                                                                    type: string
                                                                function:
                                                                    type: string
                                                                file:
                                                                    type: string
                                                                    type: string
                                                                actionbar:
                                                                    type: array
                                                                    items:
                                                                        type: object
                                                                        required: 
                                                                        -   tooltip
                                                                        -   action
                                                                        -   icon
                                                                        additionalProperties: false
                                                                        properties:
                                                                            tooltip:
                                                                                type: string
                                                                            action:
                                                                                type: string
                                                                            icon:
                                                                                type: string
                                                listview:
                                                    type: object
                                                    additionalProperties: false
                                                    required: 
                                                    -   width
                                                    -   index
                                                    properties:
                                                        width:
                                                            type: string
                                                        index:
                                                            type: integer
                                                        sort:
                                                            type: boolean
                                                        filter:
                                                            type: boolean
                                                tab:
                                                    type: object
                                                    additionalProperties: false
                                                    required: 
                                                    -   label
                                                    -   index
                                                    properties:
                                                        label:
                                                            type: string
                                                        index:
                                                            type: integer
"""


def getTemplateV2():
    return yaml.load( io.StringIO( _GENCRUD_SCHEME_V2_YAML ), Loader = yaml.Loader )
