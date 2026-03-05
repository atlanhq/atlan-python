from typing import Any

import msgspec

from pyatlan_v9.model.credential import Credential
from pyatlan_v9.model.workflow import (
    NameValuePair,
    PackageParameter,
    Workflow,
    WorkflowDAG,
    WorkflowMetadata,
    WorkflowParameters,
    WorkflowSpec,
    WorkflowTask,
    WorkflowTemplate,
    WorkflowTemplateRef,
    _remove_nones,
)

# Map of camelCase / legacy aliases → v9 Credential Python field names.
# Crawlers were written against the legacy Pydantic model which accepted
# either camelCase aliases or snake_case names.
_CRED_KEY_MAP: dict[str, str] = {
    "authType": "auth_type",
    "connectorConfigName": "connector_config_name",
    "connectorType": "connector_type",
    "extra": "extras",
}


def _normalize_cred_keys(raw: dict[str, Any]) -> dict[str, Any]:
    """Normalize credential dict keys to v9 Credential Python field names."""
    return {_CRED_KEY_MAP.get(k, k): v for k, v in raw.items()}


class AbstractPackage:
    """
    Abstract class for packages (v9 — uses msgspec workflow models).
    """

    _PACKAGE_NAME: str = ""
    _PACKAGE_PREFIX: str = ""

    def __init__(self):
        self._parameters = []
        self._credentials_body: dict[str, Any] = {}

    def _get_metadata(self) -> WorkflowMetadata:
        raise NotImplementedError

    def to_workflow(self) -> Workflow:
        metadata = self._get_metadata()
        spec = WorkflowSpec(
            entrypoint="main",
            templates=[
                WorkflowTemplate(
                    name="main",
                    dag=WorkflowDAG(
                        tasks=[
                            WorkflowTask(
                                name="run",
                                arguments=WorkflowParameters(
                                    parameters=msgspec.convert(
                                        self._parameters, list[NameValuePair]
                                    )
                                ),
                                template_ref=WorkflowTemplateRef(
                                    name=self._PACKAGE_PREFIX,
                                    template="main",
                                    cluster_scope=True,
                                ),
                            )
                        ]
                    ),
                )
            ],
            workflow_metadata=WorkflowMetadata(
                annotations={"package.argoproj.io/name": self._PACKAGE_NAME}
            ),
        )
        payload: list[PackageParameter] = []
        if self._credentials_body:
            cred = Credential(**_normalize_cred_keys(self._credentials_body))
            # Convert to dict with camelCase keys, excluding None values
            cred_dict: dict[str, Any] = _remove_nones(msgspec.to_builtins(cred))
            payload = [
                PackageParameter(
                    parameter="credentialGuid",
                    type="credential",
                    body=cred_dict,
                )
            ]
        return Workflow(
            metadata=metadata,
            spec=spec,
            payload=payload,
        )
