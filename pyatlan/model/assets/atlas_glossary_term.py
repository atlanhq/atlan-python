# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional, Set
from warnings import warn

from pydantic.v1 import Field, StrictStr, root_validator, validator

from pyatlan.model.enums import AtlasGlossaryTermType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField
from pyatlan.utils import (
    init_guid,
    next_id,
    validate_required_fields,
    validate_single_required_field,
)

from .asset import Asset, SelfAsset


class AtlasGlossaryTerm(Asset, type_name="AtlasGlossaryTerm"):
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
        cls,
        *,
        name: StrictStr,
        anchor: Optional[AtlasGlossary] = None,
        glossary_qualified_name: Optional[StrictStr] = None,
        glossary_guid: Optional[StrictStr] = None,
        categories: Optional[List[AtlasGlossaryCategory]] = None,
    ) -> AtlasGlossaryTerm:
        validate_required_fields(["name"], [name])
        return cls(
            attributes=AtlasGlossaryTerm.Attributes.create(
                name=name,
                anchor=anchor,
                glossary_qualified_name=glossary_qualified_name,
                glossary_guid=glossary_guid,
                categories=categories,
            )
        )

    @classmethod
    @init_guid
    def create(
        cls,
        *,
        name: StrictStr,
        anchor: Optional[AtlasGlossary] = None,
        glossary_qualified_name: Optional[StrictStr] = None,
        glossary_guid: Optional[StrictStr] = None,
        categories: Optional[List[AtlasGlossaryCategory]] = None,
    ) -> AtlasGlossaryTerm:
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
            anchor=anchor,
            glossary_qualified_name=glossary_qualified_name,
            glossary_guid=glossary_guid,
            categories=categories,
        )

    def trim_to_required(self) -> AtlasGlossaryTerm:
        if self.anchor is None or not self.anchor.guid:
            raise ValueError("anchor.guid must be available")
        return self.create_for_modification(
            qualified_name=self.qualified_name or "",
            name=self.name or "",
            glossary_guid=self.anchor.guid,
        )

    @classmethod
    def updater(
        cls: type[SelfAsset],
        qualified_name: str = "",
        name: str = "",
        glossary_guid: str = "",
    ) -> SelfAsset:
        validate_required_fields(
            ["name", "qualified_name", "glossary_guid"],
            [name, qualified_name, glossary_guid],
        )
        glossary = AtlasGlossary()
        glossary.guid = glossary_guid
        return cls(
            attributes=cls.Attributes(
                qualified_name=qualified_name, name=name, anchor=glossary
            )
        )

    @classmethod
    def create_for_modification(
        cls,
        qualified_name: str = "",
        name: str = "",
        glossary_guid: str = "",
    ) -> AtlasGlossaryTerm:
        warn(
            (
                "This method is deprecated, please use 'updater' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.updater(
            qualified_name=qualified_name, name=name, glossary_guid=glossary_guid
        )

    ANCHOR: ClassVar[KeywordField] = KeywordField("anchor", "__glossary")
    """Glossary in which the term is contained, searchable by the qualifiedName of the glossary."""

    CATEGORIES: ClassVar[KeywordField] = KeywordField("categories", "__categories")
    """Categories in which the term is organized, searchable by the qualifiedName of the category."""

    type_name: str = Field(default="AtlasGlossaryTerm", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AtlasGlossaryTerm":
            raise ValueError("must be AtlasGlossaryTerm")
        return v

    def __setattr__(self, name, value):
        if name in AtlasGlossaryTerm._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SHORT_DESCRIPTION: ClassVar[KeywordField] = KeywordField(
        "shortDescription", "shortDescription"
    )
    """
    Unused. Brief summary of the term. See 'description' and 'userDescription' instead.
    """
    LONG_DESCRIPTION: ClassVar[KeywordField] = KeywordField(
        "longDescription", "longDescription"
    )
    """
    Unused. Detailed definition of the term. See 'readme' instead.
    """
    EXAMPLES: ClassVar[KeywordField] = KeywordField("examples", "examples")
    """
    Unused. Exmaples of the term.
    """
    ABBREVIATION: ClassVar[KeywordField] = KeywordField("abbreviation", "abbreviation")
    """
    Unused. Abbreviation of the term.
    """
    USAGE: ClassVar[KeywordField] = KeywordField("usage", "usage")
    """
    Unused. Intended usage for the term.
    """
    ADDITIONAL_ATTRIBUTES: ClassVar[KeywordField] = KeywordField(
        "additionalAttributes", "additionalAttributes"
    )
    """
    Unused. Arbitrary set of additional attributes for the terrm.
    """
    TERM_TYPE: ClassVar[KeywordField] = KeywordField("termType", "termType")
    """
    TBC
    """

    VALID_VALUES_FOR: ClassVar[RelationField] = RelationField("validValuesFor")
    """
    TBC
    """
    VALID_VALUES: ClassVar[RelationField] = RelationField("validValues")
    """
    TBC
    """
    SEE_ALSO: ClassVar[RelationField] = RelationField("seeAlso")
    """
    TBC
    """
    IS_A: ClassVar[RelationField] = RelationField("isA")
    """
    TBC
    """
    ANTONYMS: ClassVar[RelationField] = RelationField("antonyms")
    """
    TBC
    """
    ASSIGNED_ENTITIES: ClassVar[RelationField] = RelationField("assignedEntities")
    """
    TBC
    """
    CLASSIFIES: ClassVar[RelationField] = RelationField("classifies")
    """
    TBC
    """
    PREFERRED_TO_TERMS: ClassVar[RelationField] = RelationField("preferredToTerms")
    """
    TBC
    """
    PREFERRED_TERMS: ClassVar[RelationField] = RelationField("preferredTerms")
    """
    TBC
    """
    TRANSLATION_TERMS: ClassVar[RelationField] = RelationField("translationTerms")
    """
    TBC
    """
    SYNONYMS: ClassVar[RelationField] = RelationField("synonyms")
    """
    TBC
    """
    REPLACED_BY: ClassVar[RelationField] = RelationField("replacedBy")
    """
    TBC
    """
    REPLACEMENT_TERMS: ClassVar[RelationField] = RelationField("replacementTerms")
    """
    TBC
    """
    TRANSLATED_TERMS: ClassVar[RelationField] = RelationField("translatedTerms")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "short_description",
        "long_description",
        "examples",
        "abbreviation",
        "usage",
        "additional_attributes",
        "term_type",
        "valid_values_for",
        "valid_values",
        "see_also",
        "is_a",
        "antonyms",
        "assigned_entities",
        "classifies",
        "categories",
        "preferred_to_terms",
        "preferred_terms",
        "translation_terms",
        "synonyms",
        "replaced_by",
        "replacement_terms",
        "translated_terms",
        "anchor",
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
    def examples(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.examples

    @examples.setter
    def examples(self, examples: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.examples = examples

    @property
    def abbreviation(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.abbreviation

    @abbreviation.setter
    def abbreviation(self, abbreviation: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.abbreviation = abbreviation

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
    def term_type(self) -> Optional[AtlasGlossaryTermType]:
        return None if self.attributes is None else self.attributes.term_type

    @term_type.setter
    def term_type(self, term_type: Optional[AtlasGlossaryTermType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.term_type = term_type

    @property
    def valid_values_for(self) -> Optional[List[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.valid_values_for

    @valid_values_for.setter
    def valid_values_for(self, valid_values_for: Optional[List[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.valid_values_for = valid_values_for

    @property
    def valid_values(self) -> Optional[List[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.valid_values

    @valid_values.setter
    def valid_values(self, valid_values: Optional[List[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.valid_values = valid_values

    @property
    def see_also(self) -> Optional[List[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.see_also

    @see_also.setter
    def see_also(self, see_also: Optional[List[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.see_also = see_also

    @property
    def is_a(self) -> Optional[List[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.is_a

    @is_a.setter
    def is_a(self, is_a: Optional[List[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_a = is_a

    @property
    def antonyms(self) -> Optional[List[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.antonyms

    @antonyms.setter
    def antonyms(self, antonyms: Optional[List[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.antonyms = antonyms

    @property
    def assigned_entities(self) -> Optional[List[Referenceable]]:
        return None if self.attributes is None else self.attributes.assigned_entities

    @assigned_entities.setter
    def assigned_entities(self, assigned_entities: Optional[List[Referenceable]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.assigned_entities = assigned_entities

    @property
    def classifies(self) -> Optional[List[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.classifies

    @classifies.setter
    def classifies(self, classifies: Optional[List[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.classifies = classifies

    @property
    def categories(self) -> Optional[List[AtlasGlossaryCategory]]:
        return None if self.attributes is None else self.attributes.categories

    @categories.setter
    def categories(self, categories: Optional[List[AtlasGlossaryCategory]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.categories = categories

    @property
    def preferred_to_terms(self) -> Optional[List[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.preferred_to_terms

    @preferred_to_terms.setter
    def preferred_to_terms(self, preferred_to_terms: Optional[List[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preferred_to_terms = preferred_to_terms

    @property
    def preferred_terms(self) -> Optional[List[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.preferred_terms

    @preferred_terms.setter
    def preferred_terms(self, preferred_terms: Optional[List[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preferred_terms = preferred_terms

    @property
    def translation_terms(self) -> Optional[List[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.translation_terms

    @translation_terms.setter
    def translation_terms(self, translation_terms: Optional[List[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.translation_terms = translation_terms

    @property
    def synonyms(self) -> Optional[List[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.synonyms

    @synonyms.setter
    def synonyms(self, synonyms: Optional[List[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.synonyms = synonyms

    @property
    def replaced_by(self) -> Optional[List[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.replaced_by

    @replaced_by.setter
    def replaced_by(self, replaced_by: Optional[List[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.replaced_by = replaced_by

    @property
    def replacement_terms(self) -> Optional[List[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.replacement_terms

    @replacement_terms.setter
    def replacement_terms(self, replacement_terms: Optional[List[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.replacement_terms = replacement_terms

    @property
    def translated_terms(self) -> Optional[List[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.translated_terms

    @translated_terms.setter
    def translated_terms(self, translated_terms: Optional[List[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.translated_terms = translated_terms

    @property
    def anchor(self) -> Optional[AtlasGlossary]:
        return None if self.attributes is None else self.attributes.anchor

    @anchor.setter
    def anchor(self, anchor: Optional[AtlasGlossary]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anchor = anchor

    class Attributes(Asset.Attributes):
        short_description: Optional[str] = Field(default=None, description="")
        long_description: Optional[str] = Field(default=None, description="")
        examples: Optional[Set[str]] = Field(default=None, description="")
        abbreviation: Optional[str] = Field(default=None, description="")
        usage: Optional[str] = Field(default=None, description="")
        additional_attributes: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        term_type: Optional[AtlasGlossaryTermType] = Field(default=None, description="")
        valid_values_for: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        valid_values: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        see_also: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        is_a: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        antonyms: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        assigned_entities: Optional[List[Referenceable]] = Field(
            default=None, description=""
        )  # relationship
        classifies: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        categories: Optional[List[AtlasGlossaryCategory]] = Field(
            default=None, description=""
        )  # relationship
        preferred_to_terms: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        preferred_terms: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        translation_terms: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        synonyms: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        replaced_by: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        replacement_terms: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        translated_terms: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        anchor: Optional[AtlasGlossary] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: StrictStr,
            anchor: Optional[AtlasGlossary] = None,
            glossary_qualified_name: Optional[StrictStr] = None,
            glossary_guid: Optional[StrictStr] = None,
            categories: Optional[List[AtlasGlossaryCategory]] = None,
        ) -> AtlasGlossaryTerm.Attributes:
            validate_required_fields(["name"], [name])
            validate_single_required_field(
                ["anchor", "glossary_qualified_name", "glossary_guid"],
                [anchor, glossary_qualified_name, glossary_guid],
            )
            if glossary_qualified_name:
                anchor = AtlasGlossary()
                anchor.unique_attributes = {"qualifiedName": glossary_qualified_name}
            if glossary_guid:
                anchor = AtlasGlossary()
                anchor.guid = glossary_guid
            return AtlasGlossaryTerm.Attributes(
                name=name,
                anchor=anchor,
                categories=categories,
                qualified_name=next_id(),
            )

    attributes: AtlasGlossaryTerm.Attributes = Field(
        default_factory=lambda: AtlasGlossaryTerm.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .atlas_glossary import AtlasGlossary  # noqa
from .atlas_glossary_category import AtlasGlossaryCategory  # noqa
from .referenceable import Referenceable  # noqa
