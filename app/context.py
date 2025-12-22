import json
from typing import TypedDict

from sdx_base.errors.errors import DataError
from sdx_base.models.pubsub import Message, get_data

from app import get_logger
from app.definitions import Receipt

logger = get_logger()


class FileContext(TypedDict):
    input_name: str
    output_path: str
    survey_type: str


class MalformedReceipt(DataError):
    pass


def extract_context(message: Message) -> FileContext:
    # "name": "a148ac43-a937-401f-1234-b9bc5c123b5a.zip"
    # "dataset": "139|survey/a148ac43-a937-401f-1234-b9bc5c123b5a"
    #
    # "name": "b0227f64-c6c9-4b50-9b9e-c3e42c384419.zip"
    # "dataset": "740|feedback/b0227f64-c6c9-4b50-9b9e-c3e42c384419"
    #
    # "name": "49902989748D_202512_221_20251222131411.xlsx.gpg.zip"
    # "dataset": "221|seft/49902989748D_202512_221_20251222131411.xlsx.gpg"
    #
    # "name": "2025-12-22_06-00-21.zip.zip"
    # "dataset": "Comments|comments/2025-12-22_06-00-21.zip"
    #

    data: str = get_data(message)
    receipt: Receipt = json.loads(data)
    if 'dataset' not in receipt:
        logger.error(f"Malformed receipt: No dataset found in {data}")
        raise MalformedReceipt()

    dataset = receipt['dataset']

    if '|' not in dataset:
        logger.error(f"Malformed receipt: No | found in {dataset}")
        raise MalformedReceipt()

    output_path = dataset.split('|', 1)[1]

    if '/' not in output_path:
        logger.error(f"Malformed receipt: No / found in {dataset}")
        raise MalformedReceipt()

    survey_type, input_name = output_path.split('/', 1)

    return {
        "input_name": input_name,
        "output_path": output_path,
        "survey_type": survey_type,
    }
