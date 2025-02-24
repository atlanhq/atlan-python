# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    RelationField,
    TextField,
)

from .a_d_f import ADF


class AdfLinkedservice(ADF):
    """Description"""

    type_name: str = Field(default="AdfLinkedservice", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AdfLinkedservice":
            raise ValueError("must be AdfLinkedservice")
        return v

    def __setattr__(self, name, value):
        if name in AdfLinkedservice._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ADF_LINKEDSERVICE_TYPE: ClassVar[KeywordField] = KeywordField(
        "adfLinkedserviceType", "adfLinkedserviceType"
    )
    """
    Defines the type of the linked service.
    """
    ADF_LINKEDSERVICE_ANNOTATIONS: ClassVar[TextField] = TextField(
        "adfLinkedserviceAnnotations", "adfLinkedserviceAnnotations"
    )
    """
    The list of annotation assigned to a linked service.
    """
    ADF_LINKEDSERVICE_ACCOUNT_NAME: ClassVar[TextField] = TextField(
        "adfLinkedserviceAccountName", "adfLinkedserviceAccountName"
    )
    """
    Defines the name of the account used in the cosmos linked service.
    """
    ADF_LINKEDSERVICE_DATABASE_NAME: ClassVar[TextField] = TextField(
        "adfLinkedserviceDatabaseName", "adfLinkedserviceDatabaseName"
    )
    """
    Defines the name of the database used in the cosmos, snowflake linked service.
    """
    ADF_LINKEDSERVICE_VERSION_ABOVE: ClassVar[BooleanField] = BooleanField(
        "adfLinkedserviceVersionAbove", "adfLinkedserviceVersionAbove"
    )
    """
    Indicates whether the service version is above 3.2 or not in the cosmos linked service.
    """
    ADF_LINKEDSERVICE_VERSION: ClassVar[TextField] = TextField(
        "adfLinkedserviceVersion", "adfLinkedserviceVersion"
    )
    """
    Defines the version of the linked service in the cosmos linked service.
    """
    ADF_LINKEDSERVICE_AZURE_CLOUD_TYPE: ClassVar[TextField] = TextField(
        "adfLinkedserviceAzureCloudType", "adfLinkedserviceAzureCloudType"
    )
    """
    Defines the type of cloud being used in the ADLS linked service.
    """
    ADF_LINKEDSERVICE_CREDENTIAL_TYPE: ClassVar[TextField] = TextField(
        "adfLinkedserviceCredentialType", "adfLinkedserviceCredentialType"
    )
    """
    Defines the type of credential, authentication being used in the ADLS, snowflake, azure sql linked service.
    """
    ADF_LINKEDSERVICE_TENANT: ClassVar[TextField] = TextField(
        "adfLinkedserviceTenant", "adfLinkedserviceTenant"
    )
    """
    Defines the tenant of cloud being used in the ADLS linked service.
    """
    ADF_LINKEDSERVICE_DOMAIN_ENDPOINT: ClassVar[TextField] = TextField(
        "adfLinkedserviceDomainEndpoint", "adfLinkedserviceDomainEndpoint"
    )
    """
    Defines the url, domain, account_identifier, server in the ADLS, Azure databricks delta lake, snowflake, azure sql linked service.
    """  # noqa: E501
    ADF_LINKEDSERVICE_CLUSTER_ID: ClassVar[TextField] = TextField(
        "adfLinkedserviceClusterId", "adfLinkedserviceClusterId"
    )
    """
    Defines the cluster id in the Azure databricks delta lake linked service.
    """
    ADF_LINKEDSERVICE_RESOURCE_ID: ClassVar[TextField] = TextField(
        "adfLinkedserviceResourceId", "adfLinkedserviceResourceId"
    )
    """
    Defines the resource id in the Azure databricks delta lake linked service.
    """
    ADF_LINKEDSERVICE_USER_NAME: ClassVar[TextField] = TextField(
        "adfLinkedserviceUserName", "adfLinkedserviceUserName"
    )
    """
    Defines the name of the db user in the snowflake linked service.
    """
    ADF_LINKEDSERVICE_WAREHOUSE_NAME: ClassVar[TextField] = TextField(
        "adfLinkedserviceWarehouseName", "adfLinkedserviceWarehouseName"
    )
    """
    Defines the name of the warehouse in the snowflake linked service.
    """
    ADF_LINKEDSERVICE_ROLE_NAME: ClassVar[TextField] = TextField(
        "adfLinkedserviceRoleName", "adfLinkedserviceRoleName"
    )
    """
    Defines the name of the role in the snowflake linked service.
    """

    ADF_DATASETS: ClassVar[RelationField] = RelationField("adfDatasets")
    """
    TBC
    """
    ADF_ACTIVITIES: ClassVar[RelationField] = RelationField("adfActivities")
    """
    TBC
    """
    ADF_DATAFLOWS: ClassVar[RelationField] = RelationField("adfDataflows")
    """
    TBC
    """
    ADF_PIPELINES: ClassVar[RelationField] = RelationField("adfPipelines")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "adf_linkedservice_type",
        "adf_linkedservice_annotations",
        "adf_linkedservice_account_name",
        "adf_linkedservice_database_name",
        "adf_linkedservice_version_above",
        "adf_linkedservice_version",
        "adf_linkedservice_azure_cloud_type",
        "adf_linkedservice_credential_type",
        "adf_linkedservice_tenant",
        "adf_linkedservice_domain_endpoint",
        "adf_linkedservice_cluster_id",
        "adf_linkedservice_resource_id",
        "adf_linkedservice_user_name",
        "adf_linkedservice_warehouse_name",
        "adf_linkedservice_role_name",
        "adf_datasets",
        "adf_activities",
        "adf_dataflows",
        "adf_pipelines",
    ]

    @property
    def adf_linkedservice_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.adf_linkedservice_type
        )

    @adf_linkedservice_type.setter
    def adf_linkedservice_type(self, adf_linkedservice_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_linkedservice_type = adf_linkedservice_type

    @property
    def adf_linkedservice_annotations(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_linkedservice_annotations
        )

    @adf_linkedservice_annotations.setter
    def adf_linkedservice_annotations(
        self, adf_linkedservice_annotations: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_linkedservice_annotations = adf_linkedservice_annotations

    @property
    def adf_linkedservice_account_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_linkedservice_account_name
        )

    @adf_linkedservice_account_name.setter
    def adf_linkedservice_account_name(
        self, adf_linkedservice_account_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_linkedservice_account_name = adf_linkedservice_account_name

    @property
    def adf_linkedservice_database_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_linkedservice_database_name
        )

    @adf_linkedservice_database_name.setter
    def adf_linkedservice_database_name(
        self, adf_linkedservice_database_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_linkedservice_database_name = (
            adf_linkedservice_database_name
        )

    @property
    def adf_linkedservice_version_above(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_linkedservice_version_above
        )

    @adf_linkedservice_version_above.setter
    def adf_linkedservice_version_above(
        self, adf_linkedservice_version_above: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_linkedservice_version_above = (
            adf_linkedservice_version_above
        )

    @property
    def adf_linkedservice_version(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_linkedservice_version
        )

    @adf_linkedservice_version.setter
    def adf_linkedservice_version(self, adf_linkedservice_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_linkedservice_version = adf_linkedservice_version

    @property
    def adf_linkedservice_azure_cloud_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_linkedservice_azure_cloud_type
        )

    @adf_linkedservice_azure_cloud_type.setter
    def adf_linkedservice_azure_cloud_type(
        self, adf_linkedservice_azure_cloud_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_linkedservice_azure_cloud_type = (
            adf_linkedservice_azure_cloud_type
        )

    @property
    def adf_linkedservice_credential_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_linkedservice_credential_type
        )

    @adf_linkedservice_credential_type.setter
    def adf_linkedservice_credential_type(
        self, adf_linkedservice_credential_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_linkedservice_credential_type = (
            adf_linkedservice_credential_type
        )

    @property
    def adf_linkedservice_tenant(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_linkedservice_tenant
        )

    @adf_linkedservice_tenant.setter
    def adf_linkedservice_tenant(self, adf_linkedservice_tenant: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_linkedservice_tenant = adf_linkedservice_tenant

    @property
    def adf_linkedservice_domain_endpoint(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_linkedservice_domain_endpoint
        )

    @adf_linkedservice_domain_endpoint.setter
    def adf_linkedservice_domain_endpoint(
        self, adf_linkedservice_domain_endpoint: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_linkedservice_domain_endpoint = (
            adf_linkedservice_domain_endpoint
        )

    @property
    def adf_linkedservice_cluster_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_linkedservice_cluster_id
        )

    @adf_linkedservice_cluster_id.setter
    def adf_linkedservice_cluster_id(self, adf_linkedservice_cluster_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_linkedservice_cluster_id = adf_linkedservice_cluster_id

    @property
    def adf_linkedservice_resource_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_linkedservice_resource_id
        )

    @adf_linkedservice_resource_id.setter
    def adf_linkedservice_resource_id(
        self, adf_linkedservice_resource_id: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_linkedservice_resource_id = adf_linkedservice_resource_id

    @property
    def adf_linkedservice_user_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_linkedservice_user_name
        )

    @adf_linkedservice_user_name.setter
    def adf_linkedservice_user_name(self, adf_linkedservice_user_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_linkedservice_user_name = adf_linkedservice_user_name

    @property
    def adf_linkedservice_warehouse_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_linkedservice_warehouse_name
        )

    @adf_linkedservice_warehouse_name.setter
    def adf_linkedservice_warehouse_name(
        self, adf_linkedservice_warehouse_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_linkedservice_warehouse_name = (
            adf_linkedservice_warehouse_name
        )

    @property
    def adf_linkedservice_role_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_linkedservice_role_name
        )

    @adf_linkedservice_role_name.setter
    def adf_linkedservice_role_name(self, adf_linkedservice_role_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_linkedservice_role_name = adf_linkedservice_role_name

    @property
    def adf_datasets(self) -> Optional[List[AdfDataset]]:
        return None if self.attributes is None else self.attributes.adf_datasets

    @adf_datasets.setter
    def adf_datasets(self, adf_datasets: Optional[List[AdfDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_datasets = adf_datasets

    @property
    def adf_activities(self) -> Optional[List[AdfActivity]]:
        return None if self.attributes is None else self.attributes.adf_activities

    @adf_activities.setter
    def adf_activities(self, adf_activities: Optional[List[AdfActivity]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activities = adf_activities

    @property
    def adf_dataflows(self) -> Optional[List[AdfDataflow]]:
        return None if self.attributes is None else self.attributes.adf_dataflows

    @adf_dataflows.setter
    def adf_dataflows(self, adf_dataflows: Optional[List[AdfDataflow]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_dataflows = adf_dataflows

    @property
    def adf_pipelines(self) -> Optional[List[AdfPipeline]]:
        return None if self.attributes is None else self.attributes.adf_pipelines

    @adf_pipelines.setter
    def adf_pipelines(self, adf_pipelines: Optional[List[AdfPipeline]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_pipelines = adf_pipelines

    class Attributes(ADF.Attributes):
        adf_linkedservice_type: Optional[str] = Field(default=None, description="")
        adf_linkedservice_annotations: Optional[Set[str]] = Field(
            default=None, description=""
        )
        adf_linkedservice_account_name: Optional[str] = Field(
            default=None, description=""
        )
        adf_linkedservice_database_name: Optional[str] = Field(
            default=None, description=""
        )
        adf_linkedservice_version_above: Optional[bool] = Field(
            default=None, description=""
        )
        adf_linkedservice_version: Optional[str] = Field(default=None, description="")
        adf_linkedservice_azure_cloud_type: Optional[str] = Field(
            default=None, description=""
        )
        adf_linkedservice_credential_type: Optional[str] = Field(
            default=None, description=""
        )
        adf_linkedservice_tenant: Optional[str] = Field(default=None, description="")
        adf_linkedservice_domain_endpoint: Optional[str] = Field(
            default=None, description=""
        )
        adf_linkedservice_cluster_id: Optional[str] = Field(
            default=None, description=""
        )
        adf_linkedservice_resource_id: Optional[str] = Field(
            default=None, description=""
        )
        adf_linkedservice_user_name: Optional[str] = Field(default=None, description="")
        adf_linkedservice_warehouse_name: Optional[str] = Field(
            default=None, description=""
        )
        adf_linkedservice_role_name: Optional[str] = Field(default=None, description="")
        adf_datasets: Optional[List[AdfDataset]] = Field(
            default=None, description=""
        )  # relationship
        adf_activities: Optional[List[AdfActivity]] = Field(
            default=None, description=""
        )  # relationship
        adf_dataflows: Optional[List[AdfDataflow]] = Field(
            default=None, description=""
        )  # relationship
        adf_pipelines: Optional[List[AdfPipeline]] = Field(
            default=None, description=""
        )  # relationship

    attributes: AdfLinkedservice.Attributes = Field(
        default_factory=lambda: AdfLinkedservice.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .adf_activity import AdfActivity  # noqa
from .adf_dataflow import AdfDataflow  # noqa
from .adf_dataset import AdfDataset  # noqa
from .adf_pipeline import AdfPipeline  # noqa
