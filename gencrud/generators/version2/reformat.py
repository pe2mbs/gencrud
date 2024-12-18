import os.path
import sys
import logging
import traceback
from shutil import which
from gencrud.configuraton import TemplateConfiguration
from yapf import main as yapf_main

logger = logging.getLogger( 'gencrud.reformat' )


def reformatPythonCode( filename, config: TemplateConfiguration ):
    if not config.options.UseYapf:
        return

    yapf = which('yapf')
    if not isinstance(yapf, str):
        # Is ths a vierual environment module ?
        yapf = os.path.join(os.path.split(sys.executable)[0], 'yapf.exe')

    if isinstance(yapf, str):
        logger.info(f"Using {yapf} to format the code {os.path.basename(filename)}")
        try:
            yapf_main( ( 'yapf', '--style', config.options.YapfStyle, '--in-place', '--print-modified', filename ) )

        except Exception:
            print( traceback.format_exc() )

