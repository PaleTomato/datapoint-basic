from .api_requests.codes import region_names
from .api_requests.request import SitelistRequest
from .locations import Region, Site


def get_all_sites():
    """
    Return a nested structure containing all UK Sites.
    """
    
    regionlist            = SitelistRequest('txt','wxfcs','regionalforecast')
    sitelist_forecast     = SitelistRequest('val', 'wxfcs', 'all')
    sitelist_observations = SitelistRequest('val', 'wxobs', 'all')
    sitelist_all = merge_sitelists(sitelist_forecast, sitelist_observations)
    
    # Begin with UK region
    for region in regionlist.site_data:
        if region['@name'] == 'uk':
            sites = region_from_json(region)
            break
    
    # Add remaining regions to the structure
    for region in regionlist.site_data:
        if region['@name'] != 'uk':
            sites.add(region_from_json(region))
        
    # Add forecast sites to the regions
    for site in sitelist_all:
        if 'region' in site:
            this_region = region_names[site['region']]
            for region in sites.regions:
                if region == this_region:
                    region.add(site_from_json(site))
                    
            
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
    name         = json['name']
    identifier   = int(json['id'])
    latitude     = json['latitude']     if 'latitude'     in json else None
    longitude    = json['longitude']    if 'longitude'    in json else None
    elevation    = json['elevation']    if 'elevation'    in json else None
    has_forecast = json['has_forecast'] if 'has_forecast' in json else False
    has_obs      = json['has_obs']      if 'has_obs'      in json else False
    
    return Site(name, identifier, latitude=latitude, longitude=longitude,
                elevation=elevation, has_forecast=has_forecast,
                has_obs=has_obs)
    

def merge_sitelists(sitelist_forecast, sitelist_obs):
    """
    Merge together the sitelists for the forecasts and observations.
    """
    
    all_sites = {}
    
    for site in sitelist_forecast.site_data:
        site['has_forecast'] = True
        all_sites[site['id']] = site
        
    for site in sitelist_obs.site_data:
        site['has_obs'] = True
        site_id = site['id']
        for key, value in site.items():
            all_sites[site_id][key] = value
    
    return list(all_sites.values())