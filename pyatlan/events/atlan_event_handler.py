# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
from abc import ABC
from typing import Dict, Iterable, List, Optional
from warnings import warn

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Asset, Catalog
from pyatlan.model.events import AtlanEvent, AtlanEventPayload
from pyatlan.model.search import DSL, Bool, IndexSearchRequest, Term

WEBHOOK_VALIDATION_REQUEST = '{"atlan-webhook": "Hello, humans of data! It worked. Excited to see what you build!"}'


def is_validation_request(data: str) -> bool:
    return WEBHOOK_VALIDATION_REQUEST == data


def valid_signature(expected: str, headers: Dict[str, str]) -> bool:
    """
    Validate the signing secret provided with a request matches the expected signing secret.

    :param expected: signature that must be found for a valid request
    :param headers: that were sent with the request
    :returns: True if and only if the headers contain a signing secret that matches the expected signature
    """
    if not headers:
        return False
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

    :param client: connectivity to Atlan
    :param from_event: details of the asset in the event
    :param limited_to_attributes: the limited set of attributes to retrieve about the asset
    :param include_meanings: if True, include any assigned terms
    :param include_atlan_tags: if True, include any assigned Atlan tags
    :returns: the current information about the asset in Atlan, limited to what was requested
    """
    be_active = Term.with_state("ACTIVE")
    be_of_type = Term.with_type_name(from_event.type_name)
    have_qn = Term.with_qualified_name(from_event.qualified_name or "")
    query = Bool(must=[be_active, be_of_type, have_qn])
    dsl = DSL(query=query)
    attributes = ["name", "anchor", "awsArn"]
    if limited_to_attributes:
        attributes.extend(limited_to_attributes)
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=attributes,
        relation_attributes=["guid"],
        exclude_meanings=not include_meanings,
        exclude_atlan_tags=not include_atlan_tags,
    )
    response = client.asset.search(criteria=request)
    return (
        result
        if (
            result := (
                response.current_page()[0] if len(response.current_page()) > 0 else None
            )
        )
        else None
    )


def has_description(asset: Asset) -> bool:
    """
    Check if the asset has either a user-provided or system-provided description.

    :param asset: to check for the presence of a description
    :returns: True if there is either a user-provided or system-provided description
    """
    description = asset.user_description or asset.description
    return description is not None and description != ""


def has_owner(asset: Asset) -> bool:
    """
    Check if the asset has any individual or group owners.

    :param asset: to check for the presence of an owner
    :returns: True if there is at least one individual or group owner
    """
    return (asset.owner_users is not None) or (asset.owner_groups is not None)


def has_lineage(asset: Asset) -> bool:
    """
    Check if the asset has any lineage.

    :param asset: to check for the presence of lineage
    :returns: True if the asset is input to or output from at least one process
    """
    # If possible, look directly on inputs and outputs rather than the __hasLineage flag
    if isinstance(asset, Catalog):
        return (asset.input_to_processes is not None) or (
            asset.output_from_processes is not None
        )
    else:
        return bool(asset.has_lineage)


class AtlanEventHandler(ABC):  # noqa: B024
    def __init__(self, client: AtlanClient):
        self.client = client

    def validate_prerequisites(self, event: AtlanEvent) -> bool:
        """
        Validate the prerequisites expected by the event handler. These should generally run before
        trying to do any other actions.
        This default implementation will only confirm that an event has been received and there are
        details of an asset embedded within the event.

        :param event: the event to be processed
        :returns: True if the prerequisites are met, otherwise False
        """
        return (
            event is not None
            and isinstance(event.payload, AtlanEventPayload)
            and isinstance(event.payload.asset, Asset)
        )

    def get_current_state(self, from_event: Asset) -> Optional[Asset]:
        """
        Retrieve the current state of the asset, with minimal required info to handle any logic
        the event handler requires to make its decisions.
        This default implementation will only really check that the asset still exists in Atlan.

        :param from_event: the asset from the event (which could be stale at this point)
        :returns: the current state of the asset, as retrieved from Atlan
        """
        return get_current_view_of_asset(self.client, from_event)

    def calculate_changes(self, current_view: Asset) -> List[Asset]:
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

        :param current_view: the current view / state of the asset in Atlan, as the starting point for any changes
        :returns: a list of only those assets that have changes to send to Atlan (empty, if there are no changes to
                  send)
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

        :param current: the current view / state of the asset in Atlan, that was the starting point for any change
                        calculations
        :param modified: the in-memory-modified asset against which to check if any changes actually need to be sent
                         to Atlan
        :returns: True if the modified asset should be sent on to (updated in) Atlan, or False if there are no actual
                  changes to apply
        """
        return current == modified

    def upsert_changes(self, changed_assets: List[Asset]):
        """
        Deprecated — send the changed assets to Atlan so that they are persisted.
        Use 'save_changes' instead.

        :param changed_assets: the in-memory-modified assets to send to Atlan
        """
        warn(
            "This method is deprecated, please use 'save_changes' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.save_changes(changed_assets)

    def save_changes(self, changed_assets: List[Asset]):
        """
        Actually send the changed assets to Atlan so that they are persisted.

        :param changed_assets: the in-memory-modified assets to send to Atlan
        """
        # TODO: Migrate to an AssetBatch once implemented
        for one in changed_assets:
            self.client.asset.save_merging_cm(one)
