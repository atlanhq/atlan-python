# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.
import logging
import random
from os import path
from typing import List, Optional, Type

from nanoid import generate as generate_nanoid  # type: ignore
from pydantic.v1 import StrictStr

from pyatlan.cache.role_cache import RoleCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.api_tokens import ApiToken
from pyatlan.model.assets import (
    Asset,
    AtlasGlossary,
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    Column,
    Connection,
    Database,
    MaterialisedView,
    Schema,
    Table,
    View,
)
from pyatlan.model.enums import AtlanConnectorType, AtlanIcon, AtlanTagColor
from pyatlan.model.group import AtlanGroup, CreateGroupResponse
from pyatlan.model.response import A, AssetMutationResponse
from pyatlan.model.typedef import AttributeDef, CustomMetadataDef

LOGGER = logging.getLogger(__name__)


class TestId:
    session_id = generate_nanoid(
        alphabet="1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        size=5,
    )

    @classmethod
    def make_unique(cls, input: str):
        return f"psdk_{input}_{cls.session_id}"


def get_random_connector():
    return random.choice(list(AtlanConnectorType))  # noqa: S311


def delete_token(client: AtlanClient, token: Optional[ApiToken] = None):
    # If there is a partial failure on the server side
    # and the token is still visible in the Atlan UI,
    # in that case, the create method may not return a token.
    # We should retrieve the list of all tokens and delete them here.
    if not token:
        tokens = client.token.get().records
        assert tokens  # noqa: S101
        delete_tokens = [
            token
            for token in tokens
            if token.display_name and "psdk_Requests" in token.display_name
        ]
        for token in delete_tokens:
            assert token and token.guid  # noqa: S101
            client.token.purge(token.guid)
        return
    # In case of no partial failure, directly delete the token
    token.guid and client.token.purge(token.guid)


def save_with_purge(client: AtlanClient):
    guids: List[str] = []

    def _save(asset: Asset) -> AssetMutationResponse:
        _response = client.asset.save(asset)
        if (
            _response
            and _response.mutated_entities
            and _response.mutated_entities.CREATE
        ):
            guids.append(_response.mutated_entities.CREATE[0].guid)
        return _response

    yield _save

    for guid in reversed(guids):
        response = client.asset.purge_by_guid(guid)
        if (
            not response
            or not response.mutated_entities
            or not response.mutated_entities.DELETE
        ):
            LOGGER.error(f"Failed to remove asset with GUID {guid}.")


def delete_asset(client: AtlanClient, asset_type: Type[A], guid: str) -> None:
    # These assertions check the cleanup actually worked
    r = client.asset.purge_by_guid(guid)
    s = r is not None
    s = s and len(r.assets_deleted(asset_type)) == 1
    s = s and r.assets_deleted(asset_type)[0].guid == guid
    if not s:
        LOGGER.error(f"Failed to remove {asset_type} with GUID {guid}.")


def create_connection(
    client: AtlanClient, name: str, connector_type: AtlanConnectorType
) -> Connection:
    admin_role_guid = str(RoleCache.get_id_for_name("$admin"))
    to_create = Connection.create(
        name=name, connector_type=connector_type, admin_roles=[admin_role_guid]
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=Connection)[0]
    return client.asset.get_by_guid(result.guid, asset_type=Connection)


def create_group(client: AtlanClient, name: str) -> CreateGroupResponse:
    g = AtlanGroup.create(alias=StrictStr(name))
    r = client.group.create(g)
    return r


def create_glossary(client: AtlanClient, name: str) -> AtlasGlossary:
    g = AtlasGlossary.create(name=StrictStr(name))
    r = client.asset.save(g)
    return r.assets_created(AtlasGlossary)[0]


