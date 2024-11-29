from pyatlan.client.atlan import AtlanClient

client = AtlanClient()

groups = client.group.get_all(limit=1)

print(groups)
