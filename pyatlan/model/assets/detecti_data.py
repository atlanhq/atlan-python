# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, KeywordTextField

from .core.catalog import Catalog


class DetectiData(Catalog):
    """Description"""

    type_name: str = Field(default="DetectiData", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DetectiData":
            raise ValueError("must be DetectiData")
        return v

    def __setattr__(self, name, value):
        if name in DetectiData._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DETECTI_DATA_DOSSIER_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "detectiDataDossierName",
        "detectiDataDossierName.keyword",
        "detectiDataDossierName",
    )
    """
    Simple name of the dossier in which this asset exists, or empty if it is itself a dossier.
    """
    DETECTI_DATA_DOSSIER_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "detectiDataDossierQualifiedName", "detectiDataDossierQualifiedName"
    )
    """
    Unique name of the dossier in which this asset exists, or empty if it is itself a dossier.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "detecti_data_dossier_name",
        "detecti_data_dossier_qualified_name",
    ]

    @property
    def detecti_data_dossier_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.detecti_data_dossier_name
        )

    @detecti_data_dossier_name.setter
    def detecti_data_dossier_name(self, detecti_data_dossier_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.detecti_data_dossier_name = detecti_data_dossier_name

    @property
    def detecti_data_dossier_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.detecti_data_dossier_qualified_name
        )

    @detecti_data_dossier_qualified_name.setter
    def detecti_data_dossier_qualified_name(
        self, detecti_data_dossier_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.detecti_data_dossier_qualified_name = (
            detecti_data_dossier_qualified_name
        )

    class Attributes(Catalog.Attributes):
        detecti_data_dossier_name: Optional[str] = Field(default=None, description="")
        detecti_data_dossier_qualified_name: Optional[str] = Field(
            default=None, description=""
        )

    attributes: DetectiData.Attributes = Field(
        default_factory=lambda: DetectiData.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


DetectiData.Attributes.update_forward_refs()
