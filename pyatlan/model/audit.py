from datetime import datetime
from enum import Enum
from typing import Any, Generator, Iterable, Optional, Union

from pydantic import Field, ValidationError, parse_obj_as

from pyatlan.client.constants import AUDIT_SEARCH
from pyatlan.client.workflow import ApiCaller
from pyatlan.errors import ErrorCode
from pyatlan.model.assets import Asset
from pyatlan.model.core import AtlanObject, AtlanTag, AtlanTagName
from pyatlan.model.enums import EntityStatus
from pyatlan.model.search import DSL, Query, SearchRequest, SortItem, SortOrder, Term


class AuditActionType(str, Enum):
    ENTITY_CREATE = "ENTITY_CREATE"
    ENTITY_UPDATE = "ENTITY_UPDATE"
    ENTITY_DELETE = "ENTITY_DELETE"
    CUSTOM_METADATA_UPDATE = "BUSINESS_ATTRIBUTE_UPDATE"
    ATLAN_TAG_ADD = "CLASSIFICATION_ADD"
    PROPAGATED_ATLAN_TAG_ADD = "PROPAGATED_CLASSIFICATION_ADD"
    ATLAN_TAG_DELETE = "CLASSIFICATION_DELETE"
    PROPAGATED_ATLAN_TAG_DELETE = "PROPAGATED_CLASSIFICATION_DELETE"


class AuditSearchRequest(SearchRequest):
    """Class from which to configure a search against Atlan's activity log."""

    dsl: DSL
    attributes: list[str] = Field(default_factory=list, alias="attributes")

    class Config:
        json_encoders = {Query: lambda v: v.to_dict(), SortItem: lambda v: v.to_dict()}

    @classmethod
    def by_guid(cls, guid: str, size: int) -> "AuditSearchRequest":
        dsl = DSL(
            query=Term(field="entityId", value=guid),
            sort=[SortItem("created", order=SortOrder.ASCENDING)],
            size=size,
        )
        return AuditSearchRequest(dsl=dsl)

    @classmethod
    def by_user(cls, user: str, size: int) -> "AuditSearchRequest":
        dsl = DSL(
            query=Term(field="user", value=user),
            sort=[SortItem("created", order=SortOrder.DESCENDING)],
            size=size,
        )
        return AuditSearchRequest(dsl=dsl)


class TagDetail(AtlanObject):
    """Capture the attributes and values for tags as tracked through the audit log."""

    class Config:
        extra = "forbid"

    type_name: str
    entity_guid: Optional[str] = Field(
        None,
        description="Unique identifier of the entity instance.\n",
        example="917ffec9-fa84-4c59-8e6c-c7b114d04be3",
        alias="entityGuid",
    )
    entity_status: Optional[EntityStatus] = Field(
        None,
        description="Status of the entity",
        example=EntityStatus.ACTIVE,
        alias="entityStatus",
    )
    propagate: Optional[bool] = Field(None, description="")
    remove_propagations_on_entity_delete: Optional[bool] = Field(
        None, description="", alias="removePropagationsOnEntityDelete"
    )
    restrict_propagation_through_lineage: Optional[bool] = Field(
        None, description="", alias="restrictPropagationThroughLineage"
    )
    validity_periods: Optional[list[str]] = Field(None, alias="validityPeriods")

    @property
    def tag(self) -> AtlanTag:
        try:
            tag_name = AtlanTagName._convert_to_display_text(self.type_name)
        except ValueError:
            tag_name = AtlanTagName.get_deleted_sentinel()
        atlan_tag = AtlanTag(
            type_name=tag_name,
            entity_guid=self.entity_guid,
            entity_status=self.entity_status,
            propagate=self.propagate,
            remove_propagations_on_entity_delete=self.remove_propagations_on_entity_delete,
            restrict_propagation_through_lineage=self.restrict_propagation_through_lineage,
            validity_periods=self.validity_periods,
        )

        return atlan_tag


class CustomMetadataAttributesAuditDetail(AtlanObject):
    """Capture the attributes and values for custom metadata as tracked through the audit log."""

    class Config:
        extra = "forbid"

    type_name: str

    attributes: dict[str, Any]


class EntityAudit(AtlanObject):
    """
    Detailed entry in the audit log. These objects should be treated as immutable.
    """

    entity_qualified_name: str
    type_Name: str
    entity_id: str
    timestamp: datetime
    created: datetime
    user: str
    action: AuditActionType
    details: Optional[Any]
    event_key: str
    entity: Optional[Any]
    type: Optional[Any]
    detail: Optional[Union[CustomMetadataAttributesAuditDetail, TagDetail, Asset]]
    entity_detail: Optional[Asset]
    headers: Optional[dict[str, str]]


