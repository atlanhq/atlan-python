from pyatlan.model.fields.atlan_fields import KeywordTextField, KeywordTextStemmedField
from pyatlan.model.fields.referenceable import ReferenceableFields


class AssetFields(ReferenceableFields):

    NAME = KeywordTextStemmedField("name", "name.keyword", "name", "name.stemmed")
    """Human-readable name of the asset."""

    QUALIFIED_NAME = KeywordTextField(
        "qualifiedName", "qualifiedName", "qualifiedName.text"
    )
    """Unique fully-qualified name of the asset in Atlan."""
