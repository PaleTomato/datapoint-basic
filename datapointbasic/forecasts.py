from datapointbasic.request import SiteSpecificRequest, RegionalRequest

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
    
    pass


class RegionalExtremes(RegionalRequest):
    
    pass