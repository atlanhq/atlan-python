# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""
Suggestions models for pyatlan_v9, migrated from pyatlan/model/suggestions.py.

This module provides:
- SuggestionResponse: Response containing suggested metadata values.
- Suggestions: Builder for finding and applying metadata suggestions.
"""

from __future__ import annotations

from copy import deepcopy
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

import msgspec

from pyatlan.model.aggregation import AggregationBucketResult, Aggregations
from pyatlan.model.fields.atlan_fields import AtlanField
from pyatlan.utils import validate_type
from pyatlan_v9.model.search import Query

if TYPE_CHECKING:
    from pyatlan.client.asset import Batch
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.response import AssetMutationResponse
    from pyatlan_v9.model.assets import Asset


class SuggestionResponse(msgspec.Struct, kw_only=True):
    """Response containing suggested metadata values for an asset."""

    system_descriptions: List[SuggestionResponse.SuggestedItem] = msgspec.field(
        default_factory=list
    )
    """Suggested system descriptions."""

    user_descriptions: List[SuggestionResponse.SuggestedItem] = msgspec.field(
        default_factory=list
    )
    """Suggested user descriptions."""

    owner_users: List[SuggestionResponse.SuggestedItem] = msgspec.field(
        default_factory=list
    )
    """Suggested owner users."""

    owner_groups: List[SuggestionResponse.SuggestedItem] = msgspec.field(
        default_factory=list
    )
    """Suggested owner groups."""

    atlan_tags: List[SuggestionResponse.SuggestedItem] = msgspec.field(
        default_factory=list
    )
    """Suggested Atlan tags."""

    assigned_terms: List[SuggestionResponse.SuggestedTerm] = msgspec.field(
        default_factory=list
    )
    """Suggested glossary terms."""

    class SuggestedItem(msgspec.Struct, kw_only=True):
        """A suggested metadata value with its occurrence count."""

        count: int
        """Number of occurrences of this suggestion."""

        value: str
        """The suggested value."""

    class SuggestedTerm:
        """A suggested glossary term with its occurrence count."""

        count: int
        """Number of occurrences of this suggestion."""

        value: object  # AtlasGlossaryTerm
        """The suggested glossary term asset."""

        def __init__(self, count: int, qualified_name: str):
            from pyatlan.model.assets import AtlasGlossaryTerm

            self.count = count
            self.value = AtlasGlossaryTerm.ref_by_qualified_name(qualified_name)


class Suggestions:
    """
    Builder for finding and applying metadata suggestions for an asset.

    Uses fluent interface pattern for building suggestion queries.
    """

    AGG_DESCRIPTION = "group_by_description"
    AGG_USER_DESCRIPTION = "group_by_userDescription"
    AGG_OWNER_USERS = "group_by_ownerUsers"
    AGG_OWNER_GROUPS = "group_by_ownerGroups"
    AGG_ATLAN_TAGS = "group_by_tags"
    AGG_TERMS = "group_by_terms"

    class TYPE(str, Enum):
        """Enum representing suggestion types."""

        SYSTEM_DESCRIPTION = "SystemDescription"
        USER_DESCRIPTION = "UserDescription"
        INDIVIDUAL_OWNERS = "IndividualOwners"
        GROUP_OWNERS = "GroupOwners"
        TAGS = "Tags"
        TERMS = "Terms"

        @classmethod
        def all(cls):
            """Return all suggestion types."""
            return list(map(lambda c: c.value, cls))

    def __init__(
        self,
        asset: Optional[Asset] = None,
        include_archived: bool = False,
        includes: Optional[List[Suggestions.TYPE]] = None,
        max_suggestions: int = 5,
        with_other_types: Optional[List[str]] = None,
        wheres: Optional[List[Query]] = None,
        where_nots: Optional[List[Query]] = None,
    ):
        self.asset = asset
        self.include_archived = include_archived
        self.includes: List[Suggestions.TYPE] = includes or []
        self.max_suggestions = max_suggestions
        self.with_other_types: List[str] = with_other_types or []
        self.wheres: List[Query] = wheres or []
        self.where_nots: List[Query] = where_nots or []

    def _clone(self) -> Suggestions:
        """Return a deep copy of the current Suggestions."""
        return deepcopy(self)

    def include_archive(self, include: bool) -> Suggestions:
        """
        Add a criterion to specify whether to include archived
        assets as part of the suggestions.

        :param include: whether to include archived assets
        :returns: the Suggestions with this criterion added
        """
        validate_type(name="include", _type=bool, value=include)
        clone = self._clone()
        clone.include_archived = include
        return clone

    def include(self, type: Suggestions.TYPE) -> Suggestions:
        """
        Add a criterion for which type(s) of suggestions to include.

        :param type: suggestion type to include
        :returns: the Suggestions with this criterion added
        """
        validate_type(name="types", _type=Suggestions.TYPE, value=type)
        clone = self._clone()
        clone.includes.append(type)
        return clone

    def max_suggestion(self, value: int) -> Suggestions:
        """
        Set the maximum number of suggestions to return.

        :param value: maximum number of suggestions
        :returns: the Suggestions with this criterion added
        """
        validate_type(name="value", _type=int, value=value)
        clone = self._clone()
        clone.max_suggestions = value
        return clone

    def with_other_type(self, type: str) -> Suggestions:
        """
        Add a single criterion to include another asset type in the suggestions.

        :param type: the asset type to include
        :returns: the Suggestions with this criterion added
        """
        validate_type(name="type", _type=str, value=type)
        clone = self._clone()
        clone.with_other_types.append(type)
        return clone

    def where(self, query: Query) -> Suggestions:
        """
        Add a single criterion that must be present on every search result.

        :param query: the query criterion
        :returns: the Suggestions with this criterion added
        """
        validate_type(name="query", _type=Query, value=query)
        clone = self._clone()
        clone.wheres.append(query)
        return clone

    def where_not(self, query: Query) -> Suggestions:
        """
        Add a single criterion that must not be present on any search result.

        :param query: the query criterion
        :returns: the Suggestions with this criterion added
        """
        validate_type(name="query", _type=Query, value=query)
        clone = self._clone()
        clone.where_nots.append(query)
        return clone

    def finder(self, asset: Asset) -> Suggestions:
        """
        Build a suggestion finder for the provided asset.

        :param asset: asset for which to find suggestions
        :returns: the suggestion finder for the provided asset
        """
        self.asset = asset
        return self

    def get(self, client: AtlanClient) -> SuggestionResponse:
        """
        Execute the suggestion search and return results.

        :param client: connectivity to an Atlan tenant
        :returns: suggestion response with found suggestions
        """
        from pyatlan.model.assets import Asset
        from pyatlan.model.fluent_search import FluentSearch

        asset_name = ""
        all_types: List[str] = []

        if self.asset and self.asset.name:
            asset_name = self.asset.name
            all_types.append(self.asset.type_name)

        if self.with_other_types:
            all_types.extend(self.with_other_types)

        search = (
            FluentSearch.select(include_archived=self.include_archived)
            .where(Asset.TYPE_NAME.within(all_types))
            .where(Asset.NAME.eq(asset_name))
            .page_size(0)
            .min_somes(1)
        )

        if self.wheres:
            for condition in self.wheres:
                search = search.where(condition)

        if self.where_nots:
            for condition in self.where_nots:
                search = search.where_not(condition)

        if not self.includes:
            return SuggestionResponse()

        for incl in self.includes:
            if incl == Suggestions.TYPE.SYSTEM_DESCRIPTION:
                search = search.where_some(Asset.DESCRIPTION.has_any_value()).aggregate(
                    Suggestions.AGG_DESCRIPTION,
                    Asset.DESCRIPTION.bucket_by(
                        size=self.max_suggestions, include_source_value=True
                    ),
                )
            elif incl == Suggestions.TYPE.USER_DESCRIPTION:
                search = search.where_some(
                    Asset.USER_DESCRIPTION.has_any_value()
                ).aggregate(
                    Suggestions.AGG_USER_DESCRIPTION,
                    Asset.USER_DESCRIPTION.bucket_by(
                        size=self.max_suggestions, include_source_value=True
                    ),
                )
            elif incl == Suggestions.TYPE.INDIVIDUAL_OWNERS:
                search = search.where_some(Asset.OWNER_USERS.has_any_value()).aggregate(
                    Suggestions.AGG_OWNER_USERS,
                    Asset.OWNER_USERS.bucket_by(self.max_suggestions),
                )
            elif incl == Suggestions.TYPE.GROUP_OWNERS:
                search = search.where_some(
                    Asset.OWNER_GROUPS.has_any_value()
                ).aggregate(
                    Suggestions.AGG_OWNER_GROUPS,
                    Asset.OWNER_GROUPS.bucket_by(self.max_suggestions),
                )
            elif incl == Suggestions.TYPE.TAGS:
                search = search.where_some(Asset.ATLAN_TAGS.has_any_value()).aggregate(
                    Suggestions.AGG_ATLAN_TAGS,
                    Asset.ATLAN_TAGS.bucket_by(self.max_suggestions),
                )
            elif incl == Suggestions.TYPE.TERMS:
                search = search.where_some(
                    Asset.ASSIGNED_TERMS.has_any_value()
                ).aggregate(
                    Suggestions.AGG_TERMS,
                    Asset.ASSIGNED_TERMS.bucket_by(self.max_suggestions),
                )

            search_request = search.to_request()
            search_response = client.search(criteria=search_request)
            aggregations = search_response.aggregations
            suggestion_response = SuggestionResponse()

            for incl in self.includes:
                self._build_response(
                    client,
                    incl,
                    suggestion_response,
                    aggregations,
                )
        return suggestion_response

    def _get_descriptions(self, result: Aggregations, field: AtlanField):
        """Extract description suggestions from aggregation results."""
        results = []
        if isinstance(result, AggregationBucketResult):
            for bucket in result.buckets:
                count = bucket.doc_count
                value = bucket.get_source_value(field)
                if count and value:
                    results.append(
                        SuggestionResponse.SuggestedItem(count=count, value=value)
                    )
        return results

    def _get_terms(self, result: Aggregations):
        """Extract term suggestions from aggregation results."""
        results = []
        if isinstance(result, AggregationBucketResult):
            for bucket in result.buckets:
                count = bucket.doc_count
                value = bucket.key
                if count and value:
                    results.append(
                        SuggestionResponse.SuggestedTerm(
                            count=count, qualified_name=value
                        )
                    )
        return results

    def _get_tags(self, client: AtlanClient, result: Aggregations):
        """Extract tag suggestions from aggregation results."""
        results = []
        if isinstance(result, AggregationBucketResult):
            for bucket in result.buckets:
                count = bucket.doc_count
                value = bucket.key
                name = client.atlan_tag_cache.get_name_for_id(value)
                if count and name:
                    results.append(
                        SuggestionResponse.SuggestedItem(count=count, value=name)
                    )
        return results

    def _get_others(self, result: Aggregations):
        """Extract other suggestions from aggregation results."""
        results = []
        if isinstance(result, AggregationBucketResult):
            for bucket in result.buckets:
                count = bucket.doc_count
                value = bucket.key
                if count and value:
                    results.append(
                        SuggestionResponse.SuggestedItem(count=count, value=value)
                    )
        return results

    def _build_response(self, client, include, suggestion_response, aggregations):
        """Build the suggestion response from aggregation results."""
        if include == Suggestions.TYPE.SYSTEM_DESCRIPTION:
            suggestion_response.system_descriptions.extend(
                self._get_descriptions(
                    aggregations.get(Suggestions.AGG_DESCRIPTION),
                    self._get_asset_description_field(),
                )
            )
        elif include == Suggestions.TYPE.USER_DESCRIPTION:
            suggestion_response.user_descriptions.extend(
                self._get_descriptions(
                    aggregations.get(Suggestions.AGG_USER_DESCRIPTION),
                    self._get_asset_user_description_field(),
                )
            )
        elif include == Suggestions.TYPE.INDIVIDUAL_OWNERS:
            suggestion_response.owner_users.extend(
                self._get_others(
                    aggregations.get(Suggestions.AGG_OWNER_USERS),
                )
            )
        elif include == Suggestions.TYPE.GROUP_OWNERS:
            suggestion_response.owner_groups.extend(
                self._get_others(
                    aggregations.get(Suggestions.AGG_OWNER_GROUPS),
                )
            )
        elif include == Suggestions.TYPE.TAGS:
            suggestion_response.atlan_tags.extend(
                self._get_tags(client, aggregations.get(Suggestions.AGG_ATLAN_TAGS))
            )
        elif include == Suggestions.TYPE.TERMS:
            suggestion_response.assigned_terms.extend(
                self._get_terms(
                    aggregations.get(Suggestions.AGG_TERMS),
                )
            )

    @staticmethod
    def _get_asset_description_field() -> AtlanField:
        """Get the Asset.DESCRIPTION field."""
        from pyatlan.model.assets import Asset

        return Asset.DESCRIPTION

    @staticmethod
    def _get_asset_user_description_field() -> AtlanField:
        """Get the Asset.USER_DESCRIPTION field."""
        from pyatlan.model.assets import Asset

        return Asset.USER_DESCRIPTION

    def apply(
        self,
        client: AtlanClient,
        allow_multiple: bool = False,
        batch: Optional[Batch] = None,
    ) -> Optional[AssetMutationResponse]:
        """
        Find the requested suggestions and apply the top suggestions as changes to the asset.

        :param client: client connectivity to an Atlan tenant
        :param allow_multiple: if True, allow multiple suggestions to be applied
        :param batch: optional batch in which to apply the suggestions
        :returns: mutation response if not using batch
        """
        if batch:
            return batch.add(self._apply(client, allow_multiple).asset)
        result = self._apply(client, allow_multiple)
        return client.save(result.asset, result.include_tags)

    def _apply(self, client: AtlanClient, allow_multiple: bool) -> _Apply:
        """Apply suggestions to the asset."""
        from pyatlan_v9.model.core import AtlanTag, AtlanTagName

        response = self.get(client)
        asset = self.asset.trim_to_required()  # type: ignore[union-attr]

        description_to_apply = self._get_description_to_apply(response)
        asset.user_description = description_to_apply

        if response.owner_groups:
            if allow_multiple:
                asset.owner_groups = {group.value for group in response.owner_groups}
            else:
                asset.owner_groups = {response.owner_groups[0].value}

        if response.owner_users:
            if allow_multiple:
                asset.owner_users = {user.value for user in response.owner_users}
            else:
                asset.owner_users = {response.owner_users[0].value}

        includes_tags = False
        if response.atlan_tags:
            includes_tags = True
            if allow_multiple:
                asset.atlan_tags = [
                    AtlanTag(type_name=AtlanTagName(tag.value), propagate=False)
                    for tag in response.atlan_tags
                ]
            else:
                asset.atlan_tags = [
                    AtlanTag(
                        type_name=AtlanTagName(response.atlan_tags[0].value),
                        propagate=False,
                    )
                ]

        if response.assigned_terms:
            if allow_multiple:
                asset.assigned_terms = [term.value for term in response.assigned_terms]
            else:
                asset.assigned_terms = [response.assigned_terms[0].value]

        return _Apply(asset, includes_tags)

    def _get_description_to_apply(self, response: SuggestionResponse) -> Optional[str]:
        """Determine the best description to apply from suggestions."""
        max_description_count = 0
        description_to_apply = None

        if response.user_descriptions:
            max_description_count = response.user_descriptions[0].count
            description_to_apply = response.user_descriptions[0].value

        if response.system_descriptions:
            if response.system_descriptions[0].count > max_description_count:
                description_to_apply = response.system_descriptions[0].value

        return description_to_apply


class _Apply:
    """Internal helper to hold the asset and tag inclusion flag."""

    def __init__(self, asset: Asset, include_tags: bool):
        self.asset = asset
        self.include_tags = include_tags
