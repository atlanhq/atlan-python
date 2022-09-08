#!/usr/bin/env/python
# Copyright 2022 Atlan Pte, Ltd
# Copyright [2015-2021] The Apache Software Foundation
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pyatlan.model.enums import EntityStatus
from pyatlan.model.glossary import AtlanTermAssignmentHeader
from pyatlan.model.misc import AtlanBase, Plist, TimeBoundary, next_id
from pyatlan.utils import (
    non_null,
    type_coerce,
    type_coerce_dict,
    type_coerce_dict_list,
    type_coerce_list,
)


class AtlanStruct(AtlanBase):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanBase.__init__(self, attrs)

        self.typeName = attrs.get("typeName")
        self.attributes = attrs.get("attributes")

    def get_attribute(self, name):
        return (
            self.attributes[name]
            if self.attributes is not None and name in self.attributes
            else None
        )

    def set_attribute(self, name, value):
        if self.attributes is None:
            self.attributes = {}

        self.attributes[name] = value

    def remove_attribute(self, name):
        if name and self.attributes is not None and name in self.attributes:
            del self.attributes[name]


class AtlanEntity(AtlanStruct):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        AtlanStruct.__init__(self, attrs)
        self.guid: str = attrs.get("guid")
        self.homeId = attrs.get("homeId")
        self.relationshipAttributes = attrs.get("relationshipAttributes")
        self.classifications = attrs.get("classifications")
        self.meanings = attrs.get("meanings")
        self.customAttributes = attrs.get("customAttributes")
        self.businessAttributes = attrs.get("businessAttributes")
        self.labels = attrs.get("labels")
        self.status = attrs.get("status")
        self.isIncomplete = attrs.get("isIncomplete")
        self.provenanceType = attrs.get("provenanceType")
        self.proxy = attrs.get("proxy")
        self.version = attrs.get("version")
        self.createdBy = attrs.get("createdBy")
        self.updatedBy = attrs.get("updatedBy")
        self.createTime = attrs.get("createTime")
        self.updateTime = attrs.get("updateTime")
        if self.guid is None:
            self.guid = next_id()

    @property
    def qualified_name(self) -> str:
        return self.get_attribute("qualifiedName")

    @qualified_name.setter
    def qualified_name(self, value: str):
        self.set_attribute("qualifiedName", value)

    @property
    def replicated_from(self):
        return self.get_attribute("replicatedFrom")

    @replicated_from.setter
    def replicated_from(self, value):
        self.set_attribute("replicatedFrom", value)

    @property
    def replicated_to(self):
        return self.get_attribute("replicatedTo")

    @replicated_to.setter
    def replicated_to(self, value):
        self.set_attribute("replicatedTo", value)

    @property
    def name(self) -> str:
        return self.get_attribute("name")

    @name.setter
    def name(self, value: str):
        self.set_attribute("name", value)

    @property
    def display_name(self) -> str:
        return self.get_attribute("displayName")

    @display_name.setter
    def display_name(self, value: str):
        self.set_attribute("displayName", value)

    @property
    def description(self) -> str:
        return self.get_attribute("description")

    @description.setter
    def description(self, value: str):
        self.set_attribute("description", value)

    @property
    def user_description(self) -> str:
        return self.get_attribute("userDescription")

    @user_description.setter
    def user_description(self, value: str):
        self.set_attribute("userDescription", value)

    @property
    def tenant_id(self) -> str:
        return self.get_attribute("tenantId")

    @tenant_id.setter
    def tenant_id(self, value: str):
        self.set_attribute("tenantId", value)

    @property
    def certificate_status(self):
        return self.get_attribute("certificateStatus")

    @certificate_status.setter
    def certificate_status(self, value):
        self.set_attribute("certificateStatus", value)

    @property
    def certificate_status_message(self) -> str:
        return self.get_attribute("certificateStatusMessage")

    @certificate_status_message.setter
    def certificate_status_message(self, value: str):
        self.set_attribute("certificateStatusMessage", value)

    @property
    def certificate_updated_by(self) -> str:
        return self.get_attribute("certificateUpdatedBy")

    @certificate_updated_by.setter
    def certificate_updated_by(self, value: str):
        self.set_attribute("certificateUpdatedBy", value)

    @property
    def certificate_updated_at(self):
        return self.get_attribute("certificateUpdatedAt")

    @certificate_updated_at.setter
    def certificate_updated_at(self, value):
        self.set_attribute("certificateUpdatedAt", value)

    @property
    def announcement_title(self) -> str:
        return self.get_attribute("announcementTitle")

    @announcement_title.setter
    def announcement_title(self, value: str):
        self.set_attribute("announcementTitle", value)

    @property
    def announcement_message(self) -> str:
        return self.get_attribute("announcementMessage")

    @announcement_message.setter
    def announcement_message(self, value: str):
        self.set_attribute("announcementMessage", value)

    @property
    def announcement_type(self) -> str:
        return self.get_attribute("announcementType")

    @announcement_type.setter
    def announcement_type(self, value: str):
        self.set_attribute("announcementType", value)

    @property
    def announcement_updated_at(self):
        return self.get_attribute("announcementUpdatedAt")

    @announcement_updated_at.setter
    def announcement_updated_at(self, value):
        self.set_attribute("announcementUpdatedAt", value)

    @property
    def announcement_updated_by(self) -> str:
        return self.get_attribute("announcementUpdatedBy")

    @announcement_updated_by.setter
    def announcement_updated_by(self, value: str):
        self.set_attribute("announcementUpdatedBy", value)

    @property
    def owner_users(self) -> list[str]:
        return self.get_attribute("ownerUsers")

    @owner_users.setter
    def owner_users(self, value: list[str]):
        self.set_attribute("ownerUsers", value)

    @property
    def owner_groups(self) -> list[str]:
        return self.get_attribute("ownerGroups")

    @owner_groups.setter
    def owner_groups(self, value: list[str]):
        self.set_attribute("ownerGroups", value)

    @property
    def admin_users(self) -> list[str]:
        return self.get_attribute("adminUsers")

    @admin_users.setter
    def admin_users(self, value: list[str]):
        self.set_attribute("adminUsers", value)

    @property
    def admin_groups(self) -> list[str]:
        return self.get_attribute("adminGroups")

    @admin_groups.setter
    def admin_groups(self, value: list[str]):
        self.set_attribute("adminGroups", value)

    @property
    def viewer_users(self) -> list[str]:
        return self.get_attribute("viewerUsers")

    @viewer_users.setter
    def viewer_users(self, value: list[str]):
        self.set_attribute("viewerUsers", value)

    @property
    def viewer_groups(self) -> list[str]:
        return self.get_attribute("viewerGroups")

    @viewer_groups.setter
    def viewer_groups(self, value: list[str]):
        self.set_attribute("viewerGroups", value)

    @property
    def connector_name(self) -> str:
        return self.get_attribute("connectorName")

    @connector_name.setter
    def connector_name(self, value: str):
        self.set_attribute("connectorName", value)

    @property
    def connection_name(self) -> str:
        return self.get_attribute("connectionName")

    @connection_name.setter
    def connection_name(self, value: str):
        self.set_attribute("connectionName", value)

    @property
    def connection_qualified_name(self) -> str:
        return self.get_attribute("connectionQualifiedName")

    @connection_qualified_name.setter
    def connection_qualified_name(self, value: str):
        self.set_attribute("connectionQualifiedName", value)

    @property
    def __has_lineage(self) -> bool:
        return self.get_attribute("__hasLineage")

    @__has_lineage.setter
    def __has_lineage(self, value: bool):
        self.set_attribute("__hasLineage", value)

    @property
    def is_discoverable(self) -> bool:
        return self.get_attribute("isDiscoverable")

    @is_discoverable.setter
    def is_discoverable(self, value: bool):
        self.set_attribute("isDiscoverable", value)

    @property
    def is_editable(self) -> bool:
        return self.get_attribute("isEditable")

    @is_editable.setter
    def is_editable(self, value: bool):
        self.set_attribute("isEditable", value)

    @property
    def sub_type(self) -> str:
        return self.get_attribute("subType")

    @sub_type.setter
    def sub_type(self, value: str):
        self.set_attribute("subType", value)

    @property
    def view_score(self) -> float:
        return self.get_attribute("viewScore")

    @view_score.setter
    def view_score(self, value: float):
        self.set_attribute("viewScore", value)

    @property
    def popularity_score(self) -> float:
        return self.get_attribute("popularityScore")

    @popularity_score.setter
    def popularity_score(self, value: float):
        self.set_attribute("popularityScore", value)

    @property
    def source_owners(self) -> str:
        return self.get_attribute("sourceOwners")

    @source_owners.setter
    def source_owners(self, value: str):
        self.set_attribute("sourceOwners", value)

    @property
    def source_created_by(self) -> str:
        return self.get_attribute("sourceCreatedBy")

    @source_created_by.setter
    def source_created_by(self, value: str):
        self.set_attribute("sourceCreatedBy", value)

    @property
    def source_created_at(self):
        return self.get_attribute("sourceCreatedAt")

    @source_created_at.setter
    def source_created_at(self, value):
        self.set_attribute("sourceCreatedAt", value)

    @property
    def source_updated_at(self):
        return self.get_attribute("sourceUpdatedAt")

    @source_updated_at.setter
    def source_updated_at(self, value):
        self.set_attribute("sourceUpdatedAt", value)

    @property
    def source_updated_by(self) -> str:
        return self.get_attribute("sourceUpdatedBy")

    @source_updated_by.setter
    def source_updated_by(self, value: str):
        self.set_attribute("sourceUpdatedBy", value)

    @property
    def source_url(self) -> str:
        return self.get_attribute("sourceURL")

    @source_url.setter
    def source_url(self, value: str):
        self.set_attribute("sourceURL", value)

    @property
    def last_sync_workflow_name(self) -> str:
        return self.get_attribute("lastSyncWorkflowName")

    @last_sync_workflow_name.setter
    def last_sync_workflow_name(self, value: str):
        self.set_attribute("lastSyncWorkflowName", value)

    @property
    def last_sync_run_at(self):
        return self.get_attribute("lastSyncRunAt")

    @last_sync_run_at.setter
    def last_sync_run_at(self, value):
        self.set_attribute("lastSyncRunAt", value)

    @property
    def last_sync_run(self) -> str:
        return self.get_attribute("lastSyncRun")

    @last_sync_run.setter
    def last_sync_run(self, value: str):
        self.set_attribute("lastSyncRun", value)

    @property
    def admin_roles(self) -> list[str]:
        return self.get_attribute("adminRoles")

    @admin_roles.setter
    def admin_roles(self, value: list[str]):
        self.set_attribute("adminRoles", value)

    def type_coerce_attrs(self):
        super(AtlanEntity, self).type_coerce_attrs()
        self.classifications = type_coerce_list(
            self.classifications, AtlanClassification
        )
        self.meanings = type_coerce_list(self.meanings, AtlanTermAssignmentHeader)

    def get_relationship_attribute(self, name):
        return (
            self.relationshipAttributes[name]
            if self.relationshipAttributes is not None
            and name in self.relationshipAttributes
            else None
        )

    def set_relationship_attribute(self, name, value):
        if self.relationshipAttributes is None:
            self.relationshipAttributes = {}
        self.relationshipAttributes[name] = value

    def remove_relationship_attribute(self, name):
        if (
            name
            and self.relationshipAttributes is not None
            and name in self.relationshipAttributes
        ):
            del self.relationshipAttributes[name]


class AtlanEntityExtInfo(AtlanBase):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanBase.__init__(self, attrs)

        self.referredEntities = attrs.get("referredEntities")

    def type_coerce_attrs(self):
        super(AtlanEntityExtInfo, self).type_coerce_attrs()

        self.referredEntities = type_coerce_dict(self.referredEntities, AtlanEntity)

    def get_referenced_entity(self, guid):
        return (
            self.referredEntities[guid]
            if self.referredEntities is not None and guid in self.referredEntities
            else None
        )

    def add_referenced_entity(self, entity):
        if self.referredEntities is None:
            self.referredEntities = {}

        self.referredEntities[entity.guid] = entity


class AtlanEntityWithExtInfo(AtlanEntityExtInfo):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanEntityExtInfo.__init__(self, attrs)

        self.entity = attrs.get("entity")

    def type_coerce_attrs(self):
        super(AtlanEntityWithExtInfo, self).type_coerce_attrs()

        self.entity = type_coerce(self.entity, AtlanEntity)


class AtlanEntitiesWithExtInfo(AtlanEntityExtInfo):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanEntityExtInfo.__init__(self, attrs)

        self.entities = attrs.get("entities")

    def type_coerce_attrs(self):
        super(AtlanEntitiesWithExtInfo, self).type_coerce_attrs()

        self.entities = type_coerce_list(self.entities, AtlanEntity)

    def add_entity(self, entity):
        if self.entities is None:
            self.entities = []

        self.entities.append(entity)


