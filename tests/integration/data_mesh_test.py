from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import AtlasGlossaryTerm, DataDomain, DataProduct
from pyatlan.model.core import Announcement
from pyatlan.model.enums import AnnouncementType, CertificateStatus, EntityStatus
from pyatlan.model.fluent_search import CompoundQuery, FluentSearch
from pyatlan.model.response import AssetMutationResponse
from pyatlan.utils import to_camel_case
from tests.integration.client import TestId, delete_asset
from tests.integration.utils import block

DATA_PRODUCT_ASSETS_PLAYBOOK_FILTER = (
    '{"condition":"AND","isGroupLocked":false,"rules":[]}'
)

MODULE_NAME = TestId.make_unique("DM")

DATA_DOMAIN_NAME = f"{MODULE_NAME}-data-domain"
DATA_DOMAIN_MESH_SLUG = to_camel_case(DATA_DOMAIN_NAME)
DATA_DOMAIN_QUALIFIED_NAME = f"default/domain/{DATA_DOMAIN_MESH_SLUG}"
DATA_SUB_DOMAIN_NAME = f"{MODULE_NAME}-data-sub-domain"
DATA_SUB_DOMAIN_MESH_SLUG = to_camel_case(DATA_SUB_DOMAIN_NAME)
DATA_SUB_DOMAIN_QUALIFIED_NAME = (
    f"{DATA_DOMAIN_QUALIFIED_NAME}/domain/{DATA_SUB_DOMAIN_MESH_SLUG}"
)
DATA_PRODUCT_NAME = f"{MODULE_NAME}-data-product"
DATA_PRODUCT_MESH_SLUG = to_camel_case(DATA_PRODUCT_NAME)
DATA_PRODUCT_QUALIFIED_NAME = (
    f"{DATA_DOMAIN_QUALIFIED_NAME}/product/{DATA_PRODUCT_MESH_SLUG}"
)

CERTIFICATE_STATUS = CertificateStatus.VERIFIED
CERTIFICATE_MESSAGE = "Automated testing of the Python SDK."
ANNOUNCEMENT_TYPE = AnnouncementType.INFORMATION
ANNOUNCEMENT_TITLE = "Python SDK testing."
ANNOUNCEMENT_MESSAGE = "Automated testing of the Python SDK."

response = block(AtlanClient(), AssetMutationResponse())

pytestmark = pytest.mark.skip(
    "Reset broke data mesh stuff. Some bootstrap policies need to be reset"
)


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
    assert domain.qualified_name == DATA_DOMAIN_QUALIFIED_NAME


@pytest.fixture(scope="module")
def sub_domain(
    client: AtlanClient,
    domain: DataDomain,
) -> Generator[DataDomain, None, None]:
    assert domain.guid
    to_create = DataDomain.create(
        name=DATA_SUB_DOMAIN_NAME,
        parent_domain_qualified_name=DATA_DOMAIN_QUALIFIED_NAME,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=DataDomain)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DataDomain)


def test_data_sub_domain(client: AtlanClient, sub_domain: DataDomain):
    assert sub_domain
    assert sub_domain.guid
    assert sub_domain.qualified_name
    assert sub_domain.name == DATA_SUB_DOMAIN_NAME
    assert sub_domain.qualified_name == DATA_SUB_DOMAIN_QUALIFIED_NAME


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


@pytest.fixture(scope="module")
def product(
    client: AtlanClient,
    domain: DataDomain,
) -> Generator[DataProduct, None, None]:
    assert domain.guid
    assets = (
        FluentSearch()
        .where(CompoundQuery.active_assets())
        .where(CompoundQuery.asset_type(AtlasGlossaryTerm))
    ).to_request()
    to_create = DataProduct.create(
        name=DATA_PRODUCT_NAME,
        asset_selection=assets,
        domain_qualified_name=DATA_DOMAIN_QUALIFIED_NAME,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=DataProduct)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DataProduct)


def test_product(client: AtlanClient, product: DataProduct):
    assert product
    assert product.guid
    assert product.qualified_name
    assert product.name == DATA_PRODUCT_NAME
    assert product.qualified_name == DATA_PRODUCT_QUALIFIED_NAME
    assert (
        product.data_product_assets_playbook_filter
        == DATA_PRODUCT_ASSETS_PLAYBOOK_FILTER
    )


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
