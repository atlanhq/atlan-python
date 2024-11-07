# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .detecti_data import DetectiData


class DetectiDataDossierElement(DetectiData):
    """Description"""

    type_name: str = Field(default="DetectiDataDossierElement", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DetectiDataDossierElement":
            raise ValueError("must be DetectiDataDossierElement")
        return v

    def __setattr__(self, name, value):
        if name in DetectiDataDossierElement._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DETECTI_DATA_COMPONENT_SCORE: ClassVar[NumericField] = NumericField(
        "detectiDataComponentScore", "detectiDataComponentScore"
    )
    """
    Score of this individual component of the Dossier.
    """

    DETECTI_DATA_DOSSIER: ClassVar[RelationField] = RelationField("detectiDataDossier")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "detecti_data_component_score",
        "detecti_data_dossier",
    ]

    @property
    def detecti_data_component_score(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.detecti_data_component_score
        )

    @detecti_data_component_score.setter
    def detecti_data_component_score(self, detecti_data_component_score: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.detecti_data_component_score = detecti_data_component_score

    @property
    def detecti_data_dossier(self) -> Optional[DetectiDataDossier]:
        return None if self.attributes is None else self.attributes.detecti_data_dossier

    @detecti_data_dossier.setter
    def detecti_data_dossier(self, detecti_data_dossier: Optional[DetectiDataDossier]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.detecti_data_dossier = detecti_data_dossier

    class Attributes(DetectiData.Attributes):
        detecti_data_component_score: Optional[int] = Field(
            default=None, description=""
        )
        detecti_data_dossier: Optional[DetectiDataDossier] = Field(
            default=None, description=""
        )  # relationship

    attributes: DetectiDataDossierElement.Attributes = Field(
        default_factory=lambda: DetectiDataDossierElement.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .detecti_data_dossier import DetectiDataDossier  # noqa

DetectiDataDossierElement.Attributes.update_forward_refs()
