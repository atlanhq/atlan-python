from pydantic import BaseModel, Extra


def to_camel_case(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Value must be a string")
    value = "".join(word.capitalize() for word in value.split("_"))
    if value == "IndexTypeEsFields":
        value = "IndexTypeESFields"
    return f"{value[0].lower()}{value[1:]}"


def to_snake_case(str):
    res = [str[0].lower()]
    for c in str[1:]:
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
