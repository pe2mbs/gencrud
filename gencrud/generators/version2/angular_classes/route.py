#
#   Python backend and Angular frontend
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
import typing as t
import copy


class SectionNotFound( Exception ):
    pass


class Route( object ):
    """This class is a python implementation if the Angular Route class
    For generating the route information into xxxxx-routing.module.ts

    NOT all options are implemented, but the folloing are
    -   path / redirectTo / pathMatch
    -   path / component [, canActivate ]
    -   path / loadChildren [, canActivate ]
    -   path / children [, canActivate ]
    """
    def __init__( self, path: t.Optional[ str ] = None,
                        redirectTo: t.Optional[ str ] = None,
                        pathMatch: t.Optional[ str ] = None ):
        #   The path to match against. Cannot be used together with a custom `matcher` function.
        #   A URL string that uses router matching notation.
        #   Can be a wild card (`**`) that matches any URL (see Usage Notes below).
        #   Default is "/" (the root path).
        self.path   = path
        #   The path-matching strategy, one of 'prefix' or 'full'.
        #   Default is 'prefix'.
        self.pathMatch = pathMatch
        #   A custom URL-matching function. Cannot be used together with `path`.
        self.matcher = None
        #   The component to instantiate when the path matches.
        #   Can be empty if child routes specify components.
        self.component = None
        #   A URL to redirect to when the path matches.
        #   Note that no further redirects are evaluated after an absolute redirect.
        #
        #   When not present, router does not redirect.
        self.redirectTo = redirectTo
        #   Name of a `RouterOutlet` object where the component can be placed
        #   when the path matches.
        self.outlet = None
        #   An array of dependency-injection tokens used to look up `CanActivate()`
        #   handlers, in order to determine if the current user is allowed to
        #   activate the component. By default, any user can activate.
        #
        #   is  dict with key is filename and value the list of handler classes
        self.canActivate = {}

        self.canActivateChild = []
        self.canDeactivate = []
        self.canLoad    = []
        self.data = None
        self.resolve = None
        #   An array of child `Route` objects that specifies a nested route
        #   configuration.
        self.children = []
        #   An object specifying lazy-loaded child routes.
        #   is a list of tuples ( filename, module_name )
        self.loadChildren = []
        self.runGuardsAndResolvers = None
        #   filename where the comonent is located
        self.__sourceFile = None

    def addCanActivate( self, can_activate: t.Optional[ t.Union[ str, list ] ], filename: str ):
        if isinstance(can_activate, str):
            self.canActivate.setdefault( filename, [] ).append( can_activate )

        elif isinstance( can_activate, list ):
            for item in can_activate:
                if isinstance( item, ( tuple, list ) ) and len( item ) == 2:
                    self.canActivate.setdefault( item[ 1 ], []).append( item[ 0 ] )

                else:
                    self.canActivate.setdefault( filename, [] ).append( item )

        return

    def setComponent( self, path: str, conponent: str, filename: str ):
        self.path = path
        self.component = conponent
        self.__sourceFile   = filename
        return

    def setLazyLoadedModule( self, path: str, module_path: str, module_name: str ):
        self.path = path
        self.loadChildren.append( ( module_path, module_name ) )
        return

    def addChild( self, route: 'Route' ):
        self.children.append( route )
        return

    @staticmethod
    def _createLine( lines: list, indent: int, text: str ):
        lines.append( "{indent}{text}".format( indent = " " * indent, text = text ) )
        return

    def generate( self, indent = 4, output = 'str' ) -> t.Union[ list, str ]:
        lines = []
        self._generate_lines( lines, indent )
        if output == 'list':
            return lines

        return "\n".join(lines)

    def _generate_lines(self, lines: list, indent=4 ):
        self._createLine( lines, indent, '{' )
        indent += 4
        self._createLine(lines, indent, f"path: '{self.path}',")
        if isinstance( self.redirectTo, str ):
            self._createLine(lines, indent, f"redirectTo: '{self.redirectTo}',")

        elif len( self.canActivate ) > 0:
            canActivate = []
            for value in self.canActivate.values():
                canActivate.extend( value )

            activate = ", ".join( canActivate )
            self._createLine( lines, indent, f'canActivate: [ {activate} ],')

        if isinstance(self.component, str) and isinstance(self.__sourceFile, str):
            self._createLine( lines, indent, f'component: {self.component},')

        elif len( self.children ) > 0:
            self._createLine(lines, indent, f'children: [')
            indent += 4
            for child in self.children:
                child._generate_lines( lines, indent )

            indent -= 4
            self._createLine(lines, indent, f'],')

        elif len( self.loadChildren ) == 1:
            filename, module = self.loadChildren[ 0 ]
            self._createLine( lines, indent, f"loadChildren: () => import( '{filename}' ).then( ( m ) => m.{module}Module )," )

        elif len( self.loadChildren ) > 1:
            self._createLine(lines, indent, "loadChildren: () => {")
            indent += 4
            for filename, module in self.loadChildren:
                self._createLine( lines, indent, f"import( '{filename}' ).then( ( m ) => m.{module}Module )," )

            indent -= 4
            self._createLine(lines, indent, "}")

        if isinstance( self.pathMatch, str ):
            self._createLine(lines, indent, f"pathMatch: '{self.pathMatch}',")

        indent -= 4
        self._createLine(lines, indent, '},')
        return

    def hasImport( self ):
        return self.__sourceFile is not None

    def generateImports( self ) -> t.List[ str ]:
        result = []
        self._generateImports( result )
        return result

    def _generateImports( self, result: t.List[str] ):
        if isinstance( self.component, str ) and isinstance( self.__sourceFile, str ):
            line = f"import {{ {self.component} }} from '{ self.__sourceFile }';"
            if line not in result:
                result.append( line )

        if len( self.children ) > 0:
            for child in self.children:
                child._generateImports( result )

        if len( self.canActivate ) > 0:
            for filename, values in self.canActivate.items():
                value = ", ".join( values )
                line = f"import {{ {value} }} from '{filename}';"
                if line not in result:
                    result.append( line )

        return result

    def updateRouteModule( self, module: t.Union[str,list] ) -> t.Union[str,list]:
        if isinstance( module, str ):
            lines = module.split( '\n' )

        else:
            lines = copy.copy( module )

        idx = 0
        first_import = None
        indent = 4
        last_import = end_gencrud = start_gencrud = 0
        while idx < len(lines):
            line = lines[idx]
            if line.startswith("import "):
                if first_import is None:
                    first_import = idx

                last_import = idx
            elif "// GENGRUD BEGIN" in line:
                indent = line.index( "//" )
                start_gencrud = idx

            elif "// GENGRUD END" in line:
                end_gencrud = idx

            idx += 1

        if start_gencrud == 0 or end_gencrud == 0:
            raise SectionNotFound( "GENCRUD section not found" )

        if first_import is None or last_import == 0:
            raise SectionNotFound( "import section not found")

        path_idx = start_section = end_section = 0
        for idx in range( start_gencrud+1, end_gencrud ):
            line = lines[ idx ]
            striped_line = line.strip()
            if striped_line == '{':    # Start of route defintion
                start_section = idx
                end_section = 0

            elif striped_line == '},':  # End of route definition
                end_section = idx
                if path_idx > 0:
                    break

            elif striped_line == f"path: '{self.path}',":
                # found it
                if start_section != 0:
                    path_idx = idx

                else:
                    raise SectionNotFound( f'{{ ... {self.path} ... }} not found' )

        if path_idx != 0 and start_section != 0 and end_section != 0:
            # Remove a section to replace
            for idx in range( start_section, end_section + 1 ):
                del lines[ start_section ]

            end_gencrud = start_section

        # Add a new section
        for line in reversed( self.generate( indent=indent, output = 'list' ) ):
            lines.insert( end_gencrud, line )

        last_import += 1
        idx = 0
        for line in reversed( self.generateImports() ):
            if line not in lines[ first_import: last_import + idx ]:
                lines.insert( last_import, line )
                idx += 1

        if isinstance( module, str ):
            return "\n".join( lines )

        return lines


