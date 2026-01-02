# sdx-cleanup

![Version](https://ons-badges-752336435892.europe-west2.run.app/api/badge/custom?left=Python&right=3.13)

The SDX-Cleanup service is used within the Office National of Statistics (ONS) for removing 
any artefacts that remain after successful ingestion by NIFI - indicated by the posting 
of a receipt on the dap-receipt-topic.

# Survey Receipt example

```code
{
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
```
# Dap Survey Receipt example

```code
{
  "files": [
    {
      "md5sum": "7c467d290926d6bcf0133a07cb3ec3a3",
      "relativePath": "",
      "scanFileSize": 1806,
      "scanID": "7ae6faf787694a1397c0b3f1a471a91e",
      "scanTime": 1,
      "scanMD5": "7c467d290926d6bcf0133a07cb3ec3a3",
      "name": "206d0f2f-2d0a-1234-87a6-86c1fdf2384f.json",
      "scanSHA1": "ca61dbe81e2727898b1d28657c80b36600c3f334",
      "scanFileUploadTime": "2021-11-18T13:12:10.145+00:00",
      "scanFileType": "text/plain",
      "sizeBytes": 1806,
      "scanSHA256": "f02dce781369f1da3dfa97491a9183972583b53ac39bd134cf6258deead4a957"
    }
  ],
  "description": "283 survey response for period 202310 sample unit 61102241897K",
  "iterationL3": "",
  "dataset": "283|dap/206d0f2f-2d0a-1234-87a6-86c1fdf2384f.json",
  "version": 1,
  "tdzComplete": "2021-11-18T13:12:30+0000",
  "schemaVersion": 1,
  "manifestCreated": "2021-11-18T13:12:08.256Z",
  "iterationL4": "",
  "sourceName": "sdx_prod",
  "sensitivity": "High",
  "iterationL1": "202310",
  "iterationL2": ""
}
```
# SEFT Receipt example

```code
{
  "files": [
    {
      "md5sum": "2e3cb3fa91ae68e93d8d691857eed035",
      "relativePath": "",
      "scanFileSize": 507772,
      "scanID": "d4b918e3219c490a81612c276e189e5d",
      "scanTime": 94,
      "scanMD5": "2e3cb3fa91ae68e93d8d691857eed035",
      "name": "49912345678S_202109_093_20211118060139.xlsx.gpg",
      "scanSHA1": "833389b27cd162c6a2fb15b01fe292b7a3a32933",
      "scanFileUploadTime": "2021-11-18T06:01:51.909+00:00",
      "scanFileType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      "sizeBytes": 507772,
      "scanSHA256": "2ac5863041c1d109686149d5392e3cba48416e26701d8976b37b35fff140e992"
    }
  ],
  "iterationL4": "",
  "description": "093 seft response for period 202109 sample unit 49912345678",
  "version": 1,
  "sensitivity": "High",
  "tdzComplete": "2021-11-18T06:05:01+0000",
  "schemaVersion": 1,
  "manifestCreated": "2021-11-18T06:01:47.722Z",
  "dataset": "093|seft/49912345678S_202109_093_20211118060139.xlsx.gpg",
  "iterationL2": "",
  "iterationL1": "202109",
  "iterationL3": "",
  "sourceName": "sdx_prod"
}
```
# Comments Receipt example

```code
{
  "files": [
    {
      "md5sum": "e7c4b2fbe3f9d3536460d87456765550",
      "relativePath": "",
      "scanFileSize": 3726488,
      "scanID": "45084cd1b5f9486b9c2912e43e36c847",
      "scanTime": 1081,
      "scanMD5": "e7c4b2fbe3f9d3536460d87456765550",
      "name": "2021-11-18.zip",
      "scanSHA1": "46e4d2b3810ac3ad94cac4a603e60d5c0e897efa",
      "scanFileUploadTime": "2021-11-18T06:04:33.288+00:00",
      "scanFileType": "application/zip",
      "sizeBytes": 3726488,
      "scanSHA256": "0955f561fd503e23e05abd686d5c9acba06edd216dab70aeda5ea4a7b2dcc179"
    }
  ],
  "iterationL4": "",
  "iterationL3": "",
  "iterationL2": "",
  "iterationL1": "",
  "version": 1,
  "dataset": "sdx_comments|comments/2021-11-18.zip",
  "sensitivity": "High",
  "schemaVersion": 1,
  "tdzComplete": "2021-11-18T06:06:32+0000",
  "description": "Comments.zip",
  "sourceName": "sdx_prod",
  "manifestCreated": "2021-11-18T06:04:19.594Z"
}
```


## License

Copyright © 2016, Office for National Statistics (https://www.ons.gov.uk)

Released under MIT license, see [LICENSE](LICENSE) for details.