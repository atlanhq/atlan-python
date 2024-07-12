# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType, DataModelTool, DataModelType
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .data_modeling import DataModeling


class DataModel(DataModeling):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, name: str, connection_qualified_name: str) -> DataModel:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        attributes = DataModel.Attributes.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="DataModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataModel":
            raise ValueError("must be DataModel")
        return v

    def __setattr__(self, name, value):
        if name in DataModel._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATA_MODEL_REFRESH_TIMESTAMP: ClassVar[NumericField] = NumericField(
        "dataModelRefreshTimestamp", "dataModelRefreshTimestamp"
    )
    """

    """
    DATA_MODEL_TYPE: ClassVar[KeywordField] = KeywordField(
        "dataModelType", "dataModelType"
    )
    """

    """
    DATA_MODEL_TOOL: ClassVar[KeywordField] = KeywordField(
        "dataModelTool", "dataModelTool"
    )
    """

    """
    DATA_MODEL_OWNING_APPLICATION_SEAL_ID: ClassVar[KeywordField] = KeywordField(
        "dataModelOwningApplicationSEALId", "dataModelOwningApplicationSEALId"
    )
    """

    """

    DATA_MODEL_VERSIONS: ClassVar[RelationField] = RelationField("dataModelVersions")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "data_model_refresh_timestamp",
        "data_model_type",
        "data_model_tool",
        "data_model_owning_application_s_e_a_l_id",
        "data_model_versions",
    ]

    @property
    def data_model_refresh_timestamp(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_model_refresh_timestamp
        )

    @data_model_refresh_timestamp.setter
    def data_model_refresh_timestamp(
        self, data_model_refresh_timestamp: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_model_refresh_timestamp = data_model_refresh_timestamp

    @property
    def data_model_type(self) -> Optional[DataModelType]:
        return None if self.attributes is None else self.attributes.data_model_type

    @data_model_type.setter
    def data_model_type(self, data_model_type: Optional[DataModelType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_model_type = data_model_type

    @property
    def data_model_tool(self) -> Optional[DataModelTool]:
        return None if self.attributes is None else self.attributes.data_model_tool

    @data_model_tool.setter
    def data_model_tool(self, data_model_tool: Optional[DataModelTool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_model_tool = data_model_tool

    @property
    def data_model_owning_application_s_e_a_l_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_model_owning_application_s_e_a_l_id
        )

    @data_model_owning_application_s_e_a_l_id.setter
    def data_model_owning_application_s_e_a_l_id(
        self, data_model_owning_application_s_e_a_l_id: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_model_owning_application_s_e_a_l_id = (
            data_model_owning_application_s_e_a_l_id
        )

    @property
    def data_model_versions(self) -> Optional[List[DataModelVersion]]:
        return None if self.attributes is None else self.attributes.data_model_versions

    @data_model_versions.setter
    def data_model_versions(
        self, data_model_versions: Optional[List[DataModelVersion]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_model_versions = data_model_versions

    class Attributes(DataModeling.Attributes):
        data_model_refresh_timestamp: Optional[datetime] = Field(
            default=None, description=""
        )
        data_model_type: Optional[DataModelType] = Field(default=None, description="")
        data_model_tool: Optional[DataModelTool] = Field(default=None, description="")
        data_model_owning_application_s_e_a_l_id: Optional[str] = Field(
            default=None, description=""
        )
        data_model_versions: Optional[List[DataModelVersion]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls, *, name: str, connection_qualified_name: str
        ) -> DataModel.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )
            return DataModel.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/datamodel/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
            )

    attributes: DataModel.Attributes = Field(
        default_factory=lambda: DataModel.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .data_model_version import DataModelVersion  # noqa
