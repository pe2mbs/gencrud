from functools import wraps
from time import time
import logging
import unittest
import os
import posixpath
import requests
from webapp2.extensions.config import Config


logger = logging.getLogger()


def timeit(method):
    def start(*args, **kw):
        logging.info(f'{method.__name__}')

        def timed(*args, **kw):
            ts = time()
            result = method(*args, **kw)
            logging.info( f'{method.__name__} => {time()-ts} sec' )
            return result

        return timed

    return start


class TestCaseGeneric( unittest.TestCase ):
    HTTP_OK = 200
    PAGE_SIZE = 5
    testItemID = 0

    def __init__( self, methodName = 'runTest', validator = None):
        self.rootPath = os.path.join(os.path.dirname( __file__ ), '..', '..')
        self.config = Config( self.rootPath )
        self.config.fromYaml( os.path.join( self.rootPath, 'config.yaml' ) )
        self.BASE_URI = f'http://{self.config["HOST"]}:{self.config["PORT"]}'
        self.recordCount = 0
        self.primaryKey: str = ''
        self.secondaryKey: str = ''
        self.testKey = ''
        self.recordValidator = validator
        unittest.TestCase.__init__( self, methodName )
        return

    def setModule( self, uri: str, primary_key: str, secondary_key: str ):
        self.primaryKey = primary_key
        self.secondaryKey = secondary_key
        if self.config[ "HOST" ] == '0.0.0.0':
            host = 'localhost'
        else:
            host = self.config[ "HOST" ]

        self.BASE_URI = f'http://{host}:{self.config[ "PORT" ]}{uri}'
        return

    def getUrl( self, fn ):
        return posixpath.join( self.BASE_URI, fn )

    def getRecCount( self ):
        self.recordCount = requests.get(self.getUrl('count')).json()['recordCount']
        return

    def noRecordsReturned( self, count, page, size ):
        pages = int( count / size )
        if page == pages:
            return count - ( pages * size )

        return size

    def noPagesAvailable( self, count, size ):
        return int( count / size )

    @timeit
    def test_RecordCount(self):
        r = requests.get( self.getUrl( 'count' ) )
        logger.info( f"test_RecordCount REST elapsed {r.elapsed}" )
        self.assertEqual( self.HTTP_OK, r.status_code )
        args = r.json()
        self.assertIsInstance( args[ 'recordCount' ], int )
        return

    def test_PageFirst( self ):
        if self.recordCount < 0:
            self.skipTest( "To less records in the database" )

        r = requests.post( self.getUrl( 'pagedlist' ), json = {
            'pageIndex':        0,
            'pageSize':         self.PAGE_SIZE,
            'sorting': {
                'column':       self.primaryKey,
                'direction':    "desc"},
            'filters':          []
        } )
        logger.info(f"test_PageFirst REST elapsed {r.elapsed}")
        self.assertEqual( self.HTTP_OK, r.status_code )
        args = r.json()
        self.assertEqual( 0, args[ 'page' ] )
        self.assertEqual( self.PAGE_SIZE, args[ 'pageSize' ] )
        self.assertEqual( self.recordCount, args[ 'recordCount' ] )
        for record in args[ 'records' ]:
            self.recordValidator( self, record )

        self.assertEqual( self.noRecordsReturned( self.recordCount, args[ 'page' ], self.PAGE_SIZE ), len( args['records'] ) )
        return

    def test_PageNext( self ):
        self.getRecCount()
        if self.recordCount < self.PAGE_SIZE:
            self.skipTest( "To less records in the database" )

        r = requests.post(self.getUrl('pagedlist'), json={
            'pageIndex':        1,
            'pageSize':         self.PAGE_SIZE,
            'sorting': {
                'column':       self.primaryKey,
                'direction':    "desc"},
            'filters':          []
        })
        logger.info(f"test_PageNext REST elapsed {r.elapsed}")
        self.assertEqual( self.HTTP_OK, r.status_code )
        args = r.json()
        self.assertEqual( 1, args[ 'page' ] )
        self.assertEqual( self.PAGE_SIZE, args[ 'pageSize' ] )
        self.assertEqual( self.recordCount, args[ 'recordCount' ] )
        for record in args['records']:
            self.recordValidator( self, record )

        self.assertEqual( self.noRecordsReturned( self.recordCount, args[ 'page' ], self.PAGE_SIZE ), len( args['records'] ) )
        return

    def test_PageLast( self ):
        if self.recordCount < self.PAGE_SIZE:
            self.skipTest( "To less records in the database" )

        page = self.noPagesAvailable( self.recordCount, self.PAGE_SIZE )
        r = requests.post( self.getUrl( 'pagedlist' ), json = {
            'pageIndex':        page,
            'pageSize':         self.PAGE_SIZE,
            'sorting': {
                'column':       self.primaryKey,
                'direction':    "desc"
            },
            'filters':          []
        })
        logger.info(f"test_PageLast REST elapsed {r.elapsed}")
        self.assertEqual( self.HTTP_OK, r.status_code )
        args = r.json()
        self.assertEqual( page, args[ 'page' ] )
        self.assertEqual( self.PAGE_SIZE, args[ 'pageSize' ] )
        self.assertEqual( self.recordCount, args[ 'recordCount' ] )
        for record in args['records']:
            self.recordValidator( self, record )

        self.assertEqual(self.noRecordsReturned( self.recordCount, args[ 'page' ], self.PAGE_SIZE ), len( args['records'] ) )
        return

    def test_FullList( self ):
        r = requests.get(self.getUrl( 'list' ) )
        logger.info(f"test_FullList REST elapsed {r.elapsed}")
        self.assertEqual(self.HTTP_OK, r.status_code)
        args = r.json()
        self.assertEqual(self.recordCount, len( args ) )
        for record in args:
            self.recordValidator( self, record)

        return

    def test_SelectListByPost( self ):
        r = requests.post(self.getUrl('select'), json = { 'value': self.primaryKey, 'label': self.secondaryKey } )
        logger.info(f"test_SelectListByPost REST elapsed {r.elapsed}")
        self.assertEqual(self.HTTP_OK, r.status_code)
        args = r.json()
        for record in args:
            self.assertIsInstance( record[ 'value' ], int )
            self.assertIsInstance( record[ 'label' ], str )

        return

    def test_SelectListByGet( self ):
        r = requests.get(self.getUrl('select'), params = { 'value': self.primaryKey, 'label': self.secondaryKey } )
        logger.info(f"test_SelectListByGet REST elapsed {r.elapsed}")
        self.assertEqual(self.HTTP_OK, r.status_code)
        args = r.json()
        for record in args:
            self.assertIsInstance( record[ 'value' ], int )
            self.assertIsInstance( record[ 'label' ], str )

        return

    def test_GetPrimaryKey( self ):
        r = requests.get( self.getUrl( 'primarykey' ) )
        logger.info(f"test_GetPrimaryKey REST elapsed {r.elapsed}")
        self.assertEqual( self.HTTP_OK, r.status_code )
        args = r.json()
        self.assertEqual( 'U_ID', args[ 'primaryKey' ] )
        return

    def doFilteredListTest( self, field ):
        r = requests.get(self.getUrl( f'list/{field}/1' ) )
        logger.info(f"test_FilteredList REST elapsed {r.elapsed}")
        self.assertEqual(self.HTTP_OK, r.status_code)
        args = r.json()
        for record in args:
            self.recordValidator( self, record )

        return

    def getTestRecord( self, value, show_elapsed = False, function = '', field = None ):
        self.assertIsInstance( value, int )
        self.assertNotEqual( '', value )
        r = requests.get(self.getUrl('get'), params={ self.primaryKey: value } )
        if show_elapsed:
            logger.info(f"{function} REST elapsed {r.elapsed}")

        self.assertEqual(self.HTTP_OK, r.status_code)
        if isinstance( field, str ):
            return r.json()[ field ]

        return r.json()

    def test_RetrieveRecordByParam( self ):
        print("###############", TestCaseGeneric.testItemID)
        record = self.getTestRecord( self.testItemID, True, function = 'test_RetrieveRecordByParam' )
        self.recordValidator( self, record )
        return

    def test_RetrieveRecordById( self ):
        u_id = self.getTestRecord( TestCaseGeneric.testItemID, field = self.primaryKey )
        r = requests.get(self.getUrl( f'get/{u_id}' ) )
        logger.info(f"test_RetrieveRecordById REST elapsed {r.elapsed}")
        self.assertEqual(self.HTTP_OK, r.status_code)
        record = r.json()
        self.recordValidator( self, record )
        return

    def test_LockRecord( self ):
        u_id = self.getTestRecord( TestCaseGeneric.testItemID, field = self.primaryKey )
        r = requests.post(self.getUrl('lock'), json={self.primaryKey: u_id })
        logger.info(f"test_LockRecord REST elapsed {r.elapsed}")
        self.assertEqual(self.HTTP_OK, r.status_code)
        return

    def test_UnlockRecord( self ):
        u_id = self.getTestRecord( TestCaseGeneric.testItemID, field = self.primaryKey )
        r = requests.post(self.getUrl('unlock'), json={self.primaryKey: u_id })
        logger.info(f"test_UnlockRecord REST elapsed {r.elapsed}")
        self.assertEqual(self.HTTP_OK, r.status_code)
        return

    def test_DeleteRecord( self ):
        u_id = self.getTestRecord( TestCaseGeneric.testItemID, field = self.primaryKey )
        r = requests.delete( self.getUrl( str( u_id ) ),  params={ "tracking": False } )
        logger.info(f"test_DeleteRecord REST elapsed {r.elapsed}")
        self.assertEqual( self.HTTP_OK, r.status_code )
        return
