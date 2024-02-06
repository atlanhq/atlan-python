from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, StrictStr, root_validator, validator

from pyatlan.model.enums import AtlanIcon, AtlasGlossaryType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField
from pyatlan.utils import init_guid, next_id, validate_required_fields

from .asset00 import Asset


class AtlasGlossary(Asset, type_name="AtlasGlossary"):
    """Description"""

    @root_validator()
    def _set_qualified_name_fallback(cls, values):
        if (
            "attributes" in values
            and values["attributes"]
            and not values["attributes"].qualified_name
        ):
            values["attributes"].qualified_name = values["guid"]
        return values

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(
        cls, *, name: StrictStr, icon: Optional[AtlanIcon] = None
    ) -> AtlasGlossary:
        validate_required_fields(["name"], [name])
        return AtlasGlossary(
            attributes=AtlasGlossary.Attributes.create(name=name, icon=icon)
        )

    type_name: str = Field("AtlasGlossary", allow_mutation=False)

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
    TBC
    """
    LONG_DESCRIPTION: ClassVar[KeywordField] = KeywordField(
        "longDescription", "longDescription"
    )
    """
    TBC
    """
    LANGUAGE: ClassVar[KeywordField] = KeywordField("language", "language")
    """
    TBC
    """
    USAGE: ClassVar[KeywordField] = KeywordField("usage", "usage")
    """
    TBC
    """
    ADDITIONAL_ATTRIBUTES: ClassVar[KeywordField] = KeywordField(
        "additionalAttributes", "additionalAttributes"
    )
    """
    TBC
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

    _convenience_properties: ClassVar[list[str]] = [
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
    def additional_attributes(self) -> Optional[dict[str, str]]:
        return (
            None if self.attributes is None else self.attributes.additional_attributes
        )

    @additional_attributes.setter
    def additional_attributes(self, additional_attributes: Optional[dict[str, str]]):
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
    def terms(self) -> Optional[list[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.terms

    @terms.setter
    def terms(self, terms: Optional[list[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.terms = terms

    @property
    def categories(self) -> Optional[list[AtlasGlossaryCategory]]:
        return None if self.attributes is None else self.attributes.categories

    @categories.setter
    def categories(self, categories: Optional[list[AtlasGlossaryCategory]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.categories = categories

    class Attributes(Asset.Attributes):
        short_description: Optional[str] = Field(
            None, description="", alias="shortDescription"
        )
        long_description: Optional[str] = Field(
            None, description="", alias="longDescription"
        )
        language: Optional[str] = Field(None, description="", alias="language")
        usage: Optional[str] = Field(None, description="", alias="usage")
        additional_attributes: Optional[dict[str, str]] = Field(
            None, description="", alias="additionalAttributes"
        )
        glossary_type: Optional[AtlasGlossaryType] = Field(
            None, description="", alias="glossaryType"
        )
        terms: Optional[list[AtlasGlossaryTerm]] = Field(
            None, description="", alias="terms"
        )  # relationship
        categories: Optional[list[AtlasGlossaryCategory]] = Field(
            None, description="", alias="categories"
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls, *, name: StrictStr, icon: Optional[AtlanIcon] = None
        ) -> AtlasGlossary.Attributes:
            validate_required_fields(["name"], [name])
            icon_str = icon.value if icon is not None else None
            return AtlasGlossary.Attributes(
                name=name, qualified_name=next_id(), icon=icon_str
            )

    attributes: "AtlasGlossary.Attributes" = Field(
        default_factory=lambda: AtlasGlossary.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )

from .atlas_glossary_category import AtlasGlossaryCategory
from .atlas_glossary_term import AtlasGlossaryTerm

AtlasGlossary.Attributes.update_forward_refs()
