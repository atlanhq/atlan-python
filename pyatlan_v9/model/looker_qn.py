# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""qualifiedName helpers for the Looker creators.

These reproduce the qualifiedNames atlan-looker-app emits (``app/qualified_names.py``,
``app/asset_mapper.py``), so assets created through the SDK and assets crawled by the app
land on the same qualifiedName.
"""

from __future__ import annotations

import hashlib
import re
from typing import NamedTuple, Union

LookerId = Union[str, int, float]

_SEGMENT = r"[^/]+"
_CONNECTION = rf"(?P<connection>{_SEGMENT}/{_SEGMENT}/{_SEGMENT})"
_PROJECT_QN = re.compile(rf"^{_CONNECTION}/project/(?P<project>{_SEGMENT})$")
_MODEL_QN = re.compile(
    rf"^{_CONNECTION}/project/(?P<project>{_SEGMENT})/model/(?P<model>{_SEGMENT})$"
)
_EXPLORE_QN = re.compile(
    rf"^{_CONNECTION}/project/(?P<project>{_SEGMENT})/model/(?P<model>{_SEGMENT})"
    r"/(?P<explore_model>[^/:]+)::(?P<explore>[^/]+)$"
)
_VIEW_QN = re.compile(
    rf"^{_CONNECTION}/(?P<relative>project/(?P<project>{_SEGMENT})"
    rf"/view/{_SEGMENT}/(?P<view>{_SEGMENT}))$"
)
_FOLDER_QN = re.compile(rf"^{_CONNECTION}/folder/(?P<id>{_SEGMENT})$")
_CONTENT_QN = {
    kind: re.compile(rf"^{_CONNECTION}/{kind}/(?P<id>{_SEGMENT})$")
    for kind in ("dashboard", "look", "tile")
}
_CLONED_REPOS = "cloned_repos/"


class LookerParent(NamedTuple):
    """Parts of a parent qualifiedName, as the creators need them."""

    connection_qualified_name: str
    project_name: str = ""
    model_name: str = ""
    explore_name: str = ""
    relative: str = ""


def connector_name(connection_qualified_name: str) -> str:
    return connection_qualified_name.split("/")[1]


def looker_id(value: LookerId, field: str, *, numeric: bool = False) -> str:
    """Render a Looker id as one qualifiedName segment, like the app's ``segment()``.

    Whole floats lose their ``.0`` (``11.0`` -> ``11``), as the app's ``clean_record`` does.
    With ``numeric=True`` a digit string also loses leading zeros, as the app's
    ``_numeric_id`` does for look ids.
    """
    if value is None:
        raise ValueError(f"{field} is required")
    if isinstance(value, bool):
        raise ValueError(f"{field} must be a string or a number, got {value!r}")
    if isinstance(value, float):
        if not value.is_integer():
            raise ValueError(f"{field} must be a whole number, got {value!r}")
        value = int(value)
    text = str(value)
    if not text.strip():
        raise ValueError(f"{field} cannot be blank")
    if "/" in text:
        raise ValueError(f"{field} cannot contain '/', got {text!r}")
    if numeric and text.lstrip("-").isdigit():
        text = str(int(text))
    return text


def file_path_hash(file_path: str) -> str:
    """md5 of a LookML file path relative to the cloned repo, as in the app's view ids."""
    if _CLONED_REPOS in file_path:
        file_path = file_path.split(_CLONED_REPOS, 1)[1]
    return hashlib.md5(file_path.encode("utf-8")).hexdigest()  # noqa: S324


def refinement_hash(file_path: str, line_number: str) -> str:
    """md5 prefix of a refined view field's qualifiedName, as in the app's view-field ids."""
    if _CLONED_REPOS in file_path:
        file_path = file_path.split(_CLONED_REPOS, 1)[1]
    return hashlib.md5(  # noqa: S324
        f"{file_path}:{line_number}".encode("utf-8")
    ).hexdigest()


def _parse(pattern: re.Pattern, value: str, field: str, shape: str) -> re.Match:
    match = pattern.match(value)
    if not match:
        raise ValueError(f"Invalid {field}: {value}. Expected format: {shape}")
    return match


def connection(value: str, field: str = "connection_qualified_name") -> str:
    _parse(re.compile(rf"^{_CONNECTION}$"), value, field, "default/looker/<epoch>")
    return value


def parse_project(value: str) -> LookerParent:
    m = _parse(
        _PROJECT_QN,
        value,
        "project_qualified_name",
        "default/looker/<epoch>/project/<project>",
    )
    return LookerParent(m["connection"], project_name=m["project"])


def parse_model(value: str) -> LookerParent:
    m = _parse(
        _MODEL_QN,
        value,
        "model_qualified_name",
        "default/looker/<epoch>/project/<project>/model/<model>",
    )
    return LookerParent(m["connection"], m["project"], m["model"])


def parse_explore(value: str) -> LookerParent:
    m = _parse(
        _EXPLORE_QN,
        value,
        "explore_qualified_name",
        "default/looker/<epoch>/project/<project>/model/<model>/<model>::<explore>",
    )
    if m["explore_model"] != m["model"]:
        raise ValueError(
            f"Invalid explore_qualified_name: {value}. "
            f"The model before '::' must be '{m['model']}'"
        )
    return LookerParent(m["connection"], m["project"], m["model"], m["explore"])


def parse_view(value: str) -> LookerParent:
    m = _parse(
        _VIEW_QN,
        value,
        "view_qualified_name",
        "default/looker/<epoch>/project/<project>/view/<file hash>/<view>",
    )
    return LookerParent(
        m["connection"], project_name=m["project"], relative=m["relative"]
    )


def _same_connection(parent: LookerParent, connection_qualified_name, field, value):
    if (
        connection_qualified_name is not None
        and parent.connection_qualified_name != connection_qualified_name
    ):
        raise ValueError(
            f"Invalid {field}: {value}. "
            f"It must be in connection {connection_qualified_name}"
        )
    return parent


def parse_content(
    kind: str, value: str, connection_qualified_name: str | None = None
) -> LookerParent:
    """Parse a dashboard, look or tile qualifiedName."""
    field = f"{kind}_qualified_name"
    m = _parse(_CONTENT_QN[kind], value, field, f"default/looker/<epoch>/{kind}/<id>")
    parent = LookerParent(m["connection"], relative=f"{kind}/{m['id']}")
    return _same_connection(parent, connection_qualified_name, field, value)


def parse_folder(
    value: str,
    connection_qualified_name: str | None = None,
    field: str = "folder_qualified_name",
) -> LookerParent:
    m = _parse(_FOLDER_QN, value, field, "default/looker/<epoch>/folder/<id>")
    parent = LookerParent(m["connection"])
    return _same_connection(parent, connection_qualified_name, field, value)
