# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
import json
import os

from pyatlan.events.atlan_event_handler import (
    AtlanEventHandler,
    is_validation_request,
    valid_signature,
)
from pyatlan.model.assets import Asset
from pyatlan.model.events import AtlanEvent, AtlanEventPayload

SIGNING_SECRET = str(os.environ.get("SIGNING_SECRET"))


def process_event(handler: AtlanEventHandler, event, context):
    body = event.get("body")
    if is_validation_request(body):
        print("Matches a validation request - doing nothing and succeeding.")
        return {"statusCode": 200}
    if not valid_signature(SIGNING_SECRET, event.get("headers")):
        raise IOError(
            "Invalid signing secret received - will not process this request."
        )
    atlan_event = json.loads(body)
    atlan_event = AtlanEvent(**atlan_event)
    if handler.validate_prerequisites(atlan_event):
        if isinstance(atlan_event.payload, AtlanEventPayload) and isinstance(
            atlan_event.payload.asset, Asset
        ):
            current = handler.get_current_state(atlan_event.payload.asset)
            if current is not None:
                updated = handler.calculate_changes(current)
                if updated is not None:
                    handler.upsert_changes(updated)
