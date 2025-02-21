from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import DataProduct

client = AtlanClient()

response = client.asset.get_by_guid(
    guid="49abc625-9a03-4733-bdfb-ec0cb5315cac", asset_type=DataProduct
)
print(response)
a = response.get_assets()
print(a)
print(a.count)
