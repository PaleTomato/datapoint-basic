"""
Module containing the 3-hourly forecast object.
"""

from ..api_call import DataPointRequest
from .filters import FilterAll, FilterToday, FilterNext24, FilterTomorrow

VALID_FILTERS = [FilterAll, FilterToday, FilterTomorrow, FilterNext24]


class Forecast3Hourly(object):
    """
    A 3-hourly forecast object. Used to retrieve 3-hourly forecast data.
    """
    def __init__(self, site_id):

        self.site_id = site_id
        self.request = DataPointRequest(
            val='val',
            wx='wxfcs',
            item='all',
            feed=site_id,
            params={'res': '3hourly'}
            )

        self.filters = {}
        for filt in VALID_FILTERS:
            this_filt = filt(self.request)
            self.filters[str(this_filt)] = this_filt

    def get_params(self):
        """
        Return a list of available parameters.
        """
        full_params = self.request.json['SiteRep']['Wx']['Param']
        return sorted([param["$"] for param in full_params])

    def get_times(self, time_filter):
        """
        Return a list of times for the specified time filter.
        """
        return self.filters[time_filter].times

    def get_values(self, param, time_filter):
        """
        Return a list of values for the specified parameter and filter.
        """
        pass

    def get_filters(self):
        """
        Return a list of available time filters.
        """
        return sorted(self.filters.keys())

    def get_units(self, param):
        """
        Return the units for the specified parameter.
        """
        if param not in self.get_params():
            raise ValueError(
                'value %s for param is not a valid parameter' % param)
        full_params = self.request.json['SiteRep']['Wx']['Param']
        for full_param in full_params:
            if full_param['$'] == param:
                return full_param['units']
