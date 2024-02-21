import json
import logging.config
import os
from pathlib import Path
from typing import Any, List, Optional

from pydantic.v1 import BaseModel, BaseSettings, Field, parse_obj_as

from pyatlan.model.assets import Connection
from pyatlan.model.enums import AtlanConnectorType

PARENT = Path(__file__).parent
LOGGING_CONF = PARENT / "logging.conf"
print("LOGGING_CONF.exists():", LOGGING_CONF.exists())
if LOGGING_CONF.exists():
    logging.config.fileConfig(LOGGING_CONF)
LOGGER = logging.getLogger(__name__)

ENV = "env"


def validate_multiselect(v, values, **kwargs):
    if isinstance(v, str):
        if v.startswith("["):
            data = json.loads(v)
            v = parse_obj_as(List[str], data)
        else:
            v = [v]
    return v


def validate_connection(v, values, config, field, **kwargs):
    v = Connection.parse_raw(v)


class ConnectorAndConnection(BaseModel):
    source: AtlanConnectorType
    connections: List[str]


def validate_connector_and_connection(v, values, config, field, **kwargs):
    return ConnectorAndConnection.parse_raw(v)


class CustomConfig(BaseModel):
    """""" ""

    qn_prefix: str


class RuntimeConfig(BaseSettings):
    user_id: Optional[str] = Field(default="")
    agent: Optional[str] = Field(default="")
    agent_id: Optional[str] = Field(default="")
    agent_pkg: Optional[str] = Field(default="")
    agent_wfl: Optional[str] = Field(default="")
    custom_config: Optional[CustomConfig] = None

    class Config:
        fields = {
            "user_id": {
                ENV: "ATLAN_USER_ID",
            },
            "agent": {ENV: "X_ATLAN_AGENT"},
            "agent_id": {ENV: "X_ATLAN_AGENT_ID"},
            "agent_pkg": {ENV: "X_ATLAN_AGENT_PACKAGE_NAME"},
            "agent_wfl": {ENV: "X_ATLAN_AGENT_WORKFLOW_ID"},
            "custom_config": {ENV: "NESTED_CONFIG"},
        }

        @classmethod
        def parse_env_var(cls, field_name: str, raw_value: str) -> Any:
            if field_name == "custom_config":
                return CustomConfig.parse_raw(raw_value)
            return json.loads(raw_value)


if __name__ == "__main__":
    LOGGER.info(os.environ["NESTED_CONFIG"])
    r = RuntimeConfig()
    LOGGER.info(r.json())
