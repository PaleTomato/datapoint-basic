"""
Python module containing useful functions that are utilised by other modules
within the package_test
"""

import math

# Define radius of the Earth
radius_earth_km = 6371

class ApiManager(object):
    """
    Class that manages the datapoint API key. All instances of the class share
    the same state, so that the API key only needs to be entered once, and can
    be then shared between all objects that use it
    """
    
    _shared_state = {}
    
    def __init__(self, api_key=None):
        """
        Initalise by setting the __dict__ of the instance to the _shared_state
        variable. This allows the api key to be shared between all instances of
        this class.
        """
        self.__dict__ = ApiManager._shared_state
        
        if not api_key is None:
            self.api_key = api_key
            
        # Raise an exception if the API key has not been entered the first time
        try:
            self.api_key
        except AttributeError:
            raise ValueError(
                "API key must be set for the first instance of ApiManager"
                )
            
    
    def __repr__(self):
        
        return "ApiManager('%s')" % (self.api_key)
    
    def __str__(self):
        
        return self.api_key


def get_place_id(connection,site_name):
    """
    Function to find a place id from an inputted location. If the location is
    not found then the output is a logical False. The input should be a string.
    
    The function converts all strings to lower case so captalisation is not
    necessary for a match
    """

    # Get all the sites
    sites = connection.get_all_sites()

    # Search through the sites list
    for site in sites:
        if site.name.lower() == site_name.lower():
            return site.id

    else:
        raise ValueError("'%s' is not a real site!" % site_name)


def distance_between_points(lat1,lon1,lat2,lon2):
    """
    Function to find the distance in km between two points on the Earth, given
    their latitudes and longitudes. The function utilises the Haversine forumula
    to calculate the distance. This calculation assumes that the Earth is
    perfectly spherical.
    
    The inputs are the latitude and longitude of the two locations, where
    latitudes are between -90 and +90 degrees, and the longitudes are between
    -180 and +180 degrees.
    
    The output is the great-circle distance between the two locations.
    """
    
    # Convert to radians
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    lon1 = math.radians(lon1)
    lon2 = math.radians(lon2)
    
    # Calculate the difference deltas of the latitudes and longitudes
    delta_lat = abs(lat2 - lat1)
    delta_lon = abs(lon2 - lon1)
    
    haversine = hav(delta_lat) + \
                math.cos(lat1) * math.cos(lat2) * hav(delta_lon)
    
    haversine = 2 * math.asin( math.sqrt(haversine) )
    
    return radius_earth_km * haversine
    
    
def hav(theta):
    """
    Function that returns the Haversine function of the inputted angle. The
    input theta should be in radians
    """
    
    return (math.sin(theta/2))**2