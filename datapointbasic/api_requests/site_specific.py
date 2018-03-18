import datetime
from .generic import GenericRequest

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
        

class Forecast3hourly(SiteSpecificRequest):
    
    def __init__(self, site_id):
        SiteSpecificRequest.__init__(self, site_id)
        
        self.params['res'] = '3hourly'
        self.wx = 'wxfcs'
        
        
class ForecastDaily(SiteSpecificRequest):
    
    def __init__(self, site_id):
        SiteSpecificRequest.__init__(self, site_id)
        
        self.params['res'] = 'daily'
        self.wx = 'wxfcs'
    
    
class ObservationsHourly(SiteSpecificRequest):
    
    def __init__(self, site_id):
        SiteSpecificRequest.__init__(self, site_id)
        
        self.params['res'] = 'hourly'
        self.wx = 'wxobs'


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
    
    
def get_values(raw_data):
    
    params    = raw_data['SiteRep']['Wx']['Param']
    data_days = raw_data['SiteRep']['DV']['Location']['Period']
    
    param_values = {}
    timesteps = []
    param_names = {}
    
    for param in params:
        shortname = param['name']
        units     = param['units']
        longname  = param['$']
        
        param_names[longname]   = shortname
        param_values[shortname] = []
    
    
    for data_day in data_days:
        
        # Get the date
        date = data_day['value']
        year  = int(date[:4])
        month = int(date[5:7])
        day   = int(date[8:10])
        
        # Go through each timestep for this date
        for timestep in data_day['Rep']:
            
            for param in param_values.keys():
                if param in timestep.keys():
                    param_values[param].append(timestep[param])
                
                else:
                    param_values[param].append(None)
            
            if timestep['$'] == 'Day':
                hour   = 12
                minute = 0
            elif timestep['$'] == 'Night':
                hour   = 0
                minute = 0
            else:
                hour   = int(timestep['$']) // 60
                minute = int(timestep['$'])  % 60
                
            timesteps.append(datetime.datetime(year, month, day, hour, minute))
                
    values = {'Timesteps':timesteps}
    
    for param in param_names.keys():
        values[param] = param_values[param_names[param]]
        
    return values
        
    