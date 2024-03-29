# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .spark import Spark


class SparkJob(Spark):
    """Description"""

    type_name: str = Field(default="SparkJob", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SparkJob":
            raise ValueError("must be SparkJob")
        return v

    def __setattr__(self, name, value):
        if name in SparkJob._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SPARK_APP_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sparkAppName", "sparkAppName.keyword", "sparkAppName"
    )
    """
    Name of the Spark app containing this Spark Job For eg. extract_raw_data
    """
    SPARK_MASTER: ClassVar[KeywordField] = KeywordField("sparkMaster", "sparkMaster")
    """
    The Spark master URL eg. local, local[4], or spark://master:7077
    """

    OUTPUTS: ClassVar[RelationField] = RelationField("outputs")
    """
    TBC
    """
    PROCESS: ClassVar[RelationField] = RelationField("process")
    """
    TBC
    """
    INPUTS: ClassVar[RelationField] = RelationField("inputs")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "spark_app_name",
        "spark_master",
        "outputs",
        "process",
        "inputs",
    ]

    @property
    def spark_app_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.spark_app_name

    @spark_app_name.setter
    def spark_app_name(self, spark_app_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.spark_app_name = spark_app_name

    @property
    def spark_master(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.spark_master

    @spark_master.setter
    def spark_master(self, spark_master: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.spark_master = spark_master

    @property
    def outputs(self) -> Optional[List[Catalog]]:
        return None if self.attributes is None else self.attributes.outputs

    @outputs.setter
    def outputs(self, outputs: Optional[List[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.outputs = outputs

    @property
    def process(self) -> Optional[Process]:
        return None if self.attributes is None else self.attributes.process

    @process.setter
    def process(self, process: Optional[Process]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.process = process

    @property
    def inputs(self) -> Optional[List[Catalog]]:
        return None if self.attributes is None else self.attributes.inputs

    @inputs.setter
    def inputs(self, inputs: Optional[List[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.inputs = inputs

    class Attributes(Spark.Attributes):
        spark_app_name: Optional[str] = Field(default=None, description="")
        spark_master: Optional[str] = Field(default=None, description="")
        outputs: Optional[List[Catalog]] = Field(
            default=None, description=""
        )  # relationship
        process: Optional[Process] = Field(default=None, description="")  # relationship
        inputs: Optional[List[Catalog]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SparkJob.Attributes = Field(
        default_factory=lambda: SparkJob.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .catalog import Catalog  # noqa
from .process import Process  # noqa
