from datapointbasic.request import SiteSpecificRequest, RegionalRequest

class Forecast3hourly(SiteSpecificRequest):
    
    def __init__(self):
        SiteSpecificRequest.__init__(self)

class ForecastDaily(SiteSpecificRequest):
    
    pass


class ObservationsHourly(SiteSpecificRequest):
    
    pass


class RegionalForecast(RegionalRequest):
    
    pass


class RegionalExtremes(RegionalRequest):
    
    pass