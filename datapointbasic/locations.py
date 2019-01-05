"""
Classes to define all location types. Uses the Composite Pattern.
"""
from .api_requests.site_specific import Forecast3hourly, ForecastDaily, \
    ObservationsHourly
from .api_requests.regional import RegionalForecast

class LocationComponent(object):
    """
    Abstract component
    """
    def __init__(self, name):
        self.name = name
    
    def add(self):
        pass
    
    def remove(self):
        pass
    
    def __getitem__(self):
        pass
    
    def __iter__(self):
        return NullIterator()
    
    def __repr__(self):
        return "{}('{}')".format(type(self).__name__, self.name)
    
    def __str__(self):
        return self.name
    
    def __eq__(self, value):
        return self.name == value
    
    
class Site(LocationComponent):
    
    def __init__(self, name, site_id, latitude=None, longitude=None,
                 elevation = None, has_forecast=False, has_obs=False):
        
        LocationComponent.__init__(self, name)
        self.id        = site_id
        self.latitude  = latitude
        self.longitude = longitude
        self.elevation = elevation
        
        if has_forecast:
            self.forecast_3hourly = Forecast3hourly(self.id)
            self.forecast_daily   = ForecastDaily(self.id)
            
        if has_obs:
            self.observations = ObservationsHourly(self.id)
        
    def __repr__(self):
        return "{}('{}:{}')".format(type(self).__name__, self.name, self.id)
    
    

class Area(LocationComponent):
    
    def __init__(self, name):
        LocationComponent.__init__(self, name)
        self.children = []
        self.regions  = []
        self.areas    = []
        
    def add(self, component):
        if type(component) == Region:
            self.regions.append(component)
        if type(component) == Area:
            self.areas.append(component)
        self.children.append(component)
        
    def remove(self, idx):
        self.children[idx] = []
        
    def __len__(self):
        return len(self.children)
    
    def __getitem__(self, idx):
        return self.children[idx]
    
    def __iter__(self):
        return AreaIterator(self.children)
        
        
class Region(Area):
    
    def __init__(self, name, region_id):
        
        Area.__init__(self, name)
        self.id = region_id
        self.regional_forecast = RegionalForecast(self.id)
        
    def __repr__(self):
        return "{}('{}:{}')".format(type(self).__name__, self.name, self.id)
        
        
class AreaIterator(object):
    """
    Object to iterate through the children in an area or region
    """
    
    def __init__(self, children):
        self.position = 0
        self.children = children
        self.stack = [children.__iter__()]
        
    def __next__(self):
        
        if self.stack == []:
            raise StopIteration
        else:
            try:
                component = next(self.stack[-1])
                self.stack.append(component.__iter__())
                return component
            except StopIteration:
                self.stack.pop()
                return self.__next__()
        
        
class NullIterator(object):
    def __next__(self):
raise StopIteration()