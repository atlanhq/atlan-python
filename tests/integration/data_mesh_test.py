import re
from json import dumps
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import (
    Asset,
    Connection,
    DataContract,
    DataDomain,
    DataProduct,
    Table,
)
from pyatlan.model.core import Announcement
from pyatlan.model.enums import (
    AnnouncementType,
    AtlanCustomAttributePrimitiveType,
    AtlanTypeCategory,
    CertificateStatus,
    DataProductStatus,
    EntityStatus,
)
from pyatlan.model.fluent_search import FluentSearch
from pyatlan.model.response import AssetMutationResponse
from pyatlan.model.typedef import AttributeDef, CustomMetadataDef
from tests.integration.client import TestId, delete_asset
from tests.integration.custom_metadata_test import create_custom_metadata
from tests.integration.utils import block

DATA_PRODUCT_ASSETS_PLAYBOOK_FILTER = (
    '{"condition":"AND","isGroupLocked":false,"rules":[]}'
)

MODULE_NAME = TestId.make_unique("DM")

DATA_DOMAIN_NAME = f"{MODULE_NAME}-data-domain"
DATA_DOMAIN_QUALIFIED_NAME = f"default/domain/{DATA_DOMAIN_NAME}/super"
DATA_DOMAIN_QN_REGEX = r"default/domain/[a-zA-Z0-9-]+/super"
DATA_SUB_DOMAIN_NAME = f"{MODULE_NAME}-data-sub-domain"
DATA_SUB_DOMAIN_QUALIFIED_NAME = (
    f"{DATA_DOMAIN_QUALIFIED_NAME}/domain/{DATA_SUB_DOMAIN_NAME}"
)
DATA_SUB_DOMAIN_QN_REGEX = r"default/domain/[a-zA-Z0-9-]+/super/domain/[a-zA-Z0-9-]+"
DATA_PRODUCT_NAME = f"{MODULE_NAME}-data-product"
DATA_PRODUCT_QUALIFIED_NAME = (
    f"{DATA_DOMAIN_QUALIFIED_NAME}/product/{DATA_PRODUCT_NAME}"
)
DATA_PRODUCT_QN_REGEX = r"default/domain/[a-zA-Z0-9-]+/super/product/[a-zA-Z0-9-]+"
DD_CM = f"{MODULE_NAME}_CM"
DD_ATTR = f"{MODULE_NAME}_ATTRIBUTE"
DATA_CONTRACT_NAME = f"{MODULE_NAME}-data-contract"
CERTIFICATE_STATUS = CertificateStatus.VERIFIED
CERTIFICATE_MESSAGE = "Automated testing of the Python SDK."
ANNOUNCEMENT_TYPE = AnnouncementType.INFORMATION
ANNOUNCEMENT_TITLE = "Python SDK testing."
ANNOUNCEMENT_MESSAGE = "Automated testing of the Python SDK."

response = block(AtlanClient(), AssetMutationResponse())


@pytest.fixture(scope="module")
def domain(client: AtlanClient) -> Generator[DataDomain, None, None]:
    to_create = DataDomain.create(name=DATA_DOMAIN_NAME)
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=DataDomain)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DataDomain)


def test_data_domain(client: AtlanClient, domain: DataDomain):
    assert domain
    assert domain.guid
    assert domain.qualified_name
    assert domain.name == DATA_DOMAIN_NAME
    assert re.search(DATA_DOMAIN_QN_REGEX, domain.qualified_name)
    assert domain.parent_domain_qualified_name is None
    assert domain.super_domain_qualified_name is None


@pytest.fixture(scope="module")
def sub_domain(
    client: AtlanClient,
    domain: DataDomain,
) -> Generator[DataDomain, None, None]:
    assert domain.guid
    to_create = DataDomain.create(
        name=DATA_SUB_DOMAIN_NAME,
        parent_domain_qualified_name=domain.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=DataDomain)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DataDomain)


def test_data_sub_domain(client: AtlanClient, sub_domain: DataDomain):
    assert sub_domain
    assert sub_domain.guid
    assert sub_domain.qualified_name
    assert sub_domain.parent_domain_qualified_name
    assert sub_domain.super_domain_qualified_name
    assert sub_domain.name == DATA_SUB_DOMAIN_NAME
    assert re.search(DATA_SUB_DOMAIN_QN_REGEX, sub_domain.qualified_name)
    assert re.search(DATA_DOMAIN_QN_REGEX, sub_domain.parent_domain_qualified_name)
    assert re.search(DATA_DOMAIN_QN_REGEX, sub_domain.super_domain_qualified_name)


