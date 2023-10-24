# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import copy
from collections import deque
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional, Union, overload

from pydantic import Field

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.dataclasses import dataclass

from datetime import date

from pyatlan.errors import ErrorCode
from pyatlan.model.assets import Asset
from pyatlan.model.core import AtlanObject, SearchRequest
from pyatlan.model.enums import AtlanComparisonOperator, LineageDirection
from pyatlan.model.fields.atlan_fields import CustomMetadataField, SearchableField
from pyatlan.utils import ComparisonCategory, is_comparable_type


class LineageRelation(AtlanObject):
    from_entity_id: Optional[str]
    to_entity_id: Optional[str]
    process_id: Optional[str]
    relationship_id: Optional[str]

    @property
    def is_full_link(self):
        return self.process_id is not None


@dataclass(frozen=True)
class DirectedPair:
    process_guid: str
    target_guid: str


@dataclass(frozen=True)
class LineageGraph:
    downstream_list: dict[str, dict[DirectedPair, None]]
    upstream_list: dict[str, dict[DirectedPair, None]]

    @classmethod
    def create(cls, relations: list[LineageRelation]) -> "LineageGraph":
        downstream_list: dict[str, dict[DirectedPair, None]] = {}
        upstream_list: dict[str, dict[DirectedPair, None]] = {}

        def add_relation(relation: LineageRelation):
            if (
                relation.from_entity_id
                and relation.process_id
                and relation.to_entity_id
            ):
                add_edges(
                    relation.from_entity_id, relation.process_id, relation.to_entity_id
                )

        def add_edges(source_guid: str, process_guid: str, target_guid: str):
            if source_guid not in downstream_list:
                downstream_list[source_guid] = {}
            if target_guid not in upstream_list:
                upstream_list[target_guid] = {}
            downstream_list[source_guid][
                DirectedPair(process_guid=process_guid, target_guid=target_guid)
            ] = None
            upstream_list[target_guid][
                DirectedPair(process_guid=process_guid, target_guid=source_guid)
            ] = None

        for relation in relations:
            if relation.is_full_link:
                add_relation(relation)
            else:
                raise ErrorCode.NO_GRAPH_WITH_PROCESS.exception_with_parameters()
        return cls(downstream_list=downstream_list, upstream_list=upstream_list)

    @staticmethod
    def get_asset_guids(
        guid: str, guids: dict[str, dict[DirectedPair, None]]
    ) -> list[str]:
        if guid in guids:
            return list({pair.target_guid: None for pair in guids[guid].keys()}.keys())
        return []

    @staticmethod
    def get_process_guids(
        guid: str, guids: dict[str, dict[DirectedPair, None]]
    ) -> list[str]:
        if guid in guids:
            return list({pair.process_guid: None for pair in guids[guid].keys()}.keys())
        return []

    def get_downstream_asset_guids(self, guid: str) -> list[str]:
        return LineageGraph.get_asset_guids(guid, self.downstream_list)

    def get_downstream_process_guids(self, guid: str) -> list[str]:
        return LineageGraph.get_process_guids(guid, self.downstream_list)

    def get_upstream_asset_guids(self, guid: str) -> list[str]:
        return LineageGraph.get_asset_guids(guid, self.upstream_list)

    def get_upstream_process_guids(self, guid: str) -> list[str]:
        return LineageGraph.get_process_guids(guid, self.upstream_list)

    def get_all_downstream_asset_guids_dfs(self, guid: str) -> list[str]:
        visited: dict[str, None] = {}
        stack: deque[str] = deque()
        stack.append(guid)
        while len(stack) > 0:
            to_traverse = stack.pop()
            if to_traverse not in visited:
                visited[to_traverse] = None
                for downstream_guid in self.get_downstream_asset_guids(to_traverse):
                    if downstream_guid not in visited:
                        stack.append(downstream_guid)
        return list(visited.keys())

    def get_all_upstream_asset_guids_dfs(self, guid: str) -> list[str]:
        visited: dict[str, None] = {}
        stack: deque[str] = deque()
        stack.append(guid)
        while len(stack) > 0:
            to_traverse = stack.pop()
            if to_traverse not in visited:
                visited[to_traverse] = None
                for upstream_guid in self.get_upstream_asset_guids(to_traverse):
                    if upstream_guid not in visited:
                        stack.append(upstream_guid)
        return list(visited.keys())


class LineageResponse(AtlanObject):
    base_entity_guid: str
    lineage_direction: LineageDirection
    lineage_depth: int
    limit: int
    offset: int
    has_more_upstream_vertices: bool
    has_more_downstream_vertices: bool
    guid_entity_map: dict[str, Asset]
    relations: list[LineageRelation]
    vertex_children_info: Optional[dict[str, Any]]
    graph: Optional[LineageGraph] = None

    def get_graph(self):
        if self.graph is None:
            self.graph = LineageGraph.create(self.relations)
        return self.graph

    def get_all_downstream_asset_guids_dfs(
        self, guid: Optional[str] = None
    ) -> list[str]:
        return self.get_graph().get_all_downstream_asset_guids_dfs(
            guid if guid else self.base_entity_guid
        )

    def get_all_downstream_assets_dfs(self, guid: Optional[str] = None) -> list[Asset]:
        return [
            self.guid_entity_map[guid]
            for guid in self.get_graph().get_all_downstream_asset_guids_dfs(
                guid if guid else self.base_entity_guid
            )
        ]

    def get_all_upstream_asset_guids_dfs(self, guid: Optional[str] = None) -> list[str]:
        return self.get_graph().get_all_upstream_asset_guids_dfs(
            guid if guid else self.base_entity_guid
        )

    def get_all_upstream_assets_dfs(self, guid: Optional[str] = None) -> list[Asset]:
        return [
            self.guid_entity_map[guid]
            for guid in self.get_graph().get_all_upstream_asset_guids_dfs(
                guid if guid else self.base_entity_guid
            )
        ]

    def get_downstream_asset_guids(self, guid: Optional[str] = None) -> list[str]:
        return self.get_graph().get_downstream_asset_guids(
            guid if guid else self.base_entity_guid
        )

    def get_downstream_assets(self, guid: Optional[str] = None) -> list[Asset]:
        return [
            self.guid_entity_map[guid]
            for guid in self.get_graph().get_downstream_asset_guids(
                guid if guid else self.base_entity_guid
            )
        ]

    def get_downstream_process_guids(self, guid: Optional[str] = None) -> list[str]:
        return self.get_graph().get_downstream_process_guids(
            guid if guid else self.base_entity_guid
        )

    def get_upstream_asset_guids(self, guid: Optional[str] = None) -> list[str]:
        return self.get_graph().get_upstream_asset_guids(
            guid if guid else self.base_entity_guid
        )

    def get_upstream_assets(self, guid: Optional[str] = None) -> list[Asset]:
        return [
            self.guid_entity_map[guid]
            for guid in self.get_graph().get_upstream_asset_guids(
                guid if guid else self.base_entity_guid
            )
        ]

    def get_upstream_process_guids(self, guid: Optional[str] = None) -> list[str]:
        return self.get_graph().get_upstream_process_guids(
            guid if guid else self.base_entity_guid
        )


class LineageRequest(AtlanObject):
    guid: str
    depth: int = Field(default=0)
    direction: LineageDirection = Field(default=LineageDirection.BOTH)
    hide_process: bool = Field(default=True)
    allow_deleted_process: bool = Field(default=False)


class EntityFilter(AtlanObject):
    attribute_name: str = Field(
        description="Name of the attribute on which filtering should be applied."
    )
    operator: AtlanComparisonOperator = Field(
        description="Comparison that should be used when checking attribute_name"
        " against the provided attribute_value."
    )
    attribute_value: str = Field(
        description="Value that attribute_name should be compared against."
    )


class FilterList(AtlanObject):
    condition: str = Field(
        description="Whether the criteria must all match (AND) or any matching is sufficient (OR)."
    )
    criteria: list[EntityFilter] = Field(
        description="Basis on which to compare a result for inclusion.",
        alias="criterion",
    )


class LineageListRequest(SearchRequest):
    guid: str = Field(
        description="Unique identifier of the asset for which to retrieve lineage."
    )
    depth: int = Field(
        description="Number of degrees of separation (hops) across which lineage should be fetched."
        "A depth of 1 will fetch the immediate upstream or downstream assets, while 2"
        "will also fetch the immediate upstream or downstream assets of those assets,"
        "and so on. A large integer (for example, 1000000) will therefore in effect fetch"
        "all upstream or downstream assets. (BEWARE! This could take a long time and"
        "result in a very large response payload.)"
    )
    direction: LineageDirection = Field(
        description="Indicates whether to fetch upstream lineage only, or downstream lineage only. "
        "Note that you cannot fetch both upstream and downstream at the same time."
    )
    entity_filters: Optional[FilterList] = Field(
        description="Filters to apply on entities."
    )
    entity_traversal_filters: Optional[FilterList] = Field(
        description="Filters to apply for skipping traversal based on entities."
        "Any sub-graphs beyond the entities filtered out by these filters will not be included"
        "in the lineage result."
    )
    relationship_traversal_filters: Optional[FilterList] = Field(
        description="Filters to apply for skipping traversal based on relationships."
        "Any sub-graphs beyond the relationships filtered out by these filters will not be included"
        "in the lineage result."
    )
    offset: Optional[int] = Field(
        description="Starting point for pagination.", alias="from"
    )
    size: Optional[int] = Field(
        description="How many results to include in each page of results."
    )
    exclude_meanings: Optional[bool] = Field(
        description="Whether to include assigned terms for assets (false) or not (true)."
    )
    exclude_classifications: Optional[bool] = Field(
        description="Whether to include classifications for assets (false) or not (true)."
    )

    @staticmethod
    def create(
        guid: str,
    ) -> "LineageListRequest":
        from pyatlan.utils import validate_required_fields

        validate_required_fields(
            ["guid"],
            [guid],
        )
        return LineageListRequest(
            guid=guid,
            depth=1000000,
            direction=LineageDirection.DOWNSTREAM,
            offset=0,
            size=10,
            exclude_meanings=True,
            exclude_classifications=True,
        )


class LineageFilter(AtlanObject):
    """Class used to define how to filter assets and relationships when fetching lineage"""

    field: SearchableField
    operator: AtlanComparisonOperator
    value: str

    class Config:
        arbitrary_types_allowed = True


class LineageFilterField:
    """Class used to provide a proxy to building up a lineage filter with the appropriate
    subset of conditions available."""

    def __init__(self, field: SearchableField):
        """Create LineageFilterField

        :param field: Field on which filtering should be applied.
        """
        self._field = field

    @property
    def field(self) -> SearchableField:
        return self._field

    def has_any_value(self) -> LineageFilter:
        """
        Returns a filter that will match all assets whose provided field has any value at all (non-null).

        :returns:  a filter that will match all assets whose provided field has any value at all (non-null).
        """
        return LineageFilter(
            field=self._field, operator=AtlanComparisonOperator.NOT_NULL, value=""
        )

    def has_no_value(self) -> LineageFilter:
        """
        Returns a filter that will match all assets whose provided field has no value at all (is null).

        :returns:  a filter that will only match assets that have no value at all for the field (null).
        """
        return LineageFilter(
            field=self._field, operator=AtlanComparisonOperator.IS_NULL, value=""
        )


class LineageFilterFieldBoolean(LineageFilterField):
    """Class used to provide a proxy to building up a lineage filter with the appropriate
    subset of conditions available, for boolean fields."""

    def eq(self, value: bool) -> LineageFilter:
        """
        Returns a filter that will match all assets whose provided field has a value that is exactly
         the provided value.

        :param value: the value to check the field's value equals
        :returns:  a filter that will only match assets whose value for the field is exactly the value provided
        """
        return LineageFilter(
            field=self._field, operator=AtlanComparisonOperator.EQ, value=str(value)
        )

    def neq(self, value: bool) -> LineageFilter:
        """
        Returns a filter that will match all assets whose provided field has a value that is not exactly
         the provided value.

        :param value: the value to check the field's value does not equal
        :returns:  a filter that will only match assets whose value for the field is not exactly the value provided
        """
        return LineageFilter(
            field=self._field, operator=AtlanComparisonOperator.NEQ, value=str(value)
        )


class LineageFilterFieldCM(LineageFilterField):
    """Class used to provide a proxy to building up a lineage filter with the appropriate
    subset of conditions available, for custom metadata fields."""

    def __init__(self, field: CustomMetadataField):
        """Create LineageFilterFieldCM

        :param field: Field on which filtering should be applied.
        """
        super().__init__(field)
        self._cm_field = field

    @property
    def cm_field(self) -> CustomMetadataField:
        return self._cm_field

    @overload
    def eq(self, value: str) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is exactly
        the provided value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""

    @overload
    def eq(self, value: Enum) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is exactly
        the provided value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""

    def eq(self, value: Union[str, Enum]):
        if isinstance(value, Enum):
            return LineageFilter(
                field=self._field,
                operator=AtlanComparisonOperator.EQ,
                value=value.value,
            )
        if isinstance(value, str):
            return LineageFilter(
                field=self._field, operator=AtlanComparisonOperator.EQ, value=value
            )
        raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
            type(value).__name__, "str or Enum"
        )

    @overload
    def neq(self, value: str) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is not exactly
        the provided value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value does not equal (case-sensitive)
        """

    @overload
    def neq(self, value: Enum) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is not exactly
        the provided value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value does not equal (case-sensitive)
        """

    def neq(self, value: Union[str, Enum]):
        if isinstance(value, Enum):
            return LineageFilter(
                field=self._field,
                operator=AtlanComparisonOperator.NEQ,
                value=value.value,
            )
        if isinstance(value, str):
            return LineageFilter(
                field=self._field, operator=AtlanComparisonOperator.NEQ, value=value
            )
        raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
            type(value).__name__, "str or Enum"
        )

    def starts_with(self, value: str) -> LineageFilter:
        """ "Returns a filter that will match all assets whose provided field has a value that starts with
        the provided value. Note that this is a case-sensitive match.

        :param value: the value (prefix) to check the field's value starts with (case-sensitive)
        :return: a filter that will only match assets whose value for the field starts with the value provided
        """
        return self._with_string_comparison(
            value=value, comparison_operator=AtlanComparisonOperator.STARTS_WITH
        )
        if not isinstance(value, str):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                type(value).__name__, "str"
            )

    def ends_with(self, value: str) -> LineageFilter:
        """ "Returns a filter that will match all assets whose provided field has a value that ends with
        the provided value. Note that this is a case-sensitive match.

        :param value: the value (suffix) to check the field's value starts with (case-sensitive)
        :return: a filter that will only match assets whose value for the field ends with the value provided
        """
        return self._with_string_comparison(
            value=value, comparison_operator=AtlanComparisonOperator.ENDS_WITH
        )
        if not isinstance(value, str):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                type(value).__name__, "str"
            )

    def contains(self, value: str) -> LineageFilter:
        """ "Returns a filter that will match all assets whose provided field has a value that contains
        the provided value. Note that this is a case-sensitive match.

        :param value: the value (suffix) to check the field's value contains (case-sensitive)
        :return: a filter that will only match assets whose value for the field contains the value provided
        """
        return self._with_string_comparison(
            value=value, comparison_operator=AtlanComparisonOperator.CONTAINS
        )
        if not isinstance(value, str):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                type(value).__name__, "str"
            )

    def does_not_contain(self, value: str) -> LineageFilter:
        """ "Returns a filter that will match all assets whose provided field has a value that does not contain
        the provided value. Note that this is a case-sensitive match.

        :param value: the value (suffix) to check the field's value does not contain (case-sensitive)
        :return: a filter that will only match assets whose value for the field does not contain the value provided
        """
        return self._with_string_comparison(
            value=value, comparison_operator=AtlanComparisonOperator.NOT_CONTAINS
        )
        if not isinstance(value, str):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                type(value).__name__, "str"
            )

    @overload
    def lt(self, value: int) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than
        the provided value.

        :param value: the value to check the field's value is strictly less than
        :return value: a filter that will only match assets whose value for the field is strictly less than the value
        provided
        """

    @overload
    def lt(self, value: float) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than
        the provided value.

        :param value: the value to check the field's value is strictly less than
        :return value: a filter that will only match assets whose value for the field is strictly less than the value
        provided
        """

    @overload
    def lt(self, value: date) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than
        the provided value.

        :param value: the value to check the field's value is strictly less than
        :return value: a filter that will only match assets whose value for the field is strictly less than the value
        provided
        """

    def lt(self, value: Union[int, float, date]) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than
        the provided value.

        :param value: the value to check the field's value is strictly less than
        :return value: a filter that will only match assets whose value for the field is strictly less than the value
        provided
        """
        return self._with_numeric_comparison(
            value=value, comparison_operator=AtlanComparisonOperator.LT
        )

    @overload
    def gt(self, value: int) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than
        the provided value.

        :param value: the value to check the field's value is strictly less than
        :return value: a filter that will only match assets whose value for the field is strictly less than the value
        provided
        """

    @overload
    def gt(self, value: float) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly greater than
        the provided value.

        :param value: the value to check the field's value is strictly less than
        :return value: a filter that will only match assets whose value for the field is strictly greater than the value
         provided
        """

    @overload
    def gt(self, value: date) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly greater than
        the provided value.

        :param value: the value to check the field's value is strictly greater than
        :return value: a filter that will only match assets whose value for the field is strictly greater than the value
         provided
        """

    def gt(self, value: Union[int, float, date]) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than
        the provided value.

        :param value: the value to check the field's value is strictly greater than
        :return value: a filter that will only match assets whose value for the field is strictly greater than the
        value provided
        """
        return self._with_numeric_comparison(
            value=value, comparison_operator=AtlanComparisonOperator.GT
        )

    def _with_numeric_comparison(
        self,
        value: Union[int, float, date],
        comparison_operator: AtlanComparisonOperator,
    ):
        if isinstance(
            value,
            bool,  # needed because isinstance(value, int) evaluates to true when value is bool
        ) or (
            not isinstance(value, int)
            and not isinstance(value, float)
            and not isinstance(value, date)
        ):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                type(value).__name__, "int, float or date"
            )
        if not is_comparable_type(
            self._cm_field.attribute_def.type_name or "", ComparisonCategory.NUMBER
        ):
            raise ErrorCode.INVALID_QUERY.exception_with_parameters(
                comparison_operator,
                f"{self._cm_field.set_name}.{self._cm_field.attribute_name}",
            )
        return LineageFilter(
            field=self._field, operator=comparison_operator, value=str(value)
        )

    def _with_string_comparison(
        self, value: str, comparison_operator: AtlanComparisonOperator
    ):
        if not isinstance(value, str):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                type(value).__name__, "str"
            )
        if not is_comparable_type(
            self._cm_field.attribute_def.type_name or "", ComparisonCategory.STRING
        ):
            raise ErrorCode.INVALID_QUERY.exception_with_parameters(
                comparison_operator,
                f"{self._cm_field.set_name}.{self._cm_field.attribute_name}",
            )
        return LineageFilter(
            field=self._field, operator=comparison_operator, value=value
        )


class FluentLineage:
    """Lineage abstraction mechanism, to simplify the most common lineage requests against Atlan
    (removing the need to understand the guts of Elastic)."""

    def __init__(
        self,
        starting_guid: str,
        depth: int = 1000000,
        direction: LineageDirection = LineageDirection.DOWNSTREAM,
        size: int = 10,
        exclude_meanings: bool = True,
        exclude_classifications: bool = True,
    ):
        self._starting_guid = starting_guid
        self._depth: int = depth
        self._direction: LineageDirection = direction
        self._size: int = size
        self._exclude_meanings: bool = exclude_meanings
        self._exclude_classifications: bool = exclude_classifications
        self._include_in_results: list[LineageFilter] = []

    def _clone(self) -> "FluentLineage":
        """
        Returns a copy of the current FluentSearch that's ready for further operations.

        :returns: copy of the current FluentSearch
        """
        return copy.deepcopy(self)

    def include_in_results(self, lineage_filter: LineageFilter):
        clone = self._clone()
        clone._include_in_results.append(lineage_filter)
        return clone
