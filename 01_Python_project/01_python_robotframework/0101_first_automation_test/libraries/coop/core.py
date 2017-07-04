''' core module of coop lib, including:

    1. a proxy to API visit
    2. a proxy to mongodb visit
'''
import os
import urllib2
import json
urllib2.getproxies = lambda: {} # unset http_proxy
from robot.api import logger

COOP_API_URL = os.getenv('COOP_API_URL', r'http://127.0.0.1:3333/api')

__all__ = ('APIProxy', 'MongoProxy')


class ApiProxy(object):
    ''' proxy to API visit.
    Usage:
        example-1:
        trunkbuild = APIProxy.get_scbuilds_trunkbuild()
        it will send "GET" request to "/api/scbuilds/trunkbuild" and return the
        output back.
        example-2:
        commits = APIProxy.post_commits(commits=[{'revision':1, 'author': 'a'}])
        it will send "POST" request to "/api/commits" with data
        {
            commits: [{'revision':1, 'author': 'a'}]
        }
        and return the output back.
    '''
    def __getattr__(self, kw):
        method, api_url = kw.split('_', 1)
        api = api_url.strip('_').replace('_', '/')
        if method == 'get':
            return self._do_GET(api)
        elif method == 'post':
            return self._do_POST(api)
        else:
            raise RuntimeError('invalid method type "%s"' % kw)

    def _do_GET(self, api):
        def _get():
            return self._get_api_response(api)
        return _get

    def _do_POST(self, api):
        def _post(**kwds):
            return self._get_api_response(api, kwds)
        return _post

    def _get_api_response(self, api, data=None):
        headers = {'content-type': 'application/json'}
        data = data and json.dumps(data).encode('utf-8')
        req = urllib2.Request(COOP_API_URL + '/' + api, data, headers)
        try:
            res = urllib2.urlopen(req)
            ret_data = res.read()
            if res.getcode() >= 400:
                logger.warn(ret_data)
                raise RuntimeError('failed to execute "%s"' % api)

            logger.info(ret_data)
            try:
                return json.loads(ret_data)
            except ValueError:
                return ret_data
        except urllib2.HTTPError as err:
            logger.warn('failed on HTTP request, error: %s' % err.read())
            raise RuntimeError('failed on HTTP request')

APIProxy = ApiProxy()

class MongoProxy(object):
    # TODO: proxy to mongodb operation
    def __call__(self):
        pass
    
    def __init__(self, product = 'macrotdd'):
        self.product = product
        self.ConnectionToDB()
    
    def ConnectionToDB(self):
        self.conn = MongoClient('127.0.0.1',27017)
        self.db = self.conn['pipeline']
        self.collection = self.db[self.product+'_trunkbuild']
        
    def SaveADoc(self):
        logging.info("Saving docs...")
        mydata = {"author": "John",    
                "text": "My first post!",    
                "tags": ["python", "pymongo", "mongoDB", "arangoDB"]  
        }
        self.collection.insert(mydata)
        
    def QuerySingleDoc(self, arg):
        logging.info("First matching...")
        logging.info(self.collection.find_one(arg))
        
    def QueryDoc(self, arg):        
        for doc in self.collection.find(arg):
            pass
            #logging.info(doc)
        return self.collection.find(arg).count()    
    
    
