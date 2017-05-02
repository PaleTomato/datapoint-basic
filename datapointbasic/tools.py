"""
Python module containing useful functions that are utilised by other modules
within the package_test
"""

import math

# Define radius of the Earth
radius_earth_km = 6371

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

    return False


def lon_to_km(longitude,latitude):
    """
    Function to calculate the distance in kilometres of the inputted longitude.
    As longitude lines converge towards the poles, the distance of 1 degree of
    longitude thus varies. Note that this function assumes that the Earth is
    perfectly circular, which is not true in reality.
    
    The inputs are the longitude (in degrees), which should be between -180 and
    180, and the latitude of interest (also in degrees), which should be between
    -90 at the South Pole, and +90 at the north pole.
    
    The function returns the distance in kilometres for the inputted degrees of
    longitude.
    """
    
    # Convert latitude to radians
    latitude = math.radians(latitude)
    
    # Calculate a single degree of longitude
    degree_lon = (math.pi*radius_earth_km*math.cos(latitude))/180
    
    return longitude * degree_lon


def lat_to_km(latitude):
    """
    Function that returns the distance in kilometres for the inputted number of
    degrees latitude. Note that this function assumes that the Earth is
    perfectly spherical, which is not true in reality.
    
    The input is the latitude, in degrees. The functino returns the distance in
    kilometres for the inputted degrees of latitude.
    """
    
    degree_lat = (math.pi * radius_earth_km)/180
    
    return degree_lat * latitude