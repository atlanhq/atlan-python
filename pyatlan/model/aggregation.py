# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pydantic.v1 import Field, root_validator

from pyatlan.model.core import AtlanObject
from pyatlan.utils import validate_type

if TYPE_CHECKING:
    from pyatlan.model.fields.atlan_fields import AtlanField


class AggregationHitsResult(AtlanObject):
    "Captures the hit results from a bucket aggregation."

    class Stats(AtlanObject):
        value: Optional[int] = Field(default=None)
        """Number of search results that matched the hit value."""
        relation: Optional[str] = Field(default=None)
        """Comparison operation used to determine whether the values match."""

    class Details(AtlanObject):
        index: Optional[str] = Field(default=None, alias="_index")
        type: Optional[str] = Field(default=None, alias="_type")
        id: Optional[str] = Field(default=None, alias="_id")
        score: Optional[int] = Field(default=None, alias="_score")
        source: Optional[Dict[str, Any]] = Field(default=None, alias="_source")

    class Hits(AtlanObject):
        "Details of the hits requested."
        total: Optional[AggregationHitsResult.Stats] = Field(default=None)
        max_score: Optional[float] = Field(default=None)
        hits: List[AggregationHitsResult.Details] = Field(default_factory=list)

    hits: AggregationHitsResult.Hits


class AggregationMetricResult(AtlanObject):
    """Captures the results from a metric aggregation."""

    value: float


class AggregationBucketDetails(AtlanObject):
    """Captures the results of a single bucket within an aggregation."""

    key: Any
    doc_count: int
    key_as_string: Optional[str] = Field(default=None)
    max_matching_length: Optional[int] = Field(default=None)
    to: Optional[Any] = Field(default=None)
    to_as_string: Optional[str] = Field(default=None)
    from_: Optional[Any] = Field(default=None, alias="from")
    from_as_string: Optional[str] = Field(default=None)
    nested_results: Optional[Aggregations] = Field(default=None)

    @root_validator(pre=True)
    def populate_nested_results(cls, values):
        nested_results = {}
        for key, value in values.items():
            if isinstance(value, dict) and "buckets" in value:
                nested_results[key] = AggregationBucketResult(**value)
            elif isinstance(value, dict) and "hits" in value:
                nested_results[key] = AggregationHitsResult(**value)
        if nested_results:
            values["nested_results"] = Aggregations(__root__=nested_results)
        return values

    def get_source_value(self, field: AtlanField) -> Optional[str]:
        """
        Returns the source value of the specified field for this bucket.

        :param field: in Atlan for which to retrieve the value
        :returns: the value of the field in Atlan that
        is represented within this bucket otherwise `None`
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
                        # Need to handle the hashed-string ID
                        # stuff for custom metadata fields
                        return details.source.get(field.elastic_field_name)
                    else:
                        return details.source.get(field.atlan_field_name)
        return None


class AggregationBucketResult(AtlanObject):
    """Captures the results from a bucket aggregation."""

    doc_count_error_upper_bound: int
    sum_other_doc_count: int
    buckets: List[AggregationBucketDetails]


class Aggregation(AtlanObject):
    __root__: Dict[str, Any]


class Aggregations(AtlanObject):
    """Aggregation results from a search"""

    __root__: Dict[
        str,
        Union[AggregationMetricResult, AggregationBucketResult, AggregationHitsResult],
    ]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def get(
        self, key: str, default=None
    ) -> Optional[
        Union[AggregationMetricResult, AggregationBucketResult, AggregationHitsResult]
    ]:
        return self.__root__.get(key, default)


AggregationBucketDetails.update_forward_refs()
AggregationBucketResult.update_forward_refs()
AggregationHitsResult.Stats.update_forward_refs()
AggregationHitsResult.Details.update_forward_refs()
AggregationHitsResult.Hits.update_forward_refs()
AggregationHitsResult.update_forward_refs()
Aggregations.update_forward_refs()
