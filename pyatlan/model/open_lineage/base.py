from typing import Optional
from urllib.parse import urlparse

from dateutil import parser  # type:ignore[import-untyped]
from pydantic.v1 import Field, validator

from pyatlan.model.core import AtlanObject


class OpenLineageBaseEvent(AtlanObject):
    """
    Base model for OpenLineage events.
    """

    event_time: Optional[str] = Field(
        default=None, description="time the event occurred at", alias="eventTime"
    )
    producer: Optional[str] = Field(default=None, description="producer of the event")
    schema_url: Optional[str] = Field(
        default="https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/RunEvent",
        description="Schema URL for the event",
        alias="schemaURL",
        const=True,
    )

    def __init__(self, **data):
        super().__init__(**data)
        self.schema_url = self._get_schema()

    @staticmethod
    def _get_schema() -> str:
        return "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/BaseEvent"

    @validator("event_time")
    def validate_event_time(cls, value: str) -> str:
        # Parse and validate the ISO format
        parser.isoparse(value)
        if "t" not in value.lower():
            raise ValueError(f"Parsed date-time has to contain time: {value}")
        return value

    @validator("producer")
    def validate_producer(cls, value: str) -> str:
        urlparse(value)
        return value

    @validator("schema_url")
    def validate_schema_url(cls, value: str) -> str:
        urlparse(value)
        return value


class OpenLineageBaseFacet(AtlanObject):
    """
    Base model for OpenLineage facets.
    """

    producer: Optional[str] = Field(default=None, alias="_producer")
    schema_url: Optional[str] = Field(default=None, alias="_schemaURL")

    @staticmethod
    def _get_schema() -> str:
        return "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/BaseFacet"

    def __init__(self, **data):
        super().__init__(**data)
        self.schema_url = self._get_schema()

    @validator("producer")
    def validate_producer(cls, value: str) -> str:
        urlparse(value)
        return value

    @validator("schema_url")
    def validate_schema_url(cls, value: str) -> str:
        urlparse(value)
        return value
