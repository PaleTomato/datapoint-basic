"""
A set of classes related to making API calls to the DataPoint sevice.
"""

import requests
import time

BASE_URL = 'http://datapoint.metoffice.gov.uk'


class ApiManager(object):
    """
    Class that manages the datapoint API key. All instances of the class
    share the same state, so that the API key only needs to be entered
    once, and can be then shared between all objects that use it.
    """
    
    _shared_state = {}
    
    def __init__(self, api_key=None):
        """
        Initalise by setting the __dict__ of the instance to the
        _shared_state variable. This allows the api key to be shared
        between all instances of this class.
        """
        self.__dict__ = ApiManager._shared_state
        
        if not api_key is None:
            self.api_key = api_key
            
            # Check that the API key is valid
            if not self.api_key_is_valid():
                error_msg = ('Unable to return data from {url}.\n' + \
                    'API key "{key}" may be invalid.').format(
                        url=BASE_URL, key=self.api_key)

                raise ValueError(error_msg)
            
        # Raise an exception if the API key has not been entered the first time
        try:
            self.api_key
        except AttributeError:
            raise ValueError(
                "API key must be set for the first instance of ApiManager"
                )
            
    
    def api_key_is_valid(self):
        """
        Return True or False depending on whether the API key is valid.
        """
        
        params = {'key':self.api_key,
                  'res':'3hourly'}
        
        url = '/'.join(
            (
                BASE_URL,
                'public',
                'data',
                'val',
                'wxfcs',
                'all',
                'json',
                'capabilities'
            )
        )
        
        req = requests.get(url, params)
        
        return req.ok
    
    
    def __repr__(self):
        
        return "ApiManager('%s')" % (self.api_key)
    
    def __str__(self):
        
        return self.api_key


class DataPointRequest(object):
    """
    Class that makes a request to DataPoint and returns json.
    """

    def __init__(self, val, wx, item, feed, params={}):
        """
        Initialise the object
        """
        
        self.val  = val
        self.wx   = wx
        self.item = item
        self.feed = feed
        
        self.api_key  = ApiManager()
        self.url      = BASE_URL
        self.datatype = 'json'
        self.params   = {'key': str(self.api_key), **params}
        
        self.request_time = 0
        self.cache_time = 15 * 60
        
    
    @property
    def json(self):
        """
        Return the json from the DataPoint request.

        Makes a request to DataPoint and returns the json response. If
        a request has previously been made within the cache_time (in
        seconds) then the stored data is instead returned.
        """

        if time.time() > self.request_time + self.cache_time:
            self._json = self._retrieve_data()

        return self._json



    def _retrieve_data(self):
        """
        Forms the request together and returns the json.
        """
        
        path = '/'.join(
            (
                BASE_URL,
                'public',
                'data',
                self.val,
                self.wx,
                self.item,
                self.datatype,
                self.feed
                )
            )
        
        req = requests.get(path, self.params)

        # Note the time that the request was made.
        self.request_time = time.time()
        
        return req.json()