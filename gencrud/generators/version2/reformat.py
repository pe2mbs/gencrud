import os.path
import sys
import logging
import subprocess
from shutil import which


logger = logging.getLogger( 'gencrud.reformat' )


def reformatPythonCode( filename, config ):
    yapf = which('yapf')
    if not isinstance(yapf, str):
        # Is ths a vierual environment module ?
        yapf = os.path.join(os.path.split(sys.executable)[0], 'yapf.exe')

    if isinstance(yapf, str):
        logger.info(f"Using {yapf} to format the code {os.path.basename(filename)}")
        result = subprocess.Popen(
            (yapf, '--style', config.options.YapfStyle, '--in-place', '--print-modified', filename ),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        for line in result.stdout.readlines():
            logger.info(line.decode('utf-8'))

        result.wait()

