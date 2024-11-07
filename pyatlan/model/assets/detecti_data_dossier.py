# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .detecti_data import DetectiData


class DetectiDataDossier(DetectiData):
    """Description"""

    type_name: str = Field(default="DetectiDataDossier", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DetectiDataDossier":
            raise ValueError("must be DetectiDataDossier")
        return v

    def __setattr__(self, name, value):
        if name in DetectiDataDossier._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DETECTI_DATA_PRIVACY_CLASSIFICATION: ClassVar[KeywordField] = KeywordField(
        "detectiDataPrivacyClassification", "detectiDataPrivacyClassification"
    )
    """
    Privacy classification for this combination of data.
    """
    DETECTI_DATA_TRUST_SCORE: ClassVar[NumericField] = NumericField(
        "detectiDataTrustScore", "detectiDataTrustScore"
    )
    """
    Overall trust score for the combination of assets.
    """

    DETECTI_DATA_DOSSIER_ELEMENTS: ClassVar[RelationField] = RelationField(
        "detectiDataDossierElements"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "detecti_data_privacy_classification",
        "detecti_data_trust_score",
        "detecti_data_dossier_elements",
    ]

    @property
    def detecti_data_privacy_classification(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.detecti_data_privacy_classification
        )

    @detecti_data_privacy_classification.setter
    def detecti_data_privacy_classification(
        self, detecti_data_privacy_classification: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.detecti_data_privacy_classification = (
            detecti_data_privacy_classification
        )

    @property
    def detecti_data_trust_score(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.detecti_data_trust_score
        )

    @detecti_data_trust_score.setter
    def detecti_data_trust_score(self, detecti_data_trust_score: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.detecti_data_trust_score = detecti_data_trust_score

    @property
    def detecti_data_dossier_elements(
        self,
    ) -> Optional[List[DetectiDataDossierElement]]:
        return (
            None
            if self.attributes is None
            else self.attributes.detecti_data_dossier_elements
        )

    @detecti_data_dossier_elements.setter
    def detecti_data_dossier_elements(
        self, detecti_data_dossier_elements: Optional[List[DetectiDataDossierElement]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.detecti_data_dossier_elements = detecti_data_dossier_elements

    class Attributes(DetectiData.Attributes):
        detecti_data_privacy_classification: Optional[str] = Field(
            default=None, description=""
        )
        detecti_data_trust_score: Optional[int] = Field(default=None, description="")
        detecti_data_dossier_elements: Optional[List[DetectiDataDossierElement]] = (
            Field(default=None, description="")
        )  # relationship

    attributes: DetectiDataDossier.Attributes = Field(
        default_factory=lambda: DetectiDataDossier.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .detecti_data_dossier_element import DetectiDataDossierElement  # noqa

DetectiDataDossier.Attributes.update_forward_refs()
