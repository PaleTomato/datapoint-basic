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
    CurrentConditions class, and returns it. The methods of CurrentConditions
    can then be used to obtain the current weather conditions for a specific
    location
    
    The single input required is a valid API key for DataPoint.
    The function returns a CurrentConditions object.
    """
    search_obj = datapointbasic.forecast.FullForecast(api_key, place_name)
    
    return search_obj
