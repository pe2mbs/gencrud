from webapp.commands.clean import clean
from webapp.commands.lint import lint
from webapp.commands.rundev import rundevCommand
from webapp.commands.runssl import runsslCommand
from webapp.commands.runprod import runprdCommand
from webapp.commands.test import test
from webapp.commands.urls import urls

import webapp.api as API

def registerCommands():
    """Register Click commands.

       :param app:          The application object.
       :param module:       The actual application module.
       :return:             None.
    """
    API.app.logger.info( "Registering commands" )
    API.app.cli.add_command( test )
    API.app.cli.add_command( lint )
    API.app.cli.add_command( clean )
    API.app.cli.add_command( urls )
    API.app.cli.add_command( runsslCommand )
    API.app.cli.add_command( rundevCommand )
    API.app.cli.add_command( runprdCommand )
    return