ROUTE_MODULE_TS = """import { NgModule } from '@angular/core';
import { RouterModule, Routes, Route } from '@angular/router';
import { NotFoundComponent } from './components/not-found/not-found.component';


const routes: Routes = [
    // GENGRUD BEGIN
    // GENGRUD END
    {
        path: '**',
        component: NotFoundComponent
    },
];


@NgModule({
    imports: [ RouterModule.forRoot( routes, {{ enableTracing: true, useHash: true }} ) ],
    exports: [ RouterModule ]
})
export class ${module}RoutingModule { }
"""


if __name__ == '__main__':
    # For some testing
    r1 = Route()
    r1.setComponent( 'login', 'LoginComponent', './components/login/login.component' )
    # print( r1.generateImports() )
    # print( r1.generate() )

    r2 = Route()
    r2.setComponent( 'register', 'RegisterComponent', './components/register/register.component' )
    # print( r2.generate() )

    r3 = Route()
    r3.addCanActivate("AuthGuard", './services/auth-guard.guard')
    r3.setLazyLoadedModule( 'wa-admin', './wa-admin/wa-admin.module', 'WaAdminModule' )
    # print( r3.generate() )

    r4 = Route( '' )
    r0 = Route( '', redirectTo = '/login', pathMatch    = 'full' )
    r4.addChild( r0 )
    r4.addChild( r1 )
    r4.addChild( r2 )
    r4.addChild( r3 )
    r5 = Route()
    r5.setComponent('**', 'NotFoundComponent', './components/not-found/not-found.component' )
    r4.addChild( r5 )
    # print( r4.generate() )
    # for imp in r4.generateImports():
    #     print( imp )

    lines = ROUTE_MODULE_TS

    lines = r4.updateRouteModule( lines )

    print( lines )
