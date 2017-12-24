"""
Python module containing abstract classes to retrieve data from DataPoint
"""

import requests
from datapointbasic.tools import ApiManager

BASE_URL = 'http://datapoint.metoffice.gov.uk/public/data'


class GenericRequest(object):
    """
    Generic request to DataPoint
    """
    
    def __init__(self):
        """
        Initialise the object
        """
        
        self.api_key  = ApiManager()
        self.url      = BASE_URL
        self.datatype = 'json'
        
        
    def retrieve_data(self, params):
        """
        Forms the request together and returns the json
        """
        
        url = '{}/{}/{}/{}/{}/{}'.format(
            BASE_URL,
            self.val,
            self.wx,
            self.item,
            self.datatype,
            self.feed
            )
        
        params['key'] = self.api_key
        req = requests.get(url, params)
        
        return req.json()
        
        
class SiteSpecificRequest(GenericRequest):
    """
    Site-specific request
    """
    
    def __init__(self):
        
        GenericRequest.__init__(self)
        
        self.val  = 'val'
        self.item = 'all'
        
        
class RegionalRequest(GenericRequest):
    """
    Regional request
    """
    
    def __init__(self):
        
        GenericRequest.__init__(self)
        
        self.val = 'txt'
    
    