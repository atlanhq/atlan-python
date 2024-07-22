from __future__ import annotations

from copy import deepcopy
from enum import Enum
from typing import ClassVar, List, Optional

from pydantic.v1 import Field

from pyatlan.cache.atlan_tag_cache import AtlanTagCache
from pyatlan.client.asset import Batch
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.aggregation import AggregationBucketResult, Aggregations
from pyatlan.model.assets import Asset, AtlasGlossaryTerm
from pyatlan.model.core import AtlanObject, AtlanTag, AtlanTagName
from pyatlan.model.fields.atlan_fields import AtlanField
from pyatlan.model.fluent_search import FluentSearch
from pyatlan.model.response import AssetMutationResponse
from pyatlan.model.search import Query
from pyatlan.utils import validate_type


class SuggestionResponse(AtlanObject):
    system_descriptions: Optional[List[SuggestionResponse.SuggestedItem]] = Field(
        default_factory=list
    )
    user_descriptions: Optional[List[SuggestionResponse.SuggestedItem]] = Field(
        default_factory=list
    )
    owner_users: Optional[List[SuggestionResponse.SuggestedItem]] = Field(
        default_factory=list
    )
    owner_groups: Optional[List[SuggestionResponse.SuggestedItem]] = Field(
        default_factory=list
    )
    atlan_tags: Optional[List[SuggestionResponse.SuggestedItem]] = Field(
        default_factory=list
    )
    assigned_terms: Optional[List[SuggestionResponse.SuggestedTerm]] = Field(
        default_factory=list
    )

    class SuggestedItem(AtlanObject):
        count: int
        value: str

    class SuggestedTerm(AtlanObject):
        count: int
        value: AtlasGlossaryTerm

        def __init__(self, count: int, qualified_name: str):
            value = AtlasGlossaryTerm.ref_by_qualified_name(qualified_name)
            super().__init__(count=count, value=value)  # type: ignore[call-arg]


