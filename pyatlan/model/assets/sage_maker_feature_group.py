# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .sage_maker import SageMaker


class SageMakerFeatureGroup(SageMaker):
    """Description"""

    type_name: str = Field(default="SageMakerFeatureGroup", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SageMakerFeatureGroup":
            raise ValueError("must be SageMakerFeatureGroup")
        return v

    def __setattr__(self, name, value):
        if name in SageMakerFeatureGroup._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAGE_MAKER_FEATURE_GROUP_STATUS: ClassVar[KeywordField] = KeywordField(
        "sageMakerFeatureGroupStatus", "sageMakerFeatureGroupStatus"
    )
    """
    Current status of the Feature Group (e.g., Created, Creating, Failed).
    """
    SAGE_MAKER_FEATURE_GROUP_RECORD_ID_NAME: ClassVar[KeywordField] = KeywordField(
        "sageMakerFeatureGroupRecordIdName", "sageMakerFeatureGroupRecordIdName"
    )
    """
    Name of the feature that serves as the record identifier.
    """
    SAGE_MAKER_FEATURE_GROUP_GLUE_DATABASE_NAME: ClassVar[KeywordField] = KeywordField(
        "sageMakerFeatureGroupGlueDatabaseName", "sageMakerFeatureGroupGlueDatabaseName"
    )
    """
    AWS Glue database name associated with this Feature Group.
    """
    SAGE_MAKER_FEATURE_GROUP_GLUE_TABLE_NAME: ClassVar[KeywordField] = KeywordField(
        "sageMakerFeatureGroupGlueTableName", "sageMakerFeatureGroupGlueTableName"
    )
    """
    AWS Glue table name associated with this Feature Group.
    """
    SAGE_MAKER_FEATURE_GROUP_FEATURE_COUNT: ClassVar[NumericField] = NumericField(
        "sageMakerFeatureGroupFeatureCount", "sageMakerFeatureGroupFeatureCount"
    )
    """
    Number of features in this Feature Group.
    """

    SAGE_MAKER_FEATURES: ClassVar[RelationField] = RelationField("sageMakerFeatures")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sage_maker_feature_group_status",
        "sage_maker_feature_group_record_id_name",
        "sage_maker_feature_group_glue_database_name",
        "sage_maker_feature_group_glue_table_name",
        "sage_maker_feature_group_feature_count",
        "sage_maker_features",
    ]

    @property
    def sage_maker_feature_group_status(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_feature_group_status
        )

    @sage_maker_feature_group_status.setter
    def sage_maker_feature_group_status(
        self, sage_maker_feature_group_status: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_feature_group_status = (
            sage_maker_feature_group_status
        )

    @property
    def sage_maker_feature_group_record_id_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_feature_group_record_id_name
        )

    @sage_maker_feature_group_record_id_name.setter
    def sage_maker_feature_group_record_id_name(
        self, sage_maker_feature_group_record_id_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_feature_group_record_id_name = (
            sage_maker_feature_group_record_id_name
        )

    @property
    def sage_maker_feature_group_glue_database_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_feature_group_glue_database_name
        )

    @sage_maker_feature_group_glue_database_name.setter
    def sage_maker_feature_group_glue_database_name(
        self, sage_maker_feature_group_glue_database_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_feature_group_glue_database_name = (
            sage_maker_feature_group_glue_database_name
        )

    @property
    def sage_maker_feature_group_glue_table_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_feature_group_glue_table_name
        )

    @sage_maker_feature_group_glue_table_name.setter
    def sage_maker_feature_group_glue_table_name(
        self, sage_maker_feature_group_glue_table_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_feature_group_glue_table_name = (
            sage_maker_feature_group_glue_table_name
        )

    @property
    def sage_maker_feature_group_feature_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_feature_group_feature_count
        )

    @sage_maker_feature_group_feature_count.setter
    def sage_maker_feature_group_feature_count(
        self, sage_maker_feature_group_feature_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_feature_group_feature_count = (
            sage_maker_feature_group_feature_count
        )

    @property
    def sage_maker_features(self) -> Optional[List[SageMakerFeature]]:
        return None if self.attributes is None else self.attributes.sage_maker_features

    @sage_maker_features.setter
    def sage_maker_features(
        self, sage_maker_features: Optional[List[SageMakerFeature]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_features = sage_maker_features

    class Attributes(SageMaker.Attributes):
        sage_maker_feature_group_status: Optional[str] = Field(
            default=None, description=""
        )
        sage_maker_feature_group_record_id_name: Optional[str] = Field(
            default=None, description=""
        )
        sage_maker_feature_group_glue_database_name: Optional[str] = Field(
            default=None, description=""
        )
        sage_maker_feature_group_glue_table_name: Optional[str] = Field(
            default=None, description=""
        )
        sage_maker_feature_group_feature_count: Optional[int] = Field(
            default=None, description=""
        )
        sage_maker_features: Optional[List[SageMakerFeature]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SageMakerFeatureGroup.Attributes = Field(
        default_factory=lambda: SageMakerFeatureGroup.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sage_maker_feature import SageMakerFeature  # noqa: E402, F401

SageMakerFeatureGroup.Attributes.update_forward_refs()
