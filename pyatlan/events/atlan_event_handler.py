# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
from typing import Iterable, List, Optional

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Asset, Catalog
from pyatlan.model.events import AtlanEvent, AtlanEventPayload
from pyatlan.model.search import DSL, Bool, IndexSearchRequest, Term

WEBHOOK_VALIDATION_REQUEST = '{"atlan-webhook": "Hello, humans of data! It worked. Excited to see what you build!"}'


def is_validation_request(data: str) -> bool:
    return WEBHOOK_VALIDATION_REQUEST == data


def valid_signature(expected: str, headers: dict[str, str]) -> bool:
    """
    Validate the signing secret provided with a request matches the expected signing secret.
    """
    if not headers:
        return False
    else:
        found = headers.get("x-atlan-signing-secret")
        return found is not None and found == expected


def get_current_view_of_asset(
    client: AtlanClient,
    from_event: Asset,
    limited_to_attributes: Optional[Iterable[str]] = None,
    include_meanings: bool = False,
    include_atlan_tags: bool = False,
) -> Optional[Asset]:
    """
    Retrieve a limited set of information about the asset in Atlan,
    as up-to-date as is available in the search index, to ensure we have
    reasonably up-to-date information about it.
    Note: this will be faster than getCurrentFullAsset, but relies on the eventual
    consistency of the search index so may not have the absolute latest information about
    an asset.
    """
    be_active = Term.with_state("ACTIVE")
    be_of_type = Term.with_type_name(from_event.type_name)
    have_qn = Term.with_qualified_name(from_event.qualified_name)
    query = Bool(must=[be_active, be_of_type, have_qn])
    dsl = DSL(query=query)
    attributes = ["name", "anchor", "aws_arn"]
    if limited_to_attributes:
        attributes.extend(limited_to_attributes)
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=attributes,
        relation_attributes=["guid"],
        exclude_meanings=~include_meanings,
        exclude_atlan_tags=~include_atlan_tags,
    )
    response = client.search(criteria=request)
    if result := response.current_page()[0]:
        return result
    return None


def has_description(asset: Asset) -> bool:
    """
    Check if the asset has either a user-provided or system-provided description.
    """
    description = asset.user_description
    if not description:
        description = asset.description
    return description is not None and description != ""


def has_owner(asset: Asset) -> bool:
    """
    Check if the asset has any individual or group owners.
    """
    return (asset.owner_users is not None) or (asset.owner_groups is not None)


def has_lineage(asset: Asset) -> bool:
    """
    Check if the asset has any lineage.
    """
    # If possible, look directly on inputs and outputs rather than the __hasLineage flag
    if isinstance(asset, Catalog):
        return (asset.input_to_processes is not None) or (
            asset.output_from_processes is not None
        )
    else:
        return bool(asset.has_lineage)


class AtlanEventHandler:
    def validate_prerequisites(self, client: AtlanClient, event: AtlanEvent) -> bool:
        """
        Validate the prerequisites expected by the event handler. These should generally run before
        trying to do any other actions.
        This default implementation will only confirm that an event has been received and there are
        details of an asset embedded within the event.
        """
        return (
            event is not None
            and isinstance(event.payload, AtlanEventPayload)
            and isinstance(event.payload.asset, Asset)
        )

    def get_current_state(
        self, client: AtlanClient, from_event: Asset
    ) -> Optional[Asset]:
        """
        Retrieve the current state of the asset, with minimal required info to handle any logic
        the event handler requires to make its decisions.
        This default implementation will only really check that the asset still exists in Atlan.
        """
        return get_current_view_of_asset(client, from_event)

    def calculate_changes(
        self, client: AtlanClient, current_view: Asset
    ) -> List[Asset]:
        """
        Calculate any changes to apply to assets, and return a collection of the minimally-updated form of the assets
        with those changes applied (in-memory). Typically, you will want to call trim_to_required()
        on the current_view of each asset before making any changes, to ensure a minimal set of changes are applied to
        the asset (minimizing the risk of accidentally clobbering any other changes someone may make to the asset
        between this in-memory set of changes and the subsequent application of those changes to Atlan itself).
        Also, you should call your has_changes() method for each asset to determine whether it actually has any changes
        to include before returning it from this method.
        NOTE: The returned assets from this method should be ONLY those assets on which updates are actually being
        applied, or you will risk an infinite loop of events triggering changes, more events, more changes, etc.
        """
        return []

    def has_changes(self, current: Asset, modified: Asset) -> bool:
        """
        Check the key information this event processing is meant to handle between the original asset and the
        in-memory-modified asset. Only return true if there is actually a change to be applied to this asset in
        Atlan - this ensures idempotency, and avoids an infinite loop of making changes repeatedly in Atlan,
        which triggers a new event, a new change, a new event, and so on.
        This default implementation only blindly checks for equality. It is likely you would want to check
        specific attributes' values, rather than the entire object, for equality when determining whether a relevant
        change has been made (or not) to the asset.
        """
        return current == modified

    def upsert_changes(self, client: AtlanClient, changed_assets: List[Asset]):
        """
        Actually send the changed assets to Atlan so that they are persisted.
        """
        # TODO: Migrate to an AssetBatch once implemented
        for one in changed_assets:
            client.upsert_merging_cm(one)
