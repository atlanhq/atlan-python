# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import (
    EthicalAIAccountabilityConfig,
    EthicalAIBiasMitigationConfig,
    EthicalAIEnvironmentalConsciousnessConfig,
    EthicalAIFairnessConfig,
    EthicalAIPrivacyConfig,
    EthicalAIReliabilityAndSafetyConfig,
    EthicalAITransparencyConfig,
)
from pyatlan.model.fields.atlan_fields import KeywordField

from .core.catalog import Catalog


class AI(Catalog):
    """Description"""

    type_name: str = Field(default="AI", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AI":
            raise ValueError("must be AI")
        return v

    def __setattr__(self, name, value):
        if name in AI._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ETHICAL_AI_PRIVACY_CONFIG: ClassVar[KeywordField] = KeywordField(
        "ethicalAIPrivacyConfig", "ethicalAIPrivacyConfig"
    )
    """
    Privacy configuration for ensuring the ethical use of an AI asset
    """
    ETHICAL_AI_FAIRNESS_CONFIG: ClassVar[KeywordField] = KeywordField(
        "ethicalAIFairnessConfig", "ethicalAIFairnessConfig"
    )
    """
    Fairness configuration for ensuring the ethical use of an AI asset
    """
    ETHICAL_AI_BIAS_MITIGATION_CONFIG: ClassVar[KeywordField] = KeywordField(
        "ethicalAIBiasMitigationConfig", "ethicalAIBiasMitigationConfig"
    )
    """
    Bias mitigation configuration for ensuring the ethical use of an AI asset
    """
    ETHICAL_AI_RELIABILITY_AND_SAFETY_CONFIG: ClassVar[KeywordField] = KeywordField(
        "ethicalAIReliabilityAndSafetyConfig", "ethicalAIReliabilityAndSafetyConfig"
    )
    """
    Reliability and safety configuration for ensuring the ethical use of an AI asset
    """
    ETHICAL_AI_TRANSPARENCY_CONFIG: ClassVar[KeywordField] = KeywordField(
        "ethicalAITransparencyConfig", "ethicalAITransparencyConfig"
    )
    """
    Transparency configuration for ensuring the ethical use of an AI asset
    """
    ETHICAL_AI_ACCOUNTABILITY_CONFIG: ClassVar[KeywordField] = KeywordField(
        "ethicalAIAccountabilityConfig", "ethicalAIAccountabilityConfig"
    )
    """
    Accountability configuration for ensuring the ethical use of an AI asset
    """
    ETHICAL_AI_ENVIRONMENTAL_CONSCIOUSNESS_CONFIG: ClassVar[KeywordField] = (
        KeywordField(
            "ethicalAIEnvironmentalConsciousnessConfig",
            "ethicalAIEnvironmentalConsciousnessConfig",
        )
    )
    """
    Environmental consciousness configuration for ensuring the ethical use of an AI asset
    """

    _convenience_properties: ClassVar[List[str]] = [
        "ethical_a_i_privacy_config",
        "ethical_a_i_fairness_config",
        "ethical_a_i_bias_mitigation_config",
        "ethical_a_i_reliability_and_safety_config",
        "ethical_a_i_transparency_config",
        "ethical_a_i_accountability_config",
        "ethical_a_i_environmental_consciousness_config",
    ]

    @property
    def ethical_a_i_privacy_config(self) -> Optional[EthicalAIPrivacyConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_privacy_config
        )

    @ethical_a_i_privacy_config.setter
    def ethical_a_i_privacy_config(
        self, ethical_a_i_privacy_config: Optional[EthicalAIPrivacyConfig]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_privacy_config = ethical_a_i_privacy_config

    @property
    def ethical_a_i_fairness_config(self) -> Optional[EthicalAIFairnessConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_fairness_config
        )

    @ethical_a_i_fairness_config.setter
    def ethical_a_i_fairness_config(
        self, ethical_a_i_fairness_config: Optional[EthicalAIFairnessConfig]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_fairness_config = ethical_a_i_fairness_config

    @property
    def ethical_a_i_bias_mitigation_config(
        self,
    ) -> Optional[EthicalAIBiasMitigationConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_bias_mitigation_config
        )

    @ethical_a_i_bias_mitigation_config.setter
    def ethical_a_i_bias_mitigation_config(
        self,
        ethical_a_i_bias_mitigation_config: Optional[EthicalAIBiasMitigationConfig],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_bias_mitigation_config = (
            ethical_a_i_bias_mitigation_config
        )

    @property
    def ethical_a_i_reliability_and_safety_config(
        self,
    ) -> Optional[EthicalAIReliabilityAndSafetyConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_reliability_and_safety_config
        )

    @ethical_a_i_reliability_and_safety_config.setter
    def ethical_a_i_reliability_and_safety_config(
        self,
        ethical_a_i_reliability_and_safety_config: Optional[
            EthicalAIReliabilityAndSafetyConfig
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_reliability_and_safety_config = (
            ethical_a_i_reliability_and_safety_config
        )

    @property
    def ethical_a_i_transparency_config(self) -> Optional[EthicalAITransparencyConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_transparency_config
        )

    @ethical_a_i_transparency_config.setter
    def ethical_a_i_transparency_config(
        self, ethical_a_i_transparency_config: Optional[EthicalAITransparencyConfig]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_transparency_config = (
            ethical_a_i_transparency_config
        )

    @property
    def ethical_a_i_accountability_config(
        self,
    ) -> Optional[EthicalAIAccountabilityConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_accountability_config
        )

    @ethical_a_i_accountability_config.setter
    def ethical_a_i_accountability_config(
        self, ethical_a_i_accountability_config: Optional[EthicalAIAccountabilityConfig]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_accountability_config = (
            ethical_a_i_accountability_config
        )

    @property
    def ethical_a_i_environmental_consciousness_config(
        self,
    ) -> Optional[EthicalAIEnvironmentalConsciousnessConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.ethical_a_i_environmental_consciousness_config
        )

    @ethical_a_i_environmental_consciousness_config.setter
    def ethical_a_i_environmental_consciousness_config(
        self,
        ethical_a_i_environmental_consciousness_config: Optional[
            EthicalAIEnvironmentalConsciousnessConfig
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ethical_a_i_environmental_consciousness_config = (
            ethical_a_i_environmental_consciousness_config
        )

    class Attributes(Catalog.Attributes):
        ethical_a_i_privacy_config: Optional[EthicalAIPrivacyConfig] = Field(
            default=None, description=""
        )
        ethical_a_i_fairness_config: Optional[EthicalAIFairnessConfig] = Field(
            default=None, description=""
        )
        ethical_a_i_bias_mitigation_config: Optional[EthicalAIBiasMitigationConfig] = (
            Field(default=None, description="")
        )
        ethical_a_i_reliability_and_safety_config: Optional[
            EthicalAIReliabilityAndSafetyConfig
        ] = Field(default=None, description="")
        ethical_a_i_transparency_config: Optional[EthicalAITransparencyConfig] = Field(
            default=None, description=""
        )
        ethical_a_i_accountability_config: Optional[EthicalAIAccountabilityConfig] = (
            Field(default=None, description="")
        )
        ethical_a_i_environmental_consciousness_config: Optional[
            EthicalAIEnvironmentalConsciousnessConfig
        ] = Field(default=None, description="")

    attributes: AI.Attributes = Field(
        default_factory=lambda: AI.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


AI.Attributes.update_forward_refs()
