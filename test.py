from pyatlan.client.atlan import AtlanClient

client = AtlanClient()
groups = client.group.get_all(limit=1, offset=3, sort="-createdAt",columns=["roles","path"])
groups1 =  client.group.get_all(limit=10, offset=0, sort="-createdAt")
groups2 =  client.group.get_all(limit=10, offset=2)
groups3 =  client.group.get_all(limit=1)
groups4 =  client.group.get_all()

print("With Columns")
print(groups)
print("Wihout Columns")
print(groups1)
print("without sort")
print(groups2)
print("Without offset")
print(groups3)
print("empty")
print(groups4)