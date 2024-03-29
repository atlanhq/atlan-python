# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .sisense import Sisense


class SisenseDatamodel(Sisense):
    """Description"""

    type_name: str = Field(default="SisenseDatamodel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SisenseDatamodel":
            raise ValueError("must be SisenseDatamodel")
        return v

    def __setattr__(self, name, value):
        if name in SisenseDatamodel._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SISENSE_DATAMODEL_TABLE_COUNT: ClassVar[NumericField] = NumericField(
        "sisenseDatamodelTableCount", "sisenseDatamodelTableCount"
    )
    """
    Number of tables in this datamodel.
    """
    SISENSE_DATAMODEL_SERVER: ClassVar[KeywordField] = KeywordField(
        "sisenseDatamodelServer", "sisenseDatamodelServer"
    )
    """
    Hostname of the server on which this datamodel was created.
    """
    SISENSE_DATAMODEL_REVISION: ClassVar[KeywordField] = KeywordField(
        "sisenseDatamodelRevision", "sisenseDatamodelRevision"
    )
    """
    Revision of this datamodel.
    """
    SISENSE_DATAMODEL_LAST_BUILD_TIME: ClassVar[NumericField] = NumericField(
        "sisenseDatamodelLastBuildTime", "sisenseDatamodelLastBuildTime"
    )
    """
    Time (epoch) when this datamodel was last built, in milliseconds.
    """
    SISENSE_DATAMODEL_LAST_SUCCESSFUL_BUILD_TIME: ClassVar[NumericField] = NumericField(
        "sisenseDatamodelLastSuccessfulBuildTime",
        "sisenseDatamodelLastSuccessfulBuildTime",
    )
    """
    Time (epoch) when this datamodel was last built successfully, in milliseconds.
    """
    SISENSE_DATAMODEL_LAST_PUBLISH_TIME: ClassVar[NumericField] = NumericField(
        "sisenseDatamodelLastPublishTime", "sisenseDatamodelLastPublishTime"
    )
    """
    Time (epoch) when this datamodel was last published, in milliseconds.
    """
    SISENSE_DATAMODEL_TYPE: ClassVar[KeywordField] = KeywordField(
        "sisenseDatamodelType", "sisenseDatamodelType"
    )
    """
    Type of this datamodel, for example: 'extract' or 'custom'.
    """
    SISENSE_DATAMODEL_RELATION_TYPE: ClassVar[KeywordField] = KeywordField(
        "sisenseDatamodelRelationType", "sisenseDatamodelRelationType"
    )
    """
    Default relation type for this datamodel. 'extract' type Datamodels have regular relations by default. 'live' type Datamodels have direct relations by default.
    """  # noqa: E501

    SISENSE_DATAMODEL_TABLES: ClassVar[RelationField] = RelationField(
        "sisenseDatamodelTables"
    )
    """
    TBC
    """
    SISENSE_DASHBOARDS: ClassVar[RelationField] = RelationField("sisenseDashboards")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sisense_datamodel_table_count",
        "sisense_datamodel_server",
        "sisense_datamodel_revision",
        "sisense_datamodel_last_build_time",
        "sisense_datamodel_last_successful_build_time",
        "sisense_datamodel_last_publish_time",
        "sisense_datamodel_type",
        "sisense_datamodel_relation_type",
        "sisense_datamodel_tables",
        "sisense_dashboards",
    ]

    @property
    def sisense_datamodel_table_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_table_count
        )

    @sisense_datamodel_table_count.setter
    def sisense_datamodel_table_count(
        self, sisense_datamodel_table_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_table_count = sisense_datamodel_table_count

    @property
    def sisense_datamodel_server(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_server
        )

    @sisense_datamodel_server.setter
    def sisense_datamodel_server(self, sisense_datamodel_server: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_server = sisense_datamodel_server

    @property
    def sisense_datamodel_revision(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_revision
        )

    @sisense_datamodel_revision.setter
    def sisense_datamodel_revision(self, sisense_datamodel_revision: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_revision = sisense_datamodel_revision

    @property
    def sisense_datamodel_last_build_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_last_build_time
        )

    @sisense_datamodel_last_build_time.setter
    def sisense_datamodel_last_build_time(
        self, sisense_datamodel_last_build_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_last_build_time = (
            sisense_datamodel_last_build_time
        )

    @property
    def sisense_datamodel_last_successful_build_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_last_successful_build_time
        )

    @sisense_datamodel_last_successful_build_time.setter
    def sisense_datamodel_last_successful_build_time(
        self, sisense_datamodel_last_successful_build_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_last_successful_build_time = (
            sisense_datamodel_last_successful_build_time
        )

    @property
    def sisense_datamodel_last_publish_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_last_publish_time
        )

    @sisense_datamodel_last_publish_time.setter
    def sisense_datamodel_last_publish_time(
        self, sisense_datamodel_last_publish_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_last_publish_time = (
            sisense_datamodel_last_publish_time
        )

    @property
    def sisense_datamodel_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sisense_datamodel_type
        )

    @sisense_datamodel_type.setter
    def sisense_datamodel_type(self, sisense_datamodel_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_type = sisense_datamodel_type

    @property
    def sisense_datamodel_relation_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_relation_type
        )

    @sisense_datamodel_relation_type.setter
    def sisense_datamodel_relation_type(
        self, sisense_datamodel_relation_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_relation_type = (
            sisense_datamodel_relation_type
        )

    @property
    def sisense_datamodel_tables(self) -> Optional[List[SisenseDatamodelTable]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_tables
        )

    @sisense_datamodel_tables.setter
    def sisense_datamodel_tables(
        self, sisense_datamodel_tables: Optional[List[SisenseDatamodelTable]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_tables = sisense_datamodel_tables

    @property
    def sisense_dashboards(self) -> Optional[List[SisenseDashboard]]:
        return None if self.attributes is None else self.attributes.sisense_dashboards

    @sisense_dashboards.setter
    def sisense_dashboards(self, sisense_dashboards: Optional[List[SisenseDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_dashboards = sisense_dashboards

    class Attributes(Sisense.Attributes):
        sisense_datamodel_table_count: Optional[int] = Field(
            default=None, description=""
        )
        sisense_datamodel_server: Optional[str] = Field(default=None, description="")
        sisense_datamodel_revision: Optional[str] = Field(default=None, description="")
        sisense_datamodel_last_build_time: Optional[datetime] = Field(
            default=None, description=""
        )
        sisense_datamodel_last_successful_build_time: Optional[datetime] = Field(
            default=None, description=""
        )
        sisense_datamodel_last_publish_time: Optional[datetime] = Field(
            default=None, description=""
        )
        sisense_datamodel_type: Optional[str] = Field(default=None, description="")
        sisense_datamodel_relation_type: Optional[str] = Field(
            default=None, description=""
        )
        sisense_datamodel_tables: Optional[List[SisenseDatamodelTable]] = Field(
            default=None, description=""
        )  # relationship
        sisense_dashboards: Optional[List[SisenseDashboard]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SisenseDatamodel.Attributes = Field(
        default_factory=lambda: SisenseDatamodel.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sisense_dashboard import SisenseDashboard  # noqa
from .sisense_datamodel_table import SisenseDatamodelTable  # noqa
