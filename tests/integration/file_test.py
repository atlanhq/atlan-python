# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Connection, File
from pyatlan.model.core import Announcement
from pyatlan.model.enums import (
    AnnouncementType,
    AtlanConnectorType,
    CertificateStatus,
    FileType,
)
from tests.integration.client import TestId, delete_asset
from tests.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("File")

CONNECTOR_TYPE = AtlanConnectorType.FILE
FILE_NAME = f"{MODULE_NAME}-file.pdf"
CERTIFICATE_STATUS = CertificateStatus.VERIFIED
CERTIFICATE_MESSAGE = "Automated testing of the Python SDK."
ANNOUNCEMENT_TYPE = AnnouncementType.INFORMATION
ANNOUNCEMENT_TITLE = "Python SDK testing."
ANNOUNCEMENT_MESSAGE = "Automated testing of the Python SDK."


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=CONNECTOR_TYPE
    )
    yield result
    # TODO: proper connection delete workflow
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def file(client: AtlanClient, connection: Connection) -> Generator[File, None, None]:
    assert connection.qualified_name
    to_create = File.create(
        name=FILE_NAME,
        connection_qualified_name=connection.qualified_name,
        file_type=FileType.PDF,
    )
    to_create.file_path = "https://www.example.com"
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=File)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=File)


def test_file(
    client: AtlanClient,
    connection: Connection,
    file: File,
):
    assert file
    assert file.guid
    assert file.qualified_name
    assert file.name == FILE_NAME
    assert file.connection_qualified_name == connection.qualified_name
    assert file.file_type == FileType.PDF
    assert file.file_path == "https://www.example.com"
    assert connection.qualified_name
    assert file.connector_name == AtlanConnectorType.get_connector_name(
        connection.qualified_name
    )


@pytest.mark.order(after="test_file")
def test_update_file(
    client: AtlanClient,
    connection: Connection,
    file: File,
):
    assert file.qualified_name
    assert file.name
    updated = client.asset.update_certificate(
        qualified_name=file.qualified_name,
        name=file.name,
        asset_type=File,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status == CERTIFICATE_STATUS
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert file.qualified_name
    assert file.name
    updated = client.asset.update_announcement(
        qualified_name=file.qualified_name,
        name=file.name,
        asset_type=File,
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


@pytest.mark.order(after="test_update_file")
def test_read_file(
    client: AtlanClient,
    connection: Connection,
    file: File,
):
    r = client.asset.get_by_guid(file.guid, asset_type=File)
    assert r
    assert r.guid == file.guid
    assert r.qualified_name == file.qualified_name
    assert r.name == FILE_NAME
    assert r.certificate_status == CERTIFICATE_STATUS
    assert r.certificate_status_message == CERTIFICATE_MESSAGE
    assert r.announcement_type == ANNOUNCEMENT_TYPE.value
    assert r.announcement_title == ANNOUNCEMENT_TITLE
    assert r.announcement_message == ANNOUNCEMENT_MESSAGE
