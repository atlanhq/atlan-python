import logging
from typing import Callable, List, Optional

import pytest
import requests

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Asset, Connection
from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.response import AssetMutationResponse
from pyatlan.test_utils import TestId
from pyatlan.test_utils.base_vcr import BaseVCR

LOGGER = logging.getLogger(__name__)


class TestBaseVCR(BaseVCR):
    @pytest.mark.vcr()
    def test_sample_get(self):
        response = requests.get("https://www.google.com/")
        assert response.status_code == 201


class TestConnection(BaseVCR):
    connection: Optional[Connection] = None

    @pytest.fixture(scope="module")
    def client(self) -> AtlanClient:
        return AtlanClient()

    @pytest.fixture(scope="module")
    def upsert(self, client: AtlanClient):
        guids: List[str] = []

        def _upsert(asset: Asset) -> AssetMutationResponse:
            _response = client.asset.save(asset)
            if (
                _response
                and _response.mutated_entities
                and _response.mutated_entities.CREATE
            ):
                guids.append(_response.mutated_entities.CREATE[0].guid)
            return _response

        yield _upsert

        # for guid in reversed(guids):
        #     response = client.asset.purge_by_guid(guid)
        #     if (
        #         not response
        #         or not response.mutated_entities
        #         or not response.mutated_entities.DELETE
        #     ):
        #         LOGGER.error(f"Failed to remove asset with GUID {guid}.")

    @pytest.mark.vcr(cassette_name="TestConnectionCreate.json")
    def test_create(
        self,
        client: AtlanClient,
        upsert: Callable[[Asset], AssetMutationResponse],
    ):
        role = client.role_cache.get_id_for_name("$admin")
        assert role
        connection_name = TestId.make_unique("INT")
        c = Connection.create(
            name=connection_name,
            connector_type=AtlanConnectorType.SNOWFLAKE,
            admin_roles=[role],
        )
        assert c.guid
        response = upsert(c)
        assert response.mutated_entities
        assert response.mutated_entities.CREATE
        assert len(response.mutated_entities.CREATE) == 1
        assert isinstance(response.mutated_entities.CREATE[0], Connection)
        assert response.guid_assignments
        c = response.mutated_entities.CREATE[0]
        c = client.asset.get_by_guid(c.guid, Connection, ignore_relationships=False)
        assert isinstance(c, Connection)
        TestConnection.connection = c

    # @pytest.mark.order(after="test_create")
    # @pytest.mark.vcr()
    # def test_create_for_modification(
    #     self, client: AtlanClient, upsert: Callable[[Asset], AssetMutationResponse]
    # ):
    #     assert TestConnection.connection
    #     assert TestConnection.connection.name
    #     connection = TestConnection.connection
    #     description = f"{connection.description} more stuff"
    #     connection = Connection.create_for_modification(
    #         qualified_name=TestConnection.connection.qualified_name or "",
    #         name=TestConnection.connection.name,
    #     )
    #     connection.description = description
    #     response = upsert(connection)
    #     verify_asset_updated(response, Connection)

    # @pytest.mark.order(after="test_create")
    # @pytest.mark.vcr()
    # def test_trim_to_required(
    #     self, client: AtlanClient, upsert: Callable[[Asset], AssetMutationResponse]
    # ):
    #     assert TestConnection.connection
    #     connection = TestConnection.connection.trim_to_required()
    #     response = upsert(connection)
    #     assert response.mutated_entities is None
