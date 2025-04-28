import pytest
import requests

from pyatlan.test_utils.base_vcr import BaseVCR


class TestBaseVCRJSON(BaseVCR):
    """
    Integration tests to demonstrate VCR.py capabilities
    by recording and replaying HTTP interactions using
    HTTPBin (https://httpbin.org) for GET, POST, PUT, and DELETE requests.
    """

    BASE_URL = "https://httpbin.org"

    @pytest.fixture(scope="module")
    def vcr_config(self):
        """
        Override the VCR configuration to use JSON serialization across the module.
        """
        config = self._BASE_CONFIG.copy()
        config.update({"serializer": "pretty-json"})
        return config

    @pytest.mark.vcr()
    def test_httpbin_get(self):
        """
        Test a simple GET request to httpbin.
        """
        url = f"{self.BASE_URL}/get"
        response = requests.get(url, params={"test": "value"})
        assert response.status_code == 200
        assert response.json()["args"]["test"] == "value"

    @pytest.mark.vcr()
    def test_httpbin_post(self):
        """
        Test a simple POST request to httpbin.
        """
        url = f"{self.BASE_URL}/post"
        payload = {"name": "atlan", "type": "integration-test"}
        response = requests.post(url, json=payload)
        assert response.status_code == 200
        assert response.json()["json"] == payload

    @pytest.mark.vcr()
    def test_httpbin_put(self):
        """
        Test a simple PUT request to httpbin.
        """
        url = f"{self.BASE_URL}/put"
        payload = {"update": "value"}
        response = requests.put(url, json=payload)
        assert response.status_code == 200
        assert response.json()["json"] == payload

    @pytest.mark.vcr()
    def test_httpbin_delete(self):
        """
        Test a simple DELETE request to httpbin.
        """
        url = f"{self.BASE_URL}/delete"
        response = requests.delete(url)
        assert response.status_code == 200
        assert response.json()["args"] == {}
