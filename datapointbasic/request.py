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
        self.params   = {'key': self.api_key.api_key}
        
        
    def retrieve_data(self):
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
        
        req = requests.get(url, self.params)
        
        return req.json()
        
        
class SiteSpecificRequest(GenericRequest):
    """
    Site-specific request
    """
    
    def __init__(self, site_id):
        
        GenericRequest.__init__(self)
        
        self.val     = 'val'
        self.item    = 'all'
        self.site_id = site_id
        
    def __repr__(self):
        return "{}('{}')".format(type(self).__name__, self.site_id)
    
    @property
    def feed(self):
        
        return self.site_id
        
class RegionalRequest(GenericRequest):
    """
    Regional request
    """
    
    def __init__(self):
        
        GenericRequest.__init__(self)
        
        self.val = 'txt'
    

class SitelistRequest(GenericRequest):
    """
    Class that returns the valid sites for the forecast in question
    """
    
    def __init__(self, val, wx, item):
        
        GenericRequest.__init__(self)
        
        self.val  = val
        self.wx   = wx
        self.item = item
        self.feed = 'sitelist'
        
        self.get_all_sites()
        
    def get_all_sites(self):
        
        
        req = self.retrieve_data()
        
        self.site_data = req['Locations']['Location']
            
