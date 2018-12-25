"""
Set of classes that can produce a set of mock data for testing purposes.
"""

PARAMS_FORECAST_3HOURLY = [
    {'name': 'F', 'units': 'C', '$': 'Feels Like Temperature'},
    {'name': 'G', 'units': 'mph', '$': 'Wind Gust'},
    {'name': 'H', 'units': '%', '$': 'Screen Relative Humidity'},
    {'name': 'T', 'units': 'C', '$': 'Temperature'},
    {'name': 'V', 'units': '', '$': 'Visibility'},
    {'name': 'D', 'units': 'compass', '$': 'Wind Direction'},
    {'name': 'S', 'units': 'mph', '$': 'Wind Speed'},
    {'name': 'U', 'units': '', '$': 'Max UV Index'},
    {'name': 'W', 'units': '', '$': 'Weather Type'},
    {'name': 'Pp', 'units': '%', '$': 'Precipitation Probability'}
]

PARAMS_FORECAST_DAILY = [
    {'name': 'FDm', 'units': 'C', '$': 'Feels Like Day Maximum Temperature'},
    {'name': 'FNm', 'units': 'C', '$': 'Feels Like Night Minimum Temperature'},
    {'name': 'Dm', 'units': 'C', '$': 'Day Maximum Temperature'},
    {'name': 'Nm', 'units': 'C', '$': 'Night Minimum Temperature'},
    {'name': 'Gn', 'units': 'mph', '$': 'Wind Gust Noon'},
    {'name': 'Gm', 'units': 'mph', '$': 'Wind Gust Midnight'},
    {'name': 'Hn', 'units': '%', '$': 'Screen Relative Humidity Noon'},
    {'name': 'Hm', 'units': '%', '$': 'Screen Relative Humidity Midnight'},
    {'name': 'V', 'units': '', '$': 'Visibility'},
    {'name': 'D', 'units': 'compass', '$': 'Wind Direction'},
    {'name': 'S', 'units': 'mph', '$': 'Wind Speed'},
    {'name': 'U', 'units': '', '$': 'Max UV Index'},
    {'name': 'W', 'units': '', '$': 'Weather Type'},
    {'name': 'PPd', 'units': '%', '$': 'Precipitation Probability Day'},
    {'name': 'PPn', 'units': '%', '$': 'Precipitation Probability Night'}
]

PARAMS_OBSERVATIONS_HOURLY = [
    {'name': 'G', 'units': 'mph', '$': 'Wind Gust'},
    {'name': 'T', 'units': 'C', '$': 'Temperature'},
    {'name': 'V', 'units': 'm', '$': 'Visibility'},
    {'name': 'D', 'units': 'compass', '$': 'Wind Direction'},
    {'name': 'S', 'units': 'mph', '$': 'Wind Speed'},
    {'name': 'W', 'units': '', '$': 'Weather Type'},
    {'name': 'P', 'units': 'hpa', '$': 'Pressure'},
    {'name': 'Pt', 'units': 'Pa/s', '$': 'Pressure Tendency'},
    {'name': 'Dp', 'units': 'C', '$': 'Dew Point'},
    {'name': 'H', 'units': '%', '$': 'Screen Relative Humidity'}
]


class MockDataGenerator(object):
    """
    Class that turns several lists of weather parameters into json.

    This class formats a set of weather data into a formatted set of
    json output that is the same format as that produced by DataPoint.
    For a given set of data it can produce the sitelist, capabilities
    and site specific output data for use in testing.
    """

    def __init__(self, data_date):
        self.data_date = data_date
        self.locations = []

    def add_location(self, site_id, site_name, **kwargs):
        """
        Add a new location to the list of available locations.
        """
        self.locations.append(Location(site_id, site_name, **kwargs))


class Location(object):
    """
    A location that can store one or more forecasts and observations.
    """
    def __init__(self, site_id, site_name, **kwargs):
        self.site_id = site_id
        self.site_name = site_name
        self.site_data = kwargs
