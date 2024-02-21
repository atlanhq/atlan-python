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
    Abstract class for packages
    """

    _PACKAGE_NAME: str = ""
    _PACKAGE_PREFIX: str = ""

    def __init__(self):
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
