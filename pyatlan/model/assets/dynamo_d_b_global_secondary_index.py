# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .dynamo_d_b_secondary_index import DynamoDBSecondaryIndex


class DynamoDBGlobalSecondaryIndex(DynamoDBSecondaryIndex):
    """Description"""

    type_name: str = Field(default="DynamoDBGlobalSecondaryIndex", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DynamoDBGlobalSecondaryIndex":
            raise ValueError("must be DynamoDBGlobalSecondaryIndex")
        return v

    def __setattr__(self, name, value):
        if name in DynamoDBGlobalSecondaryIndex._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DYNAMO_DB_TABLE: ClassVar[RelationField] = RelationField("dynamoDBTable")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dynamo_dbtable",
    ]

    @property
    def dynamo_dbtable(self) -> Optional[DynamoDBTable]:
        return None if self.attributes is None else self.attributes.dynamo_dbtable

    @dynamo_dbtable.setter
    def dynamo_dbtable(self, dynamo_dbtable: Optional[DynamoDBTable]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dynamo_dbtable = dynamo_dbtable

    class Attributes(DynamoDBSecondaryIndex.Attributes):
        dynamo_dbtable: Optional[DynamoDBTable] = Field(
            default=None, description=""
        )  # relationship

    attributes: DynamoDBGlobalSecondaryIndex.Attributes = Field(
        default_factory=lambda: DynamoDBGlobalSecondaryIndex.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .dynamo_dbtable import DynamoDBTable  # noqa
