# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
from __future__ import annotations

from typing import Any, Dict, List, Union

from pyatlan.model.core import AtlanObject


class AggregationMetricResult(AtlanObject):
    """Captures the results from a metric aggregation."""

    value: float


class AggregationBucketDetails(AtlanObject):
    """Captures the results of a single bucket within an aggregation."""

    key: Any
    doc_count: int


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
