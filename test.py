from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import DataDomain

client = AtlanClient()

domain = DataDomain.create(
    name="Marketing",
)
domain.owner_users = {"jdoe", "jsmith"}
response = client.asset.save(domain)

print(response)
