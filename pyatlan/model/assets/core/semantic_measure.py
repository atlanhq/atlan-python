# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField, TextField

from .semantic import Semantic


class SemanticMeasure(Semantic):
    """Description"""

    type_name: str = Field(default="SemanticMeasure", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SemanticMeasure":
            raise ValueError("must be SemanticMeasure")
        return v

    def __setattr__(self, name, value):
        if name in SemanticMeasure._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CATALOG_DATASET_GUID: ClassVar[KeywordField] = KeywordField(
        "catalogDatasetGuid", "catalogDatasetGuid"
    )
    """
    Unique identifier of the dataset this asset belongs to.
    """
    SEMANTIC_EXPRESSION: ClassVar[KeywordField] = KeywordField(
        "semanticExpression", "semanticExpression"
    )
    """
    Column name or SQL expression for the semantic field.
    """
    SEMANTIC_TYPE: ClassVar[KeywordField] = KeywordField("semanticType", "semanticType")
    """
    Detailed type of the semantic field (e.g., type of measure, type of dimension, or type of entity).
    """
    SEMANTIC_SYNONYMS: ClassVar[KeywordField] = KeywordField(
        "semanticSynonyms", "semanticSynonyms"
    )
    """
    Alternative names or terms for the semantic field.
    """
    SEMANTIC_SAMPLE_VALUES: ClassVar[TextField] = TextField(
        "semanticSampleValues", "semanticSampleValues"
    )
    """
    Sample values for the semantic field.
    """
    SEMANTIC_ACCESS_MODIFIER: ClassVar[KeywordField] = KeywordField(
        "semanticAccessModifier", "semanticAccessModifier"
    )
    """
    Access level for the semantic field (e.g., public_access/private_access).
    """
    SEMANTIC_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "semanticDataType", "semanticDataType"
    )
    """
    Data type of the semantic field.
    """
    SEMANTIC_LABELS: ClassVar[KeywordField] = KeywordField(
        "semanticLabels", "semanticLabels"
    )
    """
    Labels associated with the semantic field.
    """

    SEMANTIC_MODEL: ClassVar[RelationField] = RelationField("semanticModel")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "catalog_dataset_guid",
        "semantic_expression",
        "semantic_type",
        "semantic_synonyms",
        "semantic_sample_values",
        "semantic_access_modifier",
        "semantic_data_type",
        "semantic_labels",
        "semantic_model",
    ]

    @property
    def catalog_dataset_guid(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.catalog_dataset_guid

    @catalog_dataset_guid.setter
    def catalog_dataset_guid(self, catalog_dataset_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.catalog_dataset_guid = catalog_dataset_guid

    @property
    def semantic_expression(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.semantic_expression

    @semantic_expression.setter
    def semantic_expression(self, semantic_expression: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.semantic_expression = semantic_expression

    @property
    def semantic_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.semantic_type

    @semantic_type.setter
    def semantic_type(self, semantic_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.semantic_type = semantic_type

    @property
    def semantic_synonyms(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.semantic_synonyms

    @semantic_synonyms.setter
    def semantic_synonyms(self, semantic_synonyms: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.semantic_synonyms = semantic_synonyms

    @property
    def semantic_sample_values(self) -> Optional[Set[str]]:
        return (
            None if self.attributes is None else self.attributes.semantic_sample_values
        )

    @semantic_sample_values.setter
    def semantic_sample_values(self, semantic_sample_values: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.semantic_sample_values = semantic_sample_values

    @property
    def semantic_access_modifier(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.semantic_access_modifier
        )

    @semantic_access_modifier.setter
    def semantic_access_modifier(self, semantic_access_modifier: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.semantic_access_modifier = semantic_access_modifier

    @property
    def semantic_data_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.semantic_data_type

    @semantic_data_type.setter
    def semantic_data_type(self, semantic_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.semantic_data_type = semantic_data_type

    @property
    def semantic_labels(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.semantic_labels

    @semantic_labels.setter
    def semantic_labels(self, semantic_labels: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.semantic_labels = semantic_labels

    @property
    def semantic_model(self) -> Optional[SemanticModel]:
        return None if self.attributes is None else self.attributes.semantic_model

    @semantic_model.setter
    def semantic_model(self, semantic_model: Optional[SemanticModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.semantic_model = semantic_model

    class Attributes(Semantic.Attributes):
        catalog_dataset_guid: Optional[str] = Field(default=None, description="")
        semantic_expression: Optional[str] = Field(default=None, description="")
        semantic_type: Optional[str] = Field(default=None, description="")
        semantic_synonyms: Optional[Set[str]] = Field(default=None, description="")
        semantic_sample_values: Optional[Set[str]] = Field(default=None, description="")
        semantic_access_modifier: Optional[str] = Field(default=None, description="")
        semantic_data_type: Optional[str] = Field(default=None, description="")
        semantic_labels: Optional[Set[str]] = Field(default=None, description="")
        semantic_model: Optional[SemanticModel] = Field(
            default=None, description=""
        )  # relationship

    attributes: SemanticMeasure.Attributes = Field(
        default_factory=lambda: SemanticMeasure.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .semantic_model import SemanticModel  # noqa: E402, F401
