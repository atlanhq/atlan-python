from pyatlan.model.core import AtlanObject


class InitRequest(AtlanObject):
    asset_type: str
    asset_qualified_name: str
