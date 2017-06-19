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
        
        self.temperature           = self._get_values("temperature")
        self.feelslike_temperature = self._get_values("feels_like_temperature")
        self.precipitation         = self._get_values("precipitation")
        self.humidity              = self._get_values("humidity")
        self.uv_index              = self._get_values("uv")
        self.weather_type          = self._get_text("weather")
        self.wind_speed            = self._get_values("wind_speed")
        self.wind_direction        = self._get_values("wind_direction")
        
    
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
        