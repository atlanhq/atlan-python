# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
import logging
from typing import List, Optional

from pyatlan.client.atlan import AtlanClient
from pyatlan.events.atlan_event_handler import (
    AtlanEventHandler,
    get_current_view_of_asset,
    has_description,
    has_lineage,
    has_owner,
)
from pyatlan.events.atlan_lambda_handler import process_event
from pyatlan.model.assets import Asset
from pyatlan.model.enums import CertificateStatus

REQUIRED_ATTRS = [
    "description",
    "userDescription",
    "ownerUsers",
    "ownerGroups",
    "__hasLineage",
    "inputToProcesses",
    "outputFromProcesses",
    "certificateStatus",
]
ENFORCEMENT_MESSAGE = (
    "To be verified, an asset must have a description, at least one owner, and lineage."
)
logger = logging.getLogger(__name__)

client = AtlanClient()


class LambdaEnforcer(AtlanEventHandler):
    def get_current_state(self, from_event: Asset) -> Optional[Asset]:
        """
        Retrieves the current state of the asset that triggered the event from
        Atlan.

        :param from_event: asset from the event payload
        :returns: current state of the asset in Atlan, if it still exists in
            Atlan
        """

        return get_current_view_of_asset(self.client, from_event, REQUIRED_ATTRS)

    def calculate_changes(self, asset: Asset) -> List[Asset]:
        """
        Applies the logic of event handling for this event handler. Any changes
        to be made to the asset as part of processing the event are made within
        this method. For this sample, this processing involves checking an asset
        has all of a description, owner and lineage to be verified.

        :param asset: asset as originally found in Atlan
        :returns: list of all assets modified by the event processing
        """

        if asset.certificate_status == CertificateStatus.VERIFIED:
            if (
                not has_description(asset)
                or not has_owner(asset)
                or not has_lineage(asset)
            ):
                trimmed = asset.trim_to_required()
                trimmed.certificate_status = CertificateStatus.DRAFT
                trimmed.certificate_status_message = ENFORCEMENT_MESSAGE
                return [trimmed]
            else:
                logger.info(
                    "Asset has all required information present to be verified, no enforcement required: %s",
                    asset.qualified_name,
                )
        else:
            logger.info(
                "Asset is no longer verified, no enforcement action to consider: %s",
                asset.qualified_name,
            )
        return []


def lambda_handler(event, context):
    """
    Entry point for event handling via an AWS Lambda function.

    :param event: event details as-received by the AWS Lambda function
    :param context: event processing execution context of the AWS Lambda
        function
    """

    process_event(LambdaEnforcer(client), event, context)
