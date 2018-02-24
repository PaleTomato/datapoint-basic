from .api_requests.codes import region_names
from .api_requests.request import SitelistRequest
from .api_requests.forecasts import Forecast3hourly, ForecastDaily, \
    ObservationsHourly
from .locations import Region, Site


def get_all_sites():
    """
    Return a nested structure containing all UK Sites.
    """
    
    sitelist_regions      = SitelistRequest('txt','wxfcs','regionalforecast')
    sitelist_forecast     = SitelistRequest('val', 'wxfcs', 'all')
    sitelist_observations = SitelistRequest('val', 'wxobs', 'all')
    
    # Begin with UK region
    for region in sitelist_regions.site_data:
        if region['@name'] == 'uk':
            sites = region_from_json(region)
            break
    
    # Add remaining regions to the structure
    for region in sitelist_regions.site_data:
        if region['@name'] != 'uk':
            sites.add(region_from_json(region))
        
    # Add forecast sites to the regions
    for site in sitelist_forecast.site_data:
        if 'region' in site:
            this_region = region_names[site['region']]
            for region in sites.regions:
                if region == this_region:
                    site = site_from_json(site)
                    site.add_forecast()
                    region.add(site)
                    
            
        else:
            # Add site at UK level if no region is specified
            sites.add(site_from_json(site))
            
    return sites
            

def region_from_json(json):
    """
    Returns a region created using the json values from a region sitelist
    """
    name = region_names[json['@name']]
    identifier = int(json['@id'])
    
    return Region(name, identifier)


def site_from_json(json):
    """
    Returns a site created using the json values from a sitelist
    """
    name = json['name']
    identifier = int(json['id'])
    latitude  = json['latitude']  if 'latitude'  in json else None
    longitude = json['longitude'] if 'longitude' in json else None
    elevation = json['elevation'] if 'elevation' in json else None
    
    return Site(name, identifier, latitude, longitude, elevation)
    