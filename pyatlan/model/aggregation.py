# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
from __future__ import annotations

from typing import Any, Optional, Union

from pydantic import Field

from pyatlan.model.core import AtlanObject


class AggregationMetricResult(AtlanObject):
    """Captures the results from a metric aggregation."""

    value: float


class Stats(AtlanObject):
    value: int
    relation: str


class Details(AtlanObject):
    index: str = Field(alias="_index")
    type_: str = Field(alias="_type")
    id_: str = Field(alias="_id")
    score: str = Field(alias="_score")
    source: Optional[dict[str, Any]] = Field(alias="_source")


class Hits(AtlanObject):
    total: Stats
    max_score: float
    hits: list[Details]


class AggregationHitsResult(AtlanObject):
    """Captures the results from a bucket aggregation."""

    hits: Optional[Hits]


class AggregationBucketDetails(AtlanObject):
    """Captures the results of a single bucket within an aggregation."""

    key: Any
    doc_count: int
    max_matching_length: Optional[int]
    to: Optional[Any]
    source_value: Optional[AggregationHitsResult]


class AggregationBucketResult(AtlanObject):
    """Captures the results from a bucket aggregation."""

    doc_count_error_upper_bound: int
    sum_other_doc_count: int
    buckets: list[AggregationBucketDetails]


class Aggregation(AtlanObject):
    __root__: dict[str, Any]


class Aggregations(AtlanObject):
    __root__: dict[str, Union[AggregationMetricResult, AggregationBucketResult]]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]
