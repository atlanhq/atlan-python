# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
import logging
from typing import List, Optional

from pyatlan.client.atlan import AtlanClient
from pyatlan.errors import AtlanError, ConflictError, NotFoundError
from pyatlan.events.atlan_event_handler import (
    AtlanEventHandler,
    get_current_view_of_asset,
    has_description,
    has_lineage,
    has_owner,
)
from pyatlan.events.atlan_lambda_handler import process_event
from pyatlan.model.assets import Asset, AtlasGlossaryTerm, Badge, Readme
from pyatlan.model.enums import (
    AtlanCustomAttributePrimitiveType,
    BadgeComparisonOperator,
    BadgeConditionColor,
    CertificateStatus,
)
from pyatlan.model.events import AtlanEvent, AtlanEventPayload
from pyatlan.model.structs import BadgeCondition
from pyatlan.model.typedef import AttributeDef, CustomMetadataDef

logger = logging.getLogger(__name__)

CM_DAAP = "DaaP"
CM_ATTR_DAAP_SCORE = "Score"

SCORED_ATTRS = [
    "description",
    "userDescription",
    "ownerUsers",
    "ownerGroups",
    "meanings",
    "__hasLineage",
    "classifications",
    "inputToProcesses",
    "outputFromProcesses",
    "assignedEntities",
    "seeAlso",
    "links",
    "certificateStatus",
    "readme",
]
client = AtlanClient()


def _create_cm_if_not_exists(client: AtlanClient) -> Optional[str]:
    """
    Creates the custom metadata structure, if it does not already exist. (If it
    already exists, does nothing.)

    :returns: unique identifier for the custom metadata structure
    """
    try:
        return client.custom_metadata_cache.get_id_for_name(CM_DAAP)
    except NotFoundError:
        try:
            cm_def = CustomMetadataDef.create(display_name=CM_DAAP)
            cm_def.attribute_defs = [
                AttributeDef.create(
                    client=client,
                    display_name=CM_ATTR_DAAP_SCORE,
                    attribute_type=AtlanCustomAttributePrimitiveType.DECIMAL,
                )
            ]
            cm_def.options = CustomMetadataDef.Options.with_logo_as_emoji("🔖")
            client.typedef.create(cm_def)
            logger.info("Created DaaP custom metadata structure.")
            badge = Badge.create(
                client=client,
                name=CM_ATTR_DAAP_SCORE,
                cm_name=CM_DAAP,
                cm_attribute=CM_ATTR_DAAP_SCORE,
                badge_conditions=[
                    BadgeCondition.create(
                        badge_condition_operator=BadgeComparisonOperator.GTE,
                        badge_condition_value="75",
                        badge_condition_colorhex=BadgeConditionColor.GREEN,
                    ),
                    BadgeCondition.create(
                        badge_condition_operator=BadgeComparisonOperator.LT,
                        badge_condition_value="75",
                        badge_condition_colorhex=BadgeConditionColor.YELLOW,
                    ),
                    BadgeCondition.create(
                        badge_condition_operator=BadgeComparisonOperator.LTE,
                        badge_condition_value="25",
                        badge_condition_colorhex=BadgeConditionColor.RED,
                    ),
                ],
            )
            try:
                client.asset.save(badge)
                logger.info("Created DaaP completeness score badge.")
                return client.custom_metadata_cache.get_id_for_name(CM_DAAP)
            except AtlanError:
                logger.info("Unable to create badge over DaaP score.")
            return None
        except ConflictError:
            # Handle cross-thread race condition that the typedef has since
            # been created
            try:
                return client.custom_metadata_cache.get_id_for_name(CM_DAAP)
            except NotFoundError:
                logger.error(
                    "Unable to look up DaaP custom metadata, even though itshould already exist."
                )
        except AtlanError:
            logger.error("Unable to create DaaP custom metadata structure.")
    except AtlanError:
        logger.error("Unable to look up DaaP custom metadata.")
    return None


