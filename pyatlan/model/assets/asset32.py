# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, field_validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)
from pyatlan.model.structs import AzureTag

from .asset00 import AirflowTask, Process
from .asset28 import Azure


class ADLS(Azure):
    """Description"""

    type_name: str = Field("ADLS", frozen=False)

    @field_validator("type_name")
    @classmethod
    def validate_type_name(cls, v):
        if v != "ADLS":
            raise ValueError("must be ADLS")
        return v

    def __setattr__(self, name, value):
        if name in ADLS._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ADLS_ACCOUNT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "adlsAccountQualifiedName",
        "adlsAccountQualifiedName",
        "adlsAccountQualifiedName.text",
    )
    """
    TBC
    """
    AZURE_RESOURCE_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "azureResourceId", "azureResourceId", "azureResourceId.text"
    )
    """
    TBC
    """
    AZURE_LOCATION: ClassVar[KeywordField] = KeywordField(
        "azureLocation", "azureLocation"
    )
    """
    TBC
    """
    ADLS_ACCOUNT_SECONDARY_LOCATION: ClassVar[KeywordField] = KeywordField(
        "adlsAccountSecondaryLocation", "adlsAccountSecondaryLocation"
    )
    """
    TBC
    """
    AZURE_TAGS: ClassVar[KeywordField] = KeywordField("azureTags", "azureTags")
    """
    TBC
    """

    INPUT_TO_PROCESSES: ClassVar[RelationField] = RelationField("inputToProcesses")
    """
    TBC
    """
    OUTPUT_FROM_AIRFLOW_TASKS: ClassVar[RelationField] = RelationField(
        "outputFromAirflowTasks"
    )
    """
    TBC
    """
    INPUT_TO_AIRFLOW_TASKS: ClassVar[RelationField] = RelationField(
        "inputToAirflowTasks"
    )
    """
    TBC
    """
    OUTPUT_FROM_PROCESSES: ClassVar[RelationField] = RelationField(
        "outputFromProcesses"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "adls_account_qualified_name",
        "azure_resource_id",
        "azure_location",
        "adls_account_secondary_location",
        "azure_tags",
        "input_to_processes",
        "output_from_airflow_tasks",
        "input_to_airflow_tasks",
        "output_from_processes",
    ]

    @property
    def adls_account_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_qualified_name
        )

    @adls_account_qualified_name.setter
    def adls_account_qualified_name(self, adls_account_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_qualified_name = adls_account_qualified_name

    @property
    def azure_resource_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.azure_resource_id

    @azure_resource_id.setter
    def azure_resource_id(self, azure_resource_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_resource_id = azure_resource_id

    @property
    def azure_location(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.azure_location

    @azure_location.setter
    def azure_location(self, azure_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_location = azure_location

    @property
    def adls_account_secondary_location(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_secondary_location
        )

    @adls_account_secondary_location.setter
    def adls_account_secondary_location(
        self, adls_account_secondary_location: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_secondary_location = (
            adls_account_secondary_location
        )

    @property
    def azure_tags(self) -> Optional[list[AzureTag]]:
        return None if self.attributes is None else self.attributes.azure_tags

    @azure_tags.setter
    def azure_tags(self, azure_tags: Optional[list[AzureTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_tags = azure_tags

    @property
    def input_to_processes(self) -> Optional[list[Process]]:
        return None if self.attributes is None else self.attributes.input_to_processes

    @input_to_processes.setter
    def input_to_processes(self, input_to_processes: Optional[list[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_to_processes = input_to_processes

    @property
    def output_from_airflow_tasks(self) -> Optional[list[AirflowTask]]:
        return (
            None
            if self.attributes is None
            else self.attributes.output_from_airflow_tasks
        )

    @output_from_airflow_tasks.setter
    def output_from_airflow_tasks(
        self, output_from_airflow_tasks: Optional[list[AirflowTask]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_from_airflow_tasks = output_from_airflow_tasks

    @property
    def input_to_airflow_tasks(self) -> Optional[list[AirflowTask]]:
        return (
            None if self.attributes is None else self.attributes.input_to_airflow_tasks
        )

    @input_to_airflow_tasks.setter
    def input_to_airflow_tasks(
        self, input_to_airflow_tasks: Optional[list[AirflowTask]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_to_airflow_tasks = input_to_airflow_tasks

    @property
    def output_from_processes(self) -> Optional[list[Process]]:
        return (
            None if self.attributes is None else self.attributes.output_from_processes
        )

    @output_from_processes.setter
    def output_from_processes(self, output_from_processes: Optional[list[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_from_processes = output_from_processes

    class Attributes(Azure.Attributes):
        adls_account_qualified_name: Optional[str] = Field(
            default=None, description="", alias="adlsAccountQualifiedName"
        )

        azure_resource_id: Optional[str] = Field(
            default=None, description="", alias="azureResourceId"
        )

        azure_location: Optional[str] = Field(
            default=None, description="", alias="azureLocation"
        )

        adls_account_secondary_location: Optional[str] = Field(
            default=None, description="", alias="adlsAccountSecondaryLocation"
        )

        azure_tags: Optional[list[AzureTag]] = Field(
            default=None, description="", alias="azureTags"
        )

        input_to_processes: Optional[list[Process]] = Field(
            default=None, description="", alias="inputToProcesses"
        )  # relationship
        output_from_airflow_tasks: Optional[list[AirflowTask]] = Field(
            default=None, description="", alias="outputFromAirflowTasks"
        )  # relationship
        input_to_airflow_tasks: Optional[list[AirflowTask]] = Field(
            default=None, description="", alias="inputToAirflowTasks"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            default=None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "ADLS.Attributes" = Field(
        default_factory=lambda: ADLS.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )
