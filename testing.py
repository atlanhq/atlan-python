from pyatlan.client.atlan import AtlanClient

# GUID="3e939271-abbd-42bf-9188-9cff9ee36387"
# request = FluentSearch().select().where(Asset.GUID.eq(GUID))
# .include_on_results(["qualified_name","name"]).execute(client)

# candidate = (response.current_page() and response.current_page()[0]) or None
# print(candidate)

client = AtlanClient()

response = client.asset.get_by_guid(guid="3e939271-abbd-42bf-9188-9cff9ee36387")
print(response)
print("next")
# client = AtlanClient()

# GUID = "3e939271-abbd-42bf-9188-9cff9ee36387"
# request = (
#     FluentSearch()
#     .select()
#     .where(Asset.GUID.eq(GUID))
#     .include_on_results(["qualified_name", "name"])  # Ensure all elements are strings
#     .execute(client)
# )

# print(request)
