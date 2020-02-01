import os
from glob import glob
from subprocess import call
import click


@click.command()
@click.option('-f', '--fix-imports', default=False, is_flag=True,
              help='Fix imports using isort, before linting')
def lint( fix_imports ):
    """Lint and check code style with flake8 and isort."""
    skip = ['requirements']
    root_files = glob('*.py')
    root_directories = [ name for name in next( os.walk( '.' ) )[ 1 ] if not name.startswith( '.' ) ]
    files_and_directories = [ arg for arg in root_files + root_directories if arg not in skip ]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments.
        """
        command_line = list(args) + files_and_directories
        click.echo('{}: {}'.format(description, ' '.join(command_line)))
        rv = call(command_line)
        if rv != 0:
            exit(rv)

    if fix_imports:
        execute_tool('Fixing import order', 'isort', '-rc')

    execute_tool('Checking code style', 'flake8')