class Suggestions(AtlanObject):
    AGG_DESCRIPTION: ClassVar[str] = "group_by_description"
    AGG_USER_DESCRIPTION: ClassVar[str] = "group_by_userDescription"
    AGG_OWNER_USERS: ClassVar[str] = "group_by_ownerUsers"
    AGG_OWNER_GROUPS: ClassVar[str] = "group_by_ownerGroups"
    AGG_ATLAN_TAGS: ClassVar[str] = "group_by_tags"
    AGG_TERMS: ClassVar[str] = "group_by_terms"

    client: AtlanClient = Field(
        default_factory=lambda: AtlanClient.get_default_client()
    )
    """Client through which to find suggestions."""
    asset: Optional[Asset] = Field(default=None)
    """Asset for which to find suggestions."""
    include_archived: bool = False
    """Whether to include archived assets as part of suggestions (`True`) or not (`False`, default)."""
    includes: List[Suggestions.TYPE] = Field(default_factory=list)
    """Which type(s) of suggestions to include in the search and results."""
    max_suggestions: int = Field(default=5)
    """Maximum number of suggestions to return (default: `5`)"""
    with_other_types: Optional[List[str]] = Field(default_factory=list)
    """
    By default, we will only look for suggestions on other
    assets with exactly the same type. You may want to expand this,
    for example, for suggested metadata for tables you might also want to look
    at Views. You can add any additional types here you want to consider where
    an asset with the same name as this asset is likely have similar metadata
    (and thus be valid for providing suggestions).
    """
    wheres: Optional[List[Query]] = Field(default_factory=list)
    """
    By default, we will only match on the name (exactly) of the provided asset.
    You may want to expand this, for example, to look for assets with the same name
    as well as with some other context, for example, looking only at columns with
    the same name that are also in parent tables that have the same name.
    (Columns like 'ID' may otherwise be insufficiently unique to have very useful suggestions.)
    """
    where_nots: Optional[List[Query]] = Field(default_factory=list)
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

        @classmethod
        def all(cls):
            return list(map(lambda c: c.value, cls))

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

    def finder(self, asset: Asset, client: Optional[AtlanClient] = None) -> Suggestions:
        """
        Build a suggestion finder against
        the provided Atlan tenant for the provided asset

        :param: client connectivity to an Atlan tenant
        :param: asset for which to find suggestions
        :return: the start of a suggestion finder
        for the provided asset, against the specified tenant
        """
        client = AtlanClient.get_default_client() if not client else client
        self.client = client
        self.asset = asset
        return self

    def get(self) -> SuggestionResponse:
        asset_name = ""
        all_types = []

        if self.asset and self.asset.name:
            asset_name = self.asset.name
            all_types.append(self.asset.type_name)

        # When other types provided by the user
        if self.with_other_types:
            all_types.extend(self.with_other_types)

        # Build fluent search
        search = (
            FluentSearch.select(include_archived=self.include_archived)
            .where(Asset.TYPE_NAME.within(all_types))
            .where(Asset.NAME.eq(asset_name))
            # We only care about the aggregations, not results
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

        for include in self.includes:
            if include == Suggestions.TYPE.SYSTEM_DESCRIPTION:
                search = search.where_some(Asset.DESCRIPTION.has_any_value()).aggregate(
                    Suggestions.AGG_DESCRIPTION,
                    Asset.DESCRIPTION.bucket_by(
                        size=self.max_suggestions, include_source_value=True
                    ),
                )
            elif include == Suggestions.TYPE.USER_DESCRIPTION:
                search = search.where_some(
                    Asset.USER_DESCRIPTION.has_any_value()
                ).aggregate(
                    Suggestions.AGG_USER_DESCRIPTION,
                    Asset.USER_DESCRIPTION.bucket_by(
                        size=self.max_suggestions, include_source_value=True
                    ),
                )
            elif include == Suggestions.TYPE.INDIVIDUAL_OWNERS:
                search = search.where_some(Asset.OWNER_USERS.has_any_value()).aggregate(
                    Suggestions.AGG_OWNER_USERS,
                    Asset.OWNER_USERS.bucket_by(self.max_suggestions),
                )
            elif include == Suggestions.TYPE.GROUP_OWNERS:
                search = search.where_some(
                    Asset.OWNER_GROUPS.has_any_value()
                ).aggregate(
                    Suggestions.AGG_OWNER_GROUPS,
                    Asset.OWNER_GROUPS.bucket_by(self.max_suggestions),
                )
            elif include == Suggestions.TYPE.TAGS:
                search = search.where_some(Asset.ATLAN_TAGS.has_any_value()).aggregate(
                    Suggestions.AGG_ATLAN_TAGS,
                    Asset.ATLAN_TAGS.bucket_by(self.max_suggestions),
                )
            elif include == Suggestions.TYPE.TERMS:
                search = search.where_some(
                    Asset.ASSIGNED_TERMS.has_any_value()
                ).aggregate(
                    Suggestions.AGG_TERMS,
                    Asset.ASSIGNED_TERMS.bucket_by(self.max_suggestions),
                )

            search_request = search.to_request()
            search_response = self.client.search(criteria=search_request)
            aggregations = search_response.aggregations
            suggestion_response = SuggestionResponse()

            for include in self.includes:
                self._build_response(include, suggestion_response, aggregations)
        return suggestion_response

    def _get_descriptions(self, result: Aggregations, field: AtlanField):
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

    def _get_tags(self, result: Aggregations):
        results = []
        if isinstance(result, AggregationBucketResult):
            for bucket in result.buckets:
                count = bucket.doc_count
                value = bucket.key
                name = AtlanTagCache.get_name_for_id(value)
                if count and name:
                    results.append(
                        SuggestionResponse.SuggestedItem(count=count, value=name)
                    )
        return results

    def _get_others(self, result: Aggregations):
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

    def _build_response(self, include, suggestion_response, aggregations):
        if include == Suggestions.TYPE.SYSTEM_DESCRIPTION:
            suggestion_response.system_descriptions.extend(
                self._get_descriptions(
                    aggregations.get(Suggestions.AGG_DESCRIPTION),
                    Asset.DESCRIPTION,
                )
            )
        elif include == Suggestions.TYPE.USER_DESCRIPTION:
            suggestion_response.user_descriptions.extend(
                self._get_descriptions(
                    aggregations.get(Suggestions.AGG_USER_DESCRIPTION),
                    Asset.USER_DESCRIPTION,
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
                self._get_tags(
                    aggregations.get(Suggestions.AGG_ATLAN_TAGS),
                )
            )
        elif include == Suggestions.TYPE.TERMS:
            suggestion_response.assigned_terms.extend(
                self._get_terms(
                    aggregations.get(Suggestions.AGG_TERMS),
                )
            )

    def apply(
        self, allow_multiple: bool = False, batch: Optional[Batch] = None
    ) -> Optional[AssetMutationResponse]:
        """
        Find the requested suggestions and apply the top suggestions as changes to the asset.

        Note: this will NOT validate whether there is any existing value for what
        you are setting, so will clobber any existing value with the suggestion.
        If you want to be certain you are only updating empty values, you should ensure
        you are only building a finder for suggestions for values that do not already
        exist on the asset in question.

        :param allow_multiple: if `True`, allow multiple suggestions to be applied
        to the asset (up to `max_suggestions` requested), i.e: for owners, terms and tags
        :param batch: (optional) the batch in which you want to apply the top suggestions as changes to the asset
        """
        if batch:
            return batch.add(self._apply(allow_multiple).asset)
        result = self._apply(allow_multiple)
        return self.client.save(result.asset, result.include_tags)

    def _apply(self, allow_multiple: bool):
        response = self.get()
        asset = self.asset.trim_to_required()  # type: ignore[union-attr]

        description_to_apply = self._get_description_to_apply(response)
        # NOTE: We only ever set the description over a
        # user-provided description (never the system-source description)
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
        max_description_count = 0
        description_to_apply = None

        # Check for suggested user descriptions
        if response.user_descriptions:
            max_description_count = response.user_descriptions[0].count
            description_to_apply = response.user_descriptions[0].value

        # If the count (frequency) of the suggested system description
        # is greater than the max_description_count (user description),
        # apply the suggested system description instead
        if response.system_descriptions:
            if response.system_descriptions[0].count > max_description_count:
                description_to_apply = response.system_descriptions[0].value

        return description_to_apply


class _Apply:
    asset: Asset
    include_tags: bool

    def __init__(self, asset: Asset, include_tags: bool):
        self.asset = asset
        self.include_tags = include_tags
