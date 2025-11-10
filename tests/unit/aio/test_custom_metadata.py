# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from unittest.mock import AsyncMock, patch

import pytest

from pyatlan.client.aio.client import AsyncAtlanClient
from pyatlan.errors import AtlanError, ErrorCode, NotFoundError
from pyatlan.model.aio.custom_metadata import (
    AsyncCustomMetadataDict,
    AsyncCustomMetadataProxy,
    AsyncCustomMetadataRequest,
)
from pyatlan.model.assets.core.asset import Asset
from pyatlan.model.enums import AtlanCustomAttributePrimitiveType
from pyatlan.model.typedef import AttributeDef

ATTR_LAST_NAME = "Last Name"
ATTR_LAST_NAME_ID = "2"
ATTR_FIRST_NAME = "First Name"
ATTR_FIRST_NAME_ID = "1"
CM_ID = "123"
CM_NAME = "Something"
CM_ATTRIBUTES = {ATTR_FIRST_NAME_ID: ATTR_FIRST_NAME, ATTR_LAST_NAME_ID: ATTR_LAST_NAME}
META_DATA = {CM_ID: CM_ATTRIBUTES}


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")


@pytest.fixture()
def client():
    return AsyncAtlanClient()


def get_attr_id_for_name(*args, **kwargs):
    return ATTR_FIRST_NAME_ID if args[1] == ATTR_FIRST_NAME else ATTR_LAST_NAME_ID


def get_attr_name_for_id(*args, **kwargs):
    return ATTR_FIRST_NAME if args[1] == ATTR_FIRST_NAME_ID else ATTR_LAST_NAME


class TestAsyncCustomMetadataDict:
    @pytest.fixture()
    async def sut(self, mock_async_custom_metadata_cache, client: AsyncAtlanClient):
        mock_async_custom_metadata_cache.get_id_for_name = AsyncMock(return_value=CM_ID)
        mock_async_custom_metadata_cache.get_attr_map_for_id = AsyncMock(
            return_value=CM_ATTRIBUTES
        )
        mock_async_custom_metadata_cache.is_attr_archived = AsyncMock(
            return_value=False
        )

        return await AsyncCustomMetadataDict.creator(client=client, name=CM_NAME)

    @pytest.mark.asyncio
    async def test_init_when_invalid_name_throws_not_found_error(
        self, mock_async_custom_metadata_cache, client: AsyncAtlanClient
    ):
        mock_async_custom_metadata_cache.get_id_for_name = AsyncMock(
            side_effect=ErrorCode.ASSET_NOT_FOUND_BY_GUID.exception_with_parameters(
                "123"
            )
        )
        with pytest.raises(NotFoundError):
            await AsyncCustomMetadataDict.creator(client=client, name=CM_NAME)
        mock_async_custom_metadata_cache.get_id_for_name.assert_called_with(CM_NAME)

    @pytest.mark.asyncio
    async def test_modified_after_init_returns_false(self, sut):
        assert sut.modified is False

    @pytest.mark.asyncio
    async def test_init_when_called_with_valid_name_initializes_names(self, sut):
        assert sut.attribute_names == set(CM_ATTRIBUTES.values())

    @pytest.mark.asyncio
    async def test_can_get_set_items(self, sut):
        sut[ATTR_FIRST_NAME] = "123"
        assert sut[ATTR_FIRST_NAME] == "123"
        assert sut.modified is True

    @pytest.mark.asyncio
    async def test_get_item_with_invalid_name_raises_key_error(self, sut):
        with pytest.raises(KeyError):
            _ = sut["Invalid Name"]

    @pytest.mark.asyncio
    async def test_set_item_with_invalid_name_raises_key_error(self, sut):
        with pytest.raises(KeyError):
            sut["Invalid Name"] = "123"

    @pytest.mark.parametrize("attribute_name", [ATTR_FIRST_NAME, ATTR_LAST_NAME])
    @pytest.mark.asyncio
    async def test_clear_all_set_all_attributes_to_none(self, sut, attribute_name):
        sut[attribute_name] = "123"
        sut.clear_all()
        assert sut[attribute_name] is None

    @pytest.mark.parametrize(
        "attribute_name,other_attr",
        [(ATTR_FIRST_NAME, ATTR_LAST_NAME), (ATTR_LAST_NAME, ATTR_FIRST_NAME)],
    )
    @pytest.mark.asyncio
    async def test_clear_unset_sets_unset_to_none(
        self, sut, attribute_name, other_attr
    ):
        sut[attribute_name] = "123"
        sut.clear_unset()
        assert sut[attribute_name] == "123"
        assert sut[other_attr] is None

    @pytest.mark.asyncio
    async def test_get_item_using_name_that_has_not_been_set_returns_none(self, sut):
        assert sut[ATTR_FIRST_NAME] is None

    @pytest.mark.asyncio
    async def test_business_attributes_when_no_changes(self, sut):
        business_attrs = await sut.business_attributes()
        assert business_attrs == {}

    @pytest.mark.asyncio
    async def test_business_attributes_with_data(
        self, mock_async_custom_metadata_cache, sut
    ):
        mock_async_custom_metadata_cache.get_attr_id_for_name = AsyncMock(
            return_value=ATTR_FIRST_NAME_ID
        )
        sut[ATTR_FIRST_NAME] = "123"
        business_attrs = await sut.business_attributes()
        assert business_attrs == {ATTR_FIRST_NAME_ID: "123"}

    @pytest.mark.parametrize("attribute_name", [ATTR_FIRST_NAME, ATTR_LAST_NAME])
    @pytest.mark.asyncio
    async def test_is_unset_initially_returns_false(self, sut, attribute_name):
        assert not sut.is_set(attribute_name)

    @pytest.mark.parametrize("attribute_name", [ATTR_FIRST_NAME, ATTR_LAST_NAME])
    @pytest.mark.asyncio
    async def test_unset_after_update_returns_true(self, sut, attribute_name):
        sut[attribute_name] = "123"
        assert sut.is_set(attribute_name)

    @pytest.mark.asyncio
    async def test_get_deleted_sentinel(self):
        sentinel = AsyncCustomMetadataDict.get_deleted_sentinel()
        assert sentinel._name == "(DELETED)"


