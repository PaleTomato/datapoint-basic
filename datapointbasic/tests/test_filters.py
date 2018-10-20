from datetime import datetime, timedelta
import unittest

from datapointbasic.weather_data import filters
from datapointbasic.tests.mock_server import MockDataPointRequest

request_3hourly = MockDataPointRequest("val", "wxfcs", "all", "1234",
    {'res':'3hourly'})

all_values_times = [datetime(2018, 9, 21) + timedelta(minutes=delta)
    for delta in range(720, 7200, 180)]

all_values_winddir = ["W", "W", "WSW", "WSW", "WSW", "WSW", "SSW", "SW","SE",
    "ESE", "E", "ENE", "ENE", "NE", "NE", "N", "N", "NNW", "NNW", "NNW", "NNW",
    "NNW", "NNW", "NNE", "NNE", "NNE", "N", "NNE", "NNE", "NE", "NE", "E",
    "SE", "SE", "SE", "ESE"]

class TestFilters(unittest.TestCase):

    def test_filter_all(self):
        filter_all = filters.filter_all(request_3hourly)
        
        self.assertEqual(filter_all.times, all_values_times)
        self.assertEqual(filter_all["D"], all_values_winddir)

    def test_filter_today(self):
        filter_today = filters.filter_today(request_3hourly)

        self.assertEqual(filter_today.times, all_values_times[:4])
        self.assertEqual(filter_today["D"], all_values_winddir[:4])
        


