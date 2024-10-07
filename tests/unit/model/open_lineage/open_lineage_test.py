# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.
from json import load, loads
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from pydantic.v1 import ValidationError

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.common import ApiCaller
from pyatlan.client.open_lineage import OpenLineageClient
from pyatlan.errors import AtlanError, InvalidRequestError
from pyatlan.model.enums import AtlanConnectorType, OpenLineageEventType
from pyatlan.model.fluent_tasks import FluentTasks
from pyatlan.model.open_lineage import OpenLineageEvent, OpenLineageJob, OpenLineageRun

TEST_DATA_DIR = Path(__file__).parent.parent.parent / "data"
OL_EVENT_START = str(TEST_DATA_DIR / "open_lineage_requests/event_start.json")
OL_EVENT_COMPLETE = str(TEST_DATA_DIR / "open_lineage_requests/event_complete.json")

PRODUCER = "https://your.orchestrator/unique/id/123"
NAMESPACE = "snowflake://abc123.snowflakecomputing.com"


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")


def load_json(filename):
    with (TEST_DATA_DIR / filename).open() as input_file:
        return load(input_file)


def to_json(model):
    return loads(model.json(by_alias=True, exclude_unset=True))


@pytest.fixture(scope="module")
def mock_api_caller():
    return Mock(spec=ApiCaller)


@pytest.fixture()
def client():
    return AtlanClient()


@pytest.fixture()
def mock_event_time():
    with patch("pyatlan.model.open_lineage.event.datetime") as mock_datetime:
        mock_datetime_instance = Mock()
        mock_datetime_instance.isoformat.return_value = (
            "2024-10-07T10:23:52.239783+00:00"
        )
        mock_datetime.now.return_value = mock_datetime_instance
        yield mock_datetime


@pytest.fixture()
def mock_run_id():
    with patch("pyatlan.model.open_lineage.run.generate_new_uuid") as mock_utils:
        mock_utils.return_value = "01826681-bfaf-7b1a-a5ce-f69f645660d9"
        yield mock_utils


@pytest.fixture()
def mock_session():
    with patch.object(AtlanClient, "_session") as mock_session:
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = (
            "Unauthorized: url path not configured to receive data, "
            "urlPath: /events/openlineage/snowflake/api/v1/lineage"
        )
        mock_session.request.return_value = mock_response
        yield mock_session


@pytest.mark.parametrize(
    "test_request, connector_type, error_msg",
    [
        [None, AtlanConnectorType.SPARK, "none is not an allowed value"],
        ["123", AtlanConnectorType.SPARK, "value is not a valid dict"],
        [
            OpenLineageEvent(),
            "invalid-connector-type",
            "value is not a valid enumeration member",
        ],
        [OpenLineageEvent(), None, "none is not an allowed value"],
    ],
)
def test_ol_client_send_raises_validation_error(
    test_request, connector_type, error_msg
):
    with pytest.raises(ValidationError) as err:
        OpenLineageClient.send(request=test_request, connector_type=connector_type)
    assert error_msg in str(err.value)


@pytest.mark.parametrize(
    "test_method, test_client",
    [["count", [None, 123, "abc"]], ["execute", [None, 123, "abc"]]],
)
def test_ol_invalid_client_raises_invalid_request_error(
    test_method,
    test_client,
):
    client_method = getattr(FluentTasks(), test_method)
    for invalid_client in test_client:
        with pytest.raises(
            InvalidRequestError, match="No Atlan client has been provided."
        ):
            client_method(client=invalid_client)


def test_ol_client_send(
    mock_api_caller,
):
    mock_api_caller._call_api.side_effect = ["Event recieved"]
    test_event = OpenLineageEvent()
    assert (
        OpenLineageClient(client=mock_api_caller).send(
            request=test_event, connector_type=AtlanConnectorType.SPARK
        )
        is None
    )

    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_ol_client_send_when_ol_not_configured(client, mock_session):
    expected_error = (
        "ATLAN-PYTHON-400-064 Requested OpenLineage "
        "connector type 'snowflake' is not configured. "
        "Suggestion: You must first run the appropriate "
        "marketplace package to configure OpenLineage for "
        "this connector before you can send events for it."
    )
    with pytest.raises(AtlanError, match=expected_error):
        client.open_lineage.send(
            request=OpenLineageEvent(), connector_type=AtlanConnectorType.SNOWFLAKE
        )


def test_ol_models(mock_run_id, mock_event_time):
    job = OpenLineageJob.creator(
        connection_name="ol-spark", job_name="dag_123", producer=PRODUCER
    )
    run = OpenLineageRun.creator(job=job)

    id = job.create_input(namespace=NAMESPACE, asset_name="OPS.DEFAULT.RUN_STATS")
    od = job.create_output(namespace=NAMESPACE, asset_name="OPS.DEFAULT.FULL_STATS")
    od.to_fields = [
        {
            "COLUMN": [
                id.from_field(field_name="COLUMN"),
                id.from_field(field_name="ONE"),
                id.from_field(field_name="TWO"),
            ]
        },
        {
            "ANOTHER": [
                id.from_field(field_name="THREE"),
            ]
        },
    ]

    start = OpenLineageEvent.creator(run=run, event_type=OpenLineageEventType.START)
    start.inputs = [
        id,
        job.create_input(namespace=NAMESPACE, asset_name="SOME.OTHER.TBL"),
        job.create_input(namespace=NAMESPACE, asset_name="AN.OTHER.TBL"),
    ]
    start.outputs = [
        od,
        job.create_output(namespace=NAMESPACE, asset_name="AN.OTHER.VIEW"),
    ]
    assert to_json(start) == load_json(OL_EVENT_START)

    complete = OpenLineageEvent.creator(
        run=run, event_type=OpenLineageEventType.COMPLETE
    )
    assert to_json(complete) == load_json(OL_EVENT_COMPLETE)
