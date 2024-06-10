# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

from enum import Enum
from typing import Dict, Protocol, Type, TypeVar

E = TypeVar("E", bound="AtlanError")
RAISE_GITHUB_ISSUE = (
    "Please raise an issue on the Python SDK GitHub "
    "repository providing context in which this error occurred."
)


class ErrorInfo(Protocol):
    http_error_code: int
    error_id: str
    error_message: str
    user_action: str


class AtlanError(Exception):
    def __init__(self, error_code: ErrorInfo, *args):
        message = error_code.error_message.format(*args)
        super().__init__(message)
        self.error_code = error_code

    def __str__(self):
        return (
            f"{self.error_code.error_id or ''} "
            f"{super().__str__()} Suggestion: {self.error_code.user_action}"
        )


class ApiConnectionError(AtlanError):
    """Error that occurs when there is an intermittent issue with the API, such as a network outage or an inability
    to connect due to an incorrect URL."""


class NotFoundError(AtlanError):
    """Error that occurs if a requested object does not exist. For example, trying to retrieve an asset
    that does not exist."""


class InvalidRequestError(AtlanError):
    """Error that occurs if the request being attempted is not valid for some reason, such as containing insufficient
    * parameters or incorrect values for those parameters."""


class ApiError(AtlanError):
    """Error that occurs when the SDK receives a response that indicates a problem, but that the SDK currently has no
    other way of interpreting. Basically, this is a catch-all for errors that do not fit any more specific exception.
    """


class AuthenticationError(AtlanError):
    """Error that occurs when there is a problem with the API token configured in the SDK."""


class PermissionError(AtlanError):
    """Error that occurs if the API token configured for the SDK does not have permission to access or carry out the
    requested operation on a given object. These can be temporary in nature, as there is some asynchronous processing
    that occurs when permissions are granted."""


class ConflictError(AtlanError):
    """Error that occurs if the operation being attempted hits a conflict within Atlan. For example, trying to create
    an object that already exists."""


class RateLimitError(AtlanError):
    """Error that occurs when no further requests are being accepted from the IP address on which the SDK is running.
    By default, Atlan allows 1800 requests per minute. If your use of the SDK exceed this, you will begin to see
    these exceptions."""


class LogicError(AtlanError):
    """Error that occurs when an unexpected logic problem arises. If these are ever experienced, they should be
    immediately reported against the SDK as bugs."""


