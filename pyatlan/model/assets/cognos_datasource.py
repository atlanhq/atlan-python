# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .cognos import Cognos


class CognosDatasource(Cognos):
    """Description"""

    type_name: str = Field(default="CognosDatasource", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CognosDatasource":
            raise ValueError("must be CognosDatasource")
        return v

    def __setattr__(self, name, value):
        if name in CognosDatasource._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COGNOS_DATASOURCE_CONNECTION_STRING: ClassVar[KeywordField] = KeywordField(
        "cognosDatasourceConnectionString", "cognosDatasourceConnectionString"
    )
    """
    Connection string of a cognos datasource
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cognos_datasource_connection_string",
    ]

    @property
    def cognos_datasource_connection_string(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cognos_datasource_connection_string
        )

    @cognos_datasource_connection_string.setter
    def cognos_datasource_connection_string(
        self, cognos_datasource_connection_string: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_datasource_connection_string = (
            cognos_datasource_connection_string
        )

    class Attributes(Cognos.Attributes):
        cognos_datasource_connection_string: Optional[str] = Field(
            default=None, description=""
        )

    attributes: CognosDatasource.Attributes = Field(
        default_factory=lambda: CognosDatasource.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
