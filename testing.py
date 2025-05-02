from pyatlan.client.atlan import AtlanClient

client = AtlanClient()
users = client.group.get_all(limit=2)

for user in users:
    print(user)
