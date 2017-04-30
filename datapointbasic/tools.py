"""
Python module containing useful functions that are utilised by other modules
within the package_test
"""

def get_place_id(connection,site_name):
    """
    Function to find a place id from an inputted location. If the location is
    not found then the output is a logical False. The input should be a string.
    
    The function converts all strings to lower case so captalisation is not
    necessary for a match
    """

    # Get all the sites
    sites = connection.get_all_sites()

    # Search through the sites list
    for site in sites:
        if site.name.lower() == site_name.lower():
            return site.id

    return False


    