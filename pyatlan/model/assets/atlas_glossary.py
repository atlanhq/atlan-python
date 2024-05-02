# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional
from warnings import warn

from pydantic.v1 import Field, StrictStr, root_validator, validator

from pyatlan.model.enums import AtlanIcon, AtlasGlossaryType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField
from pyatlan.utils import init_guid, next_id, validate_required_fields

from .asset import Asset


class AtlasGlossary(Asset, type_name="AtlasGlossary"):
    """Description"""

    @root_validator()
    def _set_qualified_name_fallback(cls, values):
        guid = values.get("guid")
        attributes = values.get("attributes")
        unique_attributes = values.get("unique_attributes")
        if attributes and not attributes.qualified_name:
            # If the qualified name is present inside
            # unique attributes (in case of a related entity)
            # Otherwise, set the qualified name to the GUID
            # to avoid collisions when creating glossary object
            attributes.qualified_name = (
                unique_attributes and unique_attributes.get("qualifiedName")
            ) or guid
        return values

    @classmethod
    @init_guid
    def creator(
        cls, *, name: StrictStr, icon: Optional[AtlanIcon] = None
    ) -> AtlasGlossary:
        validate_required_fields(["name"], [name])
        return AtlasGlossary(
            attributes=AtlasGlossary.Attributes.create(name=name, icon=icon)
        )

    @classmethod
    @init_guid
    def create(
        cls, *, name: StrictStr, icon: Optional[AtlanIcon] = None
    ) -> AtlasGlossary:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(name=name, icon=icon)

    type_name: str = Field(default="AtlasGlossary", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AtlasGlossary":
            raise ValueError("must be AtlasGlossary")
        return v

    def __setattr__(self, name, value):
        if name in AtlasGlossary._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SHORT_DESCRIPTION: ClassVar[KeywordField] = KeywordField(
        "shortDescription", "shortDescription"
    )
    """
    Unused. A short definition of the glossary. See 'description' and 'userDescription' instead.
    """
    LONG_DESCRIPTION: ClassVar[KeywordField] = KeywordField(
        "longDescription", "longDescription"
    )
    """
    Unused. A longer description of the glossary. See 'readme' instead.
    """
    LANGUAGE: ClassVar[KeywordField] = KeywordField("language", "language")
    """
    Unused. Language of the glossary's contents.
    """
    USAGE: ClassVar[KeywordField] = KeywordField("usage", "usage")
    """
    Unused. Inteded usage for the glossary.
    """
    ADDITIONAL_ATTRIBUTES: ClassVar[KeywordField] = KeywordField(
        "additionalAttributes", "additionalAttributes"
    )
    """
    Unused. Arbitrary set of additional attributes associated with this glossary.
    """
    GLOSSARY_TYPE: ClassVar[KeywordField] = KeywordField("glossaryType", "glossaryType")
    """
    TBC
    """

    TERMS: ClassVar[RelationField] = RelationField("terms")
    """
    TBC
    """
    CATEGORIES: ClassVar[RelationField] = RelationField("categories")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "short_description",
        "long_description",
        "language",
        "usage",
        "additional_attributes",
        "glossary_type",
        "terms",
        "categories",
    ]

    @property
    def short_description(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.short_description

    @short_description.setter
    def short_description(self, short_description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.short_description = short_description

    @property
    def long_description(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.long_description

    @long_description.setter
    def long_description(self, long_description: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.long_description = long_description

    @property
    def language(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.language

    @language.setter
    def language(self, language: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.language = language

    @property
    def usage(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.usage

    @usage.setter
    def usage(self, usage: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.usage = usage

    @property
    def additional_attributes(self) -> Optional[Dict[str, str]]:
        return (
            None if self.attributes is None else self.attributes.additional_attributes
        )

    @additional_attributes.setter
    def additional_attributes(self, additional_attributes: Optional[Dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.additional_attributes = additional_attributes

    @property
    def glossary_type(self) -> Optional[AtlasGlossaryType]:
        return None if self.attributes is None else self.attributes.glossary_type

    @glossary_type.setter
    def glossary_type(self, glossary_type: Optional[AtlasGlossaryType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.glossary_type = glossary_type

    @property
    def terms(self) -> Optional[List[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.terms

    @terms.setter
    def terms(self, terms: Optional[List[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.terms = terms

    @property
    def categories(self) -> Optional[List[AtlasGlossaryCategory]]:
        return None if self.attributes is None else self.attributes.categories

    @categories.setter
    def categories(self, categories: Optional[List[AtlasGlossaryCategory]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.categories = categories

    class Attributes(Asset.Attributes):
        short_description: Optional[str] = Field(default=None, description="")
        long_description: Optional[str] = Field(default=None, description="")
        language: Optional[str] = Field(default=None, description="")
        usage: Optional[str] = Field(default=None, description="")
        additional_attributes: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        glossary_type: Optional[AtlasGlossaryType] = Field(default=None, description="")
        terms: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        categories: Optional[List[AtlasGlossaryCategory]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls, *, name: StrictStr, icon: Optional[AtlanIcon] = None
        ) -> AtlasGlossary.Attributes:
            validate_required_fields(["name"], [name])
            icon_str = icon.value if icon is not None else None
            return AtlasGlossary.Attributes(
                name=name, qualified_name=next_id(), asset_icon=icon_str
            )

    attributes: AtlasGlossary.Attributes = Field(
        default_factory=lambda: AtlasGlossary.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .atlas_glossary_category import AtlasGlossaryCategory  # noqa
from .atlas_glossary_term import AtlasGlossaryTerm  # noqa
