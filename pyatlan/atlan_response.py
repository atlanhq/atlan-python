# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
# Based on original code from https://github.com/stripe/stripe-python (under MIT license)
from __future__ import absolute_import, division, print_function

import json


class AtlanResponseBase(object):
    def __init__(self, code, headers):
        self.code = code
        self.headers = headers

    @property
    def idempotency_key(self):
        try:
            return self.headers["idempotency-key"]
        except KeyError:
            return None


class AtlanResponse(AtlanResponseBase):
    def __init__(self, body, code, headers):
        AtlanResponseBase.__init__(self, code, headers)
        self.body = body
        self.data = json.loads(body)


class AtlanStreamResponse(AtlanResponseBase):
    def __init__(self, io, code, headers):
        AtlanResponseBase.__init__(self, code, headers)
        self.io = io
