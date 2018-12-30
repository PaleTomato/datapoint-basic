"""
Python module containing useful functions that are utilised by other modules
within the package_test
"""

import math
import os

import yaml

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


def load_codes():
    """
    Return the code lists from the file 'codes.yaml'.
    """
    filename_codes = os.path.join(os.path.dirname(__file__),
                                  'Resources',
                                  'codes.yaml')

    with open(filename_codes, 'r') as file_codes:
        return yaml.load(file_codes)


def weather_from_code(weather_code):
    """
    Convert the inputted weather code to a weather type.
    """
    # Convert to integer if not 'NA'
    if weather_code != 'NA':
        weather_code = int(weather_code)

    codes = load_codes()
    return codes['weather_type'][weather_code]


def visibility_from_code(visibility_code):
    """
    Convert the inputted visibility code to a visibility description.
    """
    codes = load_codes()
    return codes['visibility'][visibility_code]


def region_from_code(region_code):
    """
    Convert the inputted region code to a region name.
    """
    codes = load_codes()
    return codes['region_names'][region_code]
