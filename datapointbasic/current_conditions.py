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
    
        The outputs is a numerical temperature value and the units as a string.
        If the location is not found, then False is outputted.
        """
    
        now = self.get_current_conditions(place_name)
    
        if now:
            return (now.temperature.value, now.temperature.units)
        else:
            return False
    
    def get_current_feelslike_temperature(self,place_name):
        """
        Function to get the current feels-like temperature at the inputted
        location. The input should be a string of the place name to search for.
    
        The outputs is a numerical temperature value and the units as a string.
        If the location is not found, then False is outputted.
        """
    
        now = self.get_current_conditions(place_name)
    
        if now:
            return (now.feels_like_temperature.value,
                    now.feels_like_temperature.units)
        else:
            return False
    
    def get_current_precipitation(self,place_name):
        """
        Function to get the current precipitation at the inputted location. The
        input should be a string of the place name to search for.
    
        The output is a numerical precipitation value  and the units as a
        string. If the location is not found, then False is outputted.
        """
    
        now = self.get_current_conditions(place_name)
    
        if now:
            return (now.precipitation.value, now.precipitation.units)
        else:
            return False
        
    def get_current_humidity(self,place_name):
        """
        Function to get the current humidity at the inputted location. The
        input should be a string of the place name to search for.
    
        The output is a numerical humidity value and the units as a string.
        If the location is not found, then False is outputted.
        """
    
        now = self.get_current_conditions(place_name)
    
        if now:
            return (now.humidity.value, now.humidity.units)
        else:
            return False
        
    def get_current_uv_index(self,place_name):
        """
        Function to get the current uv index at the inputted location. The
        input should be a string of the place name to search for.
    
        The output is a numerical uv index, from 1 to 10. If the location is
        not found, then False is outputted.
        """
    
        now = self.get_current_conditions(place_name)
    
        if now:
            return now.uv.value
        else:
            return False
        
    
    def get_current_weather(self,place_name):
        """
        Function to get the current weather type at the inputted location. The
        input should be a string of the place name to search for.
    
        The output is a string description of the weather e.g. 'Heavy Rain'.
        The weather code is also outputted as an integer. If the location is
        not found, then False is outputted.
        """
    
        now = self.get_current_conditions(place_name)
    
        if now:
            return (now.weather.text,now.weather.value)
        else:
            return False
        
    
    def get_current_windspeed(self,place_name):
        """
        Function to get the current wind speed at the inputted location. The
        input should be a string of the place name to search for.
    
        The output is a numerical precipitation wind speed, and the units as a
        string. If the location is not found, then False is outputted.
        """
    
        now = self.get_current_conditions(place_name)
    
        if now:
            return (now.wind_speed.value,now.wind_speed.units)
        else:
            return False
        
    
    def get_current_winddirection(self,place_name):
        """
        Function to get the current wind direction at the inputted location. The
        input should be a string of the place name to search for.
    
        The output is a string compass direction from which the wind is coming,
        e.g. 'NW'. If the location is not found, then False is outputted.
        """
    
        now = self.get_current_conditions(place_name)
    
        if now:
            return now.wind_direction.value
        else:
            return False
        
    
        
