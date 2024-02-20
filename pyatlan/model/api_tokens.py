# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
import json
from typing import Any, List, Optional, Set

from pydantic.v1 import Field, root_validator

from pyatlan.model.core import AtlanObject


class ApiTokenPersona(AtlanObject):
    class Config:
        frozen = True

    guid: Optional[str] = Field(
        default=None,
        description="Unique identifier (GUID) of the linked persona.",
        alias="id",
    )
    persona: Optional[str] = Field(
        default=None, description="Unique name of the linked persona."
    )
    persona_qualified_name: Optional[str] = Field(
        default=None, description="Unique qualified_name of the persona"
    )


class ApiToken(AtlanObject):
    class ApiTokenAttributes(AtlanObject):
        access_token_lifespan: Optional[int] = Field(
            description="Time, in seconds, from created_at after which the token will expire.",
            alias="access.token.lifespan",
        )
        access_token: Optional[str] = Field(
            default=None,
            description="The actual API token that can be used as a bearer token.",
        )
        client_id: Optional[str] = Field(
            default=None,
            description="Unique client identifier (GUID) of the API token.",
        )
        created_at: Optional[int] = Field(
            description="Epoch time, in milliseconds, at which the API token was created."
        )
        created_by: Optional[str] = Field(
            default=None, description="User who created the API token."
        )
        description: Optional[str] = Field(
            default=None, description="Explanation of the API token."
        )
        display_name: Optional[str] = Field(
            default=None,
            description="Human-readable name provided when creating the token.",
        )
        personas: Optional[List[Any]] = Field(
            default_factory=list,
            description="Deprecated (now unused): personas associated with the API token.",
        )
        persona_qualified_name: Optional[Set[ApiTokenPersona]] = Field(
            default_factory=set, description="Personas associated with the API token."
        )
        purposes: Optional[Any] = Field(
            default=None,
            description="Possible future placeholder for purposes associated with the token.",
        )
        workspace_permissions: Optional[Set[str]] = Field(
            default_factory=set,
            description="Detailed permissions given to the API token.",
        )

        @root_validator(pre=True)
        def check_embedded_objects(cls, values):
            if "workspacePermissions" in values and isinstance(
                values["workspacePermissions"], str
            ):
                values["workspacePermissions"] = json.loads(
                    values["workspacePermissions"]
                )
            if "personas" in values and isinstance(values["personas"], str):
                values["personas"] = json.loads(values["personas"])
            if "personaQualifiedName" in values and isinstance(
                values["personaQualifiedName"], str
            ):
                persona_qns = json.loads(values["personaQualifiedName"])
                values["personaQualifiedName"] = set()
                for persona_qn in persona_qns:
                    values["personaQualifiedName"].add(
                        ApiTokenPersona(persona_qualified_name=persona_qn)
                    )
            return values

    guid: Optional[str] = Field(
        default=None,
        description="Unique identifier (GUID) of the API token.",
        alias="id",
    )
    client_id: Optional[str] = Field(
        default=None,
        description="Unique client identifier (GUID) of the API token.",
        alias="clientId",
    )
    display_name: Optional[str] = Field(
        default=None,
        description="Human-readable name provided when creating the token.",
        alias="displayName",
    )
    attributes: Optional[ApiTokenAttributes] = Field(
        default=None, description="Detailed characteristics of the API token."
    )

    @root_validator(pre=True)
    def copy_values(cls, values):
        if "attributes" in values:
            if (
                "displayName" in values["attributes"]
                and values["attributes"]["displayName"]
            ):
                values["displayName"] = values["attributes"]["displayName"]
            if "clientId" in values["attributes"] and values["attributes"]["clientId"]:
                values["clientId"] = values["attributes"]["clientId"]
        return values


class ApiTokenRequest(AtlanObject):
    display_name: Optional[str] = Field(
        default=None,
        description="Human-readable name provided when creating the token.",
    )
    description: str = Field(default="", description="Explanation of the token.")
    personas: Optional[Set[str]] = Field(
        default=None,
        description="Deprecated (now unused): GUIDs of personas that are associated with the token.",
    )
    persona_qualified_names: Optional[Set[str]] = Field(
        default=None,
        description="Unique qualified_names of personas that are associated with the token.",
    )
    validity_seconds: Optional[int] = Field(
        default=None,
        description="Length of time, in seconds, after which the token will expire and no longer be usable.",
    )

    @root_validator(pre=True)
    def set_max_validity(cls, values):
        if "validitySeconds" in values and values["validitySeconds"]:
            if values["validitySeconds"] < 0:
                values["validitySeconds"] = 409968000
            else:
                values["validitySeconds"] = min(values["validitySeconds"], 409968000)
        if "personas" in values and not values["personas"]:
            values["personas"] = set()
        return values


class ApiTokenResponse(AtlanObject):
    total_record: Optional[int] = Field(
        default=None, description="Total number of API tokens."
    )
    filter_record: Optional[int] = Field(
        default=None,
        description="Number of API records that matched the specified filters.",
    )
    records: Optional[List[ApiToken]] = Field(
        default=None,
        description="Actual API tokens that matched the specified filters.",
    )