def test_update_domain(client: AtlanClient, domain: DataDomain):
    assert domain.qualified_name
    assert domain.name
    updated = client.asset.update_certificate(
        asset_type=DataDomain,
        qualified_name=domain.qualified_name,
        name=domain.name,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert domain.qualified_name
    assert domain.name
    updated = client.asset.update_announcement(
        asset_type=DataDomain,
        qualified_name=domain.qualified_name,
        name=domain.name,
        announcement=Announcement(
            announcement_type=ANNOUNCEMENT_TYPE,
            announcement_title=ANNOUNCEMENT_TITLE,
            announcement_message=ANNOUNCEMENT_MESSAGE,
        ),
    )
    assert updated
    assert updated.announcement_type == ANNOUNCEMENT_TYPE.value
    assert updated.announcement_title == ANNOUNCEMENT_TITLE
    assert updated.announcement_message == ANNOUNCEMENT_MESSAGE


@pytest.mark.order(after="test_update_domain")
def test_retrieve_domain(client: AtlanClient, domain: DataDomain):
    test_domain = client.asset.get_by_guid(domain.guid, asset_type=DataDomain)
    assert test_domain
    assert test_domain.guid == domain.guid
    assert test_domain.qualified_name == domain.qualified_name
    assert test_domain.name == domain.name
    assert test_domain.certificate_status == CERTIFICATE_STATUS
    assert test_domain.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_retrieve_domain")
def test_find_domain_by_name(client: AtlanClient, domain: DataDomain):
    response = client.asset.find_domain_by_name(
        name=domain.name, attributes=["certificateStatus"]
    )

    assert response
    assert response.guid == domain.guid
    assert response.certificate_status == CertificateStatus.VERIFIED


def test_update_sub_domain(client: AtlanClient, sub_domain: DataDomain):
    assert sub_domain.qualified_name
    assert sub_domain.name
    updated = client.asset.update_certificate(
        asset_type=DataDomain,
        qualified_name=sub_domain.qualified_name,
        name=sub_domain.name,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert sub_domain.qualified_name
    assert sub_domain.name
    updated = client.asset.update_announcement(
        asset_type=DataDomain,
        qualified_name=sub_domain.qualified_name,
        name=sub_domain.name,
        announcement=Announcement(
            announcement_type=ANNOUNCEMENT_TYPE,
            announcement_title=ANNOUNCEMENT_TITLE,
            announcement_message=ANNOUNCEMENT_MESSAGE,
        ),
    )
    assert updated
    assert updated.announcement_type == ANNOUNCEMENT_TYPE.value
    assert updated.announcement_title == ANNOUNCEMENT_TITLE
    assert updated.announcement_message == ANNOUNCEMENT_MESSAGE


@pytest.mark.order(after="test_update_sub_domain")
def test_retrieve_sub_domain(client: AtlanClient, sub_domain: DataDomain):
    test_sub_domain = client.asset.get_by_guid(sub_domain.guid, asset_type=DataDomain)
    assert test_sub_domain
    assert test_sub_domain.guid == sub_domain.guid
    assert test_sub_domain.qualified_name == sub_domain.qualified_name
    assert test_sub_domain.name == sub_domain.name
    assert test_sub_domain.certificate_status == CERTIFICATE_STATUS
    assert test_sub_domain.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_retrieve_sub_domain")
def test_find_sub_domain_by_name(client: AtlanClient, sub_domain: DataDomain):
    response = client.asset.find_domain_by_name(
        name=sub_domain.name, attributes=["certificateStatus"]
    )

    assert response
    assert response.guid == sub_domain.guid
    assert response.certificate_status == CertificateStatus.VERIFIED


@pytest.fixture(scope="module")
def data_domain_cm(
    client: AtlanClient, domain: DataDomain
) -> Generator[CustomMetadataDef, None, None]:
    assert domain.qualified_name
    attribute_defs = [
        AttributeDef.create(
            display_name=DD_ATTR,
            attribute_type=AtlanCustomAttributePrimitiveType.STRING,
            applicable_domain_types={"DataDomain", "DataProduct"},
            applicable_domains={domain.qualified_name},
        )
    ]
    dd_cm = create_custom_metadata(
        client, name=DD_CM, attribute_defs=attribute_defs, logo="📦", locked=True
    )
    yield dd_cm
    client.typedef.purge(DD_CM, CustomMetadataDef)


def test_data_domain_cm(data_domain_cm: CustomMetadataDef):
    assert data_domain_cm.guid
    assert data_domain_cm.name != DD_CM
    assert data_domain_cm.display_name == DD_CM
    assert data_domain_cm.category == AtlanTypeCategory.CUSTOM_METADATA

    attributes = data_domain_cm.attribute_defs
    attribute = attributes[0]
    assert attribute.name != DD_ATTR
    assert attribute.display_name == DD_ATTR
    assert attribute.options
    assert not attribute.options.multi_value_select
    assert attribute.type_name == AtlanCustomAttributePrimitiveType.STRING.value


@pytest.fixture(scope="module")
def product(
    client: AtlanClient,
    domain: DataDomain,
    table: Table,
) -> Generator[DataProduct, None, None]:
    assert domain.guid
    assert table and table.guid
    assets = FluentSearch().where(Asset.GUID.eq(table.guid)).to_request()
    product = DataProduct.create(
        name=DATA_PRODUCT_NAME,
        asset_selection=assets,
        domain_qualified_name=domain.qualified_name,
    )
    product.output_ports = [table]
    response = client.asset.save(product)
    result = response.assets_created(asset_type=DataProduct)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DataProduct)


def test_product(client: AtlanClient, product: DataProduct):
    assert product
    assert product.guid
    assert product.qualified_name
    assert product.parent_domain_qualified_name
    assert product.super_domain_qualified_name
    assert product.name == DATA_PRODUCT_NAME
    assert (
        product.data_product_assets_playbook_filter
        == DATA_PRODUCT_ASSETS_PLAYBOOK_FILTER
    )
    assert re.search(DATA_PRODUCT_QN_REGEX, product.qualified_name)
    assert re.search(DATA_DOMAIN_QN_REGEX, product.parent_domain_qualified_name)
    assert re.search(DATA_DOMAIN_QN_REGEX, product.super_domain_qualified_name)


@pytest.fixture(scope="module")
def contract(
    client: AtlanClient,
    table: Table,
    connection: Connection,
) -> Generator[DataContract, None, None]:
    assert table and table.guid
    contract_json = {
        "type": table.type_name,
        "status": CertificateStatus.DRAFT,
        "kind": "DataContract",
        "data_source": connection.name,
        "dataset": table.name,
        "description": "Automated testing of the Python SDK.",
    }
    contract = DataContract.creator(
        asset_qualified_name=table.qualified_name,
        contract_json=dumps(contract_json),
    )
    response = client.asset.save(contract)
    result = response.assets_created(asset_type=DataContract)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DataContract)


@pytest.fixture(scope="module")
def updated_contract(
    client: AtlanClient,
    table: Table,
    connection: Connection,
) -> Generator[DataContract, None, None]:
    assert table and table.guid
    contract_json = {
        "type": table.type_name,
        "status": CertificateStatus.DRAFT,
        "kind": "DataContract",
        "data_source": connection.name,
        "dataset": table.name,
        "description": "Automated testing of the Python SDK (UPDATED).",
    }
    contract = DataContract.creator(
        asset_qualified_name=table.qualified_name,
        contract_json=dumps(contract_json),
    )
    response = client.asset.save(contract)
    result = response.assets_created(asset_type=DataContract)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DataContract)


def test_contract(
    client: AtlanClient, table: Table, product: DataProduct, contract: DataContract
):
    assert product and product.guid
    product = client.asset.get_by_guid(guid=product.guid, asset_type=DataProduct)
    assert product and product.output_ports and len(product.output_ports)
    table_asset = product.output_ports[0]
    assert table and table.guid
    assert table.guid == table_asset.guid
    table = client.asset.get_by_guid(guid=table_asset.guid, asset_type=Table)
    assert table.has_contract
    assert table.data_contract_latest
    table_data_contract = table.data_contract_latest
    assert contract and table_data_contract
    assert table.name and contract.name and table.name in contract.name
    assert contract.guid == table_data_contract.guid
    assert contract.data_contract_json
    assert contract.data_contract_version == 1
    assert contract.data_contract_asset_guid == table.guid


def test_update_contract(
    client: AtlanClient, table: Table, updated_contract: DataContract
):
    assert table and table.guid
    table = client.asset.get_by_guid(guid=table.guid, asset_type=Table)
    assert table.has_contract
    assert table.data_contract_latest
    table_data_contract = table.data_contract_latest
    assert table.name and updated_contract and table_data_contract
    assert updated_contract.name and table.name in updated_contract.name
    assert updated_contract.guid == table_data_contract.guid
    assert updated_contract.data_contract_asset_guid == table.guid
    assert updated_contract.data_contract_json
    assert updated_contract.data_contract_version == 2
    assert "(UPDATED)" in updated_contract.data_contract_json


def test_update_product(client: AtlanClient, product: DataProduct):
    assert product.qualified_name
    assert product.name
    updated = client.asset.update_certificate(
        asset_type=DataProduct,
        qualified_name=product.qualified_name,
        name=product.name,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert updated.certificate_status == CERTIFICATE_STATUS
    assert product.qualified_name
    assert product.name
    updated = client.asset.update_announcement(
        asset_type=DataProduct,
        qualified_name=product.qualified_name,
        name=product.name,
        announcement=Announcement(
            announcement_type=ANNOUNCEMENT_TYPE,
            announcement_title=ANNOUNCEMENT_TITLE,
            announcement_message=ANNOUNCEMENT_MESSAGE,
        ),
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert updated.certificate_status == CERTIFICATE_STATUS
    assert product.qualified_name
    assert product.name


@pytest.mark.order(after="test_update_product")
def test_retrieve_product(client: AtlanClient, product: DataProduct):
    test_product = client.asset.get_by_guid(product.guid, asset_type=DataProduct)
    assert test_product
    assert test_product.guid == product.guid
    assert test_product.qualified_name == product.qualified_name
    assert test_product.name == product.name
    assert test_product.certificate_status == CERTIFICATE_STATUS
    assert test_product.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_update_contract")
def test_retrieve_contract(
    client: AtlanClient, table: Table, updated_contract: DataContract
):
    test_contract = client.asset.get_by_guid(
        updated_contract.guid, asset_type=DataContract
    )
    assert test_contract
    assert test_contract.name == updated_contract.name
    assert table.name and updated_contract.name and table.name in updated_contract.name
    assert test_contract.guid == updated_contract.guid
    assert test_contract.qualified_name == updated_contract.qualified_name
    assert test_contract.data_contract_asset_guid == table.guid
    assert test_contract.data_contract_json
    assert test_contract.data_contract_version == 2
    assert "(UPDATED)" in test_contract.data_contract_json


@pytest.mark.order(after="test_retrieve_product")
def test_find_product_by_name(client: AtlanClient, product: DataProduct):
    response = client.asset.find_product_by_name(
        name=product.name, attributes=["daapStatus"]
    )

    assert response
    assert response.guid == product.guid
    assert response.daap_status == DataProductStatus.ACTIVE


@pytest.mark.order(after="test_retrieve_contract")
def test_delete_contract(client: AtlanClient, contract: DataContract):
    response = client.asset.purge_by_guid(contract.guid)
    assert response
    assert not response.assets_created(asset_type=DataContract)
    assert not response.assets_updated(asset_type=DataContract)
    deleted = response.assets_deleted(asset_type=DataContract)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == contract.guid
    assert deleted[0].qualified_name == contract.qualified_name
    assert deleted[0].delete_handler == "PURGE"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_retrieve_product")
def test_delete_product(client: AtlanClient, product: DataProduct):
    response = client.asset.purge_by_guid(product.guid)
    assert response
    assert not response.assets_created(asset_type=DataProduct)
    assert not response.assets_updated(asset_type=DataProduct)
    deleted = response.assets_deleted(asset_type=DataProduct)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == product.guid
    assert deleted[0].qualified_name == product.qualified_name
    assert deleted[0].delete_handler == "PURGE"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_product")
def test_delete_sub_domain(client: AtlanClient, sub_domain: DataDomain):
    response = client.asset.purge_by_guid(sub_domain.guid)
    assert response
    assert not response.assets_created(asset_type=DataDomain)
    assert not response.assets_updated(asset_type=DataDomain)
    deleted = response.assets_deleted(asset_type=DataDomain)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == sub_domain.guid
    assert deleted[0].qualified_name == sub_domain.qualified_name
    assert deleted[0].delete_handler == "PURGE"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_sub_domain")
def test_delete_domain(client: AtlanClient, domain: DataDomain):
    response = client.asset.purge_by_guid(domain.guid)
    assert response
    assert not response.assets_created(asset_type=DataDomain)
    assert not response.assets_updated(asset_type=DataDomain)
    deleted = response.assets_deleted(asset_type=DataDomain)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == domain.guid
    assert deleted[0].qualified_name == domain.qualified_name
    assert deleted[0].delete_handler == "PURGE"
    assert deleted[0].status == EntityStatus.DELETED
