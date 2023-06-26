import json

from pyatlan.events.atlan_event_handler import is_validation_request, valid_signature

SIGNING = "abc123"

VALIDATION_PAYLOAD = (
    "{"
    '  "version": "2.0",'
    '  "routeKey": "$default",'
    '  "rawPath": "/",'
    '  "rawQueryString": "",'
    '  "headers": {'
    '    "content-length": "85",'
    '    "x-amzn-tls-cipher-suite": "ECDHE-RSA-AES128-GCM-SHA256",'
    '    "x-amzn-tls-version": "TLSv1.2",'
    '    "x-amzn-trace-id": "Root=1-64931f85-02856e0b115997577ed16d97",'
    '    "x-forwarded-proto": "https",'
    '    "host": "uo8rokyifhnhubgagp106xhrpvgmuqhx.lambda-url.us-east-1.on.aws",'
    '    "x-forwarded-port": "443",'
    '    "content-type": "text/plain; charset=utf-8",'
    '    "x-forwarded-for": "34.194.9.164",'
    '    "accept-encoding": "gzip",'
    '    "user-agent": "go-resty/1.12.0 (https://github.com/go-resty/resty)"'
    "  },"
    '  "requestContext": {'
    '    "accountId": "anonymous",'
    '    "apiId": "uo8rokyifhnhubgagp106xhrpvgmuqhx",'
    '    "domainName": "uo8rokyifhnhubgagp106xhrpvgmuqhx.lambda-url.us-east-1.on.aws",'
    '    "domainPrefix": "uo8rokyifhnhubgagp106xhrpvgmuqhx",'
    '    "http": {'
    '      "method": "POST",'
    '      "path": "/",'
    '      "protocol": "HTTP/1.1",'
    '      "sourceIp": "34.194.9.164",'
    '      "userAgent": "go-resty/1.12.0 (https://github.com/go-resty/resty)"'
    "    },"
    '    "requestId": "27539f31-d444-419e-b1ad-4382657b7e04",'
    '    "routeKey": "$default",'
    '    "stage": "$default",'
    '    "time": "21/Jun/2023:16:04:21 +0000",'
    '    "timeEpoch": 1687363461544'
    "  },"
    '  "body": "{\\"atlan-webhook\\": \\"Hello, humans of data! It worked. Excited to see what you build!\\"}",'
    '  "isBase64Encoded": false'
    "}"
)


ACTUAL_PAYLOAD = (
    "{"
    '  "version": "2.0",'
    '  "routeKey": "$default",'
    '  "rawPath": "/",'
    '  "rawQueryString": "",'
    '  "headers": {'
    '    "content-length": "85",'
    '    "x-atlan-signing-secret": "abc123",'
    '    "x-amzn-tls-cipher-suite": "ECDHE-RSA-AES128-GCM-SHA256",'
    '    "x-amzn-tls-version": "TLSv1.2",'
    '    "x-amzn-trace-id": "Root=1-64931f85-02856e0b115997577ed16d97",'
    '    "x-forwarded-proto": "https",'
    '    "host": "uo8rokyifhnhubgagp106xhrpvgmuqhx.lambda-url.us-east-1.on.aws",'
    '    "x-forwarded-port": "443",'
    '    "content-type": "text/plain; charset=utf-8",'
    '    "x-forwarded-for": "34.194.9.164",'
    '    "accept-encoding": "gzip",'
    '    "user-agent": "go-resty/1.12.0 (https://github.com/go-resty/resty)"'
    "  },"
    '  "requestContext": {'
    '    "accountId": "anonymous",'
    '    "apiId": "uo8rokyifhnhubgagp106xhrpvgmuqhx",'
    '    "domainName": "uo8rokyifhnhubgagp106xhrpvgmuqhx.lambda-url.us-east-1.on.aws",'
    '    "domainPrefix": "uo8rokyifhnhubgagp106xhrpvgmuqhx",'
    '    "http": {'
    '      "method": "POST",'
    '      "path": "/",'
    '      "protocol": "HTTP/1.1",'
    '      "sourceIp": "34.194.9.164",'
    '      "userAgent": "go-resty/1.12.0 (https://github.com/go-resty/resty)"'
    "    },"
    '    "requestId": "27539f31-d444-419e-b1ad-4382657b7e04",'
    '    "routeKey": "$default",'
    '    "stage": "$default",'
    '    "time": "21/Jun/2023:16:04:21 +0000",'
    '    "timeEpoch": 1687363461544'
    "  },"
    '  "body": "{\\"version\\":\\"0\\",\\"id\\":\\"256b9058-ba7a-7236-1b47-88406fdc4d2d\\",\\"detail-type\\":'
    '\\"ENTITY_CREATE\\",\\"source\\":\\"com.atlan.kafka\\",\\"account\\":\\"123456789012\\",\\"time\\":'
    '\\"2022-10-26T13:52:17Z\\",\\"region\\":\\"ap-south-1\\",\\"resources\\":[],\\"detail\\":{\\"source\\":{},'
    '\\"version\\":{\\"version\\":\\"1.0.0\\",\\"versionParts\\":[1]},\\"msgCompressionKind\\":\\"NONE\\",'
    '\\"msgSplitIdx\\":1,\\"msgSplitCount\\":1,\\"msgSourceIP\\":\\"10.121.193.228\\",\\"msgCreatedBy\\":\\"\\",'
    '\\"msgCreationTime\\":1666792334952,\\"spooled\\":false,\\"message\\":{\\"type\\":\\"ENTITY_NOTIFICATION_V2\\",'
    '\\"entity\\":{\\"typeName\\":\\"AtlasGlossaryTerm\\",\\"attributes\\":{\\"qualifiedName\\":'
    '\\"rrSsMGHn1q1W2dWHqSHWe@Q07rYkHOACJkmUZJgmKFP\\",\\"name\\":\\"Example\\"},\\"guid\\":'
    '\\"bacab52b-6c4b-4dbe-b5da-97ec2e509c7e\\",\\"status\\":\\"ACTIVE\\",\\"displayText\\":\\"Example\\"},'
    '\\"operationType\\":\\"ENTITY_CREATE\\",\\"eventTime\\":1666792332986}}}",'
    '  "isBase64Encoded": false'
    "}"
)


def test_validation_payload():
    event = json.loads(VALIDATION_PAYLOAD)
    body = event.get("body")
    assert is_validation_request(body)


def test_no_signing_key():
    event = json.loads(VALIDATION_PAYLOAD)
    assert not valid_signature(SIGNING, event.get("headers"))


def test_signing_key():
    event = json.loads(ACTUAL_PAYLOAD)
    assert valid_signature(SIGNING, event.get("headers"))
