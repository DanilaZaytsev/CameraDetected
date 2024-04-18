from unittest.mock import patch

class TestDetection:
    @patch("CamDetected.count_unique_persons")
    def test_count_unique_persons(self, mock_count_unique_persons):
        # Call the function with valid arguments
        mock_count_unique_persons(None, None, {"person": 2}, None)
        # Assert that the function was called with the correct arguments
        mock_count_unique_persons.assert_called_once_with(None, None, {"person": 2}, None)