"""
Python module containing abstract classes to retrieve data from DataPoint
"""

import requests
import datetime
from ..tools import ApiManager

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
        
        self._retreived_data = False
        
    def __repr__(self):
        return "{}('{}')".format(type(self).__name__, self.site_id)
    
    @property
    def feed(self):
        
        return self.site_id
    
    @property
    def days(self):
        
        if not self._retreived_data:
            self._get_days()
            self._retreived_data = True
        
        return self._days
        
    
    def _get_days(self):
        
        raw_data = self.retrieve_data()
        
        params = raw_data['SiteRep']['Wx']['Param']
        days   = raw_data['SiteRep']['DV']['Location']['Period']
        
        self._days = [Day(params, day) for day in days]
        
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
            

class Day(object):
    """
    Class to store a day of weather.
    """
    
    def __init__(self, params, day):
        
        self._set_params(params, day)
                
    def _set_params(self, params, day):
        """
        Assign the inputted data for the day to the object.
        """
        
        timesteps = day['Rep']
        
        # Assign the day and get times of each timestep
        date = day['value']
        year  = int(date[:4])
        month = int(date[5:7])
        day   = int(date[8:10])
        hours = [int(timestep['$']) // 60 for timestep in timesteps]
        mins  = [int(timestep['$']) % 60 for timestep in timesteps]
        
        self.date = datetime.date(year, month, day)
        times     = [datetime.datetime(year, month, day, hour, minute) 
                     for hour, minute in zip(hours, mins)]
        
        # Assign the remaining parameters
        self.params = {}
        
        for param in params:
            
            shortname = param['name']
            units     = param['units']
            longname  = param['$']
            
            
            values = [timestep[shortname] if shortname in timestep else None for timestep in timesteps]
            
            self.__setattr__(
                longname.replace(' ','_'),
                WeatherField(longname, units, values, times)
                )
            
    
    def __repr__(self):
        return "{}('{}')".format(type(self).__name__, str(self.date))
                     

class WeatherField(object):
    """
    Class to store a data field returned from DataPoint
    """
    
    def __init__(self, name, units, values, times):
        
        self.name   = name
        self.units  = units
        self.values = values
        self.times  = times
        
        
    def __repr__(self):
        return "{}('{}')".format(type(self).__name__, self.name)