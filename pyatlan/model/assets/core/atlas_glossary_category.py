# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional
from warnings import warn

from pydantic.v1 import Field, StrictStr, root_validator, validator

from pyatlan.model.enums import AtlasGlossaryCategoryType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField
from pyatlan.utils import init_guid, next_id, validate_required_fields

from .asset import Asset, SelfAsset


class AtlasGlossaryCategory(Asset, type_name="AtlasGlossaryCategory"):
    """Description"""

    @classmethod
    def can_be_archived(self) -> bool:
        """
        Indicates if an asset can be archived via the asset.delete_by_guid method.
        :returns: True if archiving is supported
        """
        return False

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
        anchor: AtlasGlossary,
        parent_category: Optional[AtlasGlossaryCategory] = None,
    ) -> AtlasGlossaryCategory:
        validate_required_fields(["name", "anchor"], [name, anchor])
        return cls(
            attributes=AtlasGlossaryCategory.Attributes.create(
                name=name, anchor=anchor, parent_category=parent_category
            )
        )

    @classmethod
    @init_guid
    def create(
        cls,
        *,
        name: StrictStr,
        anchor: AtlasGlossary,
        parent_category: Optional[AtlasGlossaryCategory] = None,
    ) -> AtlasGlossaryCategory:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(name=name, anchor=anchor, parent_category=parent_category)

    def trim_to_required(self) -> AtlasGlossaryCategory:
        # The backend raises an exception unless the `glossary_guid` is provided.
        # Providing the `glossary_qualified_name` won't work
        if self.anchor is None or not self.anchor.guid:
            raise ValueError("anchor.guid must be available")
        return self.updater(
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
        glossary = AtlasGlossary.ref_by_guid(glossary_guid)
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
    ) -> AtlasGlossaryCategory:
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
    """Glossary in which the category is contained, searchable by the qualifiedName of the glossary."""

    PARENT_CATEGORY: ClassVar[KeywordField] = KeywordField(
        "parentCategory", "__parentCategory"
    )
    """Parent category in which a subcategory is contained, searchable by the qualifiedName of the category."""

    type_name: str = Field(default="AtlasGlossaryCategory", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AtlasGlossaryCategory":
            raise ValueError("must be AtlasGlossaryCategory")
        return v

    def __setattr__(self, name, value):
        if name in AtlasGlossaryCategory._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SHORT_DESCRIPTION: ClassVar[KeywordField] = KeywordField(
        "shortDescription", "shortDescription"
    )
    """
    Unused. Brief summary of the category. See 'description' and 'userDescription' instead.
    """
    LONG_DESCRIPTION: ClassVar[KeywordField] = KeywordField(
        "longDescription", "longDescription"
    )
    """
    Unused. Detailed description of the category. See 'readme' instead.
    """
    ADDITIONAL_ATTRIBUTES: ClassVar[KeywordField] = KeywordField(
        "additionalAttributes", "additionalAttributes"
    )
    """
    Unused. Arbitrary set of additional attributes associated with the category.
    """
    CATEGORY_TYPE: ClassVar[KeywordField] = KeywordField("categoryType", "categoryType")
    """
    TBC
    """

    TERMS: ClassVar[RelationField] = RelationField("terms")
    """
    TBC
    """
    CHILDREN_CATEGORIES: ClassVar[RelationField] = RelationField("childrenCategories")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "short_description",
        "long_description",
        "additional_attributes",
        "category_type",
        "terms",
        "anchor",
        "parent_category",
        "children_categories",
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
    def category_type(self) -> Optional[AtlasGlossaryCategoryType]:
        return None if self.attributes is None else self.attributes.category_type

    @category_type.setter
    def category_type(self, category_type: Optional[AtlasGlossaryCategoryType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.category_type = category_type

    @property
    def terms(self) -> Optional[List[AtlasGlossaryTerm]]:
        return None if self.attributes is None else self.attributes.terms

    @terms.setter
    def terms(self, terms: Optional[List[AtlasGlossaryTerm]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.terms = terms

    @property
    def anchor(self) -> Optional[AtlasGlossary]:
        return None if self.attributes is None else self.attributes.anchor

    @anchor.setter
    def anchor(self, anchor: Optional[AtlasGlossary]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anchor = anchor

    @property
    def parent_category(self) -> Optional[AtlasGlossaryCategory]:
        return None if self.attributes is None else self.attributes.parent_category

    @parent_category.setter
    def parent_category(self, parent_category: Optional[AtlasGlossaryCategory]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        if not parent_category:
            self.relationship_attributes = {"parentCategory": None}
        self.attributes.parent_category = parent_category

    @property
    def children_categories(self) -> Optional[List[AtlasGlossaryCategory]]:
        return None if self.attributes is None else self.attributes.children_categories

    @children_categories.setter
    def children_categories(
        self, children_categories: Optional[List[AtlasGlossaryCategory]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.children_categories = children_categories

    class Attributes(Asset.Attributes):
        short_description: Optional[str] = Field(default=None, description="")
        long_description: Optional[str] = Field(default=None, description="")
        additional_attributes: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        category_type: Optional[AtlasGlossaryCategoryType] = Field(
            default=None, description=""
        )
        terms: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        anchor: Optional[AtlasGlossary] = Field(
            default=None, description=""
        )  # relationship
        parent_category: Optional[AtlasGlossaryCategory] = Field(
            default=None, description=""
        )  # relationship
        children_categories: Optional[List[AtlasGlossaryCategory]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: StrictStr,
            anchor: AtlasGlossary,
            parent_category: Optional[AtlasGlossaryCategory] = None,
        ) -> AtlasGlossaryCategory.Attributes:
            validate_required_fields(["name", "anchor"], [name, anchor])
            return AtlasGlossaryCategory.Attributes(
                name=name,
                anchor=anchor,
                parent_category=parent_category,
                qualified_name=next_id(),
            )

    attributes: AtlasGlossaryCategory.Attributes = Field(
        default_factory=lambda: AtlasGlossaryCategory.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .atlas_glossary import AtlasGlossary  # noqa
from .atlas_glossary_term import AtlasGlossaryTerm  # noqa
