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

    _PACKAGE_NAME: str = ""
    _PACKAGE_PREFIX: str = ""

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
                                    parameters=self._parameters  # type: ignore
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
                body=self._credentials_body,  # type: ignore
            )
        ]
        return Workflow(
            metadata=metadata,
            spec=spec,
            payload=payload if self._credentials_body else [],  # type: ignore
        )
