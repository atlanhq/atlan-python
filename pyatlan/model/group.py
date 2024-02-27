# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

from typing import Any, Dict, Generator, List, Optional

from pydantic.v1 import Field, PrivateAttr, ValidationError, parse_obj_as

from pyatlan.client.common import ApiCaller
from pyatlan.errors import ErrorCode
from pyatlan.model.core import AtlanObject
from pyatlan.utils import API


class AtlanGroup(AtlanObject):
    class Attributes(AtlanObject):
        alias: Optional[List[str]] = Field(
            default=None, description="Name of the group as it appears in the UI."
        )
        created_at: Optional[List[str]] = Field(
            default=None,
            description="Time (epoch) at which the group was created, in milliseconds.",
        )
        created_by: Optional[List[str]] = Field(
            default=None, description="User who created the group."
        )
        updated_at: Optional[List[str]] = Field(
            default=None,
            description="Time (epoch) at which the group was last updated, in milliseconds.",
        )
        updated_by: Optional[List[str]] = Field(
            default=None, description="User who last updated the group."
        )
        description: Optional[List[str]] = Field(
            default=None, description="Description of the group."
        )
        is_default: Optional[List[str]] = Field(
            default=None,
            description="Whether this group should be auto-assigned to all new users or not.",
        )
        channels: Optional[List[str]] = Field(
            default=None, description="Slack channels for this group."
        )

    alias: Optional[str] = Field(
        default=None, description="Name of the group as it appears in the UI."
    )
    attributes: Optional[AtlanGroup.Attributes] = Field(
        default=None, description="Detailed attributes of the group."
    )
    decentralized_roles: Optional[List[Any]] = Field(default=None, description="TBC")
    id: Optional[str] = Field(
        default=None, description="Unique identifier for the group (GUID)."
    )
    name: Optional[str] = Field(
        default=None, description="Unique (internal) name for the group."
    )
    path: Optional[str] = Field(default=None, description="TBC")
    personas: Optional[List[Any]] = Field(
        default=None, description="Personas the group is associated with."
    )
    purposes: Optional[List[Any]] = Field(
        default=None, description="Purposes the group is associated with."
    )
    user_count: Optional[int] = Field(
        default=None, description="Number of users in the group."
    )

    def is_default(self) -> bool:
        return (
            self.attributes is not None
            and self.attributes.is_default is not None
            and self.attributes.is_default == ["true"]
        )

    @staticmethod
    def create(
        alias: str,
    ) -> AtlanGroup:
        from pyatlan.utils import validate_required_fields

        validate_required_fields(
            ["alias"],
            [alias],
        )
        return AtlanGroup(
            name=AtlanGroup.generate_name(alias),
            attributes=AtlanGroup.Attributes(alias=[alias]),
        )

    @staticmethod
    def create_for_modification(
        guid: str,
        path: str,
    ) -> AtlanGroup:
        from pyatlan.utils import validate_required_fields

        validate_required_fields(
            ["guid", "path"],
            [guid, path],
        )
        return AtlanGroup(id=guid, path=path)

    @staticmethod
    def generate_name(
        alias: str,
    ) -> str:
        from pyatlan.utils import validate_required_fields

        validate_required_fields(
            ["alias"],
            [alias],
        )
        internal = alias.lower()
        return internal.replace(" ", "_")


class GroupResponse(AtlanObject):
    _size: int = PrivateAttr()
    _start: int = PrivateAttr()
    _endpoint: API = PrivateAttr()
    _client: ApiCaller = PrivateAttr()
    _criteria: GroupRequest = PrivateAttr()
    total_record: Optional[int] = Field(description="Total number of groups.")
    filter_record: Optional[int] = Field(
        description="Number of groups in the filtered response.",
    )
    records: Optional[List[AtlanGroup]] = Field(
        description="Details of each group included in the response."
    )

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._endpoint = data.get("endpoint")  # type: ignore[assignment]
        self._client = data.get("client")  # type: ignore[assignment]
        self._criteria = data.get("criteria")  # type: ignore[assignment]
        self._size = data.get("size")  # type: ignore[assignment]
        self._start = data.get("start")  # type: ignore[assignment]

    def current_page(self) -> Optional[List[AtlanGroup]]:
        return self.records

    def next_page(self, start=None, size=None) -> bool:
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return self._get_next_page() if self.records else False

    def _get_next_page(self):
        self._criteria.offset = self._start
        self._criteria.limit = self._size
        raw_json = self._client._call_api(
            api=self._endpoint.format_path_with_params(),
            query_params=self._criteria.query_params,
        )
        if not raw_json.get("records"):
            self.records = []
            return False
        try:
            self.records = parse_obj_as(List[AtlanGroup], raw_json.get("records"))
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err
        return True

    def __iter__(self) -> Generator[AtlanGroup, None, None]:  # type: ignore[override]
        while True:
            yield from self.current_page() or []
            if not self.next_page():
                break


class GroupRequest(AtlanObject):
    post_filter: Optional[str] = Field(
        default=None,
        description="Criteria by which to filter the list of groups to retrieve.",
    )
    sort: Optional[str] = Field(
        default="name",
        description="Property by which to sort the resulting list of groups.",
    )
    count: bool = Field(
        default=True,
        description="Whether to include an overall count of groups (True) or not (False).",
    )
    offset: int = Field(
        default=0,
        description="Starting point for the list of groups when paging.",
    )
    limit: Optional[int] = Field(
        default=20,
        description="Maximum number of groups to return per page.",
    )

    @property
    def query_params(self) -> dict:
        qp: Dict[str, object] = {}
        if self.post_filter:
            qp["filter"] = self.post_filter
        if self.sort:
            qp["sort"] = self.sort
        qp["count"] = self.count
        qp["offset"] = self.offset
        qp["limit"] = self.limit
        return qp


class CreateGroupRequest(AtlanObject):
    group: AtlanGroup = Field(description="Group to be created.")
    users: Optional[List[str]] = Field(
        default=None,
        description="List of users (their GUIDs) to be included in the group.",
    )


class RemoveFromGroupRequest(AtlanObject):
    users: Optional[List[str]] = Field(
        default=None,
        description="List of users (their GUIDs) to remove from the group.",
    )


class CreateGroupResponse(AtlanObject):
    class UserStatus(AtlanObject):
        status: Optional[int] = Field(
            default=None,
            description="Response code for the association (200 is success).",
        )
        status_message: Optional[str] = Field(
            default=None,
            description="Status message for the association ('success' means the association was successful).",
        )

        def was_successful(self) -> bool:
            return (self.status is not None and self.status == 200) or (
                self.status_message is not None and self.status_message == "success"
            )

    group: str = Field(
        description="Unique identifier (GUID) of the group that was created."
    )
    users: Optional[Dict[str, CreateGroupResponse.UserStatus]] = Field(
        default=None,
        description="Map of user association statuses, keyed by unique identifier (GUID) of the user.",
    )
