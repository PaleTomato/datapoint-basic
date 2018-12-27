from datetime import datetime, timedelta
import unittest
from unittest.mock import patch

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

MOCK_NOW = datetime(2018, 9, 21, 11, 31)

class TestFilters(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Mock datetime.now() in order to test against static data.
        """
        datetime_patch = patch('datapointbasic.weather_data.filters.datetime')
        cls.mock_datetime = datetime_patch.start()
        cls.mock_datetime.now.return_value = MOCK_NOW
        cls.mock_datetime.side_effect = \
            lambda *args, **kw: datetime(*args, **kw)
        cls.mock_datetime.strptime.side_effect = \
            lambda *args, **kw: datetime.strptime(*args, **kw)

    @classmethod
    def tearDownClass(cls):
        """
        Stop the mocking of datetime.now()
        """
        cls.mock_datetime.stop()

    def test_filter_all(self):
        filter_all = filters.FilterAll(request_3hourly)
        
        self.assertEqual(filter_all.times, all_values_times)
        self.assertEqual(filter_all["D"], all_values_winddir)

    def test_filter_today(self):
        filter_today = filters.FilterToday(request_3hourly)

        self.assertEqual(filter_today.times, all_values_times[:4])
        self.assertEqual(filter_today["D"], all_values_winddir[:4])
        
    def test_filter_tomorrow(self):
        filter_tomorrow = filters.FilterTomorrow(request_3hourly)

        self.assertEqual(filter_tomorrow.times, all_values_times[4:12])
        self.assertEqual(filter_tomorrow["D"], all_values_winddir[4:12])
        
    def test_filter_next24(self):
        filter_next24 = filters.FilterNext24(request_3hourly)
        
        self.assertEqual(filter_next24.times, all_values_times[:8])
        self.assertEqual(filter_next24["D"], all_values_winddir[:8])

if __name__ == "__main__":
       unittest.main()