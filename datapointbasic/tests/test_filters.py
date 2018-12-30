"""
A set of tests for testing filters.py.
"""
from datetime import datetime, timedelta
import unittest
from unittest.mock import patch

from datapointbasic.weather_data import filters
from datapointbasic.tests.mock_server import MockDataPointRequest

REQUEST_3HOURLY = MockDataPointRequest("val", "wxfcs", "all", "1234",
                                       {'res': '3hourly'})

ALL_VALUES_TIMES = [datetime(2018, 9, 21) + timedelta(minutes=delta)
                    for delta in range(720, 7200, 180)]

ALL_VALUES_WINDDIR = ["W", "W", "WSW", "WSW", "WSW", "WSW", "SSW", "SW", "SE",
                      "ESE", "E", "ENE", "ENE", "NE", "NE", "N", "N", "NNW",
                      "NNW", "NNW", "NNW", "NNW", "NNW", "NNE", "NNE", "NNE",
                      "N", "NNE", "NNE", "NE", "NE", "E", "SE", "SE", "SE",
                      "ESE"]

MOCK_NOW = datetime(2018, 9, 21, 11, 31)


class TestFilters(unittest.TestCase):
    """
    A class containing the tests for filters.py
    """

    @classmethod
    def setUpClass(cls):
        """
        Patch datetime in order to test against static data.
        """
        cls.datetime_patch = patch(
            'datapointbasic.weather_data.filters.datetime',
            new=FakeDatetime)
        cls.datetime_patch.start()

    @classmethod
    def tearDownClass(cls):
        """
        Stop the patching of datetime
        """
        cls.datetime_patch.stop()

    def test_filter_all(self):
        """
        Test the FilterAll class.
        """
        filter_all = filters.FilterAll(REQUEST_3HOURLY)

        self.assertEqual(filter_all.times, ALL_VALUES_TIMES)
        self.assertEqual(filter_all["D"], ALL_VALUES_WINDDIR)

    def test_filter_today(self):
        """
        Test the FilterToday class.
        """
        filter_today = filters.FilterToday(REQUEST_3HOURLY)

        self.assertEqual(filter_today.times, ALL_VALUES_TIMES[:4])
        self.assertEqual(filter_today["D"], ALL_VALUES_WINDDIR[:4])

    def test_filter_tomorrow(self):
        """
        Test the FilterTomorrow class.
        """
        filter_tomorrow = filters.FilterTomorrow(REQUEST_3HOURLY)

        self.assertEqual(filter_tomorrow.times, ALL_VALUES_TIMES[4:12])
        self.assertEqual(filter_tomorrow["D"], ALL_VALUES_WINDDIR[4:12])

    def test_filter_next24(self):
        """
        Test the FilterNext24 class.
        """
        filter_next24 = filters.FilterNext24(REQUEST_3HOURLY)

        self.assertEqual(filter_next24.times, ALL_VALUES_TIMES[:8])
        self.assertEqual(filter_next24["D"], ALL_VALUES_WINDDIR[:8])


class FakeDatetime(datetime):
    """
    A replacement for datetime that mocks some methods for testing.
    """
    def __new__(cls, *args, **kwargs):  # pylint: disable=arguments-differ
        return datetime.__new__(cls, *args, **kwargs)

    @staticmethod
    def now(tz=None):
        """
        Replace now() method with a specific date for testing.
        """
        return MOCK_NOW


if __name__ == "__main__":
    unittest.main()
