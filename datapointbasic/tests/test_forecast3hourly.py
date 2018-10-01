import json
import os
import unittest
from unittest.mock import patch

from datapointbasic.weather_data import forecast3hourly

RESOURCE_PATH = os.path.join(os.path.dirname(__file__), 'Resources',
            'val', 'wxfcs', 'all', '3hourly', '1234.json')

class Test3Hourly(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.mock_request_patcher = patch(
            'datapointbasic.weather_data.forecast3hourly.DataPointRequest')
        mock_request = self.mock_request_patcher.start()
        with open(RESOURCE_PATH, 'r') as file:
            content = file.read()
        mock_request.return_value.json = json.loads(content)
    
    @classmethod
    def tearDownClass(self):
        self.mock_request_patcher.stop()

    def test_json_present(self):
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

if __name__ == '__main__':
    unittest.main()