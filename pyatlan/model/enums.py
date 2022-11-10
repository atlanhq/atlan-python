from enum import Enum


class AnnouncementType(Enum):
    information = "information"
    warning = "warning"
    issue = "issue"


class Cardinality(Enum):
    SINGLE = "SINGLE"
    LIST = "LIST"
    SET = "SET"


class CertificateStatus(Enum):
    VERIFIED = "VERIFIED"
    DRAFT = "DRAFT"
    DEPRECATED = "DEPRECATED"


class EntityStatus(Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"


class AtlanTypeCategory(Enum):
    ENUM = "ENUM"
    STRUCT = "STRUCT"
    CLASSIFICATION = "CLASSIFICATION"
    ENTITY = "ENTITY"
    RELATIONSHIP = "RELATIONSHIP"
    CUSTOM_METADATA = "BUSINESS_METADATA"


class TypeName(Enum):
    STRING = "string"
    ARRAY_STRING = "array<string>"


class IndexType(Enum):
    DEFAULT = "DEFAULT"
    STRING = "STRING"
