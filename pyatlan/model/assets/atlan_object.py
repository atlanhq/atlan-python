from __future__ import annotations

from pydantic.v1 import BaseModel, Extra

from pyatlan.model.utils import encoders, to_camel_case


class AtlanObject(BaseModel):
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel_case
        extra = Extra.ignore
        json_encoders = encoders()
        validate_assignment = True
