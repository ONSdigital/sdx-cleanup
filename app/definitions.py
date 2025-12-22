from typing import TypedDict


class File(TypedDict):
    md5sum: str
    relativePath: str
    scanFileSize: int
    scanID: str
    scanTime: int
    scanMD5: str
    name: str
    scanSHA1: str
    scanFileUploadTime: str
    scanFileType: str
    sizeBytes: int
    scanSHA256: str


class Receipt(TypedDict):
     files: list[File]
     manifestCreated: str
     sourceName: str
     version: int
     iterationL3: str
     sensitivity: str
     iterationL4: str
     schemaVersion: int
     tdzComplete: str
     iterationL1: str
     iterationL2: str
     description: str
     dataset: str
