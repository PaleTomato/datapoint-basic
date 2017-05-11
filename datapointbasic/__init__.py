import datapointbasic.searchtools
import datapointbasic.forecast

def placesearch(api_key=""):
    """
    Function placesearch creates a new instance of the datapointbasic
    LocationSearch class, and returns it. The methods of the LocationSearch can
    then be used to search for locations in the Met Office DataPoint.
    
    The single input required is a valid API key for DataPoint.
    The function returns a LocationSearch object.
    """
    search_obj = datapointbasic.searchtools.LocationSearch(api_key=api_key)
    
    return search_obj

def locationforecast(place_name, api_key=""):
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
    search_obj = datapointbasic.forecast.FullForecast(api_key, place_name)
    
    return search_obj
