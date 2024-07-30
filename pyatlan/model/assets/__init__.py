# Copyright 2022 Atlan Pte. Ltd.
# isort: skip_file
import lazy_loader as lazy

submod_attrs = {
    "asset": ["Asset"],
    "referenceable": ["Referenceable"],
    "atlas_glossary": ["AtlasGlossary"],
    "atlas_glossary_term": ["AtlasGlossaryTerm"],
    "atlas_glossary_category": ["AtlasGlossaryCategory"],
    "database": ["Database"],
    "table": ["Table"],
    "column": ["Column"],
    "view": ["View"],
    "materialised_view": ["MaterialisedView"],
}

lazy_loader = lazy.attach(__name__, submod_attrs=submod_attrs)
__getattr__, __dir__, __all__ = lazy_loader
from .referenceable import Referenceable
