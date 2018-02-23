"""
Classes to define all location types. Uses the Composite Pattern.
"""

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
    
    def __len__(self):
        return len(self.children)
    
    def __iter__(self):
        return NullIterator()
    
    
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
        self.children = []
        
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