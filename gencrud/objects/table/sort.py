
DIRECTIONS = ( 'asc', 'desc', '' )


class SortInfo( object ):
    def __init__( self, data ):
        self.__field    = data[ 'field' ]
        self.__direction = 'asc'
        # 'asc'
        # 'desc'
        # ''
        if 'direction' in data:
            if data[ 'direction' ] in DIRECTIONS:
                self.__direction    = data[ 'direction' ]

            else:
                raise Exception( "Sorting order must be one of the following: 'asc', 'desc' or ''")

        return

    @property
    def Field( self ):
        return self.__field

    @property
    def Direction( self ):
        return self.__direction

    def htmlMaterialSorting( self ):
        return 'matSortActive="{}" matSortDirection="{}"'.format( self.__field, self.__direction )

    def injectAngular( self ):
        return self.AngularInject()

    def AngularInject( self ):
        return "this.sort.sort( {{ id: '{field}', start: '{order}' }} as MatSortable );".format( field = self.__field,
                                                                                                 order = self.__direction )

    def __repr__(self):
        return "<SortInfo >"