import json
import unittest
from unittest.mock import patch, call, Mock

from google.api_core.exceptions import NotFound

from app import cleanup
from app.cleanup import remove_from_bucket


class TestCleanup(unittest.TestCase):

    receipt = '''{
        "files": [
            {
                "md5sum": "11a3d51f6145a68beaf2b76684e6e7c5",
                "relativePath": "",
                "scanFileSize": 74657,
                "scanID": "bad4dd615fd9431d82fb77927489be27",
                "scanTime": 5,
                "scanMD5": "11a3d51f6145a68beaf2b76684e6e7c5",
                "name": "a148ac43-a937-401f-1234-b9bc5c123b5a",
                "scanSHA1": "ff0320264a0338866fb42b7765693a0709f88425",
                "scanFileUploadTime": "2021-11-18T13:10:43.732+00:00",
                "scanFileType": "application/zip",
                "sizeBytes": 74657,
                "scanSHA256": "e5ee35349bdb9f79f378437124fb3a9237f888cfb92029b2ad4c9d544510ba8a"
            }
        ],
        "iterationL1": "2110",
        "description": "228 survey response for period 2110 sample unit 48806979667T",
        "sensitivity": "High",
        "tdzComplete": "2021-11-18T13:10:59+0000",
        "manifestCreated": "2021-11-18T13:10:41.946Z",
        "sourceName": "sdx_prod",
        "iterationL2": "",
        "iterationL4": "",
        "dataset": "228|survey/a148ac43-a937-401f-1234-b9bc5c123b5a",
        "version": 1,
        "iterationL3": "",
        "schemaVersion": 1
    }'''

    @patch.object(cleanup, 'remove_from_bucket')
    @patch.object(cleanup, 'CONFIG')
    def test_survey_receipt(self, mock_config, remove_from_bucket):
        cleanup.process(self.receipt)
        calls = [
            call(
                "survey/a148ac43-a937-401f-1234-b9bc5c123b5a",
                mock_config.OUTPUT_BUCKET),
            call(
                "a148ac43-a937-401f-1234-b9bc5c123b5a",
                mock_config.SURVEY_INPUT_BUCKET)
        ]
        remove_from_bucket.assert_has_calls(calls, any_order=True)

    @patch.object(cleanup, 'remove_from_bucket')
    @patch.object(cleanup, 'CONFIG')
    def test_dap_receipt(self, mock_config, remove_from_bucket):
        receipt_dict = json.loads(self.receipt)
        receipt_dict['dataset'] = "283|dap/206d0f2f-2d0a-1234-87a6-86c1fdf2384f.json"
        receipt = json.dumps(receipt_dict)
        cleanup.process(receipt)
        calls = [
            call(
                "dap/206d0f2f-2d0a-1234-87a6-86c1fdf2384f.json",
                mock_config.OUTPUT_BUCKET),
            call(
                "206d0f2f-2d0a-1234-87a6-86c1fdf2384f",
                mock_config.SURVEY_INPUT_BUCKET)
        ]
        remove_from_bucket.assert_has_calls(calls, any_order=True)

    @patch.object(cleanup, 'remove_from_bucket')
    @patch.object(cleanup, 'CONFIG')
    def test_seft_receipt(self, mock_config, remove_from_bucket):
        receipt_dict = json.loads(self.receipt)
        receipt_dict['dataset'] = "093|seft/49912345678S_202109_093_20211118060139.xlsx.gpg"
        receipt = json.dumps(receipt_dict)
        cleanup.process(receipt)
        calls = [
            call(
                "seft/49912345678S_202109_093_20211118060139.xlsx.gpg",
                mock_config.OUTPUT_BUCKET),
            call(
                "49912345678S_202109_093_20211118060139.xlsx.gpg",
                mock_config.SEFT_INPUT_BUCKET)
        ]
        remove_from_bucket.assert_has_calls(calls, any_order=True)

    @patch.object(cleanup, 'remove_from_bucket')
    @patch.object(cleanup, 'CONFIG')
    def test_feedback_receipt(self, mock_config, remove_from_bucket):
        receipt_dict = json.loads(self.receipt)
        receipt_dict['dataset'] = "093|feedback/d41a586c-bea2-47c8-b782-f9bdb322b089-fb-1645465208"
        receipt = json.dumps(receipt_dict)
        cleanup.process(receipt)
        calls = [
            call(
                "feedback/d41a586c-bea2-47c8-b782-f9bdb322b089-fb-1645465208",
                mock_config.OUTPUT_BUCKET),
            call(
                "d41a586c-bea2-47c8-b782-f9bdb322b089",
                mock_config.SURVEY_INPUT_BUCKET)
        ]
        remove_from_bucket.assert_has_calls(calls, any_order=True)

    @patch.object(cleanup, 'remove_from_bucket')
    @patch.object(cleanup, 'CONFIG')
    @patch.object(cleanup, 'delete_stale_comments')
    def test_comments_receipt(self, mock_delete_comments, mock_config, remove_from_bucket):
        receipt_dict = json.loads(self.receipt)
        receipt_dict['dataset'] = "sdx_comments|comments/2021-11-18.zip"
        receipt = json.dumps(receipt_dict)
        cleanup.process(receipt)
        remove_from_bucket.assert_called_with("comments/2021-11-18.zip", mock_config.OUTPUT_BUCKET)
        mock_delete_comments.assert_called()

    def test_remove_from_bucket(self):
        mock_blob = Mock()
        mock_bucket = Mock()
        mock_bucket.blob.return_value = mock_blob
        filename = "9010576d-f3df-4011-aa42-adecd9bee011"
        remove_from_bucket(filename, mock_bucket)
        mock_bucket.blob.assert_called_with(filename)
        mock_blob.delete.assert_called()

    @patch.object(cleanup, 'logger')
    def test_not_found_in_bucket(self, mock_logger):
        mock_bucket = Mock()
        mock_bucket.blob.side_effect = NotFound("Not found")
        filename = "9010576d-f3df-4011-aa42-adecd9bee011"
        remove_from_bucket(filename, mock_bucket)
        mock_logger.error.assert_called()

    @patch.object(cleanup, 'remove_from_bucket')
    @patch.object(cleanup, 'CONFIG')
    def test_find_seft_with_file_type_and_name(self, mock_config, remove_from_bucket):
        seft_receipt_dict = json.loads(self.receipt)
        seft_receipt_dict["dataset"] = "093|"
        seft_receipt_dict["files"][0]["name"] = "49912345678S_202109_093_20211118060139.xlsx.gpg"
        seft_receipt_dict["description"] = "093 seft response for period 202212 sample unit 48806979667T"
        seft_receipt_dump = json.dumps(seft_receipt_dict)

        cleanup.process(seft_receipt_dump)

        calls = [
            call(
                "seft/49912345678S_202109_093_20211118060139.xlsx.gpg",
                mock_config.OUTPUT_BUCKET),
            call(
                "49912345678S_202109_093_20211118060139.xlsx.gpg",
                mock_config.SEFT_INPUT_BUCKET)
        ]
        remove_from_bucket.assert_has_calls(calls, any_order=True)