class TestAsyncCustomMetadataProxy:
    @pytest.mark.asyncio
    async def test_when_intialialized_with_no_business_attributes_then_modified_is_false(
        self, client: AsyncAtlanClient
    ):
        proxy = AsyncCustomMetadataProxy(client=client, business_attributes=None)
        assert not proxy.modified

    @pytest.mark.asyncio
    async def test_when_intialialized_with_no_business_attributes_then_business_attributes_returns_none(
        self, client: AsyncAtlanClient
    ):
        proxy = AsyncCustomMetadataProxy(client=client, business_attributes=None)
        business_attrs = await proxy.business_attributes()
        assert business_attrs is None

    @pytest.mark.asyncio
    async def test_set_custom_metadata(
        self, mock_async_custom_metadata_cache, client: AsyncAtlanClient
    ):
        mock_async_custom_metadata_cache.get_id_for_name = AsyncMock(return_value=CM_ID)
        mock_async_custom_metadata_cache.get_attr_map_for_id = AsyncMock(
            return_value=CM_ATTRIBUTES
        )
        mock_async_custom_metadata_cache.is_attr_archived = AsyncMock(
            return_value=False
        )

        proxy = AsyncCustomMetadataProxy(client=client, business_attributes=None)

        custom_metadata_dict = await AsyncCustomMetadataDict.creator(
            client=client, name=CM_NAME
        )
        await proxy.set_custom_metadata(custom_metadata_dict)

        assert proxy.modified

    @pytest.mark.asyncio
    async def test_after_modifying_metadata_modified_is_true(
        self, mock_async_custom_metadata_cache, client: AsyncAtlanClient
    ):
        mock_async_custom_metadata_cache.get_id_for_name = AsyncMock(return_value=CM_ID)
        mock_async_custom_metadata_cache.get_attr_map_for_id = AsyncMock(
            return_value=CM_ATTRIBUTES
        )
        mock_async_custom_metadata_cache.is_attr_archived = AsyncMock(
            return_value=False
        )

        proxy = AsyncCustomMetadataProxy(client=client, business_attributes=None)

        custom_metadata = await proxy.get_custom_metadata(CM_NAME)
        custom_metadata[ATTR_FIRST_NAME] = "Jane"

        assert proxy.modified

    @pytest.mark.asyncio
    async def test_when_not_modified_returns_business_attributes(
        self, mock_async_custom_metadata_cache, client: AsyncAtlanClient
    ):
        business_attrs_input = {CM_ID: {ATTR_FIRST_NAME_ID: "Jane"}}
        mock_async_custom_metadata_cache.get_id_for_name = AsyncMock(return_value=CM_ID)
        mock_async_custom_metadata_cache.get_name_for_id = AsyncMock(
            return_value=CM_NAME
        )
        mock_async_custom_metadata_cache.get_attr_map_for_id = AsyncMock(
            return_value=CM_ATTRIBUTES
        )
        mock_async_custom_metadata_cache.get_attr_name_for_id = AsyncMock(
            return_value=ATTR_FIRST_NAME
        )
        mock_async_custom_metadata_cache.is_attr_archived = AsyncMock(
            return_value=False
        )

        proxy = AsyncCustomMetadataProxy(
            client=client, business_attributes=business_attrs_input
        )
        business_attrs = await proxy.business_attributes()

        assert business_attrs == business_attrs_input

    @pytest.mark.asyncio
    async def test_when_modified_returns_updated_business_attributes(
        self, mock_async_custom_metadata_cache, client: AsyncAtlanClient
    ):
        mock_async_custom_metadata_cache.get_id_for_name = AsyncMock(return_value=CM_ID)
        mock_async_custom_metadata_cache.get_attr_map_for_id = AsyncMock(
            return_value=CM_ATTRIBUTES
        )
        mock_async_custom_metadata_cache.is_attr_archived = AsyncMock(
            return_value=False
        )
        mock_async_custom_metadata_cache.get_attr_id_for_name = AsyncMock(
            return_value=ATTR_FIRST_NAME_ID
        )

        proxy = AsyncCustomMetadataProxy(client=client, business_attributes=None)

        custom_metadata = await proxy.get_custom_metadata(CM_NAME)
        custom_metadata[ATTR_FIRST_NAME] = "Jane"

        business_attrs = await proxy.business_attributes()
        assert business_attrs == {CM_ID: {ATTR_FIRST_NAME_ID: "Jane"}}

    @pytest.mark.asyncio
    async def test_when_invalid_metadata_set_then_delete_sentinel_is_used(
        self, mock_async_custom_metadata_cache, client: AsyncAtlanClient
    ):
        mock_async_custom_metadata_cache.get_name_for_id = AsyncMock(
            side_effect=ErrorCode.CM_NOT_FOUND_BY_ID.exception_with_parameters(
                "invalid-id"
            )
        )

        business_attrs_input = {"invalid-id": {ATTR_FIRST_NAME_ID: "Jane"}}
        proxy = AsyncCustomMetadataProxy(
            client=client, business_attributes=business_attrs_input
        )
        await proxy._initialize_metadata()

        assert proxy._metadata is not None
        assert "(DELETED)" in proxy._metadata

    @pytest.mark.asyncio
    async def test_when_property_is_archived(
        self, mock_async_custom_metadata_cache, client: AsyncAtlanClient
    ):
        mock_async_custom_metadata_cache.get_id_for_name = AsyncMock(return_value=CM_ID)
        mock_async_custom_metadata_cache.get_name_for_id = AsyncMock(
            return_value=CM_NAME
        )
        mock_async_custom_metadata_cache.get_attr_map_for_id = AsyncMock(
            return_value=CM_ATTRIBUTES
        )
        mock_async_custom_metadata_cache.get_attr_name_for_id = AsyncMock(
            return_value=ATTR_FIRST_NAME
        )
        mock_async_custom_metadata_cache.is_attr_archived = AsyncMock(
            return_value=True
        )  # Archived

        business_attrs_input = {CM_ID: {ATTR_FIRST_NAME_ID: "Jane"}}
        proxy = AsyncCustomMetadataProxy(
            client=client, business_attributes=business_attrs_input
        )
        await proxy._initialize_metadata()

        # Should not include archived attributes in the names set
        assert proxy._metadata is not None
        custom_metadata = proxy._metadata[CM_NAME]
        assert ATTR_FIRST_NAME not in custom_metadata.attribute_names


class TestAsyncCustomMetadataRequest:
    @pytest.mark.asyncio
    async def test_create(
        self, mock_async_custom_metadata_cache, client: AsyncAtlanClient
    ):
        mock_async_custom_metadata_cache.get_id_for_name = AsyncMock(return_value=CM_ID)
        mock_async_custom_metadata_cache.get_attr_map_for_id = AsyncMock(
            return_value=CM_ATTRIBUTES
        )
        mock_async_custom_metadata_cache.is_attr_archived = AsyncMock(
            return_value=False
        )
        mock_async_custom_metadata_cache.get_attr_id_for_name = AsyncMock(
            return_value=ATTR_FIRST_NAME_ID
        )

        custom_metadata_dict = await AsyncCustomMetadataDict.creator(
            client=client, name=CM_NAME
        )
        custom_metadata_dict[ATTR_FIRST_NAME] = "Jane"

        request = await AsyncCustomMetadataRequest.create(custom_metadata_dict)

        assert request.__root__ == {ATTR_FIRST_NAME_ID: "Jane"}
        assert request.custom_metadata_set_id == CM_ID


class TestAsyncReferenceableCustomMetadata:
    """Test async custom metadata methods on Referenceable (via Asset)"""

    @pytest.mark.asyncio
    async def test_get_custom_metadata_async(
        self, mock_async_custom_metadata_cache, client: AsyncAtlanClient
    ):
        # Configure the mock
        mock_async_custom_metadata_cache.get_id_for_name = AsyncMock(return_value=CM_ID)
        mock_async_custom_metadata_cache.get_name_for_id = AsyncMock(
            return_value=CM_NAME
        )
        mock_async_custom_metadata_cache.get_attr_map_for_id = AsyncMock(
            return_value=CM_ATTRIBUTES
        )
        mock_async_custom_metadata_cache.get_attr_name_for_id = AsyncMock(
            return_value=ATTR_FIRST_NAME
        )
        mock_async_custom_metadata_cache.is_attr_archived = AsyncMock(
            return_value=False
        )

        # Create an asset with business attributes
        asset = Asset()
        asset.business_attributes = {CM_ID: {ATTR_FIRST_NAME_ID: "Jane"}}

        # Test get_custom_metadata_async
        custom_metadata = await asset.get_custom_metadata_async(client, CM_NAME)

        assert isinstance(custom_metadata, AsyncCustomMetadataDict)
        assert custom_metadata.attribute_names == {ATTR_FIRST_NAME, ATTR_LAST_NAME}

    @pytest.mark.asyncio
    async def test_set_custom_metadata_async(
        self, mock_async_custom_metadata_cache, client: AsyncAtlanClient
    ):
        # Configure the mock
        mock_async_custom_metadata_cache.get_id_for_name = AsyncMock(return_value=CM_ID)
        mock_async_custom_metadata_cache.get_attr_map_for_id = AsyncMock(
            return_value=CM_ATTRIBUTES
        )
        mock_async_custom_metadata_cache.is_attr_archived = AsyncMock(
            return_value=False
        )

        # Create an asset
        asset = Asset()
        asset.business_attributes = None

        # Create custom metadata
        custom_metadata = await AsyncCustomMetadataDict.creator(
            client=client, name=CM_NAME
        )
        custom_metadata[ATTR_FIRST_NAME] = "John"

        # Test set_custom_metadata_async
        await asset.set_custom_metadata_async(client, custom_metadata)

        # Verify the async metadata proxy was created and modified
        assert asset._async_metadata_proxy is not None
        assert asset._async_metadata_proxy.modified

    @pytest.mark.asyncio
    async def test_flush_custom_metadata_async(
        self, mock_async_custom_metadata_cache, client: AsyncAtlanClient
    ):
        # Configure the mock
        mock_async_custom_metadata_cache.get_id_for_name = AsyncMock(return_value=CM_ID)
        mock_async_custom_metadata_cache.get_attr_map_for_id = AsyncMock(
            return_value=CM_ATTRIBUTES
        )
        mock_async_custom_metadata_cache.is_attr_archived = AsyncMock(
            return_value=False
        )
        mock_async_custom_metadata_cache.get_attr_id_for_name = AsyncMock(
            return_value=ATTR_FIRST_NAME_ID
        )

        # Create an asset
        asset = Asset()
        asset.business_attributes = None

        # Create and set custom metadata
        custom_metadata = await AsyncCustomMetadataDict.creator(
            client=client, name=CM_NAME
        )
        custom_metadata[ATTR_FIRST_NAME] = "John"
        await asset.set_custom_metadata_async(client, custom_metadata)

        # Test flush_custom_metadata_async
        await asset.flush_custom_metadata_async(client)

        # Verify business_attributes was updated
        assert asset.business_attributes is not None
        assert CM_ID in asset.business_attributes
        assert asset.business_attributes[CM_ID][ATTR_FIRST_NAME_ID] == "John"

    @pytest.mark.asyncio
    async def test_async_metadata_proxy_independence(
        self, mock_async_custom_metadata_cache, client: AsyncAtlanClient
    ):
        """Test that async and sync metadata proxies are independent"""
        # Configure the mock
        mock_async_custom_metadata_cache.get_id_for_name = AsyncMock(return_value=CM_ID)
        mock_async_custom_metadata_cache.get_attr_map_for_id = AsyncMock(
            return_value=CM_ATTRIBUTES
        )
        mock_async_custom_metadata_cache.is_attr_archived = AsyncMock(
            return_value=False
        )

        # Create an asset
        asset = Asset()
        asset.business_attributes = None

        # Use async methods
        await asset.get_custom_metadata_async(client, CM_NAME)

        # Verify async proxy was created but sync proxy was not
        assert asset._async_metadata_proxy is not None
        assert asset._metadata_proxy is None

        # Create sync client and use sync method (for comparison)
        from pyatlan.client.atlan import AtlanClient

        with patch.object(AtlanClient, "custom_metadata_cache") as sync_mock_cache:
            sync_mock_cache.get_id_for_name.return_value = CM_ID
            sync_mock_cache.map_attr_id_to_name = {CM_ID: CM_ATTRIBUTES}
            sync_mock_cache.is_attr_archived.return_value = False

            sync_client = AtlanClient(
                base_url="https://test.atlan.com", api_key="test-key"
            )
            asset.get_custom_metadata(sync_client, CM_NAME)

            # Verify both proxies exist and are independent
            assert asset._async_metadata_proxy is not None
            assert asset._metadata_proxy is not None
            assert asset._async_metadata_proxy != asset._metadata_proxy


class TestAsyncAttributeDefRichText:
    """Test async RICH_TEXT AttributeDef functionality"""

    @pytest.mark.asyncio
    async def test_async_rich_text_attribute_creation(self, client: AsyncAtlanClient):
        """Test that RICH_TEXT attributes are created correctly using async method"""

        # Mock the client.asset.search method that _get_all_qualified_names_async calls
        with patch.object(
            client.asset, "search", new_callable=AsyncMock
        ) as mock_search:
            # Mock an empty search result
            async def async_generator():
                return
                yield  # pragma: no cover

            mock_search.return_value = async_generator()

            attr_def = await AttributeDef.create_async(
                client=client,
                display_name="Rich Content",
                attribute_type=AtlanCustomAttributePrimitiveType.RICH_TEXT,
                description="Test rich text attribute",
            )

        assert attr_def.display_name == "Rich Content"
        assert attr_def.type_name == AtlanCustomAttributePrimitiveType.STRING.value
        assert attr_def.description == "Test rich text attribute"
        assert attr_def.options
        assert attr_def.options.is_rich_text is True
        assert attr_def.options.multi_value_select is False

    @pytest.mark.asyncio
    async def test_async_rich_text_cannot_be_multi_valued(
        self, client: AsyncAtlanClient
    ):
        """Test that async RICH_TEXT attributes cannot be multi-valued"""

        # Mock the client.asset.search method that _get_all_qualified_names_async calls
        with patch.object(
            client.asset, "search", new_callable=AsyncMock
        ) as mock_search:
            # Mock an empty search result
            async def async_generator():
                return
                yield  # pragma: no cover

            mock_search.return_value = async_generator()

            with pytest.raises(AtlanError) as exc_info:
                await AttributeDef.create_async(
                    client=client,
                    display_name="Invalid Rich Text",
                    attribute_type=AtlanCustomAttributePrimitiveType.RICH_TEXT,
                    multi_valued=True,
                )

        error = exc_info.value
        assert "ATLAN-PYTHON-400-076" in str(error)

    @pytest.mark.asyncio
    async def test_async_rich_text_options_configuration(
        self, client: AsyncAtlanClient
    ):
        """Test that async RICH_TEXT options are configured correctly"""

        # Mock the client.asset.search method that _get_all_qualified_names_async calls
        with patch.object(
            client.asset, "search", new_callable=AsyncMock
        ) as mock_search:
            # Mock an empty search result
            async def async_generator():
                return
                yield  # pragma: no cover

            mock_search.return_value = async_generator()

            attr_def = await AttributeDef.create_async(
                client=client,
                display_name="Rich Text Field",
                attribute_type=AtlanCustomAttributePrimitiveType.RICH_TEXT,
            )

        options = attr_def.options
        assert options is not None
        # Rich text uses string primitive type
        assert options.primitive_type == AtlanCustomAttributePrimitiveType.STRING.value
        # Should have rich text flag enabled
        assert options.is_rich_text is True
        # Cannot be multi-valued
        assert options.multi_value_select is False
        # Should not have custom_type set (that's for SQL, URL, etc.)
        assert not hasattr(options, "custom_type") or options.custom_type is None
