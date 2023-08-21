from pyatlan.model.fields.asset import AssetFields
from pyatlan.model.fields.atlan_fields import KeywordField


class AtlasGlossaryTermFields(AssetFields):

    ANCHOR = KeywordField("anchor", "__glossary")
    """Glossary in which the term is contained, searchable by the qualifiedName of the glossary."""

    CATEGORIES = KeywordField("categories", "__categories")
    """Categories in which the term is organized, searchable by the qualifiedName of the category."""
