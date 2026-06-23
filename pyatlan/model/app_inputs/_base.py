# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Base for generated app-input models (BLDX-1472).

Generated ``*Inputs`` classes (one per app/entrypoint, emitted from each app's
live ``/v1/apps/{app}/inputs`` JSON Schema) inherit this. Field names are the
snake_case wire keys, so serialization needs no aliasing. Pass an instance
straight to ``client.app.create(..., inputs=...)``.
"""

from __future__ import annotations

from typing import Any, Dict

from pydantic.v1 import BaseModel, Extra


class AppInput(BaseModel):
    """A typed, contract-derived ``inputs`` payload for an app workflow."""

    class Config:
        extra = Extra.allow  # tolerate fields newer than the generated snapshot
        allow_population_by_field_name = True
        validate_assignment = True

    def to_inputs(self) -> Dict[str, Any]:
        """Return the ``inputs`` dict for the v3 API.

        Includes contract defaults (matching the UI), drops unset optionals.
        """
        return self.dict(exclude_none=True)
