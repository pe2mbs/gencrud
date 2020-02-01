import os
import click
import webapp.api as API


TEST_PATH       = os.path.join( API.PROJECT_ROOT, 'tests' )


@click.command()
def test():
    """Run the tests."""
    import pytest
    rv = pytest.main( [ TEST_PATH, '--verbose' ] )
    exit( rv )