class AtlanEntityHeader(AtlanStruct):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanStruct.__init__(self, attrs)

        self.guid = attrs.get("guid")
        self.status = non_null(attrs.get("status"), EntityStatus.ACTIVE.name)
        self.displayText = attrs.get("displayText")
        self.classificationNames = attrs.get("classificationNames")
        self.classifications = attrs.get("classifications")
        self.meaningNames = attrs.get("meaningNames")
        self.meanings = attrs.get(".meanings")
        self.isIncomplete = non_null(attrs.get("isIncomplete"), False)
        self.labels = attrs.get("labels")

        if self.guid is None:
            self.guid = next_id()

    def type_coerce_attrs(self):
        super(AtlanEntityHeader, self).type_coerce_attrs()

        self.classifications = type_coerce_list(
            self.classifications, AtlanClassification
        )
        self.meanings = type_coerce_list(self.meanings, AtlanTermAssignmentHeader)


class AtlanClassification(AtlanStruct):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanStruct.__init__(self, attrs)

        self.entityGuid = attrs.get("entityGuid")
        self.entityStatus = non_null(
            attrs.get("entityStatus"), EntityStatus.ACTIVE.name
        )
        self.propagate = attrs.get("propagate")
        self.validityPeriods = attrs.get("validityPeriods")
        self.removePropagationsOnEntityDelete = attrs.get(
            "removePropagationsOnEntityDelete"
        )

    def type_coerce_attrs(self):
        super(AtlanClassification, self).type_coerce_attrs()

        self.validityPeriods = type_coerce_list(self.validityPeriods, TimeBoundary)


