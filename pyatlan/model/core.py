from pydantic import BaseModel, Extra, Field
from typing import Optional
from pyatlan.model.enums import EntityStatus

CAMEL_CASE_OVERRIDES = {
    "IndexTypeEsFields": "IndexTypeESFields",
    "sourceUrl": "sourceURL",
    "sourceEmbedUrl": "sourceEmbedURL",
}


def to_camel_case(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Value must be a string")
    value = "".join(word.capitalize() for word in value.split("_"))
    if value in CAMEL_CASE_OVERRIDES:
        value = CAMEL_CASE_OVERRIDES[value]
    if value.startswith("__"):
        value = value[2:]
    return f"{value[0].lower()}{value[1:]}"


def to_snake_case(str):
    if str.startswith("__"):
        str = str[2:]
    res = [str[0].lower()]
    for c in str.replace("URL", "Url")[1:]:
        if c in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            res.append("_")
            res.append(c.lower())
        else:
            res.append(c)
    return "".join(res)


class AtlanObject(BaseModel):
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel_case
        extra = Extra.forbid


class Classification(AtlanObject):
    type_name: Optional[str] = Field(
        None,
        description="Name of the type definition that defines this instance.\n",
        alias="typeName",
    )
    entity_guid: Optional[str] = Field(
        None,
        description="Unique identifier of the entity instance.\n",
        example="917ffec9-fa84-4c59-8e6c-c7b114d04be3",
        alias="entityGuid",
    )
    entity_status: Optional[EntityStatus] = Field(
        None,
        description="Status of the entity",
        example=EntityStatus.ACTIVE,
        alias="entityStatus",
    )
    propagate: Optional[bool] = Field(None, description="")
    remove_propagations_on_entity_delete: Optional[bool] = Field(
        None, description="", alias="removePropagationsOnEntityDelete"
    )
    restrict_propagation_through_lineage: Optional[bool] = Field(
        None, description="", alias="restrictPropagationThroughLineage"
    )
