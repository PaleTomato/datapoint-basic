from .request import SiteSpecificRequest, RegionalRequest

class Forecast3hourly(SiteSpecificRequest):
    
    def __init__(self, site_id):
        SiteSpecificRequest.__init__(self, site_id)
        
        self.params['res'] = '3hourly'
        self.wx = 'wxfcs'
        
        
class ForecastDaily(SiteSpecificRequest):
    
    def __init__(self, site_id):
        SiteSpecificRequest.__init__(self, site_id)
        
        self.params['res'] = 'daily'
        self.wx = 'wxfcs'
    
    
class ObservationsHourly(SiteSpecificRequest):
    
    def __init__(self, site_id):
        SiteSpecificRequest.__init__(self, site_id)
        
        self.params['res'] = 'hourly'
        self.wx = 'wxobs'

class RegionalForecast(RegionalRequest):
    
    def __init__(self, region_id):
        RegionalRequest.__init__(self)
        
        self.id = region_id
        self.wx = 'wxfcs'
        self.item = 'regionalforecast'
        self._retreived_data = False
        
    @property
    def feed(self):
        return self.id
    
    
    @property
    def day1to2(self):
        return self._get_period('day1to2')
    
    @property
    def day3to5(self):
        return self._get_period('day3to5')
    
    @property
    def day6to15(self):
        return self._get_period('day6to15')
    
    @property
    def day16to30(self):
        return self._get_period('day16to30')
    
    def _get_period(self,period):
        if not self._retreived_data:
            self._get_forecast()
            self._retreived_data = True
        return self._data[period]
    
    def _get_forecast(self):
        raw_data = self.retrieve_data()
        
        periods = raw_data['RegionalFcst']['FcstPeriods']['Period']
        self._data = {}
        
        for period in periods:
            period_id = period['id']
            
            if period_id == 'day1to2':
                values = []
                for section in period['Paragraph']:
                    values.append(self.ForecastText(section['title'],
                                                    section['$']))
            else:
                section = period['Paragraph']
                values = self.ForecastText(section['title'],section['$'])
            
            self._data[period_id] = values 
        
    class ForecastText(object):
        """
        Basic class used to store the regional forecast text.
        """
        def __init__(self, title, text):
            self.title = title.replace(':','')
            self.text  = text
            
        def __repr__(self):
            return "{}('{}')".format(type(self).__name__, self.title)
        
        def __str__(self):
            return self.text
            
    


class RegionalExtremes(RegionalRequest):
    
    pass