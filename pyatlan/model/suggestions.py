from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, List, Optional

from pydantic.v1 import Field

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.aggregation import AggregationBucketResult
from pyatlan.model.assets import Asset, AtlasGlossaryTerm
from pyatlan.model.core import AtlanObject
from pyatlan.model.fluent_search import FluentSearch
from pyatlan.model.search import Query
from pyatlan.utils import validate_type


class SuggestedItem(AtlanObject):
    count: int
    value: str


class SuggestedTerm(AtlanObject):
    count: int
    value: AtlasGlossaryTerm

    def __init__(self, count: int, qualified_name: str):
        value = AtlasGlossaryTerm.ref_by_qualified_name(qualified_name)
        super().__init__(count=count, value=value)


class SuggestionResponse(AtlanObject):
    system_descriptions: Optional[List[SuggestedItem]] = Field(default=None)
    user_descriptions: Optional[List[SuggestedItem]] = Field(default=None)
    owner_users: Optional[List[SuggestedItem]] = Field(default=None)
    owner_groups: Optional[List[SuggestedItem]] = Field(default=None)
    atlan_tags: Optional[List[SuggestedItem]] = Field(default=None)
    assigned_terms: Optional[List[SuggestedTerm]] = Field(default=None)


@dataclass
class Suggestions(AtlanObject):
    AGG_DESCRIPTION: ClassVar[str] = "group_by_description"
    AGG_USER_DESCRIPTION: ClassVar[str] = "group_by_userDescription"
    AGG_OWNER_USERS: ClassVar[str] = "group_by_ownerUsers"
    AGG_OWNER_GROUPS: ClassVar[str] = "group_by_ownerGroups"
    AGG_ATLAN_TAGS: ClassVar[str] = "group_by_tags"
    AGG_TERMS: ClassVar[str] = "group_by_terms"

    client: Optional[AtlanClient] = None
    """Client through which to find suggestions."""
    asset: Optional[Asset] = None
    """Asset for which to find suggestions."""
    include_archived: bool = False
    """Whether to include archived assets as part of suggestions (`True`) or not (`False`, default)."""
    includes: Optional[List[Suggestions.TYPE]] = None
    """Which type(s) of suggestions to include in the search and results."""
    max_suggestions: int = 5
    """Maximum number of suggestions to return (default: `5`)"""
    with_other_types: Optional[List[str]] = None
    """
    By default, we will only look for suggestions on other
    assets with exactly the same type. You may want to expand this,
    for example, for suggested metadata for tables you might also want to look
    at Views. You can add any additional types here you want to consider where
    an asset with the same name as this asset is likely have similar metadata
    (and thus be valid for providing suggestions).
    """
    wheres: Optional[List[Query]] = None
    """
    By default, we will only match on the name (exactly) of the provided asset.
    You may want to expand this, for example, to look for assets with the same name
    as well as with some other context, for example, looking only at columns with
    the same name that are also in parent tables that have the same name.
    (Columns like 'ID' may otherwise be insufficiently unique to have very useful suggestions.)
    """
    where_nots: Optional[List[Query]] = None
    """
    By default, we will only match on the name (exactly)
    of the provided asset. You may want to expand this, for example,
    to look for assets with the same name as well as without some other context,
    for example, looking only at columns with the same name that are not
    in a particular schema (e.g. one used purely for testing purposes).
    """

    class TYPE(str, Enum):
        """Enum representing suggestion types."""

        # System-level description suggestions
        SYSTEM_DESCRIPTION = "SystemDescription"
        # User-provided description suggestions
        USER_DESCRIPTION = "UserDescription"
        # Suggestions for individual users who could be owners
        INDIVIDUAL_OWNERS = "IndividualOwners"
        # Suggestions for groups who could be owners
        GROUP_OWNERS = "GroupOwners"
        # Suggestions for Atlan tags to assign to the asset
        TAGS = "Tags"
        # Suggestions for terms to assign to the asset
        TERMS = "Terms"

    def _clone(self) -> Suggestions:
        """
        Returns a copy of the current `Suggestions`
        that's ready for further operations.

        :returns: copy of the current `Suggestions`
        """
        return deepcopy(self)

    def include_archive(self, include: bool) -> Suggestions:
        """
        Add a criterion to specify whether to include archived
        assets as part of the suggestions (`True`) or not (`False`).

        :param include: criterion by which to sort the results
        :returns: the `Suggestions` with this `include_archived` criterion added
        """
        validate_type(name="include", _type=bool, value=include)
        clone = self._clone()
        clone.include_archived = include
        return clone

    def include(self, type: Suggestions.TYPE) -> Suggestions:
        """
        Add a criterion for which type(s)
        of suggestions to include in the search results.

        :param include: criterion by which to sort the results
        :returns: the `Suggestions` with this `includes` criterion added
        """
        validate_type(name="types", _type=Suggestions.TYPE, value=type)
        clone = self._clone()
        if clone.includes is None:
            clone.includes = []
        clone.includes.append(type)
        return clone

    def max_suggestion(self, value: int) -> Suggestions:
        """
        Add a criterion for maximum number of suggestions to return.

        :param value: maximum number of suggestions to return
        :returns: the `Suggestions` with this `max_suggestions` criterion added
        """
        validate_type(name="value", _type=int, value=value)
        clone = self._clone()
        clone.max_suggestions = value
        return clone

    def with_other_type(self, type: str) -> Suggestions:
        """
        Add a single criterion to include another asset type in the suggestions.

        :param type: the asset type to include
        :returns: the `Suggestions` with this `with_other_type` criterion added
        """
        validate_type(name="type", _type=str, value=type)
        clone = self._clone()
        if clone.with_other_types is None:
            clone.with_other_types = []
        clone.with_other_types.append(type)
        return clone

    def where(self, query: Query) -> Suggestions:
        """
        Add a single criterion that must be present on every search result.
        (Note: these are translated to filters.)

        :param query: the query to set as a criterion
        that must be present on every search result
        :returns: the `Suggestions` with this `where` criterion added
        """
        validate_type(name="query", _type=Query, value=query)
        clone = self._clone()
        if clone.wheres is None:
            clone.wheres = []
        clone.wheres.append(query)
        return clone

    def where_not(self, query: Query) -> Suggestions:
        """
        Add a single criterion that must not be present on any search result.

        :param query: the query to set as a criterion
        that must not be present on any search result
        :returns: the `Suggestions` with this `where_not` criterion added
        """
        validate_type(name="query", _type=Query, value=query)
        clone = self._clone()
        if clone.where_nots is None:
            clone.where_nots = []
        clone.where_nots.append(query)
        return clone

    @staticmethod
    def finder(asset: Asset, client: Optional[AtlanClient] = None) -> Suggestions:
        """
        Build a suggestion finder against
        the provided Atlan tenant for the provided asset

        :param: client connectivity to an Atlan tenant
        :param: asset for which to find suggestions
        :return: the start of a suggestion finder
        for the provided asset, against the specified tenant
        """
        client = AtlanClient.get_default_client() if not client else client
        return Suggestions(client=client, asset=asset)

    def get(self) -> SuggestionResponse:
        all_types = []
        all_types.append(self.asset.type_name)

        # When other types provided by the user
        if self.with_other_types:
            all_types.append(self.with_other_types)

        # Build fluent search
        search = (
            FluentSearch.select(include_archived=self.include_archived)
            .where(Asset.TYPE_NAME.within(all_types))
            .where(Asset.NAME.eq(self.asset.NAME))
            # We only care about the aggregations, not results
            .page_size(0)
            .min_somes(1)
        )

        if self.wheres:
            for condition in self.wheres:
                search.where(condition)

        if self.where_nots:
            for condition in self.where_nots:
                search.where_not(condition)

        for include in self.includes:
            if include == Suggestions.TYPE.SYSTEM_DESCRIPTION:
                search.where_some(Asset.DESCRIPTION.has_any_value()).aggregate(
                    Suggestions.AGG_DESCRIPTION,
                    Asset.DESCRIPTION.bucket_by(self.max_suggestions),
                )
            elif include == Suggestions.TYPE.USER_DESCRIPTION:
                search.where_some(Asset.USER_DESCRIPTION.has_any_value()).aggregate(
                    Suggestions.AGG_USER_DESCRIPTION,
                    Asset.USER_DESCRIPTION.bucket_by(self.max_suggestions),
                )
            elif include == Suggestions.TYPE.INDIVIDUAL_OWNERS:
                search.where_some(Asset.OWNER_USERS.has_any_value()).aggregate(
                    Suggestions.AGG_OWNER_USERS,
                    Asset.OWNER_USERS.bucket_by(self.max_suggestions),
                )
            elif include == Suggestions.TYPE.GROUP_OWNERS:
                search.where_some(Asset.OWNER_GROUPS.has_any_value()).aggregate(
                    Suggestions.AGG_OWNER_GROUPS,
                    Asset.OWNER_GROUPS.bucket_by(self.max_suggestions),
                )
            elif include == Suggestions.TYPE.TAGS:
                search.where_some(Asset.ATLAN_TAGS.has_any_value()).aggregate(
                    Suggestions.AGG_ATLAN_TAGS,
                    Asset.ATLAN_TAGS.bucket_by(self.max_suggestions),
                )
            elif include == Suggestions.TYPE.TERMS:
                search.where_some(Asset.ASSIGNED_TERMS.has_any_value()).aggregate(
                    Suggestions.AGG_TERMS,
                    Asset.ASSIGNED_TERMS.bucket_by(self.max_suggestions),
                )

            search_request = search.to_request()
            search_response = self.client.search(criteria=search_request)
            aggregations = search_response.aggregations
            suggestion_response = SuggestionResponse()

            for include in self.includes:
                if include == Suggestions.TYPE.SYSTEM_DESCRIPTION:
                    suggestion_response.system_descriptions(
                        self._get_descriptions(
                            aggregations.get(Suggestions.AGG_DESCRIPTION),
                            Asset.DESCRIPTION,
                        ),
                    )

    def _get_descriptions(self, result, field):
        if isinstance(result, AggregationBucketResult):
            for bucket in result.buckets:
                bucket.doc_count
                # TODO: Add support for handling nested aggregations
