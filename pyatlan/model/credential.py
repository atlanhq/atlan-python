from typing import Any, Dict, List, Optional, Union

from pydantic.v1 import Field

from pyatlan.model.core import AtlanObject


class Credential(AtlanObject):
    id: Optional[str] = Field(
        default=None, description="Unique identifier (GUID) of the credential."
    )
    name: Optional[str] = Field(default=None, description="Name of the credential.")
    description: Optional[str] = Field(
        default=None, description="Description of the credential."
    )
    host: Optional[str] = Field(
        default=None,
        description="Hostname for which connectivity is defined by the credential.",
    )
    port: Optional[int] = Field(
        default=None, description="Port number on which connectivity should be done."
    )
    auth_type: Optional[str] = Field(
        default=None,
        description="Authentication mechanism represented by the credential.",
    )
    connector_type: Optional[str] = Field(
        default=None,
        description="Type of connector used by the credential.",
    )
    username: Optional[str] = Field(
        default=None,
        description=(
            "Less sensitive portion of the credential, typically used for a username "
            "for basic authentication or client IDs for other forms of authentication."
        ),
    )
    password: Optional[str] = Field(
        default=None,
        description=(
            "More sensitive portion of the credential, typically used for a password "
            "for basic authentication or client secrets for other forms of authentication."
        ),
    )
    extras: Optional[Dict[str, Any]] = Field(
        default=None,
        alias="extra",
        description=(
            "Additional details about the credential. This can capture, for example, "
            "a secondary secret for particular forms of authentication and / or additional details "
            "about the scope of the connectivity (a specific database, role, warehouse, etc."
        ),
    )
    connector_config_name: Optional[str] = Field(
        default=None,
        description="Name of the connector configuration responsible for managing the credential.",
    )
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="TBD")
    level: Optional[Union[Dict[str, Any], str]] = Field(default=None, description="TBD")
    connector: Optional[str] = Field(
        default=None,
        description="Name of the connector used by the credential",
    )


class CredentialResponse(AtlanObject):
    id: Optional[str]
    version: Optional[str]
    is_active: Optional[bool]
    created_at: Optional[int]
    updated_at: Optional[int]
    created_by: Optional[str]
    tenant_id: Optional[str]
    name: Optional[str]
    description: Optional[str]
    connector_config_name: Optional[str]
    connector: Optional[str]
    connector_type: Optional[str]
    auth_type: Optional[str]
    host: Optional[str]
    port: Optional[int]
    metadata: Optional[Dict[str, Any]]
    level: Optional[Union[Dict[str, Any], str]]
    connection: Optional[Union[Dict[str, Any], str]]
    username: Optional[str]
    extras: Optional[Dict[str, Any]] = Field(default=None, alias="extra")

    def to_credential(self) -> Credential:
        """
        Convert this response into a credential instance.
        Note: The password field must still be populated manually,
        as it will never be returned by a credential lookup for security reasons.
        """
        return Credential(
            id=self.id,
            name=self.name,
            host=self.host,
            port=self.port,
            auth_type=self.auth_type,
            connector_type=self.connector_type,
            connector_config_name=self.connector_config_name,
            username=self.username,
            extras=self.extras,  # type: ignore[call-arg]
        )


class CredentialListResponse(AtlanObject):
    """
    Model representing a response containing a list of CredentialResponse objects.
    """

    records: Optional[List[CredentialResponse]] = Field(
        default_factory=list, description="list of credential records returned."
    )


class CredentialTestResponse(AtlanObject):
    code: Optional[int]
    error: Optional[str]
    info: Optional[object]
    message: str
    request_id: Optional[str]

    @property
    def is_successful(self) -> bool:
        """
        Whether the test was successful (True) or failed (False).

        Returns:
            bool: True if the test was successful, False otherwise.
        """
        return self.message == "successful"
