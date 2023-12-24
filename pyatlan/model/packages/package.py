from pyatlan.model.assets import Connection
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
    """

    _parameters: list = []
    _credentials_body: dict = {}
    _PACKAGE_NAME: str = ""
    _PACKAGE_PREFIX: str = ""
    _WORKFLOW_METADATA: dict = {}

    def _get_metadata(self) -> WorkflowMetadata:
        raise NotImplementedError

    def _get_connection(self) -> Connection:
        raise NotImplementedError

    def to_workflow(self) -> Workflow:
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
