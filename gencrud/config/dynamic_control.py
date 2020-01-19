import yaml
from gencrud.config.dynamic.controls import DymanicControls
from gencrud.config.dynamic.control import TemplateDymanicControl

def main():
    ctrls = DymanicControls()

    # filename = '/home/mbertens/src/python/pytemplate/gencrud/templates/pyt-controls.yaml'
    # with open( filename, 'r' ) as stream:
    #     cfg = yaml.load( stream, Loader = yaml.Loader )
    #
    # for name, value in cfg.items():
    #     if any(c.islower() for c in name):
    #         ctrls.append( TemplateDymanicControl( ctrls,
    #                                               name,
    #                                               arguments = value[ 'properties' ],
    #                                               htmlTemplate = value[ 'html' ] ) )
    #
    #
    # obj = ctrls.get( 'password' )
    # obj.hint.value = "This is a TEST to set the dynamic property"
    # obj.error.value = True
    #
    # obj.dump()
    # obj.hint.value = None
    # data = { 'hint':        { 'default': 'This is the second text', 'type': 'str' },
    #          'minLength':   { 'default': 8, 'type': 'int' },
    #          'maxLength':   { 'default': 32, 'type': 'int' },
    #          'allowed':     { 'default': [ 'lower', 'upper', 'digit' ], 'type': 'list' } }
    # obj.set( data )
    # obj.dump()
    # obj.maxLength.value = 64
    # obj.dump()

    inputFile = '/home/mbertens/src/angular/mat-table-crud/templates/systems.yaml'
    with open( inputFile, 'r' ) as stream:
        config = TemplateConfiguration( **yaml.load( stream ) )

    for obj in config:
        print( "Object name: {}".format( obj.name ) )
        for fld in obj.table:
            print( "Field name: {}".format( fld.name ) )
            print( fld.build( ctrls, config ) )


if __name__ == '__main__':

    import io
    import copy
    from gencrud.configuraton import TemplateConfiguration

    main()