class AtlanObjectId(AtlanBase):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanBase.__init__(self, attrs)

        self.guid = attrs.get("guid")
        self.typeName = attrs.get("typeName")
        self.uniqueAttributes = attrs.get("uniqueAttributes")


class AtlanRelatedObjectId(AtlanObjectId):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanObjectId.__init__(self, attrs)

        self.entityStatus = attrs.get("entityStatus")
        self.displayText = attrs.get("displayText")
        self.relationshipType = attrs.get("relationshipType")
        self.relationshipGuid = attrs.get("relationshipGuid")
        self.relationshipStatus = attrs.get("relationshipStatus")
        self.relationshipAttributes = attrs.get("relationshipAttributes")

    def type_coerce_attrs(self):
        super(AtlanRelatedObjectId, self).type_coerce_attrs()

        self.relationshipAttributes = type_coerce(
            self.relationshipAttributes, AtlanStruct
        )


class AtlanClassifications(Plist):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        Plist.__init__(self, attrs)

    def type_coerce_attrs(self):
        super(AtlanClassifications, self).type_coerce_attrs()

        Plist.list = type_coerce_list(Plist.list, AtlanClassification)


class AtlanEntityHeaders(AtlanBase):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanBase.__init__(self, attrs)

        self.guidHeaderMap = attrs.get("guidHeaderMap")

    def type_coerce_attrs(self):
        super(AtlanEntityHeaders, self).type_coerce_attrs()

        self.guidHeaderMap = type_coerce_dict(self.guidHeaderMap, AtlanEntityHeader)


class EntityMutationResponse(AtlanBase):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanBase.__init__(self, attrs)

        self.mutatedEntities = attrs.get("mutatedEntities")
        self.guidAssignments = attrs.get("guidAssignments")

    def type_coerce_attrs(self):
        super(EntityMutationResponse, self).type_coerce_attrs()

        self.mutatedEntities = type_coerce_dict_list(
            self.mutatedEntities, AtlanEntityHeader
        )

    def get_assigned_guid(self, guid):
        return self.guidAssignments.get(guid) if self.guidAssignments else None


class EntityMutations(AtlanBase):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanBase.__init__(self, attrs)

        self.entity_mutations = attrs.get("entity_mutations")

    def type_coerce_attrs(self):
        super(EntityMutations, self).type_coerce_attrs()

        self.entity_mutations = type_coerce_list(self.entity_mutations, EntityMutation)


class EntityMutation(AtlanBase):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanBase.__init__(self, attrs)

        self.op = attrs.get("op")
        self.entity = attrs.get("entity")

    def type_coerce_attrs(self):
        super(EntityMutation, self).type_coerce_attrs()

        self.entity = type_coerce(self.entity, AtlanEntity)


class AtlanCheckStateRequest(AtlanBase):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanBase.__init__(self, attrs)

        self.entityGuids = attrs.get("entityGuids")
        self.entityTypes = attrs.get("entityTypes")
        self.fixIssues = attrs.get("fixIssues")


class AtlanCheckStateResult(AtlanBase):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanBase.__init__(self, attrs)

        self.entitiesScanned = attrs.get("entitiesScanned")
        self.entitiesOk = attrs.get("entitiesOk")
        self.entitiesFixed = attrs.get("entitiesFixed")
        self.entitiesPartiallyFixed = attrs.get("entitiesPartiallyFixed")
        self.entitiesNotFixed = attrs.get("entitiesNotFixed")
        self.state = attrs.get("state")
        self.entities = attrs.get("entities")

    def type_coerce_attrs(self):
        super(AtlanCheckStateResult, self).type_coerce_attrs()

        self.entities = type_coerce(self.entities, AtlanEntityState)


class AtlanEntityState(AtlanBase):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanBase.__init__(self, attrs)

        self.guid = attrs.get("guid")
        self.typeName = attrs.get("typeName")
        self.name = attrs.get("name")
        self.status = attrs.get("status")
        self.state = attrs.get("state")
        self.issues = attrs.get("issues")
