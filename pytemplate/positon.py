class PositionInterface( object ):
    def __init__( self, start = 0, end = 0 ):
        self.__start    = start
        self.__end      = end
        return

    @property
    def start( self ):
        return self.__start

    @start.setter
    def start( self, value ):
        self.__start = value
        return

    @property
    def end( self ):
        return self.__end

    @end.setter
    def end( self, value ):
        self.__end = value
        return

    def range( self ):
        return range( self.__start, self.__end )

    def dump( self, caption ):
        print( '{0}\n- start: {1} end {2}'.format( caption, self.__start, self.__end ) )

