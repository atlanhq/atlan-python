# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import NumericField, RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .anaplan import Anaplan


class AnaplanWorkspace(Anaplan):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, name: str, connection_qualified_name: str) -> AnaplanWorkspace:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        attributes = AnaplanWorkspace.Attributes.create(
            name=name, connection_qualified_name=connection_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="AnaplanWorkspace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AnaplanWorkspace":
            raise ValueError("must be AnaplanWorkspace")
        return v

    def __setattr__(self, name, value):
        if name in AnaplanWorkspace._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ANAPLAN_WORKSPACE_CURRENT_SIZE: ClassVar[NumericField] = NumericField(
        "anaplanWorkspaceCurrentSize", "anaplanWorkspaceCurrentSize"
    )
    """
    Current Size of the AnaplanWorkspace from the source system, estimated in MB.
    """
    ANAPLAN_WORKSPACE_ALLOWANCE_SIZE: ClassVar[NumericField] = NumericField(
        "anaplanWorkspaceAllowanceSize", "anaplanWorkspaceAllowanceSize"
    )
    """
    Alloted Size quota for the AnaplanWorkspace from the source system, estimated in MB.
    """

    ANAPLAN_MODELS: ClassVar[RelationField] = RelationField("anaplanModels")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "anaplan_workspace_current_size",
        "anaplan_workspace_allowance_size",
        "anaplan_models",
    ]

    @property
    def anaplan_workspace_current_size(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.anaplan_workspace_current_size
        )

    @anaplan_workspace_current_size.setter
    def anaplan_workspace_current_size(
        self, anaplan_workspace_current_size: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_workspace_current_size = anaplan_workspace_current_size

    @property
    def anaplan_workspace_allowance_size(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.anaplan_workspace_allowance_size
        )

    @anaplan_workspace_allowance_size.setter
    def anaplan_workspace_allowance_size(
        self, anaplan_workspace_allowance_size: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_workspace_allowance_size = (
            anaplan_workspace_allowance_size
        )

    @property
    def anaplan_models(self) -> Optional[List[AnaplanModel]]:
        return None if self.attributes is None else self.attributes.anaplan_models

    @anaplan_models.setter
    def anaplan_models(self, anaplan_models: Optional[List[AnaplanModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_models = anaplan_models

    class Attributes(Anaplan.Attributes):
        anaplan_workspace_current_size: Optional[int] = Field(
            default=None, description=""
        )
        anaplan_workspace_allowance_size: Optional[int] = Field(
            default=None, description=""
        )
        anaplan_models: Optional[List[AnaplanModel]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls, *, name: str, connection_qualified_name: str
        ) -> AnaplanWorkspace.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )
            return AnaplanWorkspace.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
            )

    attributes: AnaplanWorkspace.Attributes = Field(
        default_factory=lambda: AnaplanWorkspace.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .anaplan_model import AnaplanModel  # noqa: E402, F401

AnaplanWorkspace.Attributes.update_forward_refs()
