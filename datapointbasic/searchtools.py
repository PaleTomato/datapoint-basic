import datapoint
from datapointbasic.tools import distance_between_points

class LocationSearch(object):
    """
    Class that is useful for searching through the catalogue of stations within
    the Met Office DataPoint. 
    """
    def __init__(self, api_key=""):
        
        # Store API key and establish connection
        self.api_key = api_key
        self._conn    = datapoint.connection(api_key=self.api_key)
        
    def get_places_containing(self,phrase):
        """
        Function to find locations that contain the inputted string, for example
        inputting 'exe' will return Exeter, Exe Estuary, and any others that
        match. All strings are converted to lowercase, so capitalisation is not
        necessary.
    
        The output is a list of matching strings, sorted alphabetically. If
        there are no matches then an empty list is outputted.
        """
    
        matching_sites = []
        
        # Get all the sites
        sites = self._conn.get_all_sites()
    
        # Search through the sites list
        for site in sites:
            if phrase.lower() in site.name.lower():
                matching_sites.append(site.name)
    
        # Sort a-z
        matching_sites.sort()
        
        return matching_sites
    
    def get_places_beginning_with(self,phrase):
        """
        Function to find locations that begin with the inputted string, for
        example inputting 'exe' will return Exeter, Exe Estuary, and any others
        that begin with 'exe'. All strings are converted to lowercase, so
        capitalisation is not necessary.
    
        The output is a list of matching strings, sorted alphabetically. If
        there are no matches then an empty list is outputted.
        """
    
        matching_sites = []
        
        # Get all the sites
        sites = self._conn.get_all_sites()
    
        # Search through the sites list
        for site in sites:
            if site.name.lower()[0:len(phrase)] == phrase.lower():
                matching_sites.append(site.name)
    
        # Sort a-z
        matching_sites.sort()
        
        return matching_sites
    
    def get_places_ending_with(self,phrase):
        """
        Function to find locations that end with the inputted string, for
        example inputting 'tor' will return Haytor, Hameldown Tor and any others
        ending with 'tor'. All strings are converted to lowercase, so
        capitalisation is not necessary.
    
        The output is a list of matching strings, sorted alphabetically. If
        there are no matches then an empty list is outputted.
        """
    
        matching_sites = []
        
        # Get all the sites
        sites = self._conn.get_all_sites()
    
        # Search through the sites list
        for site in sites:
            if site.name.lower()[-len(phrase):] == phrase.lower():
                matching_sites.append(site.name)
    
        # Sort a-z
        matching_sites.sort()
        
        return matching_sites
    
    def get_sites_near(self,place_name, distance):
        """
        Function to find all places within a defined radius of the inputted
        place. Input place_name should be a string which matches the name of a
        site. Input distance should be a numerical distance in km
        The output is a list of strings of all matching sites.
        
        If no sites are within the radius then an empty array is outputted. If
        the inputted site name is not found then -1 is returned
        """
        
        matching_sites = []
        
        # Get all the sites
        sites = self._conn.get_all_sites()
        
        # Find our site in the list
        for site in sites:
            if site.name.lower() == place_name.lower():
                this_site = site
                this_lat  = float(this_site.latitude)
                this_lon  = float(this_site.longitude)
                break
            
        else:
            return -1
        
        # Search through the sites list for any within range
        for site in sites:
            lat = float(site.latitude)
            lon = float(site.longitude)
            
            this_dist = distance_between_points(this_lat, this_lon, lat, lon)
            
            if this_dist < distance:
                matching_sites.append(site.name)
                
        matching_sites.sort()
        
        return matching_sites
                
                
    def is_site(self,place_name):
        """
        Returns True if the inputted string is the name of a site. Otherwise
        logical False is returned.The function is case insensetive.
        """
        
        site_exists = False
        sites = self._conn.get_all_sites()
        
        for site in sites:
            if site.name.lower() == place_name.lower():
                site_exists = True
                break
        
        return site_exists


