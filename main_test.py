import json
import os
import argparse
from pyatlan.client.atlan import AtlanClient
from pyatlan.cache.role_cache import RoleCache
from pyatlan.model.assets import Function
from datetime import datetime, timedelta
from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.assets import (Connection, Column, Function, CogniteAsset, CogniteSequence,
                                  CogniteTimeSeries, CogniteFile, Cognite3DModel, CogniteEvent)
import logging
from pyatlan.client.audit import AuditSearchRequest
from pyatlan.model.search import DSL, IndexSearchRequest, Terms, Term, Bool, Range, Wildcard, Aggregation
from pyatlan.model.search import SortItem, Range, NestedQuery, Exists
from pyatlan.model.fluent_search import FluentSearch, Term, CompoundQuery
import textwrap
import re
from jinja2 import Environment, FileSystemLoader
import os
import boto3

tenant_name = f"https://field-typedefs.atlan.com/"
bearer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJDY3FlMVRPTVktMTZoVTdnNUpFMDZlVlNiQ2tCQkZBRzQzREdNc3pkNWk4In0.eyJleHAiOjE3MjQxMjg4NjAsImlhdCI6MTcyNDA0MjQ2MCwiYXV0aF90aW1lIjoxNzI0MDQyNDQwLCJqdGkiOiIyM2E4M2I3Zi0zN2FjLTQ2ZjEtYjJjYS04ODgzMWMyMzZkOTgiLCJpc3MiOiJodHRwczovL2ZpZWxkLXR5cGVkZWZzLmF0bGFuLmNvbS9hdXRoL3JlYWxtcy9kZWZhdWx0IiwiYXVkIjpbInJlYWxtLW1hbmFnZW1lbnQiLCJhY2NvdW50Il0sInN1YiI6IjgzNjFhMzY4LWM4YzAtNDZhMC1hZjE0LTNjNTk0ZmUwYzBiMyIsInR5cCI6IkJlYXJlciIsImF6cCI6ImF0bGFuLWZyb250ZW5kIiwibm9uY2UiOiJiMmE1ZThmOC00OTcwLTQ2N2EtOTQ4Zi1iOWNjOTJmODFkNjUiLCJzZXNzaW9uX3N0YXRlIjoiYTQyNTdhNGQtZjA4Yi00MjM4LTgzZmMtNGQ1ZGZlMGMzZDZlIiwiYWNyIjoiMCIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sInJlc291cmNlX2FjY2VzcyI6eyJyZWFsbS1tYW5hZ2VtZW50Ijp7InJvbGVzIjpbInZpZXctcmVhbG0iLCJ2aWV3LWlkZW50aXR5LXByb3ZpZGVycyIsIm1hbmFnZS1pZGVudGl0eS1wcm92aWRlcnMiLCJpbXBlcnNvbmF0aW9uIiwicmVhbG0tYWRtaW4iLCJjcmVhdGUtY2xpZW50IiwibWFuYWdlLXVzZXJzIiwicXVlcnktcmVhbG1zIiwidmlldy1hdXRob3JpemF0aW9uIiwicXVlcnktY2xpZW50cyIsInF1ZXJ5LXVzZXJzIiwibWFuYWdlLWV2ZW50cyIsIm1hbmFnZS1yZWFsbSIsInZpZXctZXZlbnRzIiwidmlldy11c2VycyIsInZpZXctY2xpZW50cyIsIm1hbmFnZS1hdXRob3JpemF0aW9uIiwibWFuYWdlLWNsaWVudHMiLCJxdWVyeS1ncm91cHMiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJzaWQiOiJhNDI1N2E0ZC1mMDhiLTQyMzgtODNmYy00ZDVkZmUwYzNkNmUiLCJjcmVhdGVkQXQiOiIxNzE2MzY2Njk5Nzc4IiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJSdXBlc2ggWWFkYXYiLCJncm91cHMiOltdLCJyZWFsbSI6ImRlZmF1bHQiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJydXBlc2gueWFkYXYiLCJnaXZlbl9uYW1lIjoiUnVwZXNoIiwiZmFtaWx5X25hbWUiOiJZYWRhdiIsInVzZXJJZCI6IjgzNjFhMzY4LWM4YzAtNDZhMC1hZjE0LTNjNTk0ZmUwYzBiMyIsImVtYWlsIjoicnVwZXNoLnlhZGF2QGF0bGFuLmNvbSIsInVzZXJuYW1lIjoicnVwZXNoLnlhZGF2In0.F_tWJsh6GZxd2iEGpMmG6JFRo_KP3BkGbvuZWO0FHrkjjHgh-xZPNa2-HUy_VZVgCjLdYTZN0oyGc5-ZJdQwW5RK9yPHkUIw7wP3J4Ib217su-NZXDm6bHvJkJ6Fi7EAPpXMj32LGHca16cvpDsr2VdU8bK7GT3Ux9EaYuijFQ9ZaSSa2AyjNErznJAf2h937lGgJjrhnaU5w_Pxk-4xbw01Z47IEFBPUOvqUoY71ySZFccBpCmRAP2adSoAnN6_GLaIaa3u2KRTN8dgaf8QUYZ1F5kp4DfAdvmizvbwmKgvXq28Ek6yZr02OGuCASAZ66L4xNtadHaUeFzQaxqjyg'
client = AtlanClient(
    base_url=tenant_name,
    api_key=bearer_token,
)
#
# client.asset.delete_by_guid('fccd9fda-d388-46c0-a57b-1f3a2c45b362')
# client.asset.delete_by_guid('3000b214-7af7-47fc-b813-308e06e89cc1')
# client.asset.delete_by_guid('e74fbf59-6f1f-4a54-8a82-85ad4214a34f')
#
#
# connector = AtlanConnectorType.COGNITE
# admin_role_guid = RoleCache.get_id_for_name("$admin")
# cognite_connection = Connection.create(connector_type=connector, name='CogniteTestConnection',
#                                        admin_roles=[admin_role_guid])
# cognite_create_response = client.asset.save(entity=cognite_connection)
# cognite_connection_qualified_name = cognite_create_response.assets_created(asset_type=Connection)[0].qualified_name
#
CogniteAsset_type = CogniteAsset.creator(
    name='Asset_test4',
    connection_qualified_name='default/cognite/1724125659'
)
#
response = client.asset.save(CogniteAsset_type)
# asset_guid = response.assets_created(asset_type=CogniteAsset)[0].qualified_name
# print(response)

