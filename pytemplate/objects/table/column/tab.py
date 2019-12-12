


class TemplateTab( object ):
    def __init__( self, parent, **cfg ):
        self.__parent   = parent
        self.__cfg = cfg
        return

    @property
    def index( self ):
        return self.__cfg.get( 'index', None )

    @property
    def label( self ):
        return self.__cfg.get( 'label', None )


class TemplateTabs( object ):
    def __init__( self, parent, **cfg ):
        self.__parent   = parent
        self.__cfg      = cfg
        self.__fields   = { l: [] for l in self.labels }
        self.__comps    = { l: None for l in self.labels }
        self.__params   = { l: None for l in self.labels }
        for col in self.__parent.columns:
            if col.hasTab:
                self.__fields[ col.tab.label ].append( col )

        for key in self.__fields.keys():
            self.__fields[ key ].sort( key = lambda x: x.tab.index, reverse = False )

        for tab in self.__cfg.get( 'tab', [] ):
            self.__comps[ tab.get( 'label', None ) ] = tab.get( 'component', None )
            self.__params[ tab.get( 'label', None ) ] = tab.get( 'params', {} )

        return

    @property
    def labels( self ):
        if isinstance( self.__cfg, ( list, tuple ) ):
            return self.__cfg

        return self.__cfg.get( 'labels', None )

    @property
    def tabTag( self ):
        return self.__cfg.get( 'tabtag', 'mat-tab' )

    @property
    def contentTag( self ):
        return self.__cfg.get( 'contenttag', None )

    @property
    def groupTag( self ):
        return self.__cfg.get( 'grouptag', 'mat-tab-group' )

    def fieldsFor( self, label ):
        result = self.__fields[ label ]
        return result

    def hasComponent( self, label ):
        value = self.__comps.get( label, None )
        return isinstance( value, str )

    def component( self, label ):
        value = self.__comps.get( label, '' )
        return value

    def params( self, label ):
        result = ''
        for key, value in self.__params[ label ].items():
            result += '[{}]="{}" '.format( key, value )
            if key == 'value':
                result += '*ngIf="{}" '.format( value )

        return result

