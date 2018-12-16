import os
import json
from mako.template import Template


pythonpath  = './output/backend'
angularpath = './output/src/app'
data = [
    {
        'name':                     'role',     # module name, variable name prefix
        'cls':                      'Role',     # Class name
        'application':              'testrun',
        # To generate the view
        'uri':                      '/api/role',
        # To generate the model
        'table_name':               'WA_ROLES',
        'primaryKeyField':          'D_ROLE_ID',
        'columns':[
            {
                'label':            'Identification',
                'index':            0,
                'ui':               'label',
                'name':             'D_ROLE_ID',
                'type_length':      'Integer',
                'length':           10,
                'type_js':          'number',
                'attrs': [
                    'auto_number=True',
                    'primary_key=True'
                ]
            },
            {
                'label':            'Role',
                'index':            1,
                'ui':               'textbox',
                'name':             'D_ROLE',
                'type_length':      'String( 20 )',
                'length':           20,
                'type_js':          'string',
                'attrs': [
                    'null=False'
                ]
            },
            {
                'label':            'Users',
                'ui':               'label',
                'name':             'USERS',
                'relationship':     'User',
                'type_js':          'User',
            },
        ]
    },
    {
        'name':                     'user',     # module name, variable name prefix
        'cls':                      'User',     # Class name
        'application':              'testrun',
        # To generate the view
        'uri':                      '/api/user',
        # To generate the model
        'table_name':               'WA_USERS',
        'primaryKeyField':          'D_USER_ID',
        'columns':[
            {
                'label':            'Identification',
                'index':            0,
                'ui':               'label',
                'name':             'D_USER_ID',
                'type_length':      'Integer',
                'length':           10,
                'type_js':          'number',
                'attrs': [
                    'auto_number=True',
                    'primary_key=True'
                ]
            },
            {
                'label':            'User name',
                'index':            1,
                'ui':               'textbox',
                'name':             'D_USER_NAME',
                'type_length':      'String( 20 )',
                'length':           20,
                'type_js':          'string',
                'attrs': [
                    'null=False'
                ]
            },
            {
                'label':            'Password',
                'index':            2,
                'ui':               'password',
                'name':             'D_PASSWORD',
                'type_length':      'String( 64 )',
                'length':           64,
                'type_js':          'string',
                'attrs': [
                    'null=False'
                ]
            },
            {
                'label':            'First name',
                'index':            3,
                'ui':               'textbox',
                'name':             'D_FIRST_NAME',
                'type_length':      'String( 30 )',
                'length':           30,
                'type_js':          'string',
                'attrs': [
                    'null=False'
                ]
            },
            {
                'label':            'Middle name',
                'index':            4,
                'ui':               'textbox',
                'name':             'D_MIDDLE_NAME',
                'type_length':      'String( 30 )',
                'length':           30,
                'type_js':          'string',
                'attrs': [
                    'null=True'
                ]
            },
            {
                'label':            'Last name',
                'index':            5,
                'ui':               'textbox',
                'name':             'D_LAST_NAME',
                'type_length':      'String( 30 )',
                'length':           30,
                'type_js':          'string',
                'attrs': [
                    'null=False'
                ]
            },
            {
                'label':            'Role',
                'ui':               'choice',
                'name':             'D_ROLE_ID',
                'type_js':          'number',
                'type_length':      'Integer, ForeignKey( "WA_ROLES.D_ROLE_ID" )',
                'attrs': [
                    'null=False'
                ]
            },
            {
                'label':            'Role',
                'ui':               'label',
                'name':             'ROLE',
                'relationship':     'Role',
                'type_js':          'Role',
            },
        ]
    }
]


def makePythonModules( root_path, *args ):
    def write__init__py():
        with open( os.path.join( root_path, '__init__.py' ), 'w' ) as stream:
            print( '', file = stream )

    if len( args ) > 0:
        modulePath = os.path.join( root_path, args[ 0 ] )
        if not os.path.isdir( modulePath ):
            os.mkdir( modulePath )

        makePythonModules( modulePath, *args[ 1: ] )

        if not os.path.isfile( os.path.join( root_path, '__init__.py' ) ):
            write__init__py()

    else:
        if not os.path.isfile( os.path.join( root_path, '__init__.py' ) ):
            write__init__py()

    return


def generatePython():
    templates = [ 'templates/python/model.templ',
                  'templates/python/schema.templ',
                  'templates/python/view.templ' ]
    def moduleName( templateName ):
        return os.path.splitext( os.path.basename( templateName ) )[ 0 ]

    for cfg in data:
        for templ in templates:
            #print( templ )
            #print( json.dumps( cfg, indent = 4, sort_keys = True ) )
            makePythonModules( pythonpath, cfg[ 'application' ], cfg[ 'name' ] )
            with open( os.path.join( pythonpath,
                                     cfg[ 'application' ],
                                     cfg[ 'name' ], moduleName( templ ) ), 'w' ) as stream:

                print( Template( filename=os.path.abspath( templ ) ).
                       render( **cfg ), file = stream )

    return


def makeAngularModule( root_path, *args ):
    if len( args ) > 0:
        modulePath = os.path.join( root_path, args[ 0 ] )
        if not os.path.isdir( modulePath ):
            os.mkdir( modulePath )

        makeAngularModule( modulePath, *args[ 1: ] )

    return


def generateAngular():
    def moduleName( templateName ):
        return os.path.splitext( os.path.basename( templateName ) )[ 0 ]

    templates = [ 'templates/angular/addedit.dialog.html.templ',
                  'templates/angular/addedit.dialog.ts.templ',
                  'templates/angular/table.component.html.templ',
                  'templates/angular/table.component.scss.templ',
                  'templates/angular/table.component.spec.ts.templ',
                  'templates/angular/table.component.ts.templ',
                  'templates/angular/datasource.ts.templ',
                  'templates/angular/delete.dialog.html.templ',
                  'templates/angular/delete.dialog.ts.templ',
                  'templates/angular/datasource.ts.templ',
                  'templates/angular/model.ts.templ',
                  'templates/angular/service.ts.templ' ]
    
    for cfg in data:
        for templ in templates:
            makeAngularModule( angularpath, cfg[ 'application' ],
                                            cfg[ 'name' ] )
            with open( os.path.join( angularpath,
                                     cfg[ 'application' ],
                                     cfg[ 'name' ], moduleName( templ ) ),
                       'w' ) as stream:
                print( Template( filename=os.path.abspath( templ ) ).
                       render( **cfg ), file = stream )

    return


def main():
    #generatePython()
    generateAngular()


if __name__ == '__main__':
    main()