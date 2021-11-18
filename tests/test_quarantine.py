import unittest
from unittest.mock import patch, Mock

from app.quarantine import quarantine_receipt


class TestQuarantine(unittest.TestCase):

    @patch('app.quarantine.CONFIG')
    def test_quarantine_submission(self, mock_config):
        message = Mock()
        receipt = b'bad receipt'
        message.data = receipt
        mock_config.QUARANTINE_TOPIC_PATH = "quarantine_path"
        error = "bad error"

        quarantine_receipt(message, error)

        mock_config.QUARANTINE_PUBLISHER.publish.assert_called_with(
            mock_config.QUARANTINE_TOPIC_PATH,
            receipt,
            error=error)
