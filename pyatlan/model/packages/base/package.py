import warnings
from json import loads
from typing import List

from pydantic.v1 import parse_obj_as

from pyatlan.model.credential import Credential
from pyatlan.model.workflow import (
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
)


class AbstractPackage:
    """
    Abstract class for packages.

    .. deprecated::
        Package workflows build Argo-orchestrated workflows, which no longer run
        on tenants migrated to the Automation Engine (AE / Temporal-native).
        Use :attr:`AtlanClient.app` (``AppClient``) instead: create workflows
        from an ``app_id`` plus an ``inputs`` dict validated against the app's
        live input contract (``client.app.get_input_contract(...)``).
    """

    _PACKAGE_NAME: str = ""
    _PACKAGE_PREFIX: str = ""

    def __init__(self):
        warnings.warn(
            "Atlan package workflows are deprecated since the Automation Engine "
            "(AE) migration and may not run on AE-migrated tenants. Use "
            "AtlanClient.app (AppClient) with the app's input contract instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self._parameters = []
        self._credentials_body = {}

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
                                    parameters=parse_obj_as(
                                        List[NameValuePair], self._parameters
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
        payload = [
            PackageParameter(
                parameter="credentialGuid",
                type="credential",
                body=loads(
                    Credential(**self._credentials_body).json(
                        by_alias=True, exclude_none=True
                    )
                ),
            )
        ]
        return Workflow(
            metadata=metadata,
            spec=spec,
            payload=payload if self._credentials_body else [],
        )
