import pytest

from pyatlan.client.atlan import AtlanClient


def test_register_client_with_bad_parameter_raises_valueerror():
    with pytest.raises(ValueError, match="client must be an instance of AtlanClient"):
        AtlanClient.register_client("")
    assert AtlanClient.get_default_client() is None


def test_register_client():
    client = AtlanClient(base_url="http://mark.atlan.com", api_key="123")
    AtlanClient.register_client(client)
    assert AtlanClient.get_default_client() == client
