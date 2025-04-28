# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

import pkg_resources  # type: ignore[import-untyped]

from pyatlan.errors import DependencyNotFoundError

# Check if pytest-vcr plugin is installed
try:
    pkg_resources.get_distribution("pytest-vcr")
except pkg_resources.DistributionNotFound:
    raise DependencyNotFoundError(
        "pytest-vcr plugin is not installed. Please install pytest-vcr."
    )

# Check if vcrpy is installed and ensure the version is 6.0.x
try:
    vcr_version = pkg_resources.get_distribution("vcrpy").version
    if not vcr_version.startswith("6.0"):
        raise DependencyNotFoundError(
            f"vcrpy version 6.0.x is required, but found {vcr_version}. Please install the correct version."
        )
except pkg_resources.DistributionNotFound:
    raise DependencyNotFoundError(
        "vcrpy version 6.0.x is not installed. Please install vcrpy version 6.0.x."
    )

import json
import os
from typing import Any, Dict, Union

import pytest
import yaml  # type: ignore[import-untyped]


class LiteralBlockScalar(str):
    """Formats the string as a literal block scalar, preserving whitespace and
    without interpreting escape characters"""


def literal_block_scalar_presenter(dumper, data):
    """Represents a scalar string as a literal block, via '|' syntax"""
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")


yaml.add_representer(LiteralBlockScalar, literal_block_scalar_presenter)


def process_string_value(string_value):
    """Pretty-prints JSON or returns long strings as a LiteralBlockScalar"""
    try:
        json_data = json.loads(string_value)
        return LiteralBlockScalar(json.dumps(json_data, indent=2))
    except (ValueError, TypeError):
        if len(string_value) > 80:
            return LiteralBlockScalar(string_value)
    return string_value


def convert_body_to_literal(data):
    """Searches the data for body strings, attempting to pretty-print JSON"""
    if isinstance(data, dict):
        for key, value in data.items():
            # Handle response body case (e.g: response.body.string)
            if key == "body" and isinstance(value, dict) and "string" in value:
                value["string"] = process_string_value(value["string"])

            # Handle request body case (e.g: request.body)
            elif key == "body" and isinstance(value, str):
                data[key] = process_string_value(value)

            else:
                convert_body_to_literal(value)

    elif isinstance(data, list):
        for idx, choice in enumerate(data):
            data[idx] = convert_body_to_literal(choice)

    return data


class VCRPrettyPrintYamlJSONBody:
    """This makes request and response YAML JSON body recordings more readable."""

    @staticmethod
    def serialize(cassette_dict):
        cassette_dict = convert_body_to_literal(cassette_dict)
        return yaml.dump(cassette_dict, default_flow_style=False, allow_unicode=True)

    @staticmethod
    def deserialize(cassette_string):
        return yaml.safe_load(cassette_string)


class VCRPrettyPrintJSONBody:
    """Makes request and response JSON body recordings more readable."""

    @staticmethod
    def _parse_json_body(
        body: Union[str, bytes, None],
    ) -> Union[Dict[str, Any], str, None, bytes]:
        """Parse JSON body if possible, otherwise return the original body."""
        if body is None:
            return None

        # Convert bytes to string if needed
        if isinstance(body, bytes):
            try:
                body = body.decode("utf-8")
            except UnicodeDecodeError:
                return body  # Return original if can't decode

        # If it's a string, try to parse as JSON
        if isinstance(body, str):
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return body  # Return original if not valid JSON

        return body  # Return original for other types

    @staticmethod
    def serialize(cassette_dict: dict) -> str:
        """
        Converts body strings to parsed JSON objects for better readability when possible.
        """
        # Safety check for cassette_dict
        if not cassette_dict or not isinstance(cassette_dict, dict):
            cassette_dict = {}

        interactions = cassette_dict.get("interactions", []) or []

        for interaction in interactions:
            if not interaction:
                continue

            # Handle response body
            response = interaction.get("response") or {}
            body_container = response.get("body")
            if isinstance(body_container, dict) and "string" in body_container:
                parsed_body = VCRPrettyPrintJSONBody._parse_json_body(
                    body_container["string"]
                )
                if isinstance(parsed_body, dict):
                    # Replace string field with parsed_json field
                    response["body"] = {"parsed_json": parsed_body}

            # Handle request body
            request = interaction.get("request") or {}
            body_container = request.get("body")
            if isinstance(body_container, dict) and "string" in body_container:
                parsed_body = VCRPrettyPrintJSONBody._parse_json_body(
                    body_container["string"]
                )
                if isinstance(parsed_body, dict):
                    # Replace string field with parsed_json field
                    request["body"] = {"parsed_json": parsed_body}

        # Serialize the final dictionary into a JSON string with pretty formatting
        try:
            return json.dumps(cassette_dict, indent=2, ensure_ascii=False) + "\n"
        except TypeError as exc:
            raise TypeError(
                "Does this HTTP interaction contain binary data? "
                "If so, use a different serializer (like the YAML serializer)."
            ) from exc

    @staticmethod
    def deserialize(cassette_string: str) -> dict:
        """
        Deserializes a JSON string into a dictionary and converts
        parsed_json fields back to string fields.
        """
        # Safety check for cassette_string
        if not cassette_string:
            return {}

        try:
            cassette_dict = json.loads(cassette_string)
        except json.JSONDecodeError:
            return {}

        # Convert parsed_json back to string format
        interactions = cassette_dict.get("interactions", []) or []

        for interaction in interactions:
            if not interaction:
                continue

            # Handle response body
            response = interaction.get("response") or {}
            body_container = response.get("body")
            if isinstance(body_container, dict) and "parsed_json" in body_container:
                json_body = body_container["parsed_json"]
                response["body"] = {"string": json.dumps(json_body)}

            # Handle request body
            request = interaction.get("request") or {}
            body_container = request.get("body")
            if isinstance(body_container, dict) and "parsed_json" in body_container:
                json_body = body_container["parsed_json"]
                request["body"] = {"string": json.dumps(json_body)}

        return cassette_dict


