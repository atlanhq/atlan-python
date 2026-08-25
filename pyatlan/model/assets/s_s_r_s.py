# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField

from .core.b_i import BI


class SSRS(BI):
    """Description"""

    type_name: str = Field(default="SSRS", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SSRS":
            raise ValueError("must be SSRS")
        return v

    def __setattr__(self, name, value):
        if name in SSRS._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SSRS_PATH: ClassVar[KeywordField] = KeywordField("ssrsPath", "ssrsPath")
    """
    Path of the asset in SSRS.
    """
    SSRS_USED_IN_REPORTS: ClassVar[BooleanField] = BooleanField(
        "ssrsUsedInReports", "ssrsUsedInReports"
    )
    """
    Whether the asset is used in a report.
    """
    SSRS_HIDDEN: ClassVar[BooleanField] = BooleanField("ssrsHidden", "ssrsHidden")
    """
    Whether the asset is hidden.
    """
    SSRS_TABLE_NAME: ClassVar[KeywordField] = KeywordField(
        "ssrsTableName", "ssrsTableName"
    )
    """
    Table name associated with this asset in the source system.
    """
    SSRS_SCHEMA_NAME: ClassVar[KeywordField] = KeywordField(
        "ssrsSchemaName", "ssrsSchemaName"
    )
    """
    Schema name associated with this asset in the source system.
    """
    SSRS_CATALOG_NAME: ClassVar[KeywordField] = KeywordField(
        "ssrsCatalogName", "ssrsCatalogName"
    )
    """
    Catalog name associated with this asset in the source system.
    """
    SSRS_REFERENCE_REPOSITORY_ID: ClassVar[KeywordField] = KeywordField(
        "ssrsReferenceRepositoryId", "ssrsReferenceRepositoryId"
    )
    """
    Reference repository ID for this asset.
    """
    SSRS_PARENT_FOLDER_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "ssrsParentFolderQualifiedName", "ssrsParentFolderQualifiedName"
    )
    """
    Unique name of the immediate parent folder containing this asset.
    """
    SSRS_FOLDER_HIERARCHIES: ClassVar[KeywordField] = KeywordField(
        "ssrsFolderHierarchies", "ssrsFolderHierarchies"
    )
    """
    Ordered array of folder assets with qualified name and name representing the complete folder hierarchy path for this asset, from immediate parent to root folder.
    """  # noqa: E501
    SSRS_REPORT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "ssrsReportQualifiedName", "ssrsReportQualifiedName"
    )
    """
    Unique name of the Report asset that contains this asset.
    """
    SSRS_REPORT_NAME: ClassVar[KeywordField] = KeywordField(
        "ssrsReportName", "ssrsReportName"
    )
    """
    Simple name of the Report asset that contains this asset.
    """
    SSRS_DATA_SET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "ssrsDataSetQualifiedName", "ssrsDataSetQualifiedName"
    )
    """
    Unique name of the DataSet asset that contains this asset.
    """
    SSRS_DATA_SET_NAME: ClassVar[KeywordField] = KeywordField(
        "ssrsDataSetName", "ssrsDataSetName"
    )
    """
    Simple name of the DataSet asset that contains this asset.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "ssrs_path",
        "ssrs_used_in_reports",
        "ssrs_hidden",
        "ssrs_table_name",
        "ssrs_schema_name",
        "ssrs_catalog_name",
        "ssrs_reference_repository_id",
        "ssrs_parent_folder_qualified_name",
        "ssrs_folder_hierarchies",
        "ssrs_report_qualified_name",
        "ssrs_report_name",
        "ssrs_data_set_qualified_name",
        "ssrs_data_set_name",
    ]

    @property
    def ssrs_path(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.ssrs_path

    @ssrs_path.setter
    def ssrs_path(self, ssrs_path: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_path = ssrs_path

    @property
    def ssrs_used_in_reports(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.ssrs_used_in_reports

    @ssrs_used_in_reports.setter
    def ssrs_used_in_reports(self, ssrs_used_in_reports: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_used_in_reports = ssrs_used_in_reports

    @property
    def ssrs_hidden(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.ssrs_hidden

    @ssrs_hidden.setter
    def ssrs_hidden(self, ssrs_hidden: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_hidden = ssrs_hidden

    @property
    def ssrs_table_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.ssrs_table_name

    @ssrs_table_name.setter
    def ssrs_table_name(self, ssrs_table_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_table_name = ssrs_table_name

    @property
    def ssrs_schema_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.ssrs_schema_name

    @ssrs_schema_name.setter
    def ssrs_schema_name(self, ssrs_schema_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_schema_name = ssrs_schema_name

    @property
    def ssrs_catalog_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.ssrs_catalog_name

    @ssrs_catalog_name.setter
    def ssrs_catalog_name(self, ssrs_catalog_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_catalog_name = ssrs_catalog_name

    @property
    def ssrs_reference_repository_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_reference_repository_id
        )

    @ssrs_reference_repository_id.setter
    def ssrs_reference_repository_id(self, ssrs_reference_repository_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_reference_repository_id = ssrs_reference_repository_id

    @property
    def ssrs_parent_folder_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_parent_folder_qualified_name
        )

    @ssrs_parent_folder_qualified_name.setter
    def ssrs_parent_folder_qualified_name(
        self, ssrs_parent_folder_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_parent_folder_qualified_name = (
            ssrs_parent_folder_qualified_name
        )

    @property
    def ssrs_folder_hierarchies(self) -> Optional[List[Dict[str, str]]]:
        return (
            None if self.attributes is None else self.attributes.ssrs_folder_hierarchies
        )

    @ssrs_folder_hierarchies.setter
    def ssrs_folder_hierarchies(
        self, ssrs_folder_hierarchies: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_folder_hierarchies = ssrs_folder_hierarchies

    @property
    def ssrs_report_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_report_qualified_name
        )

    @ssrs_report_qualified_name.setter
    def ssrs_report_qualified_name(self, ssrs_report_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_report_qualified_name = ssrs_report_qualified_name

    @property
    def ssrs_report_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.ssrs_report_name

    @ssrs_report_name.setter
    def ssrs_report_name(self, ssrs_report_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_report_name = ssrs_report_name

    @property
    def ssrs_data_set_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_data_set_qualified_name
        )

    @ssrs_data_set_qualified_name.setter
    def ssrs_data_set_qualified_name(self, ssrs_data_set_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_data_set_qualified_name = ssrs_data_set_qualified_name

    @property
    def ssrs_data_set_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.ssrs_data_set_name

    @ssrs_data_set_name.setter
    def ssrs_data_set_name(self, ssrs_data_set_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_data_set_name = ssrs_data_set_name

    class Attributes(BI.Attributes):
        ssrs_path: Optional[str] = Field(default=None, description="")
        ssrs_used_in_reports: Optional[bool] = Field(default=None, description="")
        ssrs_hidden: Optional[bool] = Field(default=None, description="")
        ssrs_table_name: Optional[str] = Field(default=None, description="")
        ssrs_schema_name: Optional[str] = Field(default=None, description="")
        ssrs_catalog_name: Optional[str] = Field(default=None, description="")
        ssrs_reference_repository_id: Optional[str] = Field(
            default=None, description=""
        )
        ssrs_parent_folder_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        ssrs_folder_hierarchies: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        ssrs_report_qualified_name: Optional[str] = Field(default=None, description="")
        ssrs_report_name: Optional[str] = Field(default=None, description="")
        ssrs_data_set_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        ssrs_data_set_name: Optional[str] = Field(default=None, description="")

    attributes: SSRS.Attributes = Field(
        default_factory=lambda: SSRS.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


SSRS.Attributes.update_forward_refs()
