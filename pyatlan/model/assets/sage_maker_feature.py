# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField, RelationField

from .sage_maker import SageMaker


class SageMakerFeature(SageMaker):
    """Description"""

    type_name: str = Field(default="SageMakerFeature", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SageMakerFeature":
            raise ValueError("must be SageMakerFeature")
        return v

    def __setattr__(self, name, value):
        if name in SageMakerFeature._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAGE_MAKER_FEATURE_GROUP_NAME: ClassVar[KeywordField] = KeywordField(
        "sageMakerFeatureGroupName", "sageMakerFeatureGroupName"
    )
    """
    Name of the Feature Group that contains this feature.
    """
    SAGE_MAKER_FEATURE_GROUP_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "sageMakerFeatureGroupQualifiedName", "sageMakerFeatureGroupQualifiedName"
    )
    """
    Qualified name of the Feature Group that contains this feature.
    """
    SAGE_MAKER_FEATURE_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "sageMakerFeatureDataType", "sageMakerFeatureDataType"
    )
    """
    Data type of the feature (e.g., String, Integral, Fractional).
    """
    SAGE_MAKER_FEATURE_IS_RECORD_IDENTIFIER: ClassVar[BooleanField] = BooleanField(
        "sageMakerFeatureIsRecordIdentifier", "sageMakerFeatureIsRecordIdentifier"
    )
    """
    Whether this feature serves as the record identifier for the Feature Group.
    """

    SAGE_MAKER_FEATURE_GROUP: ClassVar[RelationField] = RelationField(
        "sageMakerFeatureGroup"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sage_maker_feature_group_name",
        "sage_maker_feature_group_qualified_name",
        "sage_maker_feature_data_type",
        "sage_maker_feature_is_record_identifier",
        "sage_maker_feature_group",
    ]

    @property
    def sage_maker_feature_group_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_feature_group_name
        )

    @sage_maker_feature_group_name.setter
    def sage_maker_feature_group_name(
        self, sage_maker_feature_group_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_feature_group_name = sage_maker_feature_group_name

    @property
    def sage_maker_feature_group_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_feature_group_qualified_name
        )

    @sage_maker_feature_group_qualified_name.setter
    def sage_maker_feature_group_qualified_name(
        self, sage_maker_feature_group_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_feature_group_qualified_name = (
            sage_maker_feature_group_qualified_name
        )

    @property
    def sage_maker_feature_data_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_feature_data_type
        )

    @sage_maker_feature_data_type.setter
    def sage_maker_feature_data_type(self, sage_maker_feature_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_feature_data_type = sage_maker_feature_data_type

    @property
    def sage_maker_feature_is_record_identifier(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_feature_is_record_identifier
        )

    @sage_maker_feature_is_record_identifier.setter
    def sage_maker_feature_is_record_identifier(
        self, sage_maker_feature_is_record_identifier: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_feature_is_record_identifier = (
            sage_maker_feature_is_record_identifier
        )

    @property
    def sage_maker_feature_group(self) -> Optional[SageMakerFeatureGroup]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_feature_group
        )

    @sage_maker_feature_group.setter
    def sage_maker_feature_group(
        self, sage_maker_feature_group: Optional[SageMakerFeatureGroup]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_feature_group = sage_maker_feature_group

    class Attributes(SageMaker.Attributes):
        sage_maker_feature_group_name: Optional[str] = Field(
            default=None, description=""
        )
        sage_maker_feature_group_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sage_maker_feature_data_type: Optional[str] = Field(
            default=None, description=""
        )
        sage_maker_feature_is_record_identifier: Optional[bool] = Field(
            default=None, description=""
        )
        sage_maker_feature_group: Optional[SageMakerFeatureGroup] = Field(
            default=None, description=""
        )  # relationship

    attributes: SageMakerFeature.Attributes = Field(
        default_factory=lambda: SageMakerFeature.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sage_maker_feature_group import SageMakerFeatureGroup  # noqa: E402, F401

SageMakerFeature.Attributes.update_forward_refs()
