import datapoint
from datapointbasic.tools import get_place_id

class FullForecast(object):
    """
    Class that utilises a number of DayForecast objects to return a full 5 day
    forecast
    """
    
    def __init__(self, api_key, place_name):
        """
        Initialises the class by creating the various forecast objects for
        days 0 to 4, now and units
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
        
        # Add the units
        self.units = ForecastUnits(forecast.now())
        
        
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


class AbstractForecast(object):
    """
    Abstract class that is used to return forecast data
    """
    
    def __init__(self, forecast):
        """
        Initially store the forecast for the specified day. You need to define
        the _get_data method in any sub-classes
        """
        
        self._forecast  = forecast
        
        self.temperature           = self._get_data("temperature")
        self.feelslike_temperature = self._get_data("feels_like_temperature")
        self.precipitation         = self._get_data("precipitation")
        self.humidity              = self._get_data("humidity")
        self.uv_index              = self._get_data("uv")
        self.weather_type          = self._get_data("weather")
        self.wind_speed            = self._get_data("wind_speed")
        self.wind_direction        = self._get_data("wind_direction")
        
    
class DayForecast(AbstractForecast):
    """
    Class that is used to return a forecast for a specific day
    """
    
    def __init__(self, forecast):
        """
        Initalise the object, and add the date/time
        """
        AbstractForecast.__init__(self, forecast)
        
        self.timesteps = [t.date for t in self._forecast.timesteps]
        
        
    def _get_data(self, weathertype):
        """
        Returns the text for the inputted weather type, or if this is not
        available, returns the value instead
        """
        tstep = self._forecast.timesteps
        text  = [getattr(t, weathertype).text  for t in tstep]
        value = [getattr(t, weathertype).value for t in tstep]
        
        if text[0] is None:
            return value
        else:
            return text
        
        
class CurrentConditions(AbstractForecast):
    """
    Class that returns just the current weather conditions, rather than the full
    day forecast
    """
    
    def __init__(self, forecast):
        """
        Initalise the object, and add the date/time
        """
        AbstractForecast.__init__(self, forecast)
        
        self.timestep = self._forecast.date
    
    
    def _get_data(self, weathertype):
        """
        Returns the text for the inputted weather type, or if this is not
        available, returns the value instead
        """
        text  = getattr(self._forecast, weathertype).text
        value = getattr(self._forecast, weathertype).value
        
        if text is None:
            return value
        else:
            return text
        
    
class ForecastUnits(AbstractForecast):
    """
    Class that is used to return the units for each forecast property
    """
    
    def _get_data(self, weathertype):
        """
        Returns the units for the inputted weather type
        """
        return getattr(self._forecast, weathertype).units
            