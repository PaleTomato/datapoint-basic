"""
Python module containing useful functions that are utilised by other modules
within the package_test
"""

import math

# Define radius of the Earth
RADIUS_EARTH_KM = 6371


def distance_between_points(lat1, lon1, lat2, lon2):
    """
    Function to find the distance in km between two points on the Earth,
    given their latitudes and longitudes. The function utilises the
    Haversine formula to calculate the distance. This calculation
    assumes that the Earth is perfectly spherical.

    The inputs are the latitude and longitude of the two locations,
    where latitudes are between -90 and +90 degrees, and the longitudes
    are between -180 and +180 degrees.

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

    haversine = 2 * math.asin(math.sqrt(haversine))

    return RADIUS_EARTH_KM * haversine


def hav(theta):
    """
    Function that returns the Haversine function of the inputted angle. The
    input theta should be in radians
    """
    return (math.sin(theta/2))**2
