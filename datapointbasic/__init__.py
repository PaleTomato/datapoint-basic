import datapointbasic.searchtools
import datapointbasic.forecast
from datapointbasic.tools import ApiManager

def placesearch(api_key=None):
    """
    Function placesearch creates a new instance of the datapointbasic
    LocationSearch class, and returns it. The methods of the LocationSearch can
    then be used to search for locations in the Met Office DataPoint.
    
    The single input required is a valid API key for DataPoint.
    The function returns a LocationSearch object.
    """
    
    api = ApiManager(api_key)
    search_obj = datapointbasic.searchtools.LocationSearch(api.api_key)
    
    return search_obj

def locationforecast(place_name, api_key=None):
    """
    Function locationforecast creates a new instance of the datapointbasic
    FullForecast class, and returns it. You can then obtain the conditions for
    each day from the day attributes.
    e.g.
        forecast = locationforecast("Exeter", "aaaa-bbbb-cccc-dddd-eeee")
        temperatures, units = forecast.day0.temperature()
    
    
    The inputs required are a valid site name (as a string) and a valid API key
    for DataPoint. The function returns a FullForecast object.
    """
    
    api = ApiManager(api_key)
    search_obj = datapointbasic.forecast.FullForecast(api, place_name)
    
    return search_obj
