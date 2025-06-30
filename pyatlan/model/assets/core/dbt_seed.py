# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .dbt import Dbt


class DbtSeed(Dbt):
    """Description"""

    type_name: str = Field(default="DbtSeed", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DbtSeed":
            raise ValueError("must be DbtSeed")
        return v

    def __setattr__(self, name, value):
        if name in DbtSeed._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DBT_SEED_FILE_PATH: ClassVar[KeywordField] = KeywordField(
        "dbtSeedFilePath", "dbtSeedFilePath"
    )
    """
    File path of the dbt seed.
    """
    DBT_SEED_STATS: ClassVar[KeywordField] = KeywordField(
        "dbtSeedStats", "dbtSeedStats"
    )
    """
    Statistics of the dbt seed.
    """

    DBT_MODEL_COLUMNS: ClassVar[RelationField] = RelationField("dbtModelColumns")
    """
    TBC
    """
    DBT_SEED_SQL_ASSETS: ClassVar[RelationField] = RelationField("dbtSeedSqlAssets")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dbt_seed_file_path",
        "dbt_seed_stats",
        "dbt_model_columns",
        "dbt_seed_sql_assets",
    ]

    @property
    def dbt_seed_file_path(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_seed_file_path

    @dbt_seed_file_path.setter
    def dbt_seed_file_path(self, dbt_seed_file_path: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_seed_file_path = dbt_seed_file_path

    @property
    def dbt_seed_stats(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_seed_stats

    @dbt_seed_stats.setter
    def dbt_seed_stats(self, dbt_seed_stats: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_seed_stats = dbt_seed_stats

    @property
    def dbt_model_columns(self) -> Optional[List[DbtModelColumn]]:
        return None if self.attributes is None else self.attributes.dbt_model_columns

    @dbt_model_columns.setter
    def dbt_model_columns(self, dbt_model_columns: Optional[List[DbtModelColumn]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_columns = dbt_model_columns

    @property
    def dbt_seed_sql_assets(self) -> Optional[List[SQL]]:
        return None if self.attributes is None else self.attributes.dbt_seed_sql_assets

    @dbt_seed_sql_assets.setter
    def dbt_seed_sql_assets(self, dbt_seed_sql_assets: Optional[List[SQL]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_seed_sql_assets = dbt_seed_sql_assets

    class Attributes(Dbt.Attributes):
        dbt_seed_file_path: Optional[str] = Field(default=None, description="")
        dbt_seed_stats: Optional[str] = Field(default=None, description="")
        dbt_model_columns: Optional[List[DbtModelColumn]] = Field(
            default=None, description=""
        )  # relationship
        dbt_seed_sql_assets: Optional[List[SQL]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DbtSeed.Attributes = Field(
        default_factory=lambda: DbtSeed.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .dbt_model_column import DbtModelColumn  # noqa: E402, F401
from .s_q_l import SQL  # noqa: E402, F401
