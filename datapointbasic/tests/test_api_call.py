"""
A set of unit tests for testing api_call.py
"""
import unittest
from unittest.mock import patch

from datapointbasic.api_call import ApiManager
from datapointbasic.tests import mock_server


class TestApiCall(unittest.TestCase):
    """
    A class containing the tests for the ApiManager object.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up a mock server for the tests.
        """
        cls.port = mock_server.get_free_port()
        mock_server.start_mock_server(cls.port)

        # Mock the endpoint
        mock_url = 'http://localhost:{port}'.format(port=cls.port)
        cls.endpoint_patcher = patch.dict('datapointbasic.api_call.__dict__',
                                          {'BASE_URL': mock_url})
        cls.endpoint_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.endpoint_patcher.stop()

    def test_valid_api_key(self):
        """
        Test that a valid API key returns True for api_key_is_valid.
        """
        api_manager = ApiManager(mock_server.MOCK_API_KEY)
        self.assertTrue(api_manager.api_key_is_valid())

    def test_invalid_api_key(self):
        """
        Test that an invalid API key returns False for api_key_is_valid.
        """
        with self.assertRaises(ValueError):
            ApiManager('abc')

    def test_api_string(self):
        """
        Test that the __str__ method returns the API key.
        """
        api_manager = ApiManager(mock_server.MOCK_API_KEY)
        self.assertEqual(api_manager.api_key, str(api_manager))

    def test_second_instance(self):
        """
        Test that a second ApiManager instance shares the API key.
        """
        api_manager_1 = ApiManager(mock_server.MOCK_API_KEY)
        api_manager_2 = ApiManager()
        self.assertEqual(str(api_manager_1), str(api_manager_2))

if __name__ == '__main__':
    unittest.main()
