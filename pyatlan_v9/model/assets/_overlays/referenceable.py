# IMPORT: from pyatlan.model.fields.atlan_fields import InternalKeywordField, InternalKeywordTextField, InternalNumericField, KeywordField, KeywordTextField, NumericField, TextField
# INTERNAL_IMPORT: from pyatlan.model.lineage_ref import LineageRef
# DEFERRED: Referenceable.TYPE_NAME = InternalKeywordTextField("typeName", "__typeName.keyword", "__typeName", "__typeName")
# DEFERRED: Referenceable.GUID = InternalKeywordField("guid", "__guid", "__guid")
# DEFERRED: Referenceable.CREATED_BY = InternalKeywordField("createdBy", "__createdBy", "__createdBy")
# DEFERRED: Referenceable.UPDATED_BY = InternalKeywordField("updatedBy", "__modifiedBy", "__modifiedBy")
# DEFERRED: Referenceable.STATUS = InternalKeywordField("status", "__state", "__state")
# DEFERRED: Referenceable.ATLAN_TAGS = InternalKeywordTextField("classificationNames", "__traitNames", "__classificationsText", "__classificationNames")
# DEFERRED: Referenceable.PROPAGATED_ATLAN_TAGS = InternalKeywordTextField("classificationNames", "__propagatedTraitNames", "__classificationsText", "__propagatedClassificationNames")
# DEFERRED: Referenceable.ASSIGNED_TERMS = InternalKeywordTextField("meanings", "__meanings", "__meaningsText", "__meanings")
# DEFERRED: Referenceable.SUPER_TYPE_NAMES = InternalKeywordTextField("typeName", "__superTypeNames.keyword", "__superTypeNames", "__superTypeNames")
# DEFERRED: Referenceable.CREATE_TIME = InternalNumericField("createTime", "__timestamp", "__timestamp")
# DEFERRED: Referenceable.UPDATE_TIME = InternalNumericField("updateTime", "__modificationTimestamp", "__modificationTimestamp")
# DEFERRED: Referenceable.QUALIFIED_NAME = KeywordTextField("qualifiedName", "qualifiedName", "qualifiedName.text")
# DEFERRED: Referenceable.CUSTOM_ATTRIBUTES = TextField("customAttributes", "customAttributes")

    # Entity-level field descriptor placeholders (assigned at module bottom)
    TYPE_NAME: ClassVar[Any] = None
    """Type of the asset. For example Table, Column, and so on."""

    GUID: ClassVar[Any] = None
    """Globally unique identifier (GUID) of any object in Atlan."""

    CREATED_BY: ClassVar[Any] = None
    """Atlan user who created this asset."""

    UPDATED_BY: ClassVar[Any] = None
    """Atlan user who last updated the asset."""

    STATUS: ClassVar[Any] = None
    """Asset status in Atlan (active vs deleted)."""

    ATLAN_TAGS: ClassVar[Any] = None
    """All directly-assigned Atlan tags that exist on an asset."""

    PROPAGATED_ATLAN_TAGS: ClassVar[Any] = None
    """All propagated Atlan tags that exist on an asset."""

    ASSIGNED_TERMS: ClassVar[Any] = None
    """All terms attached to an asset, searchable by the term's qualifiedName."""

    SUPER_TYPE_NAMES: ClassVar[Any] = None
    """All super types of an asset."""

    CREATE_TIME: ClassVar[Any] = None
    """Time (in milliseconds) when the asset was created."""

    UPDATE_TIME: ClassVar[Any] = None
    """Time (in milliseconds) when the asset was last updated."""

    CUSTOM_ATTRIBUTES: ClassVar[Any] = None
    """Custom attributes for the asset, searchable as a single text field."""

    @classmethod
    def can_be_archived(cls) -> bool:
        """
        Indicates if an asset can be archived via the asset.delete_by_guid method.
        :returns: True if archiving is supported
        """
        return True

    @property
    def assigned_terms(self):
        """
        Get assigned glossary terms (maps to Entity.meanings).

        In legacy models, assigned_terms was a property that mapped to
        attributes.meanings. In v9, meanings is a direct field on Entity.
        """
        return self.meanings if self.meanings is not UNSET else None

    @assigned_terms.setter
    def assigned_terms(self, value):
        """Set assigned glossary terms."""
        self.meanings = value
