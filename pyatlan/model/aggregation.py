# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from pydantic.v1 import Field, root_validator

from pyatlan.model.core import AtlanObject


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
    nested_aggregations: Optional[Aggregations] = Field(default=None)

    @root_validator(pre=True)
    def populate_nested_aggs(cls, values):
        nested_aggregations = {}
        for key, value in values.items():
            if isinstance(value, dict) and "buckets" in value:
                nested_aggregations[key] = AggregationBucketResult(**value)
        if nested_aggregations:
            values["nested_aggregations"] = Aggregations(__root__=nested_aggregations)
        return values


class AggregationBucketResult(AtlanObject):
    """Captures the results from a bucket aggregation."""

    doc_count_error_upper_bound: int
    sum_other_doc_count: int
    buckets: List[AggregationBucketDetails]


class Aggregation(AtlanObject):
    __root__: Dict[str, Any]


class Aggregations(AtlanObject):
    """Aggregation results from a search"""

    __root__: Dict[str, Union[AggregationMetricResult, AggregationBucketResult]]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


AggregationBucketDetails.update_forward_refs()
AggregationBucketResult.update_forward_refs()
Aggregations.update_forward_refs()