def create_category(
    client: AtlanClient,
    name: str,
    glossary: AtlasGlossary,
    parent: Optional[AtlasGlossaryCategory] = None,
) -> AtlasGlossaryCategory:
    c = AtlasGlossaryCategory.create(
        name=name, anchor=glossary, parent_category=parent or None
    )
    return client.asset.save(c).assets_created(AtlasGlossaryCategory)[0]


def create_term(
    client: AtlanClient,
    name: str,
    glossary_guid: str,
    categories: Optional[List[AtlasGlossaryCategory]] = None,
) -> AtlasGlossaryTerm:
    t = AtlasGlossaryTerm.create(
        name=StrictStr(name),
        glossary_guid=StrictStr(glossary_guid),
        categories=categories,
    )
    r = client.asset.save(t)
    return r.assets_created(AtlasGlossaryTerm)[0]


def create_database(client: AtlanClient, database_name: str, connection: Connection):
    to_create = Database.create(
        name=database_name, connection_qualified_name=connection.qualified_name
    )
    result = client.asset.save(to_create)
    return result.assets_created(asset_type=Database)[0]


def create_schema(client: AtlanClient, schema_name: str, database: Database):
    to_create = Schema.create(
        name=schema_name, connection_qualified_name=database.qualified_name
    )
    result = client.asset.save(to_create)
    return result.assets_created(asset_type=Schema)[0]


def create_table(client: AtlanClient, table_name: str, schema: Schema):
    to_create = Table.create(
        name=table_name, schema_qualified_name=schema.qualified_name
    )
    result = client.asset.save(to_create)
    return result.assets_created(asset_type=Table)[0]


def create_view(client: AtlanClient, view_name: str, schema: Schema):
    to_create = View.create(name=view_name, schema_qualified_name=schema.qualified_name)
    result = client.asset.save(to_create)
    return result.assets_created(asset_type=View)[0]


def create_mview(client: AtlanClient, mview_name: str, schema: Schema):
    to_create = MaterialisedView.create(
        name=mview_name, schema_qualified_name=schema.qualified_name
    )
    result = client.asset.save(to_create)
    return result.assets_created(asset_type=MaterialisedView)[0]


def create_column(
    client: AtlanClient, column_name: str, parent_type: type, parent: Asset, order: int
):
    to_create = Column.create(
        name=column_name,
        parent_type=parent_type,
        parent_qualified_name=parent.qualified_name,
        order=order,
    )
    result = client.asset.save(to_create)
    return result.assets_created(asset_type=Column)[0]


def create_custom_metadata(
    client: AtlanClient,
    name: str,
    attribute_defs: List[AttributeDef],
    locked: bool,
    logo: Optional[str] = None,
    icon: Optional[AtlanIcon] = None,
    color: Optional[AtlanTagColor] = None,
) -> CustomMetadataDef:
    cm_def = CustomMetadataDef.create(display_name=name)
    cm_def.attribute_defs = attribute_defs
    if icon and color:
        cm_def.options = CustomMetadataDef.Options.with_logo_from_icon(
            icon, color, locked
        )
    elif logo and logo.startswith("http"):
        cm_def.options = CustomMetadataDef.Options.with_logo_from_url(logo, locked)
    elif logo:
        cm_def.options = CustomMetadataDef.Options.with_logo_as_emoji(logo, locked)
    else:
        raise ValueError(
            "Invalid configuration for the visual to use for the custom metadata."
        )
    r = client.typedef.create(cm_def)
    return r.custom_metadata_defs[0]


def validate_error_free_logs(files: List[str]):
    """
    Asserts that the specified log files do not contain any error messages.

    :param files: a list of file paths to the log files to be validated
    """
    for file in files:
        with open(file, "r") as log:
            log_contents = log.read()
            assert "ERROR" not in log_contents  # noqa: S101


def validate_files_exist(files: List[str]):
    """
    Asserts that the specified files exist and are non-empty.

    :param files: a list of file paths to be validated
    """
    for file in files:
        assert path.isfile(file)  # noqa: S101
        assert path.getsize(file) > 0  # noqa: S101
