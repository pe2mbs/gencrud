import os
import shutil

from pytemplate.util.positon import PositionInterface

sslVerify       = True
verbose         = False
backupFiles     = False
overWriteFiles  = False

C_FILEMODE_UPDATE = 'r+'
C_FILEMODE_WRITE  = 'w'
C_FILEMODE_READ   = 'r'


def backupFile( file_name ):
    if backupFiles:
        idx = 1
        while os.path.isfile( file_name + '.~{0}'.format( idx ) ):
            idx += 1

        shutil.copyfile( file_name, file_name + '.~{0}'.format( idx ) )

    return


def joinJson( json1, json2 ):
    result = {}
    for key, value in json2.items():
        if key not in result:
            result[ key ] = value

    for key, value in json1.items():
        if type( value ) in ( list, tuple ):
            for item in value:
                if item not in result[ key ]:
                    result[ key ].append( item )

        elif type( value ) is dict:
            result[ key ] = joinJson( result[ key ], value )

        else:
            result[ key ] = value

    return result


def findImportSection( lines ):
    rangePos            = PositionInterface()
    for lineNo, lineText in enumerate( lines ):
        if lineText.startswith( 'import' ) or ( lineText.startswith( 'from' ) and
                                                'import' in lineText ):
            rangePos.end = lineNo

    return rangePos


def insertLinesUnique( lines, rangeObj, line ):
    found = False
    if verbose:
        print( "insertLinesUnique from line {} to line {}".format( rangeObj.start, rangeObj.end ) )

    end = rangeObj.end
    if end + 1 < len( lines ):
        end += 1

    for idx in range( rangeObj.start, end ):
        if verbose:
            print( "Check line {} of {} => '{}'".format( idx, rangeObj.end, lines[ idx ].strip( '\r\n') ) )

        if line in lines[ idx ].strip( '\n' ):
            found = True

    if not found:
        if verbose:
            print( 'inject files [{0}] @ {1}'.format( line, rangeObj.end ) )

        lines.insert( rangeObj.end+1, line + '\n' )
        rangeObj.end += 1


    return


def searchSection( lines, rangeObj, sectionStart, sectionEnd ):
    stage = 0
    for lineNo, lineText in enumerate( lines ):
        if stage == 0 and lineText.startswith( sectionStart ):
            rangeObj.start = lineNo
            stage += 1

        if stage == 1 and lineText.startswith( sectionEnd ):
            rangeObj.end = lineNo
            stage += 1

    return lines[ rangeObj.start : rangeObj.end+1 ]


def replaceInList( lines, rangeObj, to_replace ):
    lineNo = rangeObj.start
    for line in rangeObj.range():
        del lines[ lineNo ]

    del lines[ lineNo ]
    for line in to_replace:
        if not line.endswith( '\n' ):
            line += '\n'

        lines.insert( lineNo, line )
        lineNo += 1

    return


def sourceName( templateName ):
    return os.path.splitext( os.path.basename( templateName ) )[ 0 ]


def check_nltk():
    try:
        from nltk.tokenize import word_tokenize
        word_tokenize( 'It\'s.' )

    except:
        from nltk import download
        if not sslVerify:
            from ssl import _create_unverified_context
            from six.moves.urllib.request import install_opener, HTTPSHandler, build_opener

            ctx = _create_unverified_context()
            opener = build_opener( HTTPSHandler( context = ctx ) )
            install_opener( opener )

        download( 'punkt' )

    return


class ModuleExistsAlready( Exception ):
    def __init__( self, obj, path ):
        self.__obj = obj
        super( ModuleExistsAlready, self ).__init__( path )
        return


class InvalidSetting( Exception ):
    def __init__( self, prop, entity, name ):
        self.__property = prop
        self.__entity   = entity
        self.__name     = name
        super( InvalidSetting, self ).__init__( '{prop} in {entity} with name {name} has an invalid value.'.format( prop = prop,
                                                           entity = entity,
                                                           name = name ) )
        return

