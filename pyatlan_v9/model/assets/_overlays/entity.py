# INTERNAL_IMPORT: from pyatlan.model.assets.related_entity import SaveSemantic

    semantic: Union[SaveSemantic, None, UnsetType] = UNSET
    """Save semantic for relationship operations (REPLACE, APPEND, REMOVE).
    Not serialized to JSON - used internally by ref_by_guid/ref_by_qualified_name."""
