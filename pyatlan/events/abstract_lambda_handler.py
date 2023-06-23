# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
import json
import os

from pyatlan.client.atlan import AtlanClient
from pyatlan.events.atlan_event_handler import (
    AtlanEventHandler,
    is_validation_request,
    valid_signature,
)
from pyatlan.model.assets import Asset
from pyatlan.model.events import AtlanEvent, AtlanEventPayload

SIGNING_SECRET = str(os.environ.get("SIGNING_SECRET"))


def process_event(
    handler: AtlanEventHandler, client: AtlanClient, event: AtlanEvent, context
):
    if handler.validate_prerequisites(client, event):
        if isinstance(event.payload, AtlanEventPayload) and isinstance(
            event.payload.asset, Asset
        ):
            current = handler.get_current_state(client, event.payload.asset)
            if current is not None:
                updated = handler.calculate_changes(client, current)
                if updated is not None:
                    handler.upsert_changes(client, updated)


def abstract_lambda_handler(
    handler: AtlanEventHandler, client: AtlanClient, event, context
):
    body = event.get("body")
    if is_validation_request(body):
        print("Matches a validation request - doing nothing and succeeding.")
        return {"statusCode": 200}
    else:
        if valid_signature(SIGNING_SECRET, event.get("headers")):
            atlan_event = json.loads(body)
            process_event(handler, client, AtlanEvent(**atlan_event), context)
        else:
            raise IOError(
                "Invalid signing secret received - will not process this request."
            )