class BaseVCR:
    """
    A base class for configuring VCR (Virtual Cassette Recorder)
    for HTTP request/response recording and replaying.

    This class provides pytest fixtures to set up the VCR configuration
    and custom serializers for JSON and YAML formats.
    It also handles cassette directory configuration.
    """

    class VCRRemoveAllHeaders:
        """
        A class responsible for removing all headers from requests and responses.
        This can be useful for scenarios where headers are not needed for matching or comparison
        in VCR (Virtual Cassette Recorder) interactions, such as when recording or replaying HTTP requests.
        """

        @staticmethod
        def remove_all_request_headers(request):
            # Save only what's necessary for matching
            request.headers = {}
            return request

        @staticmethod
        def remove_all_response_headers(response):
            # Save only what's necessary for matching
            response["headers"] = {}
            return response

    _CASSETTES_DIR = None
    _BASE_CONFIG = {
        # More config options can be found at:
        # https://vcrpy.readthedocs.io/en/latest/configuration.html#configuration
        "record_mode": "once",  # (default: "once", "always", "none", "new_episodes")
        "serializer": "pretty-yaml",  # (default: "yaml")
        "decode_compressed_response": True,  # Decode compressed responses
        # (optional) Replace the Authorization request header with "**REDACTED**" in cassettes
        # "filter_headers": [("authorization", "**REDACTED**")],
        "before_record_request": VCRRemoveAllHeaders.remove_all_request_headers,
        "before_record_response": VCRRemoveAllHeaders.remove_all_response_headers,
    }

    @pytest.fixture(scope="module")
    def vcr(self, vcr):
        """
        Registers custom serializers for VCR and returns the VCR instance.

        The method registers two custom serializers:
        - "pretty-json" for pretty-printing JSON responses.
        - "pretty-yaml" for pretty-printing YAML responses.

        :param vcr: The VCR instance provided by the pytest-vcr plugin
        :returns: modified VCR instance with custom serializers registered
        """
        vcr.register_serializer("pretty-json", VCRPrettyPrintJSONBody)
        vcr.register_serializer("pretty-yaml", VCRPrettyPrintYamlJSONBody)
        return vcr

    @pytest.fixture(scope="module")
    def vcr_config(self):
        """
        Provides the VCR configuration dictionary.

        The configuration includes default options for the recording mode,
        serializer, response decoding, and filtering headers.
        This configuration is used to set up VCR behavior during tests.

        :returns: a dictionary with VCR configuration options
        """
        return self._BASE_CONFIG

    @pytest.fixture(scope="module")
    def vcr_cassette_dir(self, request):
        """
        Provides the directory path for storing VCR cassettes.

        If a custom cassette directory is set in the class, it is used;
        otherwise, the default directory structure is created under "tests/cassettes".
        The directory path will be based on the module name.

        :param request: request object which provides metadata about the test

        :returns: directory path for storing cassettes
        """
        # Set self._CASSETTES_DIR or use the default directory path based on the test module name
        return self._CASSETTES_DIR or os.path.join(
            "tests/vcr_cassettes", request.module.__name__
        )
