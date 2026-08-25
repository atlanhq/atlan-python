from __future__ import annotations

from typing import Any, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.assets import Asset
from pyatlan.model.assets.relations import RelationshipAttributes
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import SaveSemantic


class SnowflakeSemanticLogicalTableJoinsSnowflakeSemanticLogicalTableJoins(
    RelationshipAttributes
):
    type_name: str = Field(
        allow_mutation=False,
        default="snowflake_semantic_logical_table_joins_snowflake_semantic_logical_table_joins",
        description="Describing joins between semantic logical tables.",
    )
    attributes: SnowflakeSemanticLogicalTableJoinsSnowflakeSemanticLogicalTableJoins.Attributes = Field(  # type: ignore[name-defined]
        default_factory=lambda: (
            SnowflakeSemanticLogicalTableJoinsSnowflakeSemanticLogicalTableJoins.Attributes()
        ),
        description="Map of attributes in the instance and their values",
    )

    class Attributes(AtlanObject):
        snowflake_join_foreign_keys: Optional[Set[str]] = Field(
            default=None,
            description="Columns in the left table used for the join.",
        )
        snowflake_join_ref_keys: Optional[Set[str]] = Field(
            default=None,
            description="Columns in the right table used for the join.",
        )
        snowflake_join_name: Optional[str] = Field(
            default=None,
            description="Name of the semantic relationship between logical tables.",
        )

    def __init__(__pydantic_self__, **data: Any) -> None:
        if "attributes" not in data:
            data = {"attributes": data}
        super().__init__(**data)
        __pydantic_self__.__fields_set__.update(["attributes", "type_name"])

    class SnowflakeSemanticLogicalTableJoins(Asset):
        type_name: str = Field(
            default="snowflake_semantic_logical_table_joins_snowflake_semantic_logical_table_joins",
            description="Logical tables that join to this logical table.",
        )
        relationship_type: str = Field(
            default="snowflake_semantic_logical_table_joins_snowflake_semantic_logical_table_joins",
            description="Fixed typeName for snowflake_semantic_logical_table_joins_snowflake_semantic_logical_table_joins.",
        )
        relationship_attributes: SnowflakeSemanticLogicalTableJoinsSnowflakeSemanticLogicalTableJoins = Field(
            default=None,
            description="Attributes of the snowflake_semantic_logical_table_joins_snowflake_semantic_logical_table_joins.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    def snowflake_semantic_logical_table_joins(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> SnowflakeSemanticLogicalTableJoinsSnowflakeSemanticLogicalTableJoins.SnowflakeSemanticLogicalTableJoins:
        """
        Build the SnowflakeSemanticLogicalTableJoinsSnowflakeSemanticLogicalTableJoins relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return SnowflakeSemanticLogicalTableJoinsSnowflakeSemanticLogicalTableJoins.SnowflakeSemanticLogicalTableJoins._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return SnowflakeSemanticLogicalTableJoinsSnowflakeSemanticLogicalTableJoins.SnowflakeSemanticLogicalTableJoins._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )


SnowflakeSemanticLogicalTableJoinsSnowflakeSemanticLogicalTableJoins.SnowflakeSemanticLogicalTableJoins.update_forward_refs()
SnowflakeSemanticLogicalTableJoinsSnowflakeSemanticLogicalTableJoins.update_forward_refs()
