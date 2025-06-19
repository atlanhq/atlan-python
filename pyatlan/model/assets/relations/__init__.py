import lazy_loader as lazy

__PYATLAN_ASSET_RELATIONS__ = {
    "relationship_attributes": ["RelationshipAttributes"],
    "user_def_relationship": ["UserDefRelationship"],
}

lazy_loader = lazy.attach(__name__, submod_attrs=__PYATLAN_ASSET_RELATIONS__)
__getattr__, __dir__, __all__ = lazy_loader
