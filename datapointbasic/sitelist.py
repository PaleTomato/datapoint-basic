from datapointbasic.request import SitelistRequest
from datapointbasic.forecasts import Forecast3hourly, ForecastDaily, ObservationsHourly

class SiteList(object):
    """
    Class that returns a list of sites from which data can be retrieved.
    """
    def __init__(self):
        """
        Instantiate the sitelists for each forecast type
        """
        
        self._retrieved_sites = False
        
        
    @property
    def sites(self):
        
        if not self._retrieved_sites:
            self._create_site_list()
            
        return self._sites
    
    
    def _create_site_list(self):
        """
        Create and store the site list from DataPoint.
        
        Retrieves the site lists for forecast and observations from DataPoint
        and stores those within self._sites
        """
        sitelist_forecast     = SitelistRequest('val', 'wxfcs', 'all')
        sitelist_observations = SitelistRequest('val', 'wxobs', 'all')
        
        self._sites = {}
        for location in sitelist_forecast.site_data:
            
            name      = location['name']
            site_id   = int(location['id'])
            region    = location['region']    if 'region'    in location else None
            latitude  = location['latitude']  if 'latitude'  in location else None
            longitude = location['longitude'] if 'longitude' in location else None
            elevation = location['elevation'] if 'elevation' in location else None
            
            self._sites[site_id] = Site(name, site_id, region, latitude,
                                        longitude, elevation)
            
            self._sites[site_id].forecast3hourly = Forecast3hourly(site_id)
            self._sites[site_id].forecastdaily   = ForecastDaily(site_id)
            
            
        for location in sitelist_observations.site_data:
            site_id = int(location['id'])
            
            if not site_id in self._sites.keys():
                name      = location['name']
                site_id   = int(location['id'])
                region    = location['region']    if 'region'    in location else None
                latitude  = location['latitude']  if 'latitude'  in location else None
                longitude = location['longitude'] if 'longitude' in location else None
                elevation = location['elevation'] if 'elevation' in location else None
                
                self._sites[site_id] = Site(name, site_id, region, latitude,
                                            longitude, elevation)
                
            self._sites[site_id].observations = ObservationsHourly(site_id)
            
        

class Site(object):
    
    def __init__(
            self, name, station_id, region = None, 
            latitude = None, longitude = None, elevation = None):
        
        self.name = name
        self.id   = station_id
        
        self.region    = region
        self.latitude  = latitude
        self.longitude = longitude
        self.elevation = elevation
        
    def __repr__(self):
        return "Site('{}',{})".format(self.name, self.id)
    
    def __str__(self):
        return self.name
    