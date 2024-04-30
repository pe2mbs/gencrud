#
#   Python backend and Angular frontend code
#   Copyright (C) 2018-2024 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation.
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
import logging
import os.path
import typing as t
from mako.template import Template
from gencrud.config.base import TemplateBase
from gencrud.config.column import TemplateColumn
from gencrud.config.object import TemplateObject
from gencrud.config.tab import TemplateTab, TemplateComponentTab
from gencrud.configuraton import TemplateConfiguration
from gencrud.constants import *


logger = logging.getLogger( 'gencrud.help-pages' )
MAT_ICON        = """<mat-icon class="mat-icon notranslate material-icons mat-icon-no-color" role="img">{icon}</mat-icon>"""
FONTAWSOME_ICON = """<i class="fa-solid fa-{icon}"></i>"""


class HelpButtons( TemplateBase ):
    def __init__( self, parent: TemplateBase, help: str, label: str, icon: str, provider: str = 'mat-icon' ):    # object level
        super().__init__( parent )
        self.__iconProvider = provider
        self.__icon         = icon
        self.__label        = label
        self.__helpText     = help
        return

    @property
    def Icon( self ) -> str:
        return self.__icon

    @property
    def HelpText( self ) -> str:
        return self.__helpText

    @property
    def Label( self ) -> str:
        return self.__label

    @property
    def IconProvider( self ) -> str:
        if self.__iconProvider == 'mat-icon':
            return MAT_ICON.format( icon = self.__icon )

        return FONTAWSOME_ICON.format( icon = self.__icon )

    @property
    def IconWithHelp( self ) -> str:
        return f"{ self.IconProvider } { self.__helpText }"


class HelpTemplate( TemplateBase ):
    def __init__( self, parent, columns: t.List[ TemplateColumn ], obj: TemplateObject ):    # object level
        super().__init__( parent )
        self.__obj                  = obj
        self.__tableFields          = []
        self.__tableHeaderButtons   = [
            HelpButtons( self, 'Refreshes current records in view', 'Refresh', 'refresh' ),
            HelpButtons( self, 'Shows help on the current view', 'Help', 'help_outline' )
        ]
        self.__tableRecordButtons   = []
        self.__tableFooterButtons   = [
            HelpButtons(self, 'Refreshes current records in view', 'Refresh', 'refresh'),
            HelpButtons(self, 'Jumps to the first record depended on the sorting order', 'First  page', 'first_page'),
            HelpButtons(self, 'Goto the previous page', 'Previous page', 'chevron_left'),
            HelpButtons(self, 'Goto the next page', 'Next page', 'chevron_right'),
            HelpButtons(self, 'Jumps to the last record depended on the sorting order', 'Last page', 'last_page'),
        ]
        self.__sidebarButtons       = []
        self.__screenFields         = []
        if self.hasHelp():
            for action in self.__obj.actions.getHeaderButtons():
                if action.hasHelp():
                    self.__tableHeaderButtons.append( HelpButtons( self, action.Help, action.label, action.icon ))

            for action in self.__obj.actions.getFooterButtons():
                if action.hasHelp():
                    self.__tableFooterButtons.append( HelpButtons( self, action.Help, action.label, action.icon ))

            for action in self.__obj.actions.getCellButtons():
                if action.hasHelp():
                    self.__tableRecordButtons.append( HelpButtons( self, action.Help, action.label, action.icon ))

            for action in self.__obj.actions.getCustomButtons():
                if action.hasHelp():
                    self.__sidebarButtons.append( HelpButtons( self, action.Help, action.label, action.icon ))

            for field in columns:
                field: TemplateColumn
                if field.hasHelp():
                    helpText = field.Help
                    if field.hasListView():
                        self.__tableFields.append( field )

                    if field.hasView():         # Both for Screen and Dialog
                        self.__screenFields.append( field )

            # Check if the Tabs have help too
            tab_labels = self.__obj.table.tabs().labels
            for tab in self.__obj.table.tabs().Components:
                tab: TemplateComponentTab
                if isinstance( tab.Help, str ):
                    values = { C_INDEX: tab_labels.index( tab.TabName ),
                               C_LABEL: tab.TabName, C_HELP: tab.Help }
                    self.__screenFields.append( TemplateTab( self, **values ) )

            # Now sort the table and screen fields
            # For the table fields we sort on the listview.index
            self.__tableFields.sort( key = lambda x: x.listview.index )
            # For the screen / dialog view we sort on tab.index, where no
            # tab is present we sort on column index
            def sorted_value( x ):
                if isinstance( x, TemplateTab ):
                    return float( f"{x.index}.00" )

                elif isinstance( x, TemplateColumn ):
                    return float(f"{x.index}.{x.tab.index:02d}")

            self.__screenFields.sort( key = sorted_value )

        return

    def hasHelp( self ) -> bool:
        return self.__obj.HelpTitle is not None

    @property
    def Title( self ) -> str:
        return self.__obj.HelpTitle

    @property
    def LeadInTable( self ) -> str:
        return self.__obj.HelpTable

    @property
    def LeadInScreen( self ) -> str:
        return self.__obj.HelpScreen

    @property
    def TableFields( self ) -> t.List[ TemplateColumn ]:
        return self.__tableFields

    @property
    def ScreenFields( self ) -> t.List[ TemplateColumn ]:
        return self.__screenFields

    def hasTableHeaderButtons( self ) -> bool:
        return len( self.__tableHeaderButtons ) > 0

    @property
    def TableHeaderButtons( self ):
        return self.__tableHeaderButtons

    def hasTableRecordButtons( self ) -> bool:
        return len( self.__tableRecordButtons ) > 0

    @property
    def TableRecordButtons(self):
        return self.__tableRecordButtons

    def hasTableFooterButtons( self ) -> bool:
        return len( self.__tableFooterButtons ) > 0

    @property
    def TableFooterButtons(self):
        return self.__tableFooterButtons

    def hasTableSidebarButtons( self ) -> bool:
        return len( self.__sidebarButtons ) > 0

    @property
    def TableSidebarButtons(self):
        return self.__sidebarButtons



def generateHelpPages( config: TemplateConfiguration, templates: t.List[ str ], flask_config: dict ):
    for obj in config.objects:
        obj: TemplateObject
        # Build the HELP infor structure
        help_obj = HelpTemplate( config, [ field for field in obj.table.columns ], obj )
        if not help_obj.hasHelp():
            logger.warning( f"No help pages generated for {obj.name}" )
            continue

        if 'HLP_PATH' not in flask_config:
            flask_config[ 'HLP_PATH' ] = config.HelpPages.sourceFolder

        logger.info(f"Generating help pages for {obj.name}")
        # Generate the pages
        for template in templates:
            if not os.path.exists( template ):
                continue

            templ = Template( filename = template )
            data = templ.render( help = help_obj )

            if config.hasInterface():
                targetFolder = os.path.join( config.HelpPages.sourceFolder, config.Interface.Backend.Module, obj.name )

            else:
                targetFolder = os.path.join( config.HelpPages.sourceFolder, obj.name )

            if not os.path.exists( targetFolder ):
                logger.info( f"Creating folder {targetFolder}" )
                os.makedirs( targetFolder )

            targetFilename = os.path.join( targetFolder, os.path.splitext( os.path.basename( template ) )[ 0 ] )
            logger.info( f"Creating help file {targetFilename}")
            with open( targetFilename, 'w', newline='' ) as stream:
                stream.write( data )

    return