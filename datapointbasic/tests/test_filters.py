from datetime import datetime, timedelta
import unittest

from datapointbasic.weather_data import filters
from datapointbasic.tests.mock_server import MockDataPointRequest

request_3hourly = MockDataPointRequest("val", "wxfcs", "all", "1234",
    {'res':'3hourly'})

winddir_values = ["W", "W", "WSW", "WSW", "WSW", "WSW", "SSW", "SW","SE",
    "ESE", "E", "ENE", "ENE", "NE", "NE", "N", "N", "NNW", "NNW", "NNW", "NNW",
    "NNW", "NNW", "NNE", "NNE", "NNE", "N", "NNE", "NNE", "NE", "NE", "E",
    "SE", "SE", "SE", "ESE"]

class TestFilters(unittest.TestCase):

    def test_filter_all(self):
        filter_all = filters.filter_all(request_3hourly)

        start_time = datetime(2018, 9, 21)
        times = [start_time + timedelta(minutes=delta) 
            for delta in range(720, 7200, 180)]
        

        self.assertEqual(filter_all.get_all_times(), times)
        self.assertEqual(filter_all.get_all_values("D"), winddir_values)


