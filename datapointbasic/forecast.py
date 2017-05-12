import datapoint
from datapointbasic.tools import get_place_id

class FullForecast(object):
    """
    Class that utilises a number of DayForecast objects to return a full 5 day
    forecast
    """
    
    def __init__(self, api_key, place_name):
        """
        Initialises the class by creating a number of DayForecast objects for
        days 0 to 4
        """
        self.place_name = place_name
        self.api_key    = api_key
        forecast        = self._get_forecast()
        
        # Get a forecast object for each day
        self.day0 = DayForecast(forecast.days[0])
        self.day1 = DayForecast(forecast.days[1])
        self.day2 = DayForecast(forecast.days[2])
        self.day3 = DayForecast(forecast.days[3])
        self.day4 = DayForecast(forecast.days[4])
        self.now  = CurrentConditions(forecast.now())
        
        
    def _get_forecast(self):
        """
        Function to get the current forecast for the site. The input should be
        a string of the place name to search for.
    
        The output is a datapoint Day object.
        """
        conn = datapoint.connection(api_key=self.api_key)
        
        # Get the place ID
        ID = get_place_id(conn, self.place_name)
    
        # Get the forecast for the site
        forecast = conn.get_forecast_for_site(ID, "3hourly")
    
        return forecast


class DayForecast(object):
    """
    Class that is used to return a forecast for a specific day
    """
    
    def __init__(self, forecast):
        """
        Initially store the forecast for the specified day.
        """
        self._forecast  = forecast
        
    
    def timesteps(self):
        """
        Function to return the date and time for each timestep in the forecast.
        
        The output is a list of datetime objects, from which the dates and times
        can be obtained
        """
        times = []
        for timestep in self._forecast.timesteps:
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
        
        for timestep in self._forecast.timesteps:
            values.append( getattr(timestep, weathertype).text )
        
        return values
    
    
    def _get_units(self, weathertype):
        """
        Returns the units as a string for the inputted weather type
        """
        return getattr(self._forecast.timesteps[0], weathertype).units
    
    
    def _get_values(self, weathertype):
        """
        Returns the values for the inputted weather type as a list of values for
        each timestep
        """
        values = []
        
        for timestep in self._forecast.timesteps:
            values.append( getattr(timestep, weathertype).value)
        
        return values
    
    
class CurrentConditions(DayForecast):
    """
    Class that returns just the current weather conditions, rather than the full
    day forecast
    """
    
    def timesteps(self):
        """
        Function to return the date and time for the current timestep, as a
        datetime object
        """
        return self._forecast.date
    
    
    def _get_text(self, weathertype):
        """
        Returns the text for the inputted weather type as a string
        """
        return getattr(self._forecast, weathertype).text
    
    
    def _get_units(self, weathertype):
        """
        Returns the units as a string for the inputted weather type
        """
        return getattr(self._forecast, weathertype).units
    
    
    def _get_values(self, weathertype):
        """
        Returns the value for the inputted weather type
        """
        return getattr(self._forecast, weathertype).value
        