# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

import msgspec

from pyatlan.utils import validate_type

if TYPE_CHECKING:
    from pyatlan.model.fields.atlan_fields import AtlanField


class AggregationHitsResult(msgspec.Struct, kw_only=True):
    """Captures the hit results from a bucket aggregation."""

    class Stats(msgspec.Struct, kw_only=True):
        """Statistics about the hits."""

        value: Union[int, None] = None
        """Number of search results that matched the hit value."""
        relation: Union[str, None] = None
        """Comparison operation used to determine whether the values match."""

    class Details(msgspec.Struct, kw_only=True):
        """Details of an individual hit."""

        index: Union[str, None] = msgspec.field(default=None, name="_index")
        type: Union[str, None] = msgspec.field(default=None, name="_type")
        id: Union[str, None] = msgspec.field(default=None, name="_id")
        score: Union[int, None] = msgspec.field(default=None, name="_score")
        source: Union[dict[str, Any], None] = msgspec.field(
            default=None, name="_source"
        )

    class Hits(msgspec.Struct, kw_only=True):
        """Details of the hits requested."""

        total: Union[AggregationHitsResult.Stats, None] = None
        max_score: Union[float, None] = None
        hits: list[AggregationHitsResult.Details] = msgspec.field(default_factory=list)

    hits: AggregationHitsResult.Hits


class AggregationMetricResult(msgspec.Struct, kw_only=True):
    """Captures the results from a metric aggregation."""

    value: float


class AggregationBucketDetails(msgspec.Struct, kw_only=True):
    """Captures the results of a single bucket within an aggregation."""

    key: Any
    doc_count: int
    key_as_string: Union[str, None] = None
    max_matching_length: Union[int, None] = None
    to: Union[Any, None] = None
    to_as_string: Union[str, None] = None
    from_: Union[Any, None] = msgspec.field(default=None, name="from")
    from_as_string: Union[str, None] = None
    nested_results: Union[Aggregations, None] = None

    def __post_init__(self) -> None:
        """Populate nested results from extra fields in the raw data."""
        # Note: In msgspec, nested aggregation results need to be handled
        # during deserialization with a custom decoder hook.
        pass

    def get_source_value(self, field: AtlanField) -> Union[str, None]:
        """
        Returns the source value of the specified field for this bucket.

        :param field: in Atlan for which to retrieve the value
        :returns: the value of the field in Atlan that
        is represented within this bucket otherwise None
        """
        from pyatlan.model.fields.atlan_fields import (
            AtlanField,
            CustomMetadataField,
            SearchableField,
        )

        validate_type(name="field", _type=AtlanField, value=field)

        if (
            self.nested_results
            and SearchableField.EMBEDDED_SOURCE_VALUE in self.nested_results
        ):
            result = self.nested_results[SearchableField.EMBEDDED_SOURCE_VALUE]
            if (
                isinstance(result, AggregationHitsResult)
                and result.hits
                and result.hits.hits
            ):
                details = result.hits.hits[0]
                if details and details.source:
                    if isinstance(field, CustomMetadataField):
                        return details.source.get(field.elastic_field_name)
                    else:
                        return details.source.get(field.atlan_field_name)
        return None


class AggregationBucketResult(msgspec.Struct, kw_only=True):
    """Captures the results from a bucket aggregation."""

    doc_count_error_upper_bound: int
    sum_other_doc_count: int
    buckets: list[AggregationBucketDetails]


class Aggregation(msgspec.Struct, kw_only=True):
    """Single aggregation result."""

    data: dict[str, Any] = msgspec.field(default_factory=dict)


class Aggregations:
    """
    Aggregation results from a search.

    This is a dict-like wrapper around aggregation results that supports
    iteration and key-based access, replacing the Pydantic __root__ pattern.
    """

    def __init__(
        self,
        data: Union[
            dict[
                str,
                Union[
                    AggregationMetricResult,
                    AggregationBucketResult,
                    AggregationHitsResult,
                ],
            ],
            None,
        ] = None,
    ):
        self._data: dict[
            str,
            Union[
                AggregationMetricResult,
                AggregationBucketResult,
                AggregationHitsResult,
            ],
        ] = data or {}

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, item):
        return self._data[item]

    def __contains__(self, item):
        return item in self._data

    def get(
        self, key: str, default=None
    ) -> Union[
        AggregationMetricResult, AggregationBucketResult, AggregationHitsResult, None
    ]:
        """Get an aggregation result by key."""
        return self._data.get(key, default)
