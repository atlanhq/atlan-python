

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Asset, Table
from pyatlan.model.enums import SaveSemantic
from pyatlan.model.fluent_search import FluentSearch, CompoundQuery
from pyatlan.model.assets.core.referenceable import AtlasGlossaryTerm
import logging
client = AtlanClient()
qn = "default/snowflake/1735595539/ANALYTICS/WIDE_WORLD_IMPORTERS/matillion_stg_airports"
term_qualified_name = "qZQt8hefUnbFwvCs48Kcl@LXNKR7hl7TLTPx1kKUK0V"
logging.basicConfig(level=logging.DEBUG)

# search = (
#         FluentSearch()
#         .select()
#         .where(CompoundQuery.active_assets())
#         .where(Asset.QUALIFIED_NAME.eq(QN))
#             )
# results = search.execute(client=client)
# if results and results.current_page():
#     first_result = results.current_page()[0]
#     print(first_result)

# response = client.asset.append_terms( #
#     asset_type=Table, #
#     qualified_name=qn, #
#     terms=[AtlasGlossaryTerm.ref_by_qualified_name(qualified_name=, semantic= SaveSemantic.APPEND)],
#     name="matillion_stg_airports"
#     )
asset_tables = Table.create_for_modification(qualified_name= qn,name = "matillion_stg_airports")
asset_tables.assigned_terms = [AtlasGlossaryTerm.ref_by_guid(guid="1025d13b-24d6-404d-80fd-869e72be7e00", semantic=SaveSemantic.APPEND)]
response = client.asset.save(asset_tables)
print(response)

# import ipdb; ipdb.set_trace()
# guid1 = "e60a0cb8-d416-4e21-b70a-a56a7b6cfc19"
# term = AtlasGlossaryTerm.create_for_modification(
#         qualified_name="ZWm178w8rfKUNWnoccghL@2kS6ivv9A3sMEmQawU26z",
#         name="test1",
#         glossary_guid="387df689-82e5-49c6-b77d-038222c12c34",
# )
# term.see_also = [
#     AtlasGlossaryTerm.ref_by_guid(guid="1025d13b-24d6-404d-80fd-869e72be7e00", semantic=SaveSemantic.APPEND),
# ]
# response = client.asset.save(term)