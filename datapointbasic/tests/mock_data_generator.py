"""
Set of classes that can produce a set of mock data for testing purposes.
"""
from datetime import timedelta

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

    def add_location(self, location):
        """
        Add input location to list of available locations.
        """
        if not isinstance(location, Location):
            raise TypeError('Input should be a Location object')

        self.locations.append(location)

    def get_json(self, path):
        """
        Return the output from the inputted DataPoint-like path.
        """


class Location(object):
    """
    A location that can store one or more forecasts and observations.
    """
    def __init__(self, site_id, site_name, **kwargs):
        self.site_id = site_id
        self.site_name = site_name
        self.site_data = kwargs
        self.forecast_3hourly = None

    def add_forecast_3hourly(self, forecast_3hourly):
        """
        Add a 3-hourly forecast to this location.
        """
        if not isinstance(forecast_3hourly, Forecast3Hourly):
            raise TypeError('Input should be a Forecast3Hourly object')

        self.forecast_3hourly = forecast_3hourly


class Forecast3Hourly(object):
    """
    A 3-hourly forecast set of data
    """
    def __init__(self, time_0, time_n):
        """
        Initialise with the times for the forecast.

        Creates the times used for the forecast, starting with time_0
        and through in 3-hour intervals to time_n.
        """
        self.times = []
        time = time_0

        while time <= time_n:
            self.times.append(time)
            time += timedelta(hours=3)

        self.params = {}

    def add_parameter(self, param_id, param_values):
        """
        Add a parameter to the forecast
        """
        # Check parameter is valid
        param_ids = [param['name'] for param in PARAMS_FORECAST_3HOURLY]
        if param_id not in param_ids:
            raise ValueError('Param {} is not valid'.format(param_id))

        # Check values are the correct length
        if len(param_values) != len(self.times):
            raise ValueError(
                'Length of param_values is {}. It should have length {}'
                .format(len(param_values), len(self.times)))

        self.params[param_id] = param_values
