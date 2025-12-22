import base64
import json
import os
import unittest
from pathlib import Path
from typing import Final, cast
from unittest.mock import call, Mock

from fastapi import FastAPI
from sdx_base.models.pubsub import Message, Envelope
from sdx_base.run import run
from sdx_base.server.server import RouterConfig
from sdx_base.services.secrets import SecretService
from fastapi.testclient import TestClient
from sdx_base.services.storage import StorageService

from app.comments import CommentDeleter
from app.definitions import Receipt
from app.dependencies import get_storage_service, get_comments_deleter
from app.routes import router, unrecoverable_error_handler
from app.settings import Settings
from app.txid import get_tx_id

FAKE_TX_ID: Final[str] = '123'


def encode_data(data: str) -> str:
    return base64.b64encode(data.encode()).decode("utf-8").strip()


class TestCleanup(unittest.TestCase):

    receipt: Receipt = {
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
    }

    def setUp(self):
        os.environ["PROJECT_ID"] = "ons-sdx-sandbox"
        proj_root = Path(__file__).parent.parent.parent  # sdx-cleanup dir

        router_config = RouterConfig(
            router, tx_id_getter=get_tx_id, on_unrecoverable_handler=unrecoverable_error_handler
        )
        app: FastAPI = run(
            Settings,
            routers=[router_config],
            proj_root=proj_root,
            secret_reader=cast(SecretService, Mock()),
            serve=lambda a, b: a,
        )
        self.client = TestClient(app)

        self.file_deleter = Mock(spec=StorageService)
        self.comments_deleter = Mock(spec=CommentDeleter)
        app.dependency_overrides[get_storage_service] = lambda: self.file_deleter
        app.dependency_overrides[get_comments_deleter] = lambda: self.comments_deleter


    def create_envelope(self, dataset: str) -> Envelope:
        self.receipt['dataset'] = dataset
        message: Message = {
            "attributes": {},
            "data": encode_data(json.dumps(self.receipt)),
            "message_id": "123",
            "publish_time": "today"
        }
        return {
            "message": message, "subscription": ""
        }

    def test_cleanup_survey(self):
        envelope = self.create_envelope("139|survey/a148ac43-a937-401f-1234-b9bc5c123b5a")
        self.client.post("/", json=envelope)
        calls = [
            call(
                "survey/a148ac43-a937-401f-1234-b9bc5c123b5a",
                "ons-sdx-sandbox-outputs"),
            call(
                "a148ac43-a937-401f-1234-b9bc5c123b5a",
                "ons-sdx-sandbox-survey-responses")
        ]
        self.file_deleter.delete.assert_has_calls(calls, any_order=True)

    def test_cleanup_feedback(self):
        envelope = self.create_envelope("740|feedback/b0227f64-c6c9-4b50-9b9e-c3e42c384419")
        self.client.post("/", json=envelope)
        calls = [
            call(
                "feedback/b0227f64-c6c9-4b50-9b9e-c3e42c384419",
                "ons-sdx-sandbox-outputs"),
            call(
                "b0227f64-c6c9-4b50-9b9e-c3e42c384419",
                "ons-sdx-sandbox-survey-responses")
        ]
        self.file_deleter.delete.assert_has_calls(calls, any_order=True)

    def test_cleanup_seft(self):
        envelope = self.create_envelope("221|seft/49902989748D_202512_221_20251222131411.xlsx.gpg")
        self.client.post("/", json=envelope)
        calls = [
            call(
                "seft/49902989748D_202512_221_20251222131411.xlsx.gpg",
                "ons-sdx-sandbox-outputs"),
            call(
                "49902989748D_202512_221_20251222131411.xlsx.gpg",
                "ons-sdx-sandbox-seft-responses")
        ]
        self.file_deleter.delete.assert_has_calls(calls, any_order=True)

    def test_cleanup_comments(self):
        envelope = self.create_envelope("Comments|comments/2025-12-22_06-00-21.zip")
        self.client.post("/", json=envelope)
        calls = [
            call(
                "comments/2025-12-22_06-00-21.zip",
                "ons-sdx-sandbox-outputs"),
        ]
        self.file_deleter.delete.assert_has_calls(calls, any_order=True)
