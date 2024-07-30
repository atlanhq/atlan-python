# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField, RelationField

from .s_q_l import SQL


class Function(SQL):
    """Description"""

    type_name: str = Field(default="Function", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Function":
            raise ValueError("must be Function")
        return v

    def __setattr__(self, name, value):
        if name in Function._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FUNCTION_DEFINITION: ClassVar[KeywordField] = KeywordField(
        "functionDefinition", "functionDefinition"
    )
    """
    Code or set of statements that determine the output of the function.
    """
    FUNCTION_RETURN_TYPE: ClassVar[KeywordField] = KeywordField(
        "functionReturnType", "functionReturnType"
    )
    """
    Data type of the value returned by the function.
    """
    FUNCTION_ARGUMENTS: ClassVar[KeywordField] = KeywordField(
        "functionArguments", "functionArguments"
    )
    """
    Arguments that are passed in to the function.
    """
    FUNCTION_LANGUAGE: ClassVar[KeywordField] = KeywordField(
        "functionLanguage", "functionLanguage"
    )
    """
    Programming language in which the function is written.
    """
    FUNCTION_TYPE: ClassVar[KeywordField] = KeywordField("functionType", "functionType")
    """
    Type of function.
    """
    FUNCTION_IS_EXTERNAL: ClassVar[BooleanField] = BooleanField(
        "functionIsExternal", "functionIsExternal"
    )
    """
    Whether the function is stored or executed externally (true) or internally (false).
    """
    FUNCTION_IS_SECURE: ClassVar[BooleanField] = BooleanField(
        "functionIsSecure", "functionIsSecure"
    )
    """
    Whether sensitive information of the function is omitted for unauthorized users (true) or not (false).
    """
    FUNCTION_IS_MEMOIZABLE: ClassVar[BooleanField] = BooleanField(
        "functionIsMemoizable", "functionIsMemoizable"
    )
    """
    Whether the function must re-compute if there are no underlying changes in the values (false) or not (true).
    """

    FUNCTION_SCHEMA: ClassVar[RelationField] = RelationField("functionSchema")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "function_definition",
        "function_return_type",
        "function_arguments",
        "function_language",
        "function_type",
        "function_is_external",
        "function_is_secure",
        "function_is_memoizable",
        "function_schema",
    ]

    @property
    def function_definition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.function_definition

    @function_definition.setter
    def function_definition(self, function_definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.function_definition = function_definition

    @property
    def function_return_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.function_return_type

    @function_return_type.setter
    def function_return_type(self, function_return_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.function_return_type = function_return_type

    @property
    def function_arguments(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.function_arguments

    @function_arguments.setter
    def function_arguments(self, function_arguments: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.function_arguments = function_arguments

    @property
    def function_language(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.function_language

    @function_language.setter
    def function_language(self, function_language: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.function_language = function_language

    @property
    def function_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.function_type

    @function_type.setter
    def function_type(self, function_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.function_type = function_type

    @property
    def function_is_external(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.function_is_external

    @function_is_external.setter
    def function_is_external(self, function_is_external: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.function_is_external = function_is_external

    @property
    def function_is_secure(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.function_is_secure

    @function_is_secure.setter
    def function_is_secure(self, function_is_secure: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.function_is_secure = function_is_secure

    @property
    def function_is_memoizable(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.function_is_memoizable
        )

    @function_is_memoizable.setter
    def function_is_memoizable(self, function_is_memoizable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.function_is_memoizable = function_is_memoizable

    @property
    def function_schema(self) -> Optional[Schema]:
        return None if self.attributes is None else self.attributes.function_schema

    @function_schema.setter
    def function_schema(self, function_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.function_schema = function_schema

    class Attributes(SQL.Attributes):
        function_definition: Optional[str] = Field(default=None, description="")
        function_return_type: Optional[str] = Field(default=None, description="")
        function_arguments: Optional[Set[str]] = Field(default=None, description="")
        function_language: Optional[str] = Field(default=None, description="")
        function_type: Optional[str] = Field(default=None, description="")
        function_is_external: Optional[bool] = Field(default=None, description="")
        function_is_secure: Optional[bool] = Field(default=None, description="")
        function_is_memoizable: Optional[bool] = Field(default=None, description="")
        function_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship

    attributes: Function.Attributes = Field(
        default_factory=lambda: Function.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .schema import Schema  # noqa
