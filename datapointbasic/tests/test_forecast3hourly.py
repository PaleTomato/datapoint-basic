"""
A set of unit tests for testing forecast3hourly.py
"""
import unittest
from unittest.mock import patch

from datapointbasic.weather_data import forecast3hourly
from datapointbasic.tests.mock_server import MockDataPointRequest


class Test3Hourly(unittest.TestCase):
    """
    Test case for testing Forecast3Hourly class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the tests by patching the DataPointRequest with a mock.
        """
        cls.mock_request_patcher = patch(
            'datapointbasic.weather_data.forecast3hourly.DataPointRequest',
            new=MockDataPointRequest)
        cls.mock_request_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """
        Stop the patching of DataPointRequest
        """
        cls.mock_request_patcher.stop()

    def test_json_present(self):
        """
        Test that a request object is created that has json.
        """
        forecast = forecast3hourly.Forecast3Hourly('1234')
        self.assertIsNotNone(forecast.request.json)

    def test_get_params(self):
        """
        Test that the get_params() method returns a list of parameters.
        """
        expected_params = [
            "Feels Like Temperature",
            "Max UV Index",
            "Precipitation Probability",
            "Screen Relative Humidity",
            "Temperature",
            "Visibility",
            "Weather Type",
            "Wind Direction",
            "Wind Gust",
            "Wind Speed",
        ]
        forecast = forecast3hourly.Forecast3Hourly('1234')
        self.assertEqual(forecast.get_params(), expected_params)

    def test_get_filters(self):
        """
        Test that the correct filters are outputted.
        """
        expected_filters = [
            "All",
            "Next 24 Hours",
            "Today",
            "Tomorrow"
        ]
        forecast = forecast3hourly.Forecast3Hourly('1234')
        self.assertEqual(forecast.get_filters(), expected_filters)

if __name__ == '__main__':
    unittest.main()
