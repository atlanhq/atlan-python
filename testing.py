import logging

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Table

logging.basicConfig(level=logging.DEBUG)
client = AtlanClient()
# a = client.asset.get_by_guid(guid="21757812-b08c-49f7-b723-7d8dbb2e2dd1",ignore_relationships=False, attributes=[Asset.ATLAN_TAGS])
# column = client.asset.append_terms( #
#     asset_type=Table, #
#     qualified_name="default/snowflake/1746022526/WIDE_WORLD_IMPORTERS/BRONZE_SALES/ORDERS", #
#     terms=[AtlasGlossaryTerm.ref_by_guid(guid="e46b0ac0-5451-4161-b162-5e98aafede7f"),
#            AtlasGlossaryTerm.ref_by_guid(guid="e46b0ac0-5451-4161-b162-5e98aafede7f") ]
# ) #

client = AtlanClient()
client.asset.add_atlan_tags(
    asset_type=Table,
    qualified_name="default/snowflake/1746022526/WIDE_WORLD_IMPORTERS/BRONZE_WAREHOUSE/FIVETRAN_AUDIT",
    atlan_tag_names=["Alert: DQ-F2Cfn", "Alert: DQ-q4lhS"],  # n
)
# column = client.asset.add_atlan_tags( #
#     asset_type=Table, #
#     qualified_name="default/snowflake/1746022526/WIDE_WORLD_IMPORTERS/BRONZE_SALES/ORDERS", #
#     terms=[AtlasGlossaryTerm.ref_by_guid(guid="e46b0ac0-5451-4161-b162-5e98aafede7f") ]
# ) #

# print(column)
