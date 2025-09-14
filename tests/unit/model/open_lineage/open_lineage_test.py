# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.
import json
from json import load, loads
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.common import ApiCaller
from pyatlan.client.open_lineage import OpenLineageClient
from pyatlan.errors import AtlanError, InvalidRequestError
from pyatlan.model.enums import AtlanConnectorType, OpenLineageEventType
from pyatlan.model.fluent_tasks import FluentTasks
from pyatlan.model.open_lineage import (
    OpenLineageEvent,
    OpenLineageJob,
    OpenLineageRawEvent,
    OpenLineageRun,
)

TEST_DATA_DIR = Path(__file__).parent.parent.parent / "data"
OL_EVENT_START = str(TEST_DATA_DIR / "open_lineage_requests/event_start.json")
OL_EVENT_COMPLETE = str(TEST_DATA_DIR / "open_lineage_requests/event_complete.json")

# Raw event test data files
RAW_EVENTS_LIST = str(TEST_DATA_DIR / "open_lineage_requests/raw_events_list.json")
SINGLE_EVENT = str(TEST_DATA_DIR / "open_lineage_requests/single_event.json")
MULTIPLE_EVENTS = str(TEST_DATA_DIR / "open_lineage_requests/multiple_events.json")
MINIMAL_EVENT = str(TEST_DATA_DIR / "open_lineage_requests/minimal_event.json")
EMPTY_EVENTS = str(TEST_DATA_DIR / "open_lineage_requests/empty_events.json")

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


@pytest.fixture()
def mock_api_caller():
    mock = Mock(spec=ApiCaller)
    # Reset any previous side_effect that might interfere
    mock._call_api.side_effect = None
    mock._call_api.return_value = "Event received"
    return mock


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
    "test_request, connector_type, expected_exception",
    [
        # Invalid request parameter tests
        [None, AtlanConnectorType.SPARK, InvalidRequestError],
        [123, AtlanConnectorType.SPARK, InvalidRequestError],
        [set(), AtlanConnectorType.SPARK, InvalidRequestError],
        [object(), AtlanConnectorType.SPARK, InvalidRequestError],
        # Invalid connector_type parameter tests
        [{"eventType": "START"}, None, InvalidRequestError],
        [{"eventType": "START"}, "spark", InvalidRequestError],
        [{"eventType": "START"}, 123, InvalidRequestError],
        [{"eventType": "START"}, object(), InvalidRequestError],
        [{"eventType": "START"}, set(), InvalidRequestError],
    ],
)
def test_ol_client_send_raises_validation_error(
    test_request, connector_type, expected_exception, mock_api_caller
):
    client = OpenLineageClient(client=mock_api_caller)

    with pytest.raises(expected_exception):
        client.send(request=test_request, connector_type=connector_type)


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
    mock_api_caller._call_api.return_value = "Event received"
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


@pytest.mark.parametrize(
    "test_data_file,test_description",
    [
        (SINGLE_EVENT, "single_event_dict"),
        (MULTIPLE_EVENTS, "multiple_events_list"),
        (RAW_EVENTS_LIST, "complex_event_list"),
        (MINIMAL_EVENT, "minimal_event_dict"),
    ],
)
def test_ol_raw_events_from_json_files(
    mock_api_caller, test_data_file, test_description
):
    # Load test data from file
    test_data = load_json(test_data_file)

    # Test send method with OpenLineageClient
    ol_client = OpenLineageClient(client=mock_api_caller)
    ol_client.send(request=test_data, connector_type=AtlanConnectorType.SPARK)

    assert mock_api_caller._call_api.call_count == 1
    assert isinstance(
        mock_api_caller._call_api.call_args.kwargs["request_obj"], OpenLineageRawEvent
    )
    assert (
        mock_api_caller._call_api.call_args.kwargs["request_obj"].__root__ == test_data
    )
    mock_api_caller.reset_mock()

    # Test emit_raw classmethod with AtlanClient mock
    mock_atlan_client = Mock()
    mock_atlan_client.open_lineage = ol_client

    OpenLineageEvent.emit_raw(
        client=mock_atlan_client,
        event=test_data,
        connector_type=AtlanConnectorType.SPARK,
    )
    assert mock_api_caller._call_api.call_count == 1
    assert isinstance(
        mock_api_caller._call_api.call_args.kwargs["request_obj"], OpenLineageRawEvent
    )
    assert (
        mock_api_caller._call_api.call_args.kwargs["request_obj"].__root__ == test_data
    )
    mock_api_caller.reset_mock()


@pytest.mark.parametrize(
    "test_data_file,input_type",
    [
        (SINGLE_EVENT, "json_string"),
        (MULTIPLE_EVENTS, "json_string"),
        (MINIMAL_EVENT, "json_string"),
    ],
)
def test_ol_raw_events_from_json_strings(mock_api_caller, test_data_file, input_type):
    # Load test data and convert to JSON string
    test_data = load_json(test_data_file)
    test_json_string = json.dumps(test_data)

    # Test send method with JSON string
    ol_client = OpenLineageClient(client=mock_api_caller)
    ol_client.send(request=test_json_string, connector_type=AtlanConnectorType.SPARK)

    assert mock_api_caller._call_api.call_count == 1
    assert isinstance(
        mock_api_caller._call_api.call_args.kwargs["request_obj"], OpenLineageRawEvent
    )
    # When parsing from JSON string, the __root__ should equal the original test_data
    assert (
        mock_api_caller._call_api.call_args.kwargs["request_obj"].__root__ == test_data
    )
    mock_api_caller.reset_mock()


def test_ol_raw_events_edge_cases(mock_api_caller):
    ol_client = OpenLineageClient(client=mock_api_caller)

    # Test empty list
    empty_list = load_json(EMPTY_EVENTS)
    ol_client.send(request=empty_list, connector_type=AtlanConnectorType.SPARK)
    assert mock_api_caller._call_api.call_count == 1
    assert isinstance(
        mock_api_caller._call_api.call_args.kwargs["request_obj"], OpenLineageRawEvent
    )
    assert mock_api_caller._call_api.call_args.kwargs["request_obj"].__root__ == []
    mock_api_caller.reset_mock()

    # Test custom connector type
    test_data = load_json(MINIMAL_EVENT)
    ol_client.send(request=test_data, connector_type=AtlanConnectorType.DATABRICKS)
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_ol_raw_event_model_methods():
    # Test from_dict
    test_dict = {"eventTime": "2025-01-01T00:00:00Z", "eventType": "START"}
    raw_event = OpenLineageRawEvent.from_dict(test_dict)
    assert raw_event.__root__ == test_dict

    # Test from_json
    test_json = '{"eventTime": "2025-01-01T00:00:00Z", "eventType": "COMPLETE"}'
    raw_event = OpenLineageRawEvent.from_json(test_json)
    assert raw_event.__root__ == {
        "eventTime": "2025-01-01T00:00:00Z",
        "eventType": "COMPLETE",
    }

    # Test parse_obj with list
    test_list = [{"eventType": "START"}, {"eventType": "COMPLETE"}]
    raw_event = OpenLineageRawEvent.parse_obj(test_list)
    assert raw_event.__root__ == test_list

    # Test parse_raw with complex JSON
    complex_json = json.dumps(load_json(MULTIPLE_EVENTS))
    raw_event = OpenLineageRawEvent.parse_raw(complex_json)
    assert raw_event.__root__ == load_json(MULTIPLE_EVENTS)
