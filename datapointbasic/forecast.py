import datapoint
from datapointbasic.tools import get_place_id

class DayForecast(object):
    """
    Class that is used to return a forecast for a specific day
    """
    
    def __init__(self, api_key, place_name, day=0):
        """
        Initially store the API key and other inputs, and get the forecast for
        the specified day
        """
        self.api_key    = api_key
        self.conn       = datapoint.connection(api_key=self.api_key)
        self.place_name = place_name
        self.day        = day
        self.forecast   = self._get_forecast(self.place_name)
        
    
    def timesteps(self):
        """
        Function to return the date and time for each timestep in the forecast.
        
        The output is a list of datetime objects, from which the dates and times
        can be obtained
        """
        times = []
        for timestep in self.forecast.timesteps:
            times.append(timestep.date)
        
        return times
        
        
    def temperature(self):
        """
        Function to get the current temperature at the inputted location.
    
        The outputs are a list of numerical temperature values for each
        timestep, and the units as a string.
        """
        weathertype = 'temperature'
        
        values = self._get_values(weathertype)
        units  = self._get_units(weathertype)

        return (values, units)
    
        
    def feelslike_temperature(self):
        """
        Function to get the current feels-like temperature at the inputted
        location.
    
        The outputs are a list of numerical feels-like temperature values for
        each timestep, and the units as a string.
        """
        weathertype = 'feels_like_temperature'
        
        values = self._get_values(weathertype)
        units  = self._get_units(weathertype)

        return (values, units)
        
    
    def precipitation(self):
        """
        Function to get the current precipitation at the inputted location.
    
        The outputs are a list of numerical precipitation values for each
        timestep, and the units as a string.
        """
        weathertype = 'precipitation'
        
        values = self._get_values(weathertype)
        units  = self._get_units(weathertype)

        return (values, units)
    
    
    def humidity(self):
        """
        Function to get the current humidity at the inputted location.
    
        The outputs are a list of numerical humidity values for each timestep,
        and the units as a string.
        """
        weathertype = 'humidity'
        
        values = self._get_values(weathertype)
        units  = self._get_units(weathertype)

        return (values, units)
        
        
    def uv_index(self):
        """
        Function to get the current uv index at the inputted location.
    
        The outputs are a list of numerical uv indices for each timestep, each
        from 1 to 10.
        """
        weathertype = 'uv'
        
        values = self._get_values(weathertype)
        
        return values
        
    
    def weather_type(self):
        """
        Function to get the current weather type at the inputted location.
    
        The output is a list of string descriptions of the weather for each
        timestep e.g. 'Heavy Rain'. The weather codes are also outputted as a
        list of integers.
        """
        weathertype = 'weather'
        
        text   = self._get_text(weathertype)
        values = self._get_values(weathertype)
        
        return (text, values)
            
    
    def wind_speed(self):
        """
        Function to get the current wind speed at the inputted location.
    
        The output is a list of numerical wind speeds for each timestep, and the
        units as a string.
        """
        weathertype = 'wind_speed'
        
        values = self._get_values(weathertype)
        units  = self._get_units(weathertype)
        
        return (values, units)
        
    
    def wind_direction(self):
        """
        Function to get the current wind direction at the inputted location.
    
        The output is a list of string compass directions for each timestep. The
        string denotes the direction from which the wind is coming, e.g. 'NW'
        for a wind from the north-west.
        """
        weathertype = 'wind_direction'
        
        values = self._get_values(weathertype)
        
        return values
        
    
    def _get_text(self, weathertype):
        """
        Returns the text for the inputted weather type as a list of values for
        each timestep
        """
        values = []
        
        for timestep in self.forecast.timesteps:
            values.append(timestep.__getattribute__(weathertype).text)
        
        return values
    
    
    def _get_units(self, weathertype):
        """
        Returns the units as a string for the inputted weather type
        """
        return self.forecast.timesteps[0].__getattribute__(weathertype).units
    
    
    def _get_values(self, weathertype):
        """
        Returns the values for the inputted weather type as a list of values for
        each timestep
        """
        values = []
        
        for timestep in self.forecast.timesteps:
            values.append(timestep.__getattribute__(weathertype).value)
        
        return values
        
        
    def _get_forecast(self):
        """
        Function to get the current forecast for the site. The input should be
        a string of the place name to search for.
    
        The output is a datapoint Day object.
        """
    
        # Get the place ID
        ID = get_place_id(self.conn,self.place_name)
    
        # Get the forecast for the site
        forecast = self.conn.get_forecast_for_site(ID, "3hourly")
    
        return forecast.days[self.day]
        