"""
Classes to define all location types. Uses the Composite Pattern.
"""

class LocationComponent(object):
    """
    Abstract component
    """
    def __init__(self, name):
        self.name = name
        self.children = []
    
    def add(self):
        pass
    
    def remove(self):
        pass
    
    def __getitem__(self):
        pass
    
    def __len__(self):
        return len(self.children)
    
    
class Site(LocationComponent):
    
    def __init__(self, name, site_id, latitude=None, longitude=None, 
                 forecast_3hourly=None, forecast_daily=None, observations=None):
        
        LocationComponent.__init__(self, name)
        self.id               = site_id
        self.latitude         = latitude
        self.longitude        = longitude
        self.forecast_3hourly = forecast_3hourly
        self.forecast_daily   = forecast_daily
        self.observations     = observations
        

class Area(LocationComponent):
    
    def __init__(self, name):
        LocationComponent.__init__(self, name)
        
    def add(self, component):
        self.children.append(component)
        
    def remove(self, idx):
        self.children[idx] = []
        
    def __getitem__(self, idx):
        return self.children[idx]
    
    def __iter__(self):
        # return self.children.__iter__()
        return AreaIterator(self.children)
        
        
class Region(Area):
    
    def __init__(self, name, region_id, regional_forecast=None, 
                 regional_extremes=None):
        
        Area.__init__(self, name)
        self.id = region_id
        self.regional_forecast = regional_forecast
        self.regional_extremes = regional_extremes
        
        
class AreaIterator(object):
    """
    Object to iterate through the children in an area or region
    """
    
    def __init__(self, children):
        self.position = 0
        self.children = children
        
    def __next__(self):
        if self.position < len(self.children):
            self.position += 1
            return self.children[self.position-1]
        else:
            raise StopIteration()