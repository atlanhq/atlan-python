# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, KeywordTextField

from .asset18 import BI


class Mode(BI):
    """Description"""

    type_name: str = Field("Mode", allow_mutation=False)

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
    TBC
    """
    MODE_TOKEN: ClassVar[KeywordTextField] = KeywordTextField(
        "modeToken", "modeToken", "modeToken.text"
    )
    """
    TBC
    """
    MODE_WORKSPACE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "modeWorkspaceName", "modeWorkspaceName.keyword", "modeWorkspaceName"
    )
    """
    TBC
    """
    MODE_WORKSPACE_USERNAME: ClassVar[KeywordTextField] = KeywordTextField(
        "modeWorkspaceUsername", "modeWorkspaceUsername", "modeWorkspaceUsername.text"
    )
    """
    TBC
    """
    MODE_WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "modeWorkspaceQualifiedName",
        "modeWorkspaceQualifiedName",
        "modeWorkspaceQualifiedName.text",
    )
    """
    TBC
    """
    MODE_REPORT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "modeReportName", "modeReportName.keyword", "modeReportName"
    )
    """
    TBC
    """
    MODE_REPORT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "modeReportQualifiedName",
        "modeReportQualifiedName",
        "modeReportQualifiedName.text",
    )
    """
    TBC
    """
    MODE_QUERY_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "modeQueryName", "modeQueryName.keyword", "modeQueryName"
    )
    """
    TBC
    """
    MODE_QUERY_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "modeQueryQualifiedName",
        "modeQueryQualifiedName",
        "modeQueryQualifiedName.text",
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
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
        mode_id: Optional[str] = Field(None, description="", alias="modeId")
        mode_token: Optional[str] = Field(None, description="", alias="modeToken")
        mode_workspace_name: Optional[str] = Field(
            None, description="", alias="modeWorkspaceName"
        )
        mode_workspace_username: Optional[str] = Field(
            None, description="", alias="modeWorkspaceUsername"
        )
        mode_workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="modeWorkspaceQualifiedName"
        )
        mode_report_name: Optional[str] = Field(
            None, description="", alias="modeReportName"
        )
        mode_report_qualified_name: Optional[str] = Field(
            None, description="", alias="modeReportQualifiedName"
        )
        mode_query_name: Optional[str] = Field(
            None, description="", alias="modeQueryName"
        )
        mode_query_qualified_name: Optional[str] = Field(
            None, description="", alias="modeQueryQualifiedName"
        )

    attributes: "Mode.Attributes" = Field(
        default_factory=lambda: Mode.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


Mode.Attributes.update_forward_refs()
