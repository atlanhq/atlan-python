from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
)


class ReferenceableFields:

    TYPE_NAME = KeywordTextField("typeName", "__typeName.keyword", "__typeName")
    """Type of the asset. For example Table, Column, and so on."""

    GUID = KeywordField("guid", "__guid")
    """Globally unique identifier (GUID) of any object in Atlan."""

    CREATED_BY = KeywordField("createdBy", "__createdBy")
    """Atlan user who created this asset."""

    UPDATED_BY = KeywordField("updatedBy", "__modifiedBy")
    """Atlan user who last updated the asset."""

    STATUS = KeywordField("status", "__state")
    """Asset status in Atlan (active vs deleted)."""

    ATLAN_TAGS = KeywordTextField(
        "classificationNames", "__traitNames", "__classificationsText"
    )
    """
    All directly-assigned Atlan tags that exist on an asset, searchable by internal hashed-string ID of the Atlan tag.
    """

    PROPAGATED_ATLAN_TAGS = KeywordTextField(
        "classificationNames", "__propagatedTraitNames", "__classificationsText"
    )
    """All propagated Atlan tags that exist on an asset, searchable by internal hashed-string ID of the Atlan tag."""

    ASSIGNED_TERMS = KeywordTextField("meanings", "__meanings", "__meaningsText")
    """All terms attached to an asset, searchable by the term's qualifiedName."""

    SUPER_TYPE_NAMES = KeywordTextField(
        "typeName", "__superTypeNames.keyword", "__superTypeNames"
    )
    """All super types of an asset."""

    CREATE_TIME = NumericField("createTime", "__timestamp")
    """Time (in milliseconds) when the asset was created."""

    UPDATE_TIME = NumericField("updateTime", "__modificationTimestamp")
    """Time (in milliseconds) when the asset was last updated."""
