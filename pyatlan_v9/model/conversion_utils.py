# Auto-generated support module for PythonMsgspecRenderer.pkl
"""Conversion utilities for relationship attribute handling."""

from __future__ import annotations

from typing import Any, Type, TypeVar

import msgspec
from msgspec import UNSET, UnsetType

from pyatlan_v9.model.assets.related_entity import SaveSemantic

T = TypeVar("T")


def categorize_relationships(
    entity: Any, rel_fields: list[str], rel_attrs_class: Type[T]
) -> tuple[T | UnsetType, T | UnsetType, T | UnsetType]:
    """
    Categorize relationship attributes by their SaveSemantic.

    Examines each relationship field on the entity and routes values to the
    appropriate bucket (replace, append, remove) based on the SaveSemantic
    marker on each related entity.

    Args:
        entity: The entity containing relationship attributes
        rel_fields: List of relationship field names
        rel_attrs_class: The RelationshipAttributes class to instantiate

    Returns:
        Tuple of (replace_rels, append_rels, remove_rels) as class instances,
        or UNSET for empty buckets
    """
    replace_kwargs: dict[str, Any] = {}
    append_kwargs: dict[str, Any] = {}
    remove_kwargs: dict[str, Any] = {}

    for field_name in rel_fields:
        value = getattr(entity, field_name, UNSET)
        if value is UNSET or value is None:
            continue

        # Handle list of related entities
        if isinstance(value, list):
            if len(value) == 0:
                # Empty list means "replace with nothing" (clear the relationship)
                replace_kwargs[field_name] = []
            for item in value:
                semantic = getattr(item, "semantic", UNSET)
                if semantic is UNSET or semantic == SaveSemantic.REPLACE:
                    if field_name not in replace_kwargs:
                        replace_kwargs[field_name] = []
                    replace_kwargs[field_name].append(item)
                elif semantic == SaveSemantic.APPEND:
                    if field_name not in append_kwargs:
                        append_kwargs[field_name] = []
                    append_kwargs[field_name].append(item)
                elif semantic == SaveSemantic.REMOVE:
                    if field_name not in remove_kwargs:
                        remove_kwargs[field_name] = []
                    remove_kwargs[field_name].append(item)
        else:
            # Single related entity
            semantic = getattr(value, "semantic", UNSET)
            if semantic is UNSET or semantic == SaveSemantic.REPLACE:
                replace_kwargs[field_name] = value
            elif semantic == SaveSemantic.APPEND:
                append_kwargs[field_name] = value
            elif semantic == SaveSemantic.REMOVE:
                remove_kwargs[field_name] = value

    replace_rels = rel_attrs_class(**replace_kwargs) if replace_kwargs else UNSET
    append_rels = rel_attrs_class(**append_kwargs) if append_kwargs else UNSET
    remove_rels = rel_attrs_class(**remove_kwargs) if remove_kwargs else UNSET

    return replace_rels, append_rels, remove_rels


def merge_relationships(
    replace_rels: Any,
    append_rels: Any,
    remove_rels: Any,
    rel_fields: list[str],
    rel_attrs_class: Type[T],
) -> dict[str, Any]:
    """
    Merge relationship attributes from all three buckets back into a flat dict.

    Used when converting from nested API format back to flat entity format.
    Values are merged with replace taking priority, then append, then remove.

    Args:
        replace_rels: RelationshipAttributes for replace semantic
        append_rels: RelationshipAttributes for append semantic
        remove_rels: RelationshipAttributes for remove semantic
        rel_fields: List of relationship field names
        rel_attrs_class: The RelationshipAttributes class (unused, for type info)

    Returns:
        Dict of merged relationship attributes
    """
    result: dict[str, Any] = {}

    # Merge in order of priority: replace, then append, then remove
    for source in [replace_rels, append_rels, remove_rels]:
        if source is UNSET or source is None:
            continue
        for field_name in rel_fields:
            value = getattr(source, field_name, UNSET)
            if value is not UNSET and field_name not in result:
                result[field_name] = value

    return result


def build_attributes_kwargs(entity: Any, attributes_class: Type) -> dict[str, Any]:
    """
    Build kwargs dictionary for attributes from an entity using dynamic field extraction.

    Extracts all fields from attributes_class and gets their values from entity.
    This avoids manual enumeration of all fields.

    Args:
        entity: The entity to extract attribute values from
        attributes_class: The Attributes class defining which fields to extract

    Returns:
        Dict of attribute name -> value pairs for all fields in attributes_class

    Example:
        >>> attrs_kwargs = build_attributes_kwargs(table, TableAttributes)
        >>> attrs = TableAttributes(**attrs_kwargs)
    """
    attr_field_names = {f.name for f in msgspec.structs.fields(attributes_class)}

    return {
        name: getattr(entity, name)
        for name in attr_field_names
        if hasattr(entity, name)
    }


def build_flat_kwargs(
    nested: Any,
    attrs: Any,
    merged_rels: dict[str, Any],
    nested_class: Type,
    attributes_class: Type,
) -> dict[str, Any]:
    """
    Build kwargs dictionary for flat entity from nested format using dynamic field extraction.

    Extracts fields from nested entity, attributes, and merged relationships.
    This avoids manual enumeration of all fields.

    Args:
        nested: The nested entity containing top-level fields
        attrs: The attributes object containing attribute fields
        merged_rels: Dict of merged relationship attributes
        nested_class: The Nested class defining top-level fields
        attributes_class: The Attributes class defining attribute fields

    Returns:
        Dict of field name -> value pairs for creating flat entity

    Example:
        >>> kwargs = build_flat_kwargs(
        ...     nested, attrs, merged_rels,
        ...     TableNested, TableAttributes
        ... )
        >>> table = Table(**kwargs)
    """
    # Get top-level field names (exclude attributes and relationship fields)
    top_level_fields = {
        f.name
        for f in msgspec.structs.fields(nested_class)
        if f.name
        not in (
            "attributes",
            "relationship_attributes",
            "append_relationship_attributes",
            "remove_relationship_attributes",
        )
    }

    # Get attribute field names
    attr_field_names = {f.name for f in msgspec.structs.fields(attributes_class)}

    # Build kwargs: top-level fields + attribute fields + relationships
    kwargs = {}

    # Add top-level fields from nested
    for name in top_level_fields:
        if hasattr(nested, name):
            kwargs[name] = getattr(nested, name)

    # Add attribute fields from attrs
    for name in attr_field_names:
        if hasattr(attrs, name):
            kwargs[name] = getattr(attrs, name)

    # Add merged relationships
    kwargs.update(merged_rels)

    return kwargs
