from ..api_call import DataPointRequest
from .filter import filter_all, filter_today

class Forecast3Hourly(object):
    
    def __init__(self, site_id):
        
        self.site_id = site_id
        self.request = DataPointRequest(
            val='val',
            wx='wxfcs',
            item='all',
            feed=site_id,
            params={'res':'3hourly'}
            )

        self.filters = [
            filter_all(self.request),
            filter_today(self.request)]
    
    def get_params(self):
        """
        Return a list of available parameters.
        """
        full_params = self.request.json['SiteRep']['Wx']['Param']
        return sorted([param["$"] for param in full_params])

    def get_times(self, filter):
        pass
    
    def get_values(self, param, filter):
        pass

    def get_filters(self):
        return sorted([str(filt) for filt in self.filters])
    
    def get_units(self, param):
        """
        Return the units for the specified parameter.
        """
        if not param in self.get_params():
            raise ValueError(
                'value %s for param is not a valid parameter' % param)
        full_params = self.request.json['SiteRep']['Wx']['Param']
        for full_param in full_params:
            if full_param['$'] == param:
                return full_param['units']