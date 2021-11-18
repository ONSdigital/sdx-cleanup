# sdx-cleanup

The SDX-Cleanup service is used within the Office National of Statistics (ONS) for removing 
any artefacts that remain after successful ingestion by NIFI - indicated by the posting 
of a receipt on the dap-receipt-topic.

# Receipt example

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

## License

Copyright © 2016, Office for National Statistics (https://www.ons.gov.uk)

Released under MIT license, see [LICENSE](LICENSE) for details.