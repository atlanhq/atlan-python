# from pyatlan.cache.role_cache import RoleCache
# from pyatlan.client.atlan import AtlanClient
# from pyatlan.model.assets import Connection, QuickSightDataset, Schema, Table, View, MaterialisedView, Column,
# from pyatlan.model.enums import AtlanConnectorType, QuickSightFolderType
# from pyatlan.model.enums import QuickSightDatasetImportMode

# client = AtlanClient()
# # database = QuickSightDataset.creator( #
# #     name="qs_folder_test1", #
# #     connection_qualified_name="default/quicksight/1738057453",
# #     quick_sight_id="123455",
# #     quick_sight_dataset_import_mode= QuickSightDatasetImportMode.SPICE,
# #     quick_sight_dataset_column_count=10
# # )
# # print(database)
# # a = client.asset.get_by_guid(guid="d5995cc9-8429-46f1-8219-9211ae027b0b")
# # print(a)


from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Connection

client = AtlanClient()

# create_credential = Credential()
# create_credential.auth_type = "atlan_api_key"
# create_credential.name = (
#     f"default-spark-23344-0"
# )
# create_credential.connector = "spark"
# create_credential.connector_config_name = (
#     f"atlan-connectors-spark"
# )
# create_credential.connector_type = "event"
# create_credential.extras = {
#     "events.enable-partial-assets": True,
#     "events.enabled": True,
#     "events.topic": f"openlineage_spark",
#     "events.urlPath": f"/events/openlineage/spark/api/v1/lineage",
# }

# response = client.credentials.creator(create_credential) #
# print(response)


# connection = Connection.updater(qualified_name="default/snowflake/1738006457", name="development")

# connection.default_credential_guid = "4a5d9c55-75c4-4d77-8270-b0a16d4b7e92"

# response = client.asset.save(connection)
# print(response)

connection = client.asset.get_by_qualified_name(
    qualified_name="default/snowflake/1738006457", asset_type=Connection
)
# print(connection)
print(connection.default_credential_guid)
