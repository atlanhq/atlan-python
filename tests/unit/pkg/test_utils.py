from pyatlan.model.assets import Connection
from pyatlan.pkg.models import ConnectorAndConnection
from pyatlan.pkg.utils import validate_connection, validate_connector_and_connection


def test_validate_connection():
    json_string = (
        '{"attributes":{"name":"development","qualifiedName":"default/atlan/1706613736","allowQuery":true,'
        '"allowQueryPreview":true,"rowLimit":"10000","defaultCredentialGuid":"","connectorName":"atlan",'
        '"sourceLogo":"https://assets.atlan.com/assets/ph-user-gear-light.svg","isDiscoverable":true,'
        '"isEditable":false,"category":"utility","adminUsers":["ernest"],"adminGroups":[],'
        '"adminRoles":["b2138f4d-bebf-4a42-b1cb-71fc4487357f"]},"typeName":"Connection"}'
    )

    c = validate_connection(json_string)
    assert isinstance(c, Connection)


def test_validate_connector_and_connection():
    json_string = '{"source":"snowflake","connections":["default/snowflake/1706559464","default/snowflake/1706408616"]}'

    connector_and_connection = validate_connector_and_connection(json_string)
    assert isinstance(connector_and_connection, ConnectorAndConnection)
