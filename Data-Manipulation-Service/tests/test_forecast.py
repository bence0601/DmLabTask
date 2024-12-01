import unittest
from unittest.mock import patch, MagicMock
from services.forecast import Forecast

class TestForecastMethods(unittest.TestCase):


    @patch("requests.get")
    def test_fetch_weather_data_if_needed_success(self, mock_get):
        # Mocking requests.get to simulate a successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "weather data"}
        mock_get.return_value = mock_response

        city = "Budapest"
        result = Forecast.fetch_weather_data_if_needed(city)

        # Assert that the returned data matches the mock data
        self.assertEqual(result, {"data": "weather data"})

    @patch("requests.get")
    def test_fetch_weather_data_if_needed_failure(self, mock_get):
        # Mocking requests.get to simulate a failed API response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        city = "Budapest"
        result = Forecast.fetch_weather_data_if_needed(city)

        # Assert that the error message is returned for failed API call
        self.assertEqual(result, {
            "error": "Failed to fetch weather data. Status code: 500",
            "details": "Internal Server Error"
        })