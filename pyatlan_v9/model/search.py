# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/elastic/elasticsearch-dsl-py.git (under Apache-2.0 license)
from __future__ import annotations

import json as json_lib
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import msgspec

from pyatlan.model.enums import UTMTags

# ---------------------------------------------------------------------------
# Re-export all dataclass / ABC / Enum search classes from legacy.
# These are NOT Pydantic models — they're plain Python dataclasses and ABCs
# that don't need migration.  Importing them here keeps the
# `from pyatlan_v9.model.search import Term, Bool, ...` API stable.
# ---------------------------------------------------------------------------
from pyatlan.model.search import (  # noqa: F401
    Attributes,
    Bool,
    Exists,
    Fuzzy,
    Match,
    MatchAll,
    MatchNone,
    MatchPhrase,
    NestedQuery,
    Prefix,
    Query,
    Range,
    Regexp,
    SearchFieldType,
    SortItem,
    Span,
    SpanNear,
    SpanOr,
    SpanTerm,
    SpanWithin,
    Term,
    TermAttributes,
    Terms,
    TextAttributes,
    Wildcard,
    get_with_string,
)
from pyatlan_v9.model.aggregation import Aggregation


# ---------------------------------------------------------------------------
# v9-only helpers
# ---------------------------------------------------------------------------

def _serialize_value(v: Any) -> Any:
    """Recursively serialize a value to JSON-compatible types."""
    if v is None:
        return None
    if hasattr(v, "to_dict") and callable(v.to_dict):
        return v.to_dict()
    if isinstance(v, dict):
        return {k: _serialize_value(val) for k, val in v.items()}
    if isinstance(v, list):
        return [_serialize_value(item) for item in v]
    if isinstance(v, Enum):
        return v.value
    return v


# ---------------------------------------------------------------------------
# msgspec.Struct models — these are the genuine Pydantic→msgspec migrations
# ---------------------------------------------------------------------------

class DSL(msgspec.Struct, kw_only=True):
    from_: int = msgspec.field(default=0, name="from")
    size: int = 300
    aggregations: Dict[str, Aggregation] = msgspec.field(default_factory=dict)
    track_total_hits: Optional[bool] = True
    post_filter: Optional[Union[Dict[str, Any], Query]] = None
    query: Optional[Union[Dict[str, Any], Query]] = None
    req_class_name: Optional[str] = None
    sort: List[SortItem] = msgspec.field(default_factory=list)

    def __post_init__(self):
        # Validate that either query or post_filter is provided
        if not self.query and not self.post_filter:
            raise ValueError("Either query or post_filter is required")

        # Convert dict entries to SortItem instances
        if self.sort and all(isinstance(item, dict) for item in self.sort):
            self.sort = [SortItem.from_dict(item) for item in self.sort]  # type: ignore[arg-type]

        # Ensure sort includes GUID sort
        missing_guid_sort = True
        sort_by_guid = "__guid"
        auditsearch_sort_by_guid = "entityId"
        searchlog_sort_by_guid = "entityGuidsAll"
        for option in self.sort:
            if option.field and option.field in (
                sort_by_guid,
                auditsearch_sort_by_guid,
                searchlog_sort_by_guid,
            ):
                missing_guid_sort = False
                break
        if missing_guid_sort:
            if self.req_class_name == "SearchLogRequest":
                self.sort.append(SortItem(searchlog_sort_by_guid))
            elif self.req_class_name == "AuditSearchRequest":
                self.sort.append(SortItem(auditsearch_sort_by_guid))
            elif self.req_class_name == "IndexSearchRequest":
                self.sort.append(SortItem(sort_by_guid))

    def json(
        self,
        by_alias: bool = False,
        exclude_none: bool = False,
        exclude_unset: bool = False,
    ) -> str:
        """Serialize DSL to JSON string, matching legacy Pydantic output format."""
        d: Dict[str, Any] = {}
        d["from" if by_alias else "from_"] = self.from_
        d["size"] = self.size
        d["aggregations"] = _serialize_value(self.aggregations)
        d["track_total_hits"] = self.track_total_hits
        d["post_filter"] = _serialize_value(self.post_filter)
        d["query"] = _serialize_value(self.query)
        d["sort"] = _serialize_value(self.sort)
        if exclude_none:
            d = {k: v for k, v in d.items() if v is not None}
        return json_lib.dumps(d)


class IndexSearchRequestMetadata(msgspec.Struct, kw_only=True):
    save_search_log: bool = False
    utm_tags: List[str] = msgspec.field(default_factory=list)

    def to_dict(self, by_alias: bool = True) -> Dict[str, Any]:
        """Convert to dict with camelCase keys when by_alias=True."""
        if by_alias:
            return {
                "saveSearchLog": self.save_search_log,
                "utmTags": self.utm_tags,
            }
        return {
            "save_search_log": self.save_search_log,
            "utm_tags": self.utm_tags,
        }


class IndexSearchRequest(msgspec.Struct, kw_only=True):
    dsl: DSL
    attributes: Optional[List[str]] = msgspec.field(default_factory=list)
    relation_attributes: Optional[List[str]] = msgspec.field(
        default_factory=list, name="relationAttributes"
    )
    suppress_logs: Optional[bool] = msgspec.field(default=None, name="suppressLogs")
    show_search_score: Optional[bool] = msgspec.field(
        default=None, name="showSearchScore"
    )
    exclude_meanings: Optional[bool] = msgspec.field(
        default=None, name="excludeMeanings"
    )
    exclude_atlan_tags: Optional[bool] = msgspec.field(
        default=None, name="excludeClassifications"
    )
    allow_deleted_relations: Optional[bool] = msgspec.field(
        default=None, name="allowDeletedRelations"
    )
    include_atlan_tag_names: Optional[bool] = msgspec.field(
        default=None, name="includeClassificationNames"
    )
    persona: Optional[str] = None
    purpose: Optional[str] = None
    include_relationship_attributes: Optional[bool] = False
    enable_full_restriction: Optional[bool] = msgspec.field(
        default=None, name="enableFullRestriction"
    )
    request_metadata: Optional[IndexSearchRequestMetadata] = None

    def __post_init__(self):
        # Ensure DSL has the correct req_class_name
        class_name = self.__class__.__name__
        if self.dsl and isinstance(self.dsl, DSL) and not self.dsl.req_class_name:
            self.dsl = DSL(
                req_class_name=class_name,
                from_=self.dsl.from_,
                size=self.dsl.size,
                aggregations=self.dsl.aggregations,
                track_total_hits=self.dsl.track_total_hits,
                post_filter=self.dsl.post_filter,
                query=self.dsl.query,
                sort=self.dsl.sort,
            )

        # Set default request_metadata
        if self.request_metadata is None:
            self.request_metadata = IndexSearchRequestMetadata(
                save_search_log=False,
                utm_tags=[UTMTags.PROJECT_SDK_PYTHON],
            )

    def json(
        self,
        by_alias: bool = False,
        exclude_none: bool = False,
        exclude_unset: bool = False,
    ) -> str:
        """Serialize IndexSearchRequest to JSON string, matching legacy Pydantic output format."""
        # Build dict in field-declaration order with alias mapping
        _ALIAS_MAP = {
            "attributes": "attributes",
            "dsl": "dsl",
            "relation_attributes": "relationAttributes",
            "suppress_logs": "suppressLogs",
            "show_search_score": "showSearchScore",
            "exclude_meanings": "excludeMeanings",
            "exclude_atlan_tags": "excludeClassifications",
            "allow_deleted_relations": "allowDeletedRelations",
            "include_atlan_tag_names": "includeClassificationNames",
            "persona": "persona",
            "purpose": "purpose",
            "include_relationship_attributes": "includeRelationshipAttributes",
            "enable_full_restriction": "enableFullRestriction",
            "request_metadata": "requestMetadata",
        }
        d: Dict[str, Any] = {}
        for field_name, alias in _ALIAS_MAP.items():
            val = getattr(self, field_name, None)
            key = alias if by_alias else field_name
            if field_name == "dsl" and val is not None:
                val = json_lib.loads(
                    val.json(by_alias=by_alias, exclude_none=exclude_none)
                )
            elif field_name == "request_metadata" and val is not None:
                val = val.to_dict(by_alias=by_alias)
            else:
                val = _serialize_value(val)
            d[key] = val
        if exclude_none:
            d = {k: v for k, v in d.items() if v is not None}
        return json_lib.dumps(d)


# ---------------------------------------------------------------------------
# v9-specific with_active_* helpers (use our own validation, not Pydantic's)
# ---------------------------------------------------------------------------

def _validate_name(name: str) -> None:
    """Validate that name is a non-None, non-blank string."""
    if name is None:
        raise ValueError("name must not be None")
    if not name.strip():
        raise ValueError("name must have at least 1 non-whitespace character")


def _validate_glossary_qualified_name(qualified_name: str) -> None:
    """Validate that glossary qualified_name is a non-None, non-blank string."""
    if qualified_name is None:
        raise ValueError("glossary_qualified_name must not be None")
    if not qualified_name.strip():
        raise ValueError(
            "glossary_qualified_name must have at least 1 non-whitespace character"
        )


def with_active_glossary(name: str) -> Bool:
    """Return a Bool query matching an active glossary by name."""
    _validate_name(name)
    return (
        Term.with_state("ACTIVE")
        + Term.with_type_name("AtlasGlossary")
        + Term.with_name(name)
    )


def with_active_category(name: str, glossary_qualified_name: str) -> Bool:
    """Return a Bool query matching an active glossary category by name and glossary."""
    _validate_name(name)
    _validate_glossary_qualified_name(glossary_qualified_name)
    return (
        Term.with_state("ACTIVE")
        + Term.with_type_name("AtlasGlossaryCategory")
        + Term.with_name(name)
        + Term.with_glossary(glossary_qualified_name)
    )


def with_active_term(name: str, glossary_qualified_name: str) -> Bool:
    """Return a Bool query matching an active glossary term by name and glossary."""
    _validate_name(name)
    _validate_glossary_qualified_name(glossary_qualified_name)
    return (
        Term.with_state("ACTIVE")
        + Term.with_type_name("AtlasGlossaryTerm")
        + Term.with_name(name)
        + Term.with_glossary(glossary_qualified_name)
    )