class ErrorCode(Enum):
    CONNECTION_ERROR = (
        -1,
        "ATLAN-PYTHON--1-001",
        "IOException occurred during API request to Atlan: {0}.",
        "Please check your internet connection and try again. If this problem persists,"
        + "you should check Atlan's availability via a browser,"
        + " or let us know at support@atlan.com.",
        ApiConnectionError,
    )
    INVALID_REQUEST_PASSTHROUGH = (
        400,
        "ATLAN-PYTHON-400-000",
        "Server responded with {0}: {1}.",
        "Check the details of the server's message to correct your request.",
        InvalidRequestError,
    )
    MISSING_GROUP_ID = (
        400,
        "ATLAN-PYTHON-400-001",
        "No ID was provided when attempting to retrieve or update the group.",
        "You must provide an ID when attempting to retrieve or update a group.",
        NotFoundError,
    )
    MISSING_USER_ID = (
        400,
        "ATLAN-PYTHON-400-002",
        "No ID was provided attempting to retrieve or update the user.",
        "You must provide an ID when attempting to retrieve or update a user.",
        InvalidRequestError,
    )
    MISSING_TERM_GUID = (
        400,
        "ATLAN-PYTHON-400-003",
        "No GUID was specified for the term to be removed.",
        "You must provide the GUID of the term to be removed.",
        InvalidRequestError,
    )
    MISSING_ROLE_NAME = (
        400,
        "ATLAN-PYTHON-400-004",
        "No name was provided when attempting to retrieve a role.",
        "You must provide a name of a role when attempting to retrieve one.",
        InvalidRequestError,
    )
    MISSING_ROLE_ID = (
        400,
        "ATLAN-PYTHON-400-005",
        "No ID was provided when attempting to retrieve a role.",
        "You must provide an ID of a role when attempting to retrieve one.",
        InvalidRequestError,
    )
    MISSING_ATLAN_TAG_NAME = (
        400,
        "ATLAN-PYTHON-400-006",
        "No name was provided when attempting to retrieve an Atlan tag.",
        "You must provide a name of an Atlan tag when attempting to retrieve one.",
        InvalidRequestError,
    )
    MISSING_ATLAN_TAG_ID = (
        400,
        "ATLAN-PYTHON-400-007",
        "No ID was provided when attempting to retrieve an Atlan tag.",
        "You must provide an ID of an Atlan tag when attempting to retrieve one.",
        InvalidRequestError,
    )
    MISSING_CM_NAME = (
        400,
        "ATLAN-PYTHON-400-008",
        "No name was provided when attempting to retrieve custom metadata.",
        "You must provide a name for custom metadata when attempting to retrieve it.",
        InvalidRequestError,
    )
    MISSING_CM_ID = (
        400,
        "ATLAN-PYTHON-400-009",
        "No ID was provided when attempting to retrieve custom metadata.",
        "You must provide an ID for custom metadata when attempting to retrieve it.",
        InvalidRequestError,
    )
    MISSING_CM_ATTR_NAME = (
        400,
        "ATLAN-PYTHON-400-010",
        "No name was provided when attempting to retrieve a custom metadata property.",
        "You must provide a name for the custom metadata property when attempting to retrieve it.",
        InvalidRequestError,
    )
    MISSING_CM_ATTR_ID = (
        400,
        "ATLAN-PYTHON-400-011",
        "No ID was provided when attempting to retrieve a custom metadata property.",
        "You must provide an ID for the custom metadata property when attempting to retrieve it.",
        InvalidRequestError,
    )
    MISSING_ENUM_NAME = (
        400,
        "ATLAN-PYTHON-400-012",
        "No name was provided when attempting to retrieve an enumeration.",
        "You must provide a name for the enumeration when attempting to retrieve it.",
        InvalidRequestError,
    )
    NO_GRAPH_WITH_PROCESS = (
        400,
        "ATLAN-PYTHON-400-013",
        "Lineage was retrieved using hideProces=False. We do not provide a graph view in this case.",
        "Retry your request for lineage setting hideProcess=True.",
        InvalidRequestError,
    )
    UNABLE_TO_TRANSLATE_FILTERS = (
        400,
        "ATLAN-PYTHON-400-014",
        "Unable to translate the provided include/exclude asset filters into JSON.",
        "Verify the filters you provided. If the problem persists, please raise an issue on the Python SDK GitHub "
        "repository providing context in which this error occurred.",
        InvalidRequestError,
    )
    UNABLE_TO_CREATE_TYPEDEF_CATEGORY = (
        400,
        "ATLAN-PYTHON-400-015",
        "Unable to create new type definitions of category: {0}.",
        "Atlan currently only allows you to create type definitions for new custom metadata, enumerations and "
        "Atlan tags.",
        InvalidRequestError,
    )
    UNABLE_TO_UPDATE_TYPEDEF_CATEGORY = (
        400,
        "ATLAN-PYTHON-400-016",
        "Unable to update type definitions of category: {0}.",
        "Atlan currently only allows you to update type definitions for custom metadata, enumerations and Atlan tags.",
        InvalidRequestError,
    )
    MISSING_GUID_FOR_DELETE = (
        400,
        "ATLAN-PYTHON-400-017",
        "Insufficient information provided to delete assets.",
        "You must provide the GUID of the asset you want to delete.",
        InvalidRequestError,
    )
    MISSING_REQUIRED_UPDATE_PARAM = (
        400,
        "ATLAN-PYTHON-400-018",
        "One or more required parameters to update {0} are missing: {1}.",
        "You must provide all of the parameters listed to update assets of this type.",
        InvalidRequestError,
    )
    JSON_ERROR = (
        400,
        "ATLAN-PYTHON-400-019",
        "Invalid response object from API: {0}. = (HTTP response code was {1}). Additional details: {2}.",
        "Atlan was unable to produce a valid response to your request. Please verify your request is valid.",
        ApiError,
    )
    NOTHING_TO_ENCODE = (
        400,
        "ATLAN-PYTHON-400-020",
        "Invalid null ID found for url path formatting.",
        "Verify the string ID argument to the API method is what you expect. It could be either the string ID itself "
        "is null or the relevant field in your Atlan object is null.",
        InvalidRequestError,
    )
    MISSING_REQUIRED_QUERY_PARAM = (
        400,
        "ATLAN-PYTHON-400-021",
        "One or more required parameters to query {0} are missing: {1}.",
        "You must provide all of the parameters listed to query assets of this type.",
        InvalidRequestError,
    )
    NO_CONNECTION_ADMIN = (
        400,
        "ATLAN-PYTHON-400-022",
        "No admin provided for the connection.",
        "You must specify at least one connection admin through adminRoles, adminGroups, or adminUsers to create "
        "a new connection. Without at least one admin, the connection will be inaccessible to all.",
        InvalidRequestError,
    )
    MISSING_PERSONA_ID = (
        400,
        "ATLAN-PYTHON-400-023",
        "No ID was provided when attempting to update the persona.",
        "You must provide an ID when attempting to update a persona.",
        InvalidRequestError,
    )
    MISSING_PURPOSE_ID = (
        400,
        "ATLAN-PYTHON-400-024",
        "No ID was provided when attempting to update the purpose.",
        "You must provide an ID when attempting to update a purpose.",
        InvalidRequestError,
    )
    NO_ATLAN_TAG_FOR_PURPOSE = (
        400,
        "ATLAN-PYTHON-400-025",
        "No Atlan tags provided for the purpose.",
        "You must specify at least one Atlan tag to create a new purpose.",
        InvalidRequestError,
    )
    NO_USERS_FOR_POLICY = (
        400,
        "ATLAN-PYTHON-400-026",
        "No user or group specified for the policy.",
        "You must specify at least one user or group to whom the policy in a purpose will be applied.",
        InvalidRequestError,
    )
    MISSING_GROUP_NAME = (
        400,
        "ATLAN-PYTHON-400-027",
        "No name was provided when attempting to retrieve a group.",
        "You must provide a name of a group when attempting to retrieve one.",
        InvalidRequestError,
    )
    MISSING_USER_NAME = (
        400,
        "ATLAN-PYTHON-400-028",
        "No name was provided when attempting to retrieve a user.",
        "You must provide a name of a user when attempting to retrieve one.",
        InvalidRequestError,
    )
    MISSING_USER_EMAIL = (
        400,
        "ATLAN-PYTHON-400-029",
        "No email address was provided when attempting to retrieve a user.",
        "You must provide an email address of a user when attempting to retrieve one.",
        InvalidRequestError,
    )
    MISSING_GROUP_ALIAS = (
        400,
        "ATLAN-PYTHON-400-030",
        "No alias was provided when attempting to retrieve or update the group.",
        "You must provide an alias when attempting to retrieve or update a group.",
        InvalidRequestError,
    )
    NOT_AGGREGATION_METRIC = (
        400,
        "ATLAN-PYTHON-400-031",
        "Requested extracting a metric from a non-metric aggregation result.",
        "You must provide an aggregation result that is a metric aggregation to extract a numeric metric.",
        InvalidRequestError,
    )
    MISSING_TOKEN_ID = (
        400,
        "ATLAN-PYTHON-400-032",
        "No ID was provided when attempting to update the API token.",
        "You must provide an ID when attempting to update an API token.",
        InvalidRequestError,
    )
    MISSING_TOKEN_NAME = (
        400,
        "ATLAN-PYTHON-400-033",
        "No displayName was provided when attempting to update the API token.",
        "You must provide a displayName for the API token when attempting to update it.",
        InvalidRequestError,
    )
    INVALID_LINEAGE_DIRECTION = (
        400,
        "ATLAN-PYTHON-400-034",
        "Can only request upstream or downstream lineage = (not both) through the lineage list API.",
        "Change your provided 'direction' parameter to either upstream or downstream.",
        InvalidRequestError,
    )
    INVALID_URL = (
        400,
        "ATLAN-PYTHON-400-035",
        "The URL provided for uploading a file was invalid.",
        "Check the provided URL and attempt to upload again.",
        InvalidRequestError,
    )
    INACCESSIBLE_URL = (
        400,
        "ATLAN-PYTHON-400-036",
        "The URL provided could not be accessed.",
        "Check the provided URL and attempt to upload again.",
        ApiError,
    )
    NO_ATLAN_CLIENT = (
        400,
        "ATLAN-PYTHON-400-037",
        "No Atlan client has been provided.",
        "You must provide an Atlan client to this operation, or it has no information about which Atlan "
        "tenant to run against.",
        InvalidRequestError,
    )
    MISSING_REQUIRED_RELATIONSHIP_PARAM = (
        400,
        "ATLAN-PYTHON-400-038",
        "One or more required parameters to create a relationship to {0} are missing: {1}.",
        "You must provide all of the parameters listed to relate to assets of this type.",
        InvalidRequestError,
    )
    INVALID_QUERY = (
        400,
        "ATLAN-PYTHON-400-039",
        "Cannot create a {0} query on field: {1}.",
        "You can either try a different field, or try a different kind of query.",
        InvalidRequestError,
    )
    UNABLE_TO_PURGE_TYPEDEF_OF_TYPE = (
        400,
        "ATLAN-PYTHON-400-040",
        "Unable to purge type definitions of type: {1}.",
        "Atlan currently only allows you to purge type definitions for custom metadata, enumerations and Atlan tags.",
        InvalidRequestError,
    )
    UNABLE_TO_PURGE_TYPEDEF_CATEGORY = (
        400,
        "ATLAN-PYTHON-400-041",
        "Unable to purge type definitions of type: {1}.",
        "Verify that this is the correct typedef.",
        InvalidRequestError,
    )
    QN_OR_GUID_NOT_BOTH = (
        400,
        "ATLAN-PYTHON-400-042",
        "Only qualified_name or guid should be provided but not both.",
        "Verify that either qualified_name of guid are provided but not both.",
        InvalidRequestError,
    )
    QN_OR_GUID = (
        400,
        "ATLAN-PYTHON-400-043",
        "Either qualified_name or guid should be provided.",
        "Verify that either qualified_name of guid are provided.",
        InvalidRequestError,
    )
    MISSING_TERMS = (
        400,
        "ATLAN-PYTHON-400-044",
        "A list of assigned_terms to remove must be specified.",
        "Verify that you have provided a list of assigned_terms to remove.",
        InvalidRequestError,
    )
    MISSING_ATLAN_CLIENT = (
        400,
        "ATLAN-PYTHON-400-045",
        "The client must be an instance of AtlanClient.",
        "Verify that you have provided an instance of AtlanClient.",
        InvalidRequestError,
    )
    NO_ATLAN_CLIENT_AVAILABLE = (
        400,
        "ATLAN-PYTHON-400-046",
        "No instance of AtlanClient has been created.",
        "You must create an instance of AtlanClient.",
        InvalidRequestError,
    )
    NO_PRIOR_RUN_AVAILABLE = (
        400,
        "ATLAN-PYTHON-400-047",
        "No prior runs of {0} were available.",
        "You can only re-run a workflow that has been previously run.",
        InvalidRequestError,
    )
    INVALID_PARAMETER_TYPE = (
        400,
        "ATLAN-PYTHON-400-048",
        "Invalid parameter type for {0} should be {1}.",
        "Check that you have used the correct type of parameter.",
        InvalidRequestError,
    )
    GLOSSARY_MISSING_QUALIFIED_NAME = (
        400,
        "ATLAN-PYTHON-400-049",
        "The qualified_name is not present in the Glossary.",
        "Check that the qualified_name is available from the Glossary.",
        InvalidRequestError,
    )
    MISSING_OPTIONS = (
        400,
        "ATLAN-PYTHON-400-050",
        "Options is not present in the AttributeDef.",
        "Please use the AttributeDef.create function to create the Options.",
        InvalidRequestError,
    )
    INVALID_PARAMETER_VALUE = (
        400,
        "ATLAN-PYTHON-400-051",
        "{0} is an invalid value for {1} should be in {2}.",
        "Check that value you are using is valid.",
        InvalidRequestError,
    )
    ASSET_CAN_NOT_BE_ARCHIVED = (
        400,
        "ATLAN-PYTHON-400-052",
        "Asset with guid: {0} is an asset of type {1} which does not support archiving.",
        "Please use purge if you wish to remove assets of this type.",
        InvalidRequestError,
    )
    METHOD_CAN_NOT_BE_INVOKED_ON_ASSET = (
        400,
        "ATLAN-PYTHON-400-053",
        "This method cannot be invoked on the Asset class. Please invoke on a specific asset type.",
        "Please invoke this method on a sub-class of Asset.",
        InvalidRequestError,
    )
    INVALID_CREDENTIALS = (
        400,
        "ATLAN-PYTHON-400-054",
        "Credentials provided did not work: {0}.",
        "Please double-check your credentials and test them again.",
        InvalidRequestError,
    )
    MISSING_GLOSSARY_GUID = (
        400,
        "ATLAN-PYTHON-400-055",
        "'glossary_guid' keyword argument is missing for asset type: {0}",
        "Please double-check your method keyword arguments.",
        InvalidRequestError,
    )
    MISSING_CREDENTIALS = (
        400,
        "ATLAN-PYTHON-400-056",
        "Missing privileged credentials to impersonate users.",
        "You must have both CLIENT_ID and CLIENT_SECRET configured to be able to impersonate users.",
        InvalidRequestError,
    )
    UNABLE_TO_TRANSLATE_ASSETS_DSL = (
        400,
        "ATLAN-PYTHON-400-057",
        "Unable to construct the selected assets DSL JSON string for the data product.",
        "Verify the assets index search request you provided."
        + "If the problem persists, please raise an issue on the Python SDK GitHub "
        + "repository providing context in which this error occurred.",
        InvalidRequestError,
    )
    SSO_GROUP_MAPPING_ALREADY_EXISTS = (
        400,
        "ATLAN-PYTHON-400-058",
        "SSO group mapping already exists between {0} (Atlan group) <-> {1} (SSO group).",
        "You can use SSOClient.update_group_mapping() to update the existing group mapping.",
        InvalidRequestError,
    )
    INVALID_UPLOAD_FILE_PATH = (
        400,
        "ATLAN-PYTHON-400-059",
        "Unable to upload file, Error: {0}, Path: {1}.",
        "Please check the provided file path for upload.",
        InvalidRequestError,
    )
    UNABLE_TO_DOWNLOAD_FILE = (
        400,
        "ATLAN-PYTHON-400-060",
        "Unable to download file, Error: {0}, Path: {1}.",
        "Please check the provided download file type and path.",
        InvalidRequestError,
    )
    UNSUPPORTED_PRESIGNED_URL = (
        400,
        "ATLAN-PYTHON-400-061",
        "Provided presigned URL's cloud provider storage is currently not supported for file uploads.",
        "Please raise a feature request on the Python SDK GitHub to add support for it.",
        InvalidRequestError,
    )
    INVALID_CONTRACT_JSON = (
        400,
        "ATLAN-PYTHON-400-062",
        "Provided data contract JSON is invalid.",
        "Please double-check your provided data contract JSON.",
        InvalidRequestError,
    )
    AUTHENTICATION_PASSTHROUGH = (
        401,
        "ATLAN-PYTHON-401-000",
        "Server responded with {0}: {1}.",
        "Check the details of the server's message to correct your request.",
        AuthenticationError,
    )
    NO_API_TOKEN = (
        401,
        "ATLAN-PYTHON-401-001",
        "No API token provided.",
        'Set your API token using `Atlan.setApiToken= ("<API-TOKEN>");`. You can generate API tokens from the '
        "Atlan Admin Center. See "
        + "https://ask.atlan.com/hc/en-us/articles/8312649180049 for details or contact support at "
        + "https://ask.atlan.com/hc/en-us/requests/new if you have any questions.",
        AuthenticationError,
    )
    EMPTY_API_TOKEN = (
        401,
        "ATLAN-PYTHON-401-002",
        "Your API token is invalid, as it is an empty string.",
        "You can double-check your API token from the Atlan Admin Center. See "
        + "https://ask.atlan.com/hc/en-us/articles/8312649180049 for details or contact support at "
        + "https://ask.atlan.com/hc/en-us/requests/new if you have any questions.",
        AuthenticationError,
    )
    INVALID_API_TOKEN = (
        401,
        "ATLAN-PYTHON-401-003",
        "Your API token is invalid, as it contains whitespace.",
        "You can double-check your API token from the Atlan Admin Center. See "
        + "https://ask.atlan.com/hc/en-us/articles/8312649180049 for details or contact support at "
        + "https://ask.atlan.com/hc/en-us/requests/new if you have any questions.",
        AuthenticationError,
    )
    EXPIRED_API_TOKEN = (
        401,
        "ATLAN-PYTHON-401-004",
        "Your API token is no longer valid, it can no longer lookup base Atlan structures.",
        "You can double-check your API token from the Atlan Admin Center. See "
        + "https://ask.atlan.com/hc/en-us/articles/8312649180049 for details or contact support at "
        + "https://ask.atlan.com/hc/en-us/requests/new if you have any questions.",
        AuthenticationError,
    )
    PERMISSION_PASSTHROUGH = (
        403,
        "ATLAN-PYTHON-403-000",
        "Server responded with {0}: {1}.",
        "Check the details of the server's message to correct your request.",
        PermissionError,
    )
    UNABLE_TO_ESCALATE = (
        403,
        "ATLAN-PYTHON-403-001",
        "Unable to escalate to a privileged user.",
        "Check the details of your configured privileged credentials.",
        PermissionError,
    )
    UNABLE_TO_IMPERSONATE = (
        403,
        "ATLAN-PYTHON-403-002",
        "Unable to impersonate requested user.",
        "Check the details of your configured privileged credentials and the user you requested to impersonate.",
        PermissionError,
    )
    NOT_FOUND_PASSTHROUGH = (
        404,
        "ATLAN-PYTHON-404-000",
        "Server responded with {0}: {1}.",
        "Check the details of the server's message to correct your request.",
        NotFoundError,
    )
    ASSET_NOT_FOUND_BY_GUID = (
        404,
        "ATLAN-PYTHON-404-001",
        "Asset with GUID {0} does not exist.",
        "Verify the GUID of the asset you are trying to retrieve.",
        NotFoundError,
    )
    ASSET_NOT_TYPE_REQUESTED = (
        404,
        "ATLAN-PYTHON-404-002",
        "Asset with GUID {0} is not of the type requested: {1}.",
        "Verify the GUID and expected type of the asset you are trying to retrieve.",
        NotFoundError,
    )
    ASSET_NOT_FOUND_BY_QN = (
        404,
        "ATLAN-PYTHON-404-003",
        "Asset with qualifiedName {0} of type {1} does not exist.",
        "Verify the qualifiedName and expected type of the asset you are trying to retrieve.",
        NotFoundError,
    )
    ROLE_NOT_FOUND_BY_NAME = (
        404,
        "ATLAN-PYTHON-404-004",
        "Role with name {0} does not exist.",
        "Verify the role name provided is a valid role name.",
        NotFoundError,
    )
    ROLE_NOT_FOUND_BY_ID = (
        404,
        "ATLAN-PYTHON-404-005",
        "Role with GUID {0} does not exist.",
        "Verify the role GUID provided is a valid role GUID.",
        NotFoundError,
    )
    ATLAN_TAG_NOT_FOUND_BY_NAME = (
        404,
        "ATLAN-PYTHON-404-006",
        "Atlan tag with name {0} does not exist.",
        "Verify the Atlan tag name provided is a valid Atlan tag name. This should be the human-readable name "
        "of the Atlan tag.",
        NotFoundError,
    )
    ATLAN_TAG_NOT_FOUND_BY_ID = (
        404,
        "ATLAN-PYTHON-404-007",
        "Atlan tag with ID {0} does not exist.",
        "Verify the Atlan tag ID provided is a valid Atlan tag ID. This should be the Atlan-internal hashed string"
        " representation.",
        NotFoundError,
    )
    CM_NOT_FOUND_BY_NAME = (
        404,
        "ATLAN-PYTHON-404-008",
        "Custom metadata with name {0} does not exist.",
        "Verify the custom metadata name provided is a valid custom metadata name. This should be the human-readable"
        " name of the custom metadata.",
        NotFoundError,
    )
    CM_NOT_FOUND_BY_ID = (
        404,
        "ATLAN-PYTHON-404-009",
        "Custom metadata with ID {0} does not exist.",
        "Verify the custom metadata ID provided is a valid custom metadata ID. This should be the Atlan-internal"
        " hashed string representation.",
        NotFoundError,
    )
    CM_NO_ATTRIBUTES = (
        404,
        "ATLAN-PYTHON-404-010",
        "Custom metadata with ID {0} does not have any attributes.",
        "Verify the custom metadata ID you are accessing has attributes defined before attempting to retrieve one of"
        " them.",
        NotFoundError,
    )
    CM_ATTR_NOT_FOUND_BY_NAME = (
        404,
        "ATLAN-PYTHON-404-011",
        "Custom metadata property with name {0} does not exist in custom metadata {1}.",
        "Verify the custom metadata ID you are accessing has the attribute you are looking for defined. The name of "
        "the attribute should be the human-readable name.",
        NotFoundError,
    )
    CM_ATTR_NOT_FOUND_BY_ID = (
        404,
        "ATLAN-PYTHON-404-012",
        "Custom metadata property with ID {0} does not exist in custom metadata {1}.",
        "Verify the custom metadata ID you are accessing has the attribute you are looking for defined. The ID of the "
        "attribute should be the Atlan-internal hashed string representation.",
        NotFoundError,
    )
    ENUM_NOT_FOUND = (
        404,
        "ATLAN-PYTHON-404-013",
        "Enumeration with name {0} does not exist.",
        "Verify the enumeration name provided is a valid enumeration name. This should be the human-readable name of "
        "the enumeration.",
        NotFoundError,
    )
    ASSET_NOT_FOUND_BY_NAME = (
        404,
        "ATLAN-PYTHON-404-014",
        "The {0} asset could not be found by name: {1}.",
        "Verify the requested asset type and name exist in your Atlan environment.",
        NotFoundError,
    )
    NO_CATEGORIES = (
        404,
        "ATLAN-PYTHON-404-015",
        "Unable to find any categories in glossary with GUID {0} and qualifiedName {1}.",
        "Verify the requested glossary contains categories.",
        NotFoundError,
    )
    CONNECTION_NOT_FOUND_BY_NAME = (
        404,
        "ATLAN-PYTHON-404-016",
        "Unable to find a connection with the name {0} of type: {1}.",
        "Verify the requested connection exists in your Atlan environment.",
        NotFoundError,
    )
    GROUP_NOT_FOUND_BY_NAME = (
        404,
        "ATLAN-PYTHON-404-017",
        "Group with name {0} does not exist.",
        "Verify the group name provided is a valid group name.",
        NotFoundError,
    )
    GROUP_NOT_FOUND_BY_ID = (
        404,
        "ATLAN-PYTHON-404-018",
        "Group with GUID {0} does not exist.",
        "Verify the role GUID provided is a valid group GUID.",
        NotFoundError,
    )
    USER_NOT_FOUND_BY_NAME = (
        404,
        "ATLAN-PYTHON-404-019",
        "User with username {0} does not exist.",
        "Verify the username provided is a valid username.",
        NotFoundError,
    )
    USER_NOT_FOUND_BY_ID = (
        404,
        "ATLAN-PYTHON-404-020",
        "User with GUID {0} does not exist.",
        "Verify the user GUID provided is a valid user GUID.",
        NotFoundError,
    )
    USER_NOT_FOUND_BY_EMAIL = (
        404,
        "ATLAN-PYTHON-404-021",
        "User with email {0} does not exist.",
        "Verify the user email provided is a valid user email address.",
        NotFoundError,
    )
    GROUP_NOT_FOUND_BY_ALIAS = (
        404,
        "ATLAN-PYTHON-404-022",
        "Group with alias {0} does not exist.",
        "Verify the group alias provided is a valid group alias.",
        NotFoundError,
    )
    PERSONA_NOT_FOUND_BY_NAME = (
        404,
        "ATLAN-PYTHON-404-023",
        "Unable to find a persona with the name: {0}.",
        "Verify the requested persona exists in your Atlan environment.",
        NotFoundError,
    )
    PURPOSE_NOT_FOUND_BY_NAME = (
        404,
        "ATLAN-PYTHON-404-024",
        "Unable to find a purpose with the name: {0}.",
        "Verify the requested purpose exists in your Atlan environment.",
        NotFoundError,
    )
    COLLECTION_NOT_FOUND_BY_NAME = (
        404,
        "ATLAN-PYTHON-404-025",
        "Unable to find a query collection with the name: {0}.",
        "Verify the requested query collection exists in your Atlan environment.",
        NotFoundError,
    )
    QUERY_NOT_FOUND_BY_NAME = (
        404,
        "ATLAN-PYTHON-404-026",
        "Unable to find a query with the name: {0}.",
        "Verify the requested query exists in your Atlan environment.",
        NotFoundError,
    )
    TYPEDEF_NOT_FOUND_BY_NAME = (
        404,
        "ATLAN-PYTHON-404-027",
        "Unable to find a typedef with the name: {0}.",
        "Verify the requested typedef exists in your Atlan environment.",
        NotFoundError,
    )
    API_TOKEN_NOT_FOUND_BY_NAME = (
        404,
        "ATLAN-PYTHON-404-028",
        "API token with name {0} does not exist.",
        "Verify the API token provided is a valid username for that token.",
        NotFoundError,
    )
    CONFLICT_PASSTHROUGH = (
        409,
        "ATLAN-PYTHON-409-000",
        "Server responded with {0}: {1}.",
        "Check the details of the server's message to correct your request.",
        ConflictError,
    )
    RESERVED_SERVICE_TYPE = (
        409,
        "ATLAN-PYTHON-409-001",
        "Provided service type is reserved for internal Atlan use only: {0}",
        "You cannot create, update or remove any type definitions using this service type, it is reserved for "
        "Atlan use only.",
        ConflictError,
    )

    RATE_LIMIT_PASSTHROUGH = (
        429,
        "ATLAN-PYTHON-429-000",
        "Server responded with {0}: {1}.",
        "Check the details of the server's message to correct your request.",
        RateLimitError,
    )
    ERROR_PASSTHROUGH = (
        500,
        "ATLAN-PYTHON-500-000",
        "Server responded with {0}: {1}.",
        "Check the details of the server's message to correct your request.",
        ApiError,
    )
    DUPLICATE_CUSTOM_ATTRIBUTES = (
        500,
        "ATLAN-PYTHON-500-001",
        "Multiple custom attributes with exactly the same name = ({0}) were found for: {1}.",
        RAISE_GITHUB_ISSUE,
        LogicError,
    )
    UNABLE_TO_DESERIALIZE = (
        500,
        "ATLAN-PYTHON-500-002",
        "Unable to deserialize value: {0}.",
        RAISE_GITHUB_ISSUE,
        LogicError,
    )
    UNABLE_TO_PARSE_ORIGINAL_QUERY = (
        500,
        "ATLAN-PYTHON-500-003",
        "Unable to parse original query from the response.",
        RAISE_GITHUB_ISSUE,
        LogicError,
    )
    RETRIES_INTERRUPTED = (
        500,
        "ATLAN-PYTHON-500-005",
        "Loop for retrying a failed action was interrupted.",
        "Allow the retry loop to complete, or ignore this error if it was your intention to interrupt the retries.",
        ApiError,
    )
    RETRY_OVERRUN = (
        500,
        "ATLAN-PYTHON-500-006",
        "Loop for retrying a failed action hit the maximum number of retries.",
        "Increase the maximum number of retries through Atlan.setMaxNetworkRetries= () or ignore this error if it was "
        "your intention to fail after a maximum number of retries was reached.",
        ApiError,
    )

    def __init__(
        self,
        http_error_code: int,
        error_id: str,
        error_message: str,
        user_action: str,
        exception_type: Type[E],
    ):
        self.http_error_code = http_error_code
        self.error_id = error_id
        self.error_message = error_message
        self.user_action = user_action
        self.exception_type = exception_type

    def exception_with_parameters(self, *args):
        return self.exception_type(self, *args)


ERROR_CODE_FOR_HTTP_STATUS: Dict[int, ErrorCode] = {
    400: ErrorCode.INVALID_REQUEST_PASSTHROUGH,
    401: ErrorCode.AUTHENTICATION_PASSTHROUGH,
    403: ErrorCode.PERMISSION_PASSTHROUGH,
    404: ErrorCode.NOT_FOUND_PASSTHROUGH,
    409: ErrorCode.CONFLICT_PASSTHROUGH,
    429: ErrorCode.RATE_LIMIT_PASSTHROUGH,
}
