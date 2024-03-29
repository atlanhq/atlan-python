# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, KeywordTextField

from .b_i import BI


class Mode(BI):
    """Description"""

    type_name: str = Field(default="Mode", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Mode":
            raise ValueError("must be Mode")
        return v

    def __setattr__(self, name, value):
        if name in Mode._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MODE_ID: ClassVar[KeywordField] = KeywordField("modeId", "modeId")
    """

    """
    MODE_TOKEN: ClassVar[KeywordTextField] = KeywordTextField(
        "modeToken", "modeToken", "modeToken.text"
    )
    """

    """
    MODE_WORKSPACE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "modeWorkspaceName", "modeWorkspaceName.keyword", "modeWorkspaceName"
    )
    """

    """
    MODE_WORKSPACE_USERNAME: ClassVar[KeywordTextField] = KeywordTextField(
        "modeWorkspaceUsername", "modeWorkspaceUsername", "modeWorkspaceUsername.text"
    )
    """

    """
    MODE_WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "modeWorkspaceQualifiedName",
        "modeWorkspaceQualifiedName",
        "modeWorkspaceQualifiedName.text",
    )
    """

    """
    MODE_REPORT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "modeReportName", "modeReportName.keyword", "modeReportName"
    )
    """

    """
    MODE_REPORT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "modeReportQualifiedName",
        "modeReportQualifiedName",
        "modeReportQualifiedName.text",
    )
    """

    """
    MODE_QUERY_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "modeQueryName", "modeQueryName.keyword", "modeQueryName"
    )
    """

    """
    MODE_QUERY_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "modeQueryQualifiedName",
        "modeQueryQualifiedName",
        "modeQueryQualifiedName.text",
    )
    """

    """

    _convenience_properties: ClassVar[List[str]] = [
        "mode_id",
        "mode_token",
        "mode_workspace_name",
        "mode_workspace_username",
        "mode_workspace_qualified_name",
        "mode_report_name",
        "mode_report_qualified_name",
        "mode_query_name",
        "mode_query_qualified_name",
    ]

    @property
    def mode_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_id

    @mode_id.setter
    def mode_id(self, mode_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_id = mode_id

    @property
    def mode_token(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_token

    @mode_token.setter
    def mode_token(self, mode_token: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_token = mode_token

    @property
    def mode_workspace_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_workspace_name

    @mode_workspace_name.setter
    def mode_workspace_name(self, mode_workspace_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_workspace_name = mode_workspace_name

    @property
    def mode_workspace_username(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.mode_workspace_username
        )

    @mode_workspace_username.setter
    def mode_workspace_username(self, mode_workspace_username: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_workspace_username = mode_workspace_username

    @property
    def mode_workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mode_workspace_qualified_name
        )

    @mode_workspace_qualified_name.setter
    def mode_workspace_qualified_name(
        self, mode_workspace_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_workspace_qualified_name = mode_workspace_qualified_name

    @property
    def mode_report_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_report_name

    @mode_report_name.setter
    def mode_report_name(self, mode_report_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_report_name = mode_report_name

    @property
    def mode_report_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mode_report_qualified_name
        )

    @mode_report_qualified_name.setter
    def mode_report_qualified_name(self, mode_report_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_report_qualified_name = mode_report_qualified_name

    @property
    def mode_query_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_query_name

    @mode_query_name.setter
    def mode_query_name(self, mode_query_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_query_name = mode_query_name

    @property
    def mode_query_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mode_query_qualified_name
        )

    @mode_query_qualified_name.setter
    def mode_query_qualified_name(self, mode_query_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_query_qualified_name = mode_query_qualified_name

    class Attributes(BI.Attributes):
        mode_id: Optional[str] = Field(default=None, description="")
        mode_token: Optional[str] = Field(default=None, description="")
        mode_workspace_name: Optional[str] = Field(default=None, description="")
        mode_workspace_username: Optional[str] = Field(default=None, description="")
        mode_workspace_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        mode_report_name: Optional[str] = Field(default=None, description="")
        mode_report_qualified_name: Optional[str] = Field(default=None, description="")
        mode_query_name: Optional[str] = Field(default=None, description="")
        mode_query_qualified_name: Optional[str] = Field(default=None, description="")

    attributes: Mode.Attributes = Field(
        default_factory=lambda: Mode.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
