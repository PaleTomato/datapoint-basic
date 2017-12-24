from datapointbasic.request import SiteSpecificRequest

class SiteList(object):
    """
    Class that returns a list of sites from which data can be retrieved.
    """
    def __init__(self):
        """
        Instantiate the sitelists for each forecast type
        """
        
        
        self.sitelist_3hourly      = ValidSites('wxfcs','3hourly')
        self.sitelist_daily        = ValidSites('wxfcs','daily')
        self.sitelist_observations = ValidSites('wxobs','hourly')
        
        
        
class ValidSites(SiteSpecificRequest):
    """
    Class that returns the valid sites for the forecast in question
    """
    
    def __init__(self, wx, resolution):
        
        SiteSpecificRequest.__init__(self)
        
        self.wx   = wx
        self.res  = resolution
        self.feed = 'sitelist'