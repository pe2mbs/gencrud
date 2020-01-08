#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2019 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation; either version 2 of the
#   License, or (at your option) any later version.
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
import os
import logging
import shutil

from gencrud.util.positon import PositionInterface
from platform import system

sslVerify       = True
backupFiles     = False
overWriteFiles  = False
ignoreCaseDbIds = False
useModule       = False
lazyLoading     = False
version         = 1
config          = None

C_FILEMODE_UPDATE = 'r+'
C_FILEMODE_WRITE  = 'w'
C_FILEMODE_READ   = 'r'

logger = logging.getLogger()


def get_platform():
    platf = system().lower()
    if platf == "darwin":   # as platform.system() for OS-X returns Darwin we translate for consistency.
        platf =  "osx"

    #logging.debug( "Platform '{}'".format( platf ) )
    return platf


def backupFile( file_name ):
    idx = 1
    while os.path.isfile( file_name + '.~{0}'.format( idx ) ):
        idx += 1

    if os.path.isfile( file_name ):
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
    logger.debug( "insertLinesUnique from line {} to line {}".format( rangeObj.start, rangeObj.end ) )

    end = rangeObj.end
    if end + 1 < len( lines ):
        end += 1

    for idx in range( rangeObj.start, end ):
        logger.debug( "Check line {} of {} => '{}'".format( idx, rangeObj.end, lines[ idx ].strip( '\r\n') ) )

        if line in lines[ idx ].strip( '\n' ):
            found = True

    if not found:
        logger.debug( 'inject files [{0}] @ {1}'.format( line, rangeObj.end ) )

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
