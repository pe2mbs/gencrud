from nltk.tokenize import word_tokenize

class SourceItemImport( object ):
    def __init__( self, name = '', module = '' ):
        self.__name     = name
        self.__module   = module
        return

    @property
    def module( self ):
        return self.__module

    @property
    def name( self ):
        return self.__name


class SourceImport( object ):
    def __init__( self ):
        self.__pyList = []
        self.__tsList = []
        return

    @property
    def python(self):
        return self.__pyList

    @property
    def typescript(self):
        return self.__tsList

    def appendPy(self, data ):
        def exists( name, module ):
            found = False
            for obj in self.__pyList:
                if obj.module == module and obj.name == name:
                    found = True
                    break

            return found

        if type( data ) in ( list, tuple ):
            pass

        elif type( data ) is str:
            data = data.split( ',' )

        else:
            raise Exception( 'Invalid data type for python inport' )

        for importDef in data:
            name, module = word_tokenize( importDef )
            if not exists( name, module ):
                self.__pyList.append( SourceItemImport( name, module ) )

        return

    def appendTs(self, data ):
        def exists( name, module ):
            found = False
            for obj in self.__tsList:
                if obj.module == module and obj.name == name:
                    found = True
                    break

            return found

        if type( data ) in ( list, tuple ):
            pass

        elif type( data ) is str:
            data = data.split( ',' )

        else:
            raise Exception( 'Invalid data type for typescript inport' )

        for importDef in data:
            name, module = word_tokenize( importDef )
            if not exists( name, module ):
                self.__tsList.append( SourceItemImport( name, module ) )

        return

    def append( self, source, data ):
        if source == 'pyInport':
            self.appendPy( data )

        elif source == 'tsInport':
            self.appendTs( data )

        else:
            raise Exception( 'Invalid import type {0}'.format( source ) )

        return
