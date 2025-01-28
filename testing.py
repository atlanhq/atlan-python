from pyatlan.client.atlan import AtlanClient

client = AtlanClient()

a = client.credentials.get(guid="0d53667b-f957-4d28-ac3a-fd7ab99d6e7a")
print(a)
