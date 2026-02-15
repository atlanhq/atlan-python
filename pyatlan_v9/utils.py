# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Utility functions for pyatlan_v9."""

import random
from functools import wraps


def init_guid(func):
    """
    Decorator function that can be used on the creator method of an asset to initialize the guid.

    The guid is initialized with a negative random integer to indicate it's a temporary GUID
    for objects being created (not yet persisted to Atlan).
    """

    @wraps(func)
    def call(*args, **kwargs):
        ret_value = func(*args, **kwargs)
        if hasattr(ret_value, "guid"):
            ret_value.guid = str(
                -int(random.random() * 10000000000000000)  # noqa: S311
            )
        return ret_value

    return call


def validate_required_fields(field_names: list[str], field_values: list) -> None:
    """
    Validate that required fields are provided and not empty.

    Args:
        field_names: List of field names
        field_values: List of field values corresponding to field_names

    Raises:
        ValueError: If any required field is missing or empty
    """
    for name, value in zip(field_names, field_values):
        if value is None:
            raise ValueError(f"{name} is required")
        if isinstance(value, str) and not value.strip():
            raise ValueError(f"{name} cannot be blank")
        if isinstance(value, list) and len(value) == 0:
            raise ValueError(f"{name} cannot be an empty list")