class AuditSearchResults(Iterable):
    """Captures the response from a search against Atlan's activity log."""

    def __init__(
        self,
        client: ApiCaller,
        criteria: AuditSearchRequest,
        start: int,
        size: int,
        entity_audits: list[EntityAudit],
        count: int,
        aggregations: Optional[Any],
    ):
        self._client = client
        self._endpoint = AUDIT_SEARCH
        self._criteria = criteria
        self._start = start
        self._size = size
        self._entity_audits = entity_audits
        self._count = count

    def current_page(self) -> list[EntityAudit]:
        """
        Retrieve the current page of results.

        :returns: list of assets on the current page of results
        """
        return self._entity_audits

    def next_page(self, start=None, size=None) -> bool:
        """
        Indicates whether there is a next page of results.

        :returns: True if there is a next page of results, otherwise False
        """
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return self._get_next_page() if self._entity_audits else False

    def _get_next_page(self):
        """
        Fetches the next page of results.

        :returns: True if the next page of results was fetched, False if there was no next page
        """
        self._criteria.dsl.from_ = self._start
        self._criteria.dsl.size = self._size
        if raw_json := self._get_next_page_json():
            self._count = raw_json["totalCount"] if "totalCount" in raw_json else 0
            return True
        return False

    # TODO Rename this here and in `next_page`
    def _get_next_page_json(self):
        """
        Fetches the next page of results and returns the raw JSON of the retrieval.

        :returns: JSON for the next page of results, as-is
        """
        raw_json = self._client._call_api(
            self._endpoint,
            request_obj=self._criteria,
        )
        if "entityAudits" not in raw_json or not raw_json["entityAudits"]:
            self._entity_audits = []
            return None
        try:
            self._assets = parse_obj_as(list[EntityAudit], raw_json["entityAudits"])
            return raw_json
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

    def __iter__(self) -> Generator[EntityAudit, None, None]:
        """
        Iterates through the results, lazily-fetching each next page until there
        are no more results.

        :returns: an iterable form of each result, across all pages
        """
        while True:
            yield from self.current_page()
            if not self.next_page():
                break


if __name__ == "__main__":
    detail_asset = {
        "entityQualifiedName": "fc836098-d091-43b9-9bac-73acdd1c421d/connection-entity-business-metadata",
        "typeName": "AuthPolicy",
        "entityId": "d5d44b08-e314-417b-b614-cd3d91af2a41",
        "timestamp": 1696011438537,
        "created": 1696011487655,
        "user": "service-account-apikey-a1c7beae-a558-4994-adb4-16ee422b91d6",
        "action": "ENTITY_DELETE",
        "details": None,
        "eventKey": "d5d44b08-e314-417b-b614-cd3d91af2a41:1696011438537",
        "entity": None,
        "type": None,
        "detail": {
            "typeName": "AuthPolicy",
            "attributes": {
                "qualifiedName": "fc836098-d091-43b9-9bac-73acdd1c421d/connection-entity-business-metadata"
            },
            "guid": "d5d44b08-e314-417b-b614-cd3d91af2a41",
            "isIncomplete": False,
            "provenanceType": 0,
            "status": "DELETED",
            "createdBy": "service-account-apikey-a1c7beae-a558-4994-adb4-16ee422b91d6",
            "updatedBy": "service-account-apikey-a1c7beae-a558-4994-adb4-16ee422b91d6",
            "createTime": 1696011438537,
            "updateTime": 1696011438537,
            "version": 0,
            "classifications": [],
            "meanings": [],
            "deleteHandler": "PURGE",
            "proxy": False,
        },
        "entityDetail": None,
        "headers": {"x-atlan-agent-id": "python", "x-atlan-agent": "sdk"},
    }
    detail_metadata = {
        "entityQualifiedName": "KRrLNWZ9hWbDl8Hct0Ntb@J8aDKGBBnt73Rp4QbYR2m",
        "typeName": "AtlasGlossaryTerm",
        "entityId": "f8acb54f-d6eb-4892-bbe0-04892d786751",
        "timestamp": 1695924914922,
        "created": 1695924915072,
        "user": "service-account-apikey-a1c7beae-a558-4994-adb4-16ee422b91d6",
        "action": "BUSINESS_ATTRIBUTE_UPDATE",
        "details": None,
        "eventKey": "f8acb54f-d6eb-4892-bbe0-04892d786751:1695924914922",
        "entity": None,
        "type": None,
        "detail": {
            "typeName": "cxln83UsRAMR3FVY1ycm7s",
            "attributes": {
                "m4ZeLphZSCw0AZ0VZNlAli": ["psdk_cm_djwqk1", "psdk_cm_djwqk2"],
                "lSDYAg4b9ss2fUtj2NMP3C": ["ernest"],
                "S0wq82gjzH9oXnTF4rBJqZ": ["psdk_cm_djwqk1"],
                "tLKdDBnULWew8d8jv2pqWP": "something extra...",
                "ID3s6qwmlBtbVyf8PvIrWX": "ernest",
            },
        },
        "entityDetail": None,
        "headers": {"x-atlan-agent-id": "python", "x-atlan-agent": "sdk"},
    }
    detail_tag = {
        "entityQualifiedName": "default/api/1695649284/Swagger Petstore - OpenAPI 3.0/pet",
        "typeName": "APIPath",
        "entityId": "67c7450b-aa3a-4d27-8443-76ee6da21f28",
        "timestamp": 1696254083143,
        "created": 1696254083257,
        "user": "service-account-apikey-a1c7beae-a558-4994-adb4-16ee422b91d6",
        "action": "CLASSIFICATION_DELETE",
        "details": None,
        "eventKey": "67c7450b-aa3a-4d27-8443-76ee6da21f28:1696254083143",
        "entity": None,
        "type": None,
        "detail": {"typeName": "taPaKswvHMovoskyNPsMq9123"},
        "entityDetail": {
            "typeName": "APIPath",
            "attributes": {},
            "guid": "67c7450b-aa3a-4d27-8443-76ee6da21f28",
            "status": "ACTIVE",
            "isIncomplete": False,
            "createdBy": "service-account-apikey-a1c7beae-a558-4994-adb4-16ee422b91d6",
            "updatedBy": "service-account-apikey-a1c7beae-a558-4994-adb4-16ee422b91d6",
            "createTime": 1695649801084,
            "updateTime": 1696254083143,
        },
        "headers": None,
    }
