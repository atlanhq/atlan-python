# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .sage_maker import SageMaker


class SageMakerModelDeployment(SageMaker):
    """Description"""

    type_name: str = Field(default="SageMakerModelDeployment", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SageMakerModelDeployment":
            raise ValueError("must be SageMakerModelDeployment")
        return v

    def __setattr__(self, name, value):
        if name in SageMakerModelDeployment._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAGE_MAKER_MODEL_DEPLOYMENT_STATUS: ClassVar[KeywordField] = KeywordField(
        "sageMakerModelDeploymentStatus", "sageMakerModelDeploymentStatus"
    )
    """
    Current status of the endpoint (e.g., InService, OutOfService, Creating, Failed).
    """
    SAGE_MAKER_MODEL_DEPLOYMENT_ENDPOINT_CONFIG_NAME: ClassVar[KeywordField] = (
        KeywordField(
            "sageMakerModelDeploymentEndpointConfigName",
            "sageMakerModelDeploymentEndpointConfigName",
        )
    )
    """
    Name of the endpoint configuration used by this deployment.
    """
    SAGE_MAKER_MODEL_DEPLOYMENT_MODEL_NAME: ClassVar[KeywordField] = KeywordField(
        "sageMakerModelDeploymentModelName", "sageMakerModelDeploymentModelName"
    )
    """
    Name of the parent Model.
    """
    SAGE_MAKER_MODEL_DEPLOYMENT_MODEL_QUALIFIED_NAME: ClassVar[KeywordField] = (
        KeywordField(
            "sageMakerModelDeploymentModelQualifiedName",
            "sageMakerModelDeploymentModelQualifiedName",
        )
    )
    """
    Qualified name of the parent Model.
    """

    SAGE_MAKER_MODEL: ClassVar[RelationField] = RelationField("sageMakerModel")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sage_maker_model_deployment_status",
        "sage_maker_model_deployment_endpoint_config_name",
        "sage_maker_model_deployment_model_name",
        "sage_maker_model_deployment_model_qualified_name",
        "sage_maker_model",
    ]

    @property
    def sage_maker_model_deployment_status(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_model_deployment_status
        )

    @sage_maker_model_deployment_status.setter
    def sage_maker_model_deployment_status(
        self, sage_maker_model_deployment_status: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_model_deployment_status = (
            sage_maker_model_deployment_status
        )

    @property
    def sage_maker_model_deployment_endpoint_config_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_model_deployment_endpoint_config_name
        )

    @sage_maker_model_deployment_endpoint_config_name.setter
    def sage_maker_model_deployment_endpoint_config_name(
        self, sage_maker_model_deployment_endpoint_config_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_model_deployment_endpoint_config_name = (
            sage_maker_model_deployment_endpoint_config_name
        )

    @property
    def sage_maker_model_deployment_model_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_model_deployment_model_name
        )

    @sage_maker_model_deployment_model_name.setter
    def sage_maker_model_deployment_model_name(
        self, sage_maker_model_deployment_model_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_model_deployment_model_name = (
            sage_maker_model_deployment_model_name
        )

    @property
    def sage_maker_model_deployment_model_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sage_maker_model_deployment_model_qualified_name
        )

    @sage_maker_model_deployment_model_qualified_name.setter
    def sage_maker_model_deployment_model_qualified_name(
        self, sage_maker_model_deployment_model_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_model_deployment_model_qualified_name = (
            sage_maker_model_deployment_model_qualified_name
        )

    @property
    def sage_maker_model(self) -> Optional[SageMakerModel]:
        return None if self.attributes is None else self.attributes.sage_maker_model

    @sage_maker_model.setter
    def sage_maker_model(self, sage_maker_model: Optional[SageMakerModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sage_maker_model = sage_maker_model

    class Attributes(SageMaker.Attributes):
        sage_maker_model_deployment_status: Optional[str] = Field(
            default=None, description=""
        )
        sage_maker_model_deployment_endpoint_config_name: Optional[str] = Field(
            default=None, description=""
        )
        sage_maker_model_deployment_model_name: Optional[str] = Field(
            default=None, description=""
        )
        sage_maker_model_deployment_model_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sage_maker_model: Optional[SageMakerModel] = Field(
            default=None, description=""
        )  # relationship

    attributes: SageMakerModelDeployment.Attributes = Field(
        default_factory=lambda: SageMakerModelDeployment.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sage_maker_model import SageMakerModel  # noqa: E402, F401

SageMakerModelDeployment.Attributes.update_forward_refs()
