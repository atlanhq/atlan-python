# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType, FileType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .resource import Resource


class File(Resource):
    """Description"""

    @classmethod
    @init_guid
    def creator(
        cls, *, name: str, connection_qualified_name: str, file_type: FileType
    ) -> File:
        return File(
            attributes=File.Attributes.create(
                name=name,
                connection_qualified_name=connection_qualified_name,
                file_type=file_type,
            )
        )

    @classmethod
    @init_guid
    def create(
        cls, *, name: str, connection_qualified_name: str, file_type: FileType
    ) -> File:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
            file_type=file_type,
        )

    type_name: str = Field(default="File", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "File":
            raise ValueError("must be File")
        return v

    def __setattr__(self, name, value):
        if name in File._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FILE_TYPE: ClassVar[KeywordField] = KeywordField("fileType", "fileType")
    """
    Type (extension) of the file.
    """
    FILE_PATH: ClassVar[KeywordField] = KeywordField("filePath", "filePath")
    """
    URL giving the online location where the file can be accessed.
    """

    FILE_ASSETS: ClassVar[RelationField] = RelationField("fileAssets")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "file_type",
        "file_path",
        "file_assets",
    ]

    @property
    def file_type(self) -> Optional[FileType]:
        return None if self.attributes is None else self.attributes.file_type

    @file_type.setter
    def file_type(self, file_type: Optional[FileType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.file_type = file_type

    @property
    def file_path(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.file_path

    @file_path.setter
    def file_path(self, file_path: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.file_path = file_path

    @property
    def file_assets(self) -> Optional[Asset]:
        return None if self.attributes is None else self.attributes.file_assets

    @file_assets.setter
    def file_assets(self, file_assets: Optional[Asset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.file_assets = file_assets

    class Attributes(Resource.Attributes):
        file_type: Optional[FileType] = Field(default=None, description="")
        file_path: Optional[str] = Field(default=None, description="")
        file_assets: Optional[Asset] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls, *, name: str, connection_qualified_name: str, file_type: FileType
        ) -> File.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name", "file_type"],
                [name, connection_qualified_name, file_type],
            )
            return File.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
                file_type=file_type,
            )

    attributes: File.Attributes = Field(
        default_factory=lambda: File.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .asset import Asset  # noqa
