# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
import json

from pyatlan.events.atlan_event_handler import is_validation_request, valid_signature
from pyatlan.model.assets import AtlasGlossaryTerm
from pyatlan.model.events import AssetUpdatePayload, AtlanEvent

SIGNING = "abc123"

VALIDATION_PAYLOAD = {
    "version": "2.0",
    "routeKey": "$default",
    "rawPath": "/",
    "rawQueryString": "",
    "headers": {
        "content-length": "85",
        "x-amzn-tls-cipher-suite": "ECDHE-RSA-AES128-GCM-SHA256",
        "x-amzn-tls-version": "TLSv1.2",
        "x-amzn-trace-id": "Root=1-64931f85-02856e0b115997577ed16d97",
        "x-forwarded-proto": "https",
        "host": "uo8rokyifhnhubgagp106xhrpvgmuqhx.lambda-url.us-east-1.on.aws",
        "x-forwarded-port": "443",
        "content-type": "text/plain; charset=utf-8",
        "x-forwarded-for": "34.194.9.164",
        "accept-encoding": "gzip",
        "user-agent": "go-resty/1.12.0 (https://github.com/go-resty/resty)",
    },
    "requestContext": {
        "accountId": "anonymous",
        "apiId": "uo8rokyifhnhubgagp106xhrpvgmuqhx",
        "domainName": "uo8rokyifhnhubgagp106xhrpvgmuqhx.lambda-url.us-east-1.on.aws",
        "domainPrefix": "uo8rokyifhnhubgagp106xhrpvgmuqhx",
        "http": {
            "method": "POST",
            "path": "/",
            "protocol": "HTTP/1.1",
            "sourceIp": "34.194.9.164",
            "userAgent": "go-resty/1.12.0 (https://github.com/go-resty/resty)",
        },
        "requestId": "27539f31-d444-419e-b1ad-4382657b7e04",
        "routeKey": "$default",
        "stage": "$default",
        "time": "21/Jun/2023:16:04:21 +0000",
        "timeEpoch": 1687363461544,
    },
    "body": '{"atlan-webhook": "Hello, humans of data! It worked. Excited to see what you build!"}',
    "isBase64Encoded": False,
}


ACTUAL_PAYLOAD = {
    "version": "2.0",
    "routeKey": "$default",
    "rawPath": "/",
    "rawQueryString": "",
    "headers": {
        "content-length": "85",
        "x-atlan-signing-secret": "abc123",
        "x-amzn-tls-cipher-suite": "ECDHE-RSA-AES128-GCM-SHA256",
        "x-amzn-tls-version": "TLSv1.2",
        "x-amzn-trace-id": "Root=1-64931f85-02856e0b115997577ed16d97",
        "x-forwarded-proto": "https",
        "host": "uo8rokyifhnhubgagp106xhrpvgmuqhx.lambda-url.us-east-1.on.aws",
        "x-forwarded-port": "443",
        "content-type": "text/plain; charset=utf-8",
        "x-forwarded-for": "34.194.9.164",
        "accept-encoding": "gzip",
        "user-agent": "go-resty/1.12.0 (https://github.com/go-resty/resty)",
    },
    "requestContext": {
        "accountId": "anonymous",
        "apiId": "uo8rokyifhnhubgagp106xhrpvgmuqhx",
        "domainName": "uo8rokyifhnhubgagp106xhrpvgmuqhx.lambda-url.us-east-1.on.aws",
        "domainPrefix": "uo8rokyifhnhubgagp106xhrpvgmuqhx",
        "http": {
            "method": "POST",
            "path": "/",
            "protocol": "HTTP/1.1",
            "sourceIp": "34.194.9.164",
            "userAgent": "go-resty/1.12.0 (https://github.com/go-resty/resty)",
        },
        "requestId": "27539f31-d444-419e-b1ad-4382657b7e04",
        "routeKey": "$default",
        "stage": "$default",
        "time": "21/Jun/2023:16:04:21 +0000",
        "timeEpoch": 1687363461544,
    },
    "body": '{"source":{},"version":{"version":"1.0.0",'
    '"versionParts":[1]},"msgCompressionKind":"NONE","msgSplitIdx":1,"msgSplitCount":1,"msgSourceIP":'
    '"10.121.193.228","msgCreatedBy":"","msgCreationTime":1666792334952,"spooled":false,"message":{'
    '"type":"ENTITY_NOTIFICATION_V2","entity":{"typeName":"AtlasGlossaryTerm","attributes":{'
    '"qualifiedName":"rrSsMGHn1q1W2dWHqSHWe@Q07rYkHOACJkmUZJgmKFP","name":"Example"},"guid":'
    '"bacab52b-6c4b-4dbe-b5da-97ec2e509c7e","status":"ACTIVE","displayText":"Example"},'
    '"operationType":"ENTITY_CREATE","eventTime":1666792332986}}',
    "isBase64Encoded": False,
}

JSON_ATLAN_EVENT = """
{
  "source": {
  },
  "version": {
    "version": "1.0.0",
    "versionParts": [
      1
    ]
  },
  "msgCompressionKind": "NONE",
  "msgSplitIdx": 1,
  "msgSplitCount": 1,
  "msgSourceIP": "10.147.3.150",
  "msgCreatedBy": "",
  "msgCreationTime": 1705924521864,
  "spooled": false,
  "message": {
    "type": "ENTITY_NOTIFICATION_V2",
    "entity": {
      "typeName": "AtlasGlossaryTerm",
      "attributes": {
        "popularityScore": 1.17549435e-38,
        "assetMcMonitorNames": [
        ],
        "lastSyncRunAt": 0,
        "assetSodaLastSyncRunAt": 0,
        "starredCount": 0,
        "adminUsers": [
        ],
        "assetMcIncidentQualifiedNames": [
        ],
        "assetMcIncidentTypes": [
        ],
        "assetSodaLastScanAt": 0,
        "sourceUpdatedAt": 0,
        "assetDbtJobLastRunArtifactsSaved": false,
        "isEditable": true,
        "announcementUpdatedAt": 0,
        "sourceCreatedAt": 0,
        "assetDbtJobLastRunDequedAt": 0,
        "assetDbtTags": [
        ],
        "qualifiedName": "8Wi1jGldVz1vEBXhGivg3@79FD59qksQ4G3Y6h5ZWTO",
        "assetDbtJobLastRunNotificationsSent": false,
        "assetMcMonitorTypes": [
        ],
        "assetSodaCheckCount": 0,
        "assetMcMonitorStatuses": [
        ],
        "starredBy": [],
        "name": "new-term",
        "certificateUpdatedAt": 1703077797628,
        "assetMcIncidentSeverities": [
        ],
        "ownerUsers": [
          "pskib"
        ],
        "certificateStatus": "DRAFT",
        "assetDbtJobLastRunHasSourcesGenerated": false,
        "assetMcIncidentSubTypes": [
        ],
        "isAIGenerated": false,
        "assetDbtJobLastRunHasDocsGenerated": false,
        "assetTags": [
        ],
        "assetMcIncidentStates": [
        ],
        "assetDbtJobLastRunUpdatedAt": 0,
        "ownerGroups": [
        ],
        "certificateUpdatedBy": "pskib",
        "assetMcMonitorQualifiedNames": [
        ],
        "assetDbtJobLastRunStartedAt": 0,
        "isDiscoverable": true,
        "isPartial": false,
        "assetMcMonitorScheduleTypes": [
        ],
        "viewerUsers": [
        ],
        "assetMcIncidentNames": [
        ],
        "userDescription": "test",
        "adminRoles": [
        ],
        "adminGroups": [
        ],
        "assetDbtJobLastRunCreatedAt": 0,
        "assetDbtJobNextRun": 0,
        "assetMcLastSyncRunAt": 0,
        "viewerGroups": [
        ],
        "assetDbtJobLastRun": 0
      },
      "guid": "a5ed097d-93ea-4728-b3c3-ef441c3e6094",
      "displayText": "new-term",
      "isIncomplete": false,
      "createdBy": "pskib",
      "updatedBy": "pskib",
      "createTime": 1703077797628,
      "updateTime": 1705924521736,
      "relationshipAttributes": {
        "anchor": {
          "guid": "579ae112-3f36-40ed-ad58-edcb6e719cf2",
          "typeName": "AtlasGlossary",
          "attributes": {
            "certificateStatus": "DRAFT",
            "__modifiedBy": "pskib",
            "__state": "ACTIVE",
            "__createdBy": "pskib",
            "starredBy": [
            ],
            "__modificationTimestamp": 1703077797628,
            "name": "Test-Glossary",
            "isPartial": false,
            "assetIcon": "atlanGlossary",
            "__timestamp": 1702635066946,
            "assetDbtJobLastRun": 0
          },
          "uniqueAttributes": {
            "qualifiedName": "79FD59qksQ4G3Y6h5ZWTO"
          }
        }
      }
    },
    "operationType": "ENTITY_UPDATE",
    "eventTime": 1705924521736,
    "mutatedDetails": {
      "typeName": "AtlasGlossaryTerm",
      "attributes": {
        "userDescription": "test"
      },
      "guid": "a5ed097d-93ea-4728-b3c3-ef441c3e6094",
      "isIncomplete": false,
      "provenanceType": 0,
      "updatedBy": "pskib",
      "updateTime": 1705924521736,
      "version": 0,
      "proxy": false
    },
    "headers": {
      "x-atlan-request-id": "e0a11772-8f4b-4141-08e1-4e74998cb0d2",
      "x-atlan-via-ui": "true"
    }
  }
}"""


def test_validation_payload():
    body = VALIDATION_PAYLOAD.get("body")
    assert is_validation_request(body)


def test_no_signing_key():
    assert not valid_signature(SIGNING, VALIDATION_PAYLOAD.get("headers"))


def test_signing_key():
    assert valid_signature(SIGNING, ACTUAL_PAYLOAD.get("headers"))


def test_body():
    body = json.loads(ACTUAL_PAYLOAD.get("body"))
    assert body
    atlan_event = AtlanEvent(**body)
    assert atlan_event
    assert atlan_event.payload
    assert isinstance(atlan_event.payload.asset, AtlasGlossaryTerm)


def test_correct_payload_type_returned():
    payload = json.loads(JSON_ATLAN_EVENT)
    event = AtlanEvent(**payload)
    assert isinstance(event.payload, AssetUpdatePayload)
