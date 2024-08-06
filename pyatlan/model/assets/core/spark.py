# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import OpenLineageRunState
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField

from .catalog import Catalog


class Spark(Catalog):
    """Description"""

    type_name: str = Field(default="Spark", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Spark":
            raise ValueError("must be Spark")
        return v

    def __setattr__(self, name, value):
        if name in Spark._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SPARK_RUN_VERSION: ClassVar[KeywordField] = KeywordField(
        "sparkRunVersion", "sparkRunVersion"
    )
    """
    Spark Version for the Spark Job run eg. 3.4.1
    """
    SPARK_RUN_OPEN_LINEAGE_VERSION: ClassVar[KeywordField] = KeywordField(
        "sparkRunOpenLineageVersion", "sparkRunOpenLineageVersion"
    )
    """
    OpenLineage Version of the Spark Job run eg. 1.1.0
    """
    SPARK_RUN_START_TIME: ClassVar[NumericField] = NumericField(
        "sparkRunStartTime", "sparkRunStartTime"
    )
    """
    Start time of the Spark Job eg. 1695673598218
    """
    SPARK_RUN_END_TIME: ClassVar[NumericField] = NumericField(
        "sparkRunEndTime", "sparkRunEndTime"
    )
    """
    End time of the Spark Job eg. 1695673598218
    """
    SPARK_RUN_OPEN_LINEAGE_STATE: ClassVar[KeywordField] = KeywordField(
        "sparkRunOpenLineageState", "sparkRunOpenLineageState"
    )
    """
    OpenLineage state of the Spark Job run eg. COMPLETE
    """

    _convenience_properties: ClassVar[List[str]] = [
        "spark_run_version",
        "spark_run_open_lineage_version",
        "spark_run_start_time",
        "spark_run_end_time",
        "spark_run_open_lineage_state",
    ]

    @property
    def spark_run_version(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.spark_run_version

    @spark_run_version.setter
    def spark_run_version(self, spark_run_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.spark_run_version = spark_run_version

    @property
    def spark_run_open_lineage_version(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.spark_run_open_lineage_version
        )

    @spark_run_open_lineage_version.setter
    def spark_run_open_lineage_version(
        self, spark_run_open_lineage_version: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.spark_run_open_lineage_version = spark_run_open_lineage_version

    @property
    def spark_run_start_time(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.spark_run_start_time

    @spark_run_start_time.setter
    def spark_run_start_time(self, spark_run_start_time: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.spark_run_start_time = spark_run_start_time

    @property
    def spark_run_end_time(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.spark_run_end_time

    @spark_run_end_time.setter
    def spark_run_end_time(self, spark_run_end_time: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.spark_run_end_time = spark_run_end_time

    @property
    def spark_run_open_lineage_state(self) -> Optional[OpenLineageRunState]:
        return (
            None
            if self.attributes is None
            else self.attributes.spark_run_open_lineage_state
        )

    @spark_run_open_lineage_state.setter
    def spark_run_open_lineage_state(
        self, spark_run_open_lineage_state: Optional[OpenLineageRunState]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.spark_run_open_lineage_state = spark_run_open_lineage_state

    class Attributes(Catalog.Attributes):
        spark_run_version: Optional[str] = Field(default=None, description="")
        spark_run_open_lineage_version: Optional[str] = Field(
            default=None, description=""
        )
        spark_run_start_time: Optional[datetime] = Field(default=None, description="")
        spark_run_end_time: Optional[datetime] = Field(default=None, description="")
        spark_run_open_lineage_state: Optional[OpenLineageRunState] = Field(
            default=None, description=""
        )

    attributes: Spark.Attributes = Field(
        default_factory=lambda: Spark.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