# CogniteAssetfile = CogniteFile.creator(
#     name='file1',
#     cognite_asset_qualified_name='default/cognite/1724125659/Asset_test1',
#     connection_qualified_name='default/cognite/1724125659',
# )
# CogniteAssetfile.cognite_asset = [client.asset.get_by_guid('ad20e09f-c28b-45b0-b44c-930f24216397')]
# response = client.asset.save(CogniteAssetfile)






# CogniteAsset.connection_qualified_name = cognite_connection_qualified_name
# CogniteAsset_type.connector_name = 'CogniteTestConnection'
# CogniteAsset_type.connection_name = AtlanConnectorType.COGNITE
# response = client.asset.save(CogniteAsset_type)
#
#
# CogniteAsset_type = CogniteAsset.updater(
#     name='Asset_test2',
#     qualified_name=cognite_connection_qualified_name+'/Asset_test2'
# )
# CogniteAsset.connection_qualified_name = cognite_connection_qualified_name
# CogniteAsset_type.connector_name = 'CogniteTestConnection'
# CogniteAsset_type.connection_name = AtlanConnectorType.COGNITE
# response = client.asset.save(CogniteAsset_type)
#
# CogniteAsset_type = CogniteAsset.updater(
#     name='Asset_test3',
#     qualified_name=cognite_connection_qualified_name + '/Asset_test3'
# )
# CogniteAsset.connection_qualified_name = cognite_connection_qualified_name
# CogniteAsset_type.connector_name = 'CogniteTestConnection'
# CogniteAsset_type.connection_name = AtlanConnectorType.COGNITE
# response = client.asset.save(CogniteAsset_type)
#
# CogniteAsset_type = CogniteAsset.updater(
#     name='Asset_test4',
#     qualified_name=cognite_connection_qualified_name + '/Asset_test4'
# )
# CogniteAsset.connection_qualified_name = cognite_connection_qualified_name
# CogniteAsset_type.connector_name = 'CogniteTestConnection'
# CogniteAsset_type.connection_name = AtlanConnectorType.COGNITE
# response = client.asset.save(CogniteAsset_type)
#
