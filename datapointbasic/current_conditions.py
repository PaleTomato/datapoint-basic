import datapoint
from datapointbasic.tools import get_place_id

class CurrentConditions(object):
    
    def __init__(self,api_key):
        # Store API key and establish connection
        self.api_key = api_key
        self.conn    = datapoint.connection(api_key=self.api_key)
        
    def get_current_conditions(self,place_name):
        """
        Function to get the current forecast at the inputted location. The input
        should be a string of the place name to search for.
    
        The output is a datapoint timestep object. If the location is not found,
        then False is outputted.
        """
    
        # Get the place ID
        ID = get_place_id(self.conn,place_name)
    
        if not ID:
            return False
    
        # Get the forecast for the site
        forecast = self.conn.get_forecast_for_site(ID, "3hourly")
    
        return forecast.now()
    
        
    def get_current_temperature(self,place_name):
        """
        Function to get the current temperature at the inputted location. The
        input should be a string of the place name to search for.
    
        The output is a numerical temperature value in celcius. If the location
        is not found, then False is outputted.
        """
    
        now = self.get_current_conditions(place_name)
    
        if now:
            return now.temperature.value
        else:
            return False
    
    def get_current_precipitation(self,place_name):
        """
        Function to get the current precipitation at the inputted location. The
        input should be a string of the place name to search for.
    
        The output is a numerical precipitation value in mm. If the location is
        not found, then False is outputted.
        """
    
        now = self.get_current_conditions(place_name)
    
        if now:
            return now.precipitation.value
        else:
            return False
