import os
from pytemplate.util.exceptions import ( MissingTemplate,
                                         MissingSourceFolder,
                                         KeyNotFoundException,
                                         MissingTemplateFolder,
                                         PathNotFoundException )
from platform import system

class TemplateSource( object ):
    def __init__( self, tp, **cfg ):
        platf = system().lower()
        self.__config = cfg
        self.__key = tp
        self.__source = self.__config.get( platf, self.__config ).get( 'source', {} )
        self.__template = self.__config.get( platf, self.__config ).get( 'template',
                        os.path.abspath( os.path.join( os.path.dirname( __file__ ), 'templates' ) ) )
        return

    @property
    def baseFolder( self ):
        folder = self.__source.get( 'base', os.getcwd() )
        if not os.path.isdir( folder ):
            raise PathNotFoundException( folder )

        return folder

    @property
    def sourceFolder( self ):
        folder = self.__source.get( self.__key, None )
        if folder is None:
            raise KeyNotFoundException( "source.{}".format( self.__key ) )

        if not folder.startswith( os.path.pathsep ):
            # not absolute path
            # first test with baseFolder
            if os.path.isdir( os.path.join( self.baseFolder, folder ) ):
                folder = os.path.join( self.baseFolder, folder )

            folder = os.path.abspath( folder )

        if not os.path.isdir( folder ):
            raise MissingSourceFolder( folder )

        return folder

    @property
    def templateFolder( self ):
        folder = os.path.join( self.__template, self.__key )
        if not os.path.isdir( folder ):
            raise MissingTemplateFolder( folder )

        # Now check if the templates exists
        cnt = 0
        for templ_file in os.listdir( folder ):
            if os.path.splitext( templ_file )[ 1 ] == '.templ':
                cnt += 1

        if cnt == 0:
            raise MissingTemplate( self.__template )

        return folder

    def __repr__( self ):
        return """<TemplateSource {key}
        base = {base} 
        source = {src}
        template = {templ}>""".format( key      = self.__key,
                                       src      = self.sourceFolder,
                                       templ    = self.templateFolder,
                                       base     = self.baseFolder )


class TemplateSourcePython( TemplateSource ):
    def __init__( self, **cfg ):
        TemplateSource.__init__( self, 'python', **cfg )
        return


class TemplateSourceAngular( TemplateSource ):
    def __init__( self, **cfg ):
        TemplateSource.__init__( self, 'angular', **cfg )
        return


DATA1 = {   'source': {
                'python':   '/home/mbertens/src/angular/angular-mat-table-crud/backend',
                'angular':  '/home/mbertens/src/angular/angular-mat-table-crud/src/app'
            }
        }

DATA2 = {   'source': {
                'base':     '/home/mbertens/src/angular/angular-mat-table-crud',
                'python':   'backend',
                'angular':  'src/app'
            },
            'template': '/home/mbertens/src/python/pytemplate/pytemplate/templates'
        }

DATA3 = {   'linux': {
                'source': {
                    'base':     '/home/mbertens/src/angular/angular-mat-table-crud',
                    'python':   'backend',
                    'angular':  'src/app'
                }
            },
            'windows':
            {
                'source': {
                    'base': '\\src\\angular\\angular-mat-table-crud',
                    'python': 'backend',
                    'angular': 'src\\app'
                }
            }
        }

DATA = [ DATA1, DATA2, DATA3 ]


if __name__ == '__main__':
    for data in DATA:
        obj = TemplateSourcePython( **data )
        print( obj )
        print()
        obj = TemplateSourceAngular( **data )
        print( obj )
        print()
