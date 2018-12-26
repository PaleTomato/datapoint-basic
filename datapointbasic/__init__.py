"""
A Python module that can retrieve data from the Met Office DataPoint.
"""

from .api_call import ApiManager


def enter_api_key(api_key):
    """
    Function to enter and register a DataPoint API key.

    This function is used to enter a DataPoint API key to use when retrieving
    data from the Met Office DataPoint service. The key is stored in an object
    with a shared state, so that any requests to DataPoint will use the same
    key.

    Inputs:
    -------
    api_key - Your API key that can be obtained by logging into your Met Office
              DataPoint account. The key should be entered as a single string,
              including any dashes.
    """
    ApiManager(api_key)
