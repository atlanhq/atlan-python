from typing import Any, Dict, List, Optional
import time
from pyatlan.model.workflow import (
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
    Abstract class for packages

    Attributes:
        prefix: the name of the user for which to look for any changes
        name: unique name of the package, usually @atlan/something
        labels: labels associated with the package.
        annotations: annotations associated with the package.
        parameters: parameters associated with the package.
        credentials: credentials for the package to access its source.
    """

    _PACKAGE_NAME = None
    _PACKAGE_PREFIX = None
    _WORKFLOW_METADATA = {}
    _credentials_body = {}
    _parameters = []

    @staticmethod
    def get_epoch() -> str:
        return str(int(time.time()))

    def _get_metadata(self):
        raise NotImplementedError

    def to_workflow(self):
        self._parameters.append(
            {"name": "credential-guid", "value": "{{credentialGuid}}"}
        )
        self._parameters.append(
            {
                "name": "connection",
                "value": self._get_connection().json(
                    by_alias=True, exclude_unset=True, exclude_none=True
                ),
            }
        )
        workflow_spec = WorkflowSpec(
            entrypoint="main",
            templates=[
                WorkflowTemplate(
                    name="main",
                    dag=WorkflowDAG(
                        tasks=[
                            WorkflowTask(
                                name="run",
                                arguments=WorkflowParameters(
                                    parameters=self._parameters
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
                body=self._credentials_body,
            )
        ]
        return Workflow(
            metadata=self._get_metadata(),
            spec=workflow_spec,
            payload=payload,
        )
