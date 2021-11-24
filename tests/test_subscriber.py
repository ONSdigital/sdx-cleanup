import unittest
from concurrent import futures
from unittest.mock import patch, Mock

from google.cloud.pubsub_v1.subscriber.message import Message

from app.subscriber import callback, start


class TestSubscriber(unittest.TestCase):

    @patch.object(Message, 'ack')
    @patch('app.subscriber.process')
    @patch('app.subscriber.quarantine_receipt')
    def test_quarantine_is_called(self, quarantine_receipt, mock_process, mock_message):
        mock_message.data = b'Test Data'
        mock_process.side_effect = Exception
        callback(mock_message)
        quarantine_receipt.assert_called()

    @patch('app.subscriber.CONFIG')
    def test_start_timeout(self, mock_config):
        streaming_pull_future = Mock()
        streaming_pull_future.result = Mock(side_effect=futures.TimeoutError)
        mock_config.RECEIPT_SUBSCRIBER.subscribe = Mock(return_value=streaming_pull_future)
        start()
        streaming_pull_future.cancel.assert_called()

    @patch('app.subscriber.process')
    def test_callback(self, mock_process):
        mock_message = Mock()
        mock_message.data.decode.return_value = 'my message'
        callback(mock_message)
        mock_message.ack.assert_called()