class LambdaScorer(AtlanEventHandler):
    def validate_prerequisites(self, event: AtlanEvent) -> bool:
        """
        Ensures the custom metadata structure exists (idempotently) before
        attempting any further operation.

        :returns: true if and only if the custom metadata strurcture exists
            and the event has an asset in its payload
        """

        return (
            _create_cm_if_not_exists(client) is not None
            and isinstance(event.payload, AtlanEventPayload)
            and isinstance(event.payload.asset, Asset)
        )

    def get_current_state(self, from_event: Asset) -> Optional[Asset]:
        """
        Retrieves the current state of the asset that triggered the event from
        Atlan.

        :param from_event: asset from the event payload
        :returns: current state of the asset in Atlan, if it still exists in
            Atlan
        """

        search_attrs = SCORED_ATTRS
        custom_metadata_attrs = (
            client.custom_metadata_cache.get_attributes_for_search_results(CM_DAAP)
        )

        if custom_metadata_attrs is not None:
            search_attrs.extend(custom_metadata_attrs)

        logger.info(f"Searching with: {search_attrs}")
        return get_current_view_of_asset(
            self.client,
            from_event,
            search_attrs,
            include_meanings=True,
            include_atlan_tags=True,
        )

    def has_changes(self, original: Asset, modified: Asset) -> bool:
        """
        Determines whether the asset has changed as part of this event
        processing or not.

        :param original: asset as originally found in Atlan
        :param modified: asset as changed by the event processing
        :returns: true if and only if the asset has been changed by this event
            processing
        """

        score_original: Optional[float] = -1.0
        score_modified: Optional[float] = -1.0
        if cm_original := original.get_custom_metadata(client=client, name=CM_DAAP):
            score_original = cm_original.get(CM_ATTR_DAAP_SCORE)
        if cm_modified := modified.get_custom_metadata(client=client, name=CM_DAAP):
            score_modified = cm_modified.get(CM_ATTR_DAAP_SCORE)
        logger.info(
            "Existing score = %s, new score = %s", score_original, score_modified
        )
        return score_original != score_modified

    def calculate_changes(self, asset: Asset) -> List[Asset]:
        """
        Applies the logic of event handling for this event handler. Any changes
        to be made to the asset as part of processing the event are made within
        this method. For this sample, this processing involves calculating the
        completeness score for the asset and storing the result into a custom
        metadata attribute.

        :param asset: asset as originally found in Atlan
        :returns: list of all assets modified by the event processing
        """

        score = 1.0

        if isinstance(asset, AtlasGlossaryTerm):
            s_description = 15 if has_description(asset) else 0
            s_related_term = 10 if asset.see_also else 0
            s_links = 10 if asset.links else 0
            s_related_asset = 20 if asset.assigned_entities else 0
            s_certificate = 0
            if asset.certificate_status == CertificateStatus.DRAFT:
                s_certificate = 15
            elif asset.certificate_status == CertificateStatus.VERIFIED:
                s_certificate = 25
            s_readme = 0
            readme = asset.readme
            if readme and readme.guid:
                readme = client.asset.get_by_guid(
                    readme.guid, asset_type=Readme, ignore_relationships=False
                )
                if description := readme.description:
                    if len(description) > 1000:
                        s_readme = 20
                    elif len(description) > 500:
                        s_readme = 10
                    elif len(description) > 100:
                        s_readme = 5
            score = (
                s_description
                + s_related_term
                + s_links
                + s_related_asset
                + s_certificate
                + s_readme
            )
        elif not asset.type_name.startswith("AtlasGlossary"):
            # We will not score glossaries or categories
            s_description = 15 if has_description(asset) else 0
            s_owner = 20 if has_owner(asset) else 0
            s_terms = 20 if asset.assigned_terms else 0
            s_tags = 20 if asset.atlan_tags else 0
            s_lineage = 20 if has_lineage(asset) else 0
            score = s_description + s_owner + s_lineage + s_terms + s_tags

        if score >= 0:
            revised = asset.trim_to_required()
            cma = revised.get_custom_metadata(client=client, name=CM_DAAP)
            cma[CM_ATTR_DAAP_SCORE] = score
            return [revised] if self.has_changes(asset, revised) else []
        return []


def lambda_handler(event, context):
    """
    Entry point for event handling via an AWS Lambda function.

    :param event: event details as-received by the AWS Lambda function
    :param context: event processing execution context of the AWS Lambda
        function
    """

    process_event(LambdaScorer(client), event, context)
