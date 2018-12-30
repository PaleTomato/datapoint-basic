"""
Module containing the 3-hourly forecast object.
"""

from ..api_call import DataPointRequest
from .filters import FilterAll, FilterToday, FilterNext24, FilterTomorrow
from ..tools import visibility_from_code, weather_from_code

VALID_FILTERS = [FilterAll, FilterToday, FilterTomorrow, FilterNext24]


class Forecast3Hourly(object):
    """
    A 3-hourly forecast object. Used to retrieve 3-hourly forecast data.

    Args:
        site_id (int): the identifier of the site.
    """
    def __init__(self, site_id):

        self.site_id = site_id
        self.request = DataPointRequest(
            val='val',
            wx='wxfcs',
            item='all',
            feed=str(site_id),
            params={'res': '3hourly'}
            )

        self.filters = {}
        for filt in VALID_FILTERS:
            this_filt = filt(self.request)
            self.filters[str(this_filt)] = this_filt

    def get_params(self):
        """
        Return a list of available parameters.

        Returns:
            list: A list of available weather parameters as strings,
                sorted alphabetically.
        """
        full_params = self.request.json['SiteRep']['Wx']['Param']
        return sorted([param["$"] for param in full_params])

    def get_times(self, time_filter, time_format=None):
        """
        Return a list of times for the specified time filter.

        Args:
            time_filter (str): Name of time filter to use. Use method
                get_filters() to output a list of available filters.
            time_format (str, optional): A datetime format code.

        Returns:
            list: If time_format is not specified, a list of datetime
                objects. If time_format is specified, then a list of
                strings in the time_format specified.
        """
        times = self.filters[time_filter].times

        if time_format:
            times = [time.strftime(time_format) for time in times]

        return times

    def get_values(self, param, time_filter):
        """
        Return a list of values for the specified parameter and filter.

        Args:
            param (str): Name of the parameter to use. Use method
                get_paramss() to output a list of avaiable parameters.
            time_filter (str): Name of time filter to use. Use method
                get_filters() to output a list of available filters.

        Returns:
            list: A list of values for the parameter using the specified
                time filter. The format of the values depends on the
                parameter specified.
        """
        short_name = self._get_param_shortname(param)
        values = self.filters[time_filter][short_name]

        if param == 'Weather Type':
            # Convert weather code to full description
            values = [weather_from_code(code) for code in values]
        elif param == 'Visibility':
            # Convert visibility to full description
            values = [visibility_from_code(code) for code in values]
        elif param in ('Temperature', 'Wind Speed', 'Max UV index',
                       'Precipitation Probability'):
            # Convert string values to integers
            values = [int(value) for value in values]

        return values

    def get_filters(self):
        """
        Return a list of available time filters.

        Returns:
            list: A list of the names of each time filter available.
        """
        return sorted(self.filters.keys())

    def get_units(self, param):
        """
        Return the units for the specified parameter.

        Args:
            param (str): Name of the parameter to use. Use method
                get_params() to output a list of avaiable parameters.

        Returns:
            str: A string representation of the units.
        """
        if param not in self.get_params():
            raise ValueError(
                'value %s for param is not a valid parameter' % param)

        full_params = self.request.json['SiteRep']['Wx']['Param']
        for full_param in full_params:
            if full_param['$'] == param:
                return full_param['units']

    def _get_param_shortname(self, param):
        """
        Get the 'short name' of the parameter 'param'.

        Args:
            param (str): Name of the parameter to use. Use method
                get_paramss() to output a list of avaiable parameters.

        Returns:
            str: The 'short name' of the parameter as used in DataPoint.
                For example the short name for Temperature is 'T'.
        """
        if param not in self.get_params():
            raise ValueError(
                'value %s for param is not a valid parameter' % param)

        full_params = self.request.json['SiteRep']['Wx']['Param']
        for full_param in full_params:
            if full_param['$'] == param:
                return full_param['name']
