# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .process import Process


class ColumnProcess(Process):
    """Description"""

    @classmethod
    @init_guid
    def creator(
        cls,
        name: str,
        connection_qualified_name: str,
        inputs: List["Catalog"],
        outputs: List["Catalog"],
        parent: Process,
        process_id: Optional[str] = None,
    ) -> ColumnProcess:
        return ColumnProcess(
            attributes=ColumnProcess.Attributes.create(
                name=name,
                connection_qualified_name=connection_qualified_name,
                process_id=process_id,
                inputs=inputs,
                outputs=outputs,
                parent=parent,
            )
        )

    @classmethod
    @init_guid
    def create(
        cls,
        name: str,
        connection_qualified_name: str,
        inputs: List["Catalog"],
        outputs: List["Catalog"],
        parent: Process,
        process_id: Optional[str] = None,
    ) -> ColumnProcess:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
            inputs=inputs,
            outputs=outputs,
            parent=parent,
            process_id=process_id,
        )

    type_name: str = Field(default="ColumnProcess", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ColumnProcess":
            raise ValueError("must be ColumnProcess")
        return v

    def __setattr__(self, name, value):
        if name in ColumnProcess._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    OUTPUTS: ClassVar[RelationField] = RelationField("outputs")
    """
    Assets that are outputs from this process.
    """
    PROCESS: ClassVar[RelationField] = RelationField("process")
    """
    TBC
    """
    INPUTS: ClassVar[RelationField] = RelationField("inputs")
    """
    Assets that are inputs to this process.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "outputs",
        "process",
        "inputs",
    ]

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

    class Attributes(Process.Attributes):
        outputs: Optional[List[Catalog]] = Field(
            default=None, description=""
        )  # relationship
        process: Optional[Process] = Field(default=None, description="")  # relationship
        inputs: Optional[List[Catalog]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            name: str,
            connection_qualified_name: str,
            inputs: List["Catalog"],
            outputs: List["Catalog"],
            parent: Process,
            process_id: Optional[str] = None,
        ) -> ColumnProcess.Attributes:
            validate_required_fields(["parent"], [parent])
            qualified_name = Process.Attributes.generate_qualified_name(
                name=name,
                connection_qualified_name=connection_qualified_name,
                process_id=process_id,
                inputs=inputs,
                outputs=outputs,
                parent=parent,
            )
            connector_name = connection_qualified_name.split("/")[1]
            return ColumnProcess.Attributes(
                name=name,
                qualified_name=qualified_name,
                connector_name=connector_name,
                connection_qualified_name=connection_qualified_name,
                inputs=inputs,
                outputs=outputs,
                process=parent,
            )

    attributes: ColumnProcess.Attributes = Field(
        default_factory=lambda: ColumnProcess.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .catalog import Catalog  # noqa
from .process import Process  # noqa
