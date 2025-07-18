# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from enum import Enum

from pyatlan import utils


class AdminOperationType(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    ACTION = "ACTION"


class AdminResourceType(str, Enum):
    REALM = "REALM"
    REALM_ROLE = "REALM_ROLE"
    REALM_ROLE_MAPPING = "REALM_ROLE_MAPPING"
    REALM_SCOPE_MAPPING = "REALM_SCOPE_MAPPING"
    AUTH_FLOW = "AUTH_FLOW"
    AUTH_EXECUTION_FLOW = "AUTH_EXECUTION_FLOW"
    AUTH_EXECUTION = "AUTH_EXECUTION"
    AUTHENTICATOR_CONFIG = "AUTHENTICATOR_CONFIG"
    REQUIRED_ACTION = "REQUIRED_ACTION"
    IDENTITY_PROVIDER = "IDENTITY_PROVIDER"
    IDENTITY_PROVIDER_MAPPER = "IDENTITY_PROVIDER_MAPPER"
    PROTOCOL_MAPPER = "PROTOCOL_MAPPER"
    USER = "USER"
    USER_LOGIN_FAILURE = "USER_LOGIN_FAILURE"
    USER_SESSION = "USER_SESSION"
    USER_FEDERATION_PROVIDER = "USER_FEDERATION_PROVIDER"
    USER_FEDERATION_MAPPER = "USER_FEDERATION_MAPPER"
    GROUP = "GROUP"
    GROUP_MEMBERSHIP = "GROUP_MEMBERSHIP"
    CLIENT = "CLIENT"
    CLIENT_INITIAL_ACCESS_MODEL = "CLIENT_INITIAL_ACCESS_MODEL"
    CLIENT_ROLE = "CLIENT_ROLE"
    CLIENT_ROLE_MAPPING = "CLIENT_ROLE_MAPPING"
    CLIENT_SCOPE = "CLIENT_SCOPE"
    CLIENT_SCOPE_MAPPING = "CLIENT_SCOPE_MAPPING"
    CLIENT_SCOPE_CLIENT_MAPPING = "CLIENT_SCOPE_CLIENT_MAPPING"
    CLUSTER_NODE = "CLUSTER_NODE"
    COMPONENT = "COMPONENT"
    AUTHORIZATION_RESOURCE_SERVER = "AUTHORIZATION_RESOURCE_SERVER"
    AUTHORIZATION_RESOURCE = "AUTHORIZATION_RESOURCE"
    AUTHORIZATION_SCOPE = "AUTHORIZATION_SCOPE"
    AUTHORIZATION_POLICY = "AUTHORIZATION_POLICY"
    CUSTOM = "CUSTOM"


class AnnouncementType(str, Enum):
    INFORMATION = "information"
    WARNING = "warning"
    ISSUE = "issue"


class AssetSidebarTab(str, Enum):
    OVERVIEW = "overview"
    COLUMNS = "Columns"
    RUNS = "Runs"
    TASKS = "Tasks"
    COMPONENTS = "Components"
    PROJECTS = "Projects"
    COLLECTIONS = "Collections"
    USAGE = "Usage"
    OBJECTS = "Objects"
    LINEAGE = "Lineage"
    INCIDENTS = "Incidents"
    FIELDS = "Fields"
    VISUALS = "Visuals"
    VISUALIZATIONS = "Visualizations"
    SCHEMA_OBJECTS = "Schema Objects"
    RELATIONS = "Relations"
    FACT_DIM_RELATIONS = "Fact-Dim Relations"
    PROFILE = "Profile"
    ASSETS = "Assets"
    ACTIVITY = "Activity"
    SCHEDULES = "Schedules"
    RESOURCES = "Resources"
    QUERIES = "Queries"
    REQUESTS = "Requests"
    PROPERTIES = "Properties"
    MONTE_CARLO = "Monte Carlo"
    DBT_TEST = "dbt Test"
    SODA = "Soda"


class AssetFilterGroup(str, Enum):
    TERMS = "terms"
    OWNERS = "owners"
    USAGE = "usage"
    TAGS = "__traitNames"
    PROPERTIES = "properties"
    CERTIFICATE = "certificateStatus"


class AtlanSSO(str, Enum):
    GOOGLE = "google"
    AZURE_AD = "azure"
    OKTA = "okta"
    JUMPCLOUD = "jumpcloud"
    ONELOGIN = "onelogin"


class AtlanComparisonOperator(str, Enum):
    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="
    EQ = "="
    NEQ = "!="
    IN = "in"
    LIKE = "like"
    STARTS_WITH = "startsWith"
    ENDS_WITH = "endsWith"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    CONTAINS_ANY = "containsAny"
    CONTAINS_ALL = "containsAll"
    IS_NULL = "isNull"
    NOT_NULL = "notNull"
    TIME_RANGE = "timerange"
    NOT_EMPTY = "notEmpty"


class AtlanConnectionCategory(str, Enum):
    WAREHOUSE = "warehouse"
    BI = "bi"
    OBJECT_STORE = "ObjectStore"
    SAAS = "SaaS"
    LAKE = "lake"
    QUERY_ENGINE = "queryengine"
    ELT = "elt"
    DATABASE = "database"
    API = "API"
    EVENT_BUS = "eventbus"
    DATA_QUALITY = "data-quality"
    SCHEMA_REGISTRY = "schema-registry"
    APP = "app"
    CUSTOM = "custom"


class AtlanConnectorType(str, Enum, metaclass=utils.ExtendableEnumMeta):
    category: AtlanConnectionCategory

    @classmethod
    def get_values(cls):
        return [member.value for member in cls._member_map_.values()]

    @classmethod
    def get_names(cls):
        return list(cls._member_map_.keys())

    @classmethod
    def get_items(cls):
        return [(name, member.value) for name, member in cls._member_map_.items()]

    @classmethod
    def _get_connector_type_from_qualified_name(
        cls, qualified_name: str
    ) -> "AtlanConnectorType":
        tokens = qualified_name.split("/")
        if len(tokens) < 2:
            raise ValueError(
                f"Qualified name '{qualified_name}' does not contain enough segments."
            )

        connector_value = tokens[1]
        # Ensure the enum name is converted to UPPER_SNAKE_CASE from kebab-case
        connector_type_key = tokens[1].replace("-", "_").upper()

        # Check if the connector_type_key exists in AtlanConnectorType;
        # if so, return it directly. Otherwise, it may be a custom type.
        if connector_type_key not in AtlanConnectorType.__members__:
            return AtlanConnectorType.CREATE_CUSTOM(
                name=connector_type_key,
                value=connector_value,
            )
        return AtlanConnectorType[connector_type_key]

    def __new__(
        cls, value: str, category: AtlanConnectionCategory
    ) -> "AtlanConnectorType":
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.category = category
        return obj

    @classmethod
    def CREATE_CUSTOM(
        cls, name: str, value: str, category=AtlanConnectionCategory.CUSTOM
    ) -> "AtlanConnectorType":
        return cls.add_value(name, value, category)

    def to_qualified_name(self):
        return f"default/{self.value}/{int(utils.get_epoch_timestamp())}"

    def get_connector_name(
        qualified_name: str,
        attribute_name: str = "connection_qualified_name",
        qualified_name_len: int = 3,
    ):
        """
        Extracts and returns the connector name from a given qualified name.

        :param qualified_name: qualified name to extract the connector name from.
        :param attribute_name: name of the attribute. Defaults to `connection_qualified_name`.
        :param qualified_name_len: expected length of the split qualified name. Defaults to `3`.
        :raises: `ValueError` if the qualified name is invalid or the connector type is not recognized.
        :returns: connector name extracted from the qualified name
        or tuple(connector qualified name, connector name).
        """
        err = f"Invalid {attribute_name}"
        # Split the qualified name
        # to extract necessary information
        fields = qualified_name.split("/")
        if len(fields) != qualified_name_len:
            raise ValueError(err)

        connector_value = fields[1]
        # Try enum conversion; fallback to custom connector if it fails
        try:
            connector_name = AtlanConnectorType(connector_value).value  # type: ignore
        except ValueError:
            custom_connection = AtlanConnectorType.CREATE_CUSTOM(
                # Ensure the enum name is converted to UPPER_SNAKE_CASE from kebab-case
                name=connector_value.replace("-", "_").upper(),
                value=connector_value,
            )
            connector_name = custom_connection.value
        if attribute_name != "connection_qualified_name":
            connection_qn = f"{fields[0]}/{fields[1]}/{fields[2]}"
            return connection_qn, connector_name
        return connector_name

    SNOWFLAKE = ("snowflake", AtlanConnectionCategory.WAREHOUSE)
    TABLEAU = ("tableau", AtlanConnectionCategory.BI)
    REDSHIFT = ("redshift", AtlanConnectionCategory.WAREHOUSE)
    POSTGRES = ("postgres", AtlanConnectionCategory.DATABASE)
    ATHENA = ("athena", AtlanConnectionCategory.QUERY_ENGINE)
    DATABRICKS = ("databricks", AtlanConnectionCategory.LAKE)
    POWERBI = ("powerbi", AtlanConnectionCategory.BI)
    BIGQUERY = ("bigquery", AtlanConnectionCategory.WAREHOUSE)
    LOOKER = ("looker", AtlanConnectionCategory.BI)
    METABASE = ("metabase", AtlanConnectionCategory.BI)
    SALESFORCE = ("salesforce", AtlanConnectionCategory.SAAS)
    DATAVERSE = ("dataverse", AtlanConnectionCategory.SAAS)
    MYSQL = ("mysql", AtlanConnectionCategory.WAREHOUSE)
    MSSQL = ("mssql", AtlanConnectionCategory.WAREHOUSE)
    S3 = ("s3", AtlanConnectionCategory.OBJECT_STORE)
    PRESTO = ("presto", AtlanConnectionCategory.DATABASE)
    TRINO = ("trino", AtlanConnectionCategory.DATABASE)
    DATASTUDIO = ("datastudio", AtlanConnectionCategory.BI)
    GLUE = ("glue", AtlanConnectionCategory.LAKE)
    ORACLE = ("oracle", AtlanConnectionCategory.WAREHOUSE)
    NETSUITE = ("netsuite", AtlanConnectionCategory.WAREHOUSE)
    MODE = ("mode", AtlanConnectionCategory.BI)
    DBT = ("dbt", AtlanConnectionCategory.ELT)
    FIVETRAN = ("fivetran", AtlanConnectionCategory.ELT)
    VERTICA = ("vertica", AtlanConnectionCategory.WAREHOUSE)
    PRESET = ("preset", AtlanConnectionCategory.BI)
    API = ("api", AtlanConnectionCategory.API)
    DYNAMODB = ("dynamodb", AtlanConnectionCategory.WAREHOUSE)
    GCS = ("gcs", AtlanConnectionCategory.OBJECT_STORE)
    HIVE = ("hive", AtlanConnectionCategory.WAREHOUSE)
    SAPHANA = ("sap-hana", AtlanConnectionCategory.WAREHOUSE)
    ADLS = ("adls", AtlanConnectionCategory.OBJECT_STORE)
    SIGMA = ("sigma", AtlanConnectionCategory.BI)
    SYNAPSE = ("synapse", AtlanConnectionCategory.WAREHOUSE)
    AIRFLOW = ("airflow", AtlanConnectionCategory.ELT)
    OPENLINEAGE = ("openlineage", AtlanConnectionCategory.ELT)
    DATAFLOW = ("dataflow", AtlanConnectionCategory.ELT)
    QLIKSENSE = ("qlik-sense", AtlanConnectionCategory.BI)
    KAFKA = ("kafka", AtlanConnectionCategory.EVENT_BUS)
    QUICKSIGHT = ("quicksight", AtlanConnectionCategory.BI)
    SAP_IQ = ("sap-iq", AtlanConnectionCategory.WAREHOUSE)
    HEX = ("hex", AtlanConnectionCategory.ELT)
    TERADATA = ("teradata", AtlanConnectionCategory.WAREHOUSE)
    YUGABYTEDB = ("yugabytedb", AtlanConnectionCategory.DATABASE)
    IBM_INFORMIX = ("ibm-informix", AtlanConnectionCategory.DATABASE)
    SAP_SQL = ("sap-sql", AtlanConnectionCategory.DATABASE)
    ORACLE_TIMESTEN = ("oracle-timesten", AtlanConnectionCategory.DATABASE)
    PERCONA_SERVER = ("percona-server", AtlanConnectionCategory.DATABASE)
    AURORA = ("aurora", AtlanConnectionCategory.DATABASE)
    SAP_MAXDB = ("sap-maxdb", AtlanConnectionCategory.DATABASE)
    SQLITE = ("sqlite", AtlanConnectionCategory.DATABASE)
    ROCKSET = ("rockset", AtlanConnectionCategory.WAREHOUSE)
    MONGODB = ("mongodb", AtlanConnectionCategory.DATABASE)
    GREENPLUM = ("greenplum", AtlanConnectionCategory.WAREHOUSE)
    MONETDB = ("monetdb", AtlanConnectionCategory.WAREHOUSE)
    ALLOYDB = ("alloydb", AtlanConnectionCategory.DATABASE)
    COCKROACHDB = ("cockroachdb", AtlanConnectionCategory.DATABASE)
    AZURE_COSMOS_DB = ("azure-cosmos-db", AtlanConnectionCategory.DATABASE)
    AZURE_ANALYSIS_SERVICES = (
        "azure-analysis-services",
        AtlanConnectionCategory.WAREHOUSE,
    )
    SINGLESTORE = ("singlestore", AtlanConnectionCategory.WAREHOUSE)
    FIREBIRD = ("firebird", AtlanConnectionCategory.DATABASE)
    THOUGHTSPOT = ("thoughtspot", AtlanConnectionCategory.BI)
    CLICKHOUSE = ("clickhouse", AtlanConnectionCategory.WAREHOUSE)
    MULESOFT = ("mulesoft", AtlanConnectionCategory.API)
    CLARI = ("clari", AtlanConnectionCategory.SAAS)
    MARKETO = ("marketo", AtlanConnectionCategory.SAAS)
    AZURE_DATA_LAKE = ("azure-data-lake", AtlanConnectionCategory.LAKE)
    DELTA_LAKE = ("delta-lake", AtlanConnectionCategory.LAKE)
    MINISQL = ("minisql", AtlanConnectionCategory.DATABASE)
    ICEBERG = ("iceberg", AtlanConnectionCategory.WAREHOUSE)
    IMPALA = ("impala", AtlanConnectionCategory.WAREHOUSE)
    SPARK_SQL = ("spark-sql", AtlanConnectionCategory.LAKE)
    MARIADB = ("mariadb", AtlanConnectionCategory.DATABASE)
    FIREBOLT = ("firebolt", AtlanConnectionCategory.WAREHOUSE)
    CLOUDERA_DATA_WAREHOUSE = (
        "cloudera-data-warehouse",
        AtlanConnectionCategory.WAREHOUSE,
    )
    STARBURST_GALAXY = ("starburst-galaxy", AtlanConnectionCategory.WAREHOUSE)
    REDIS = ("redis", AtlanConnectionCategory.DATABASE)
    GRAPHQL = ("graphql", AtlanConnectionCategory.DATABASE)
    ALTERYX = ("alteryx", AtlanConnectionCategory.BI)
    REDASH = ("redash", AtlanConnectionCategory.BI)
    SISENSE = ("sisense", AtlanConnectionCategory.BI)
    MONTE_CARLO = ("monte-carlo", AtlanConnectionCategory.DATA_QUALITY)
    SODA = ("soda", AtlanConnectionCategory.DATA_QUALITY)
    MATILLION = ("matillion", AtlanConnectionCategory.ELT)
    AIVEN_KAFKA = ("aiven-kafka", AtlanConnectionCategory.EVENT_BUS)
    APACHE_KAFKA = ("apache-kafka", AtlanConnectionCategory.EVENT_BUS)
    AZURE_EVENT_HUB = ("azure-event-hub", AtlanConnectionCategory.EVENT_BUS)
    CONFLUENT_KAFKA = ("confluent-kafka", AtlanConnectionCategory.EVENT_BUS)
    REDPANDA_KAFKA = ("redpanda-kafka", AtlanConnectionCategory.EVENT_BUS)
    CONFLUENT_SCHEMA_REGISTRY = (
        "confluent-schema-registry",
        AtlanConnectionCategory.SCHEMA_REGISTRY,
    )
    GAINSIGHT = ("gainsight", AtlanConnectionCategory.DATABASE)
    AIRFLOW_ASTRONOMER = ("airflow-astronomer", AtlanConnectionCategory.ELT)
    AIRFLOW_MWAA = ("airflow-mwaa", AtlanConnectionCategory.ELT)
    AIRFLOW_CLOUD_COMPOSER = ("airflow-cloud-composer", AtlanConnectionCategory.ELT)
    SPARK = ("spark", AtlanConnectionCategory.ELT)
    MPARTICLE = ("mparticle", AtlanConnectionCategory.DATABASE)
    ESSBASE = ("essbase", AtlanConnectionCategory.DATABASE)
    GENERIC = ("genericdb", AtlanConnectionCategory.DATABASE)
    FILE = ("file", AtlanConnectionCategory.OBJECT_STORE)
    MICROSTRATEGY = ("microstrategy", AtlanConnectionCategory.BI)
    AWS_SITE_WISE = ("aws-sitewise", AtlanConnectionCategory.DATABASE)
    AWS_GREENGRASS = ("aws-greengrass", AtlanConnectionCategory.DATABASE)
    COGNITE = ("cognite", AtlanConnectionCategory.SAAS)
    SYNDIGO = ("syndigo", AtlanConnectionCategory.SAAS)
    NETEZZA = ("netezza", AtlanConnectionCategory.WAREHOUSE)
    AZURE_SERVICE_BUS = ("azureservicebus", AtlanConnectionCategory.EVENT_BUS)
    PREFECT = ("prefect", AtlanConnectionCategory.ELT)
    SUPERSET = ("superset", AtlanConnectionCategory.BI)
    DM = ("dm", AtlanConnectionCategory.DATABASE)
    MODEL = ("model", AtlanConnectionCategory.DATABASE)
    IICS = ("iics", AtlanConnectionCategory.ELT)
    ABINITIO = ("abinitio", AtlanConnectionCategory.ELT)
    SAP_S4_HANA = ("sap-s4-hana", AtlanConnectionCategory.WAREHOUSE)
    INRIVER = ("inriver", AtlanConnectionCategory.DATABASE)
    AZURE_ACTIVE_DIRECTORY = ("azure-active-directory", AtlanConnectionCategory.SAAS)
    ADOBE_EXPERIENCE_MANAGER = (
        "adobe-experience-manager",
        AtlanConnectionCategory.SAAS,
    )
    ADOBE_TARGET = ("adobe-target", AtlanConnectionCategory.SAAS)
    APACHE_PULSAR = ("apache-pulsar", AtlanConnectionCategory.EVENT_BUS)
    TREASURE_DATA = ("treasure-data", AtlanConnectionCategory.SAAS)
    SAP_GIGYA = ("sap-gigya", AtlanConnectionCategory.SAAS)
    SAP_HYBRIS = ("sap-hybris", AtlanConnectionCategory.SAAS)
    IBM_DB2 = ("ibmdb2", AtlanConnectionCategory.DATABASE)
    APP = ("app", AtlanConnectionCategory.APP)
    BIGID = ("bigid", AtlanConnectionCategory.SAAS)
    ANAPLAN = ("anaplan", AtlanConnectionCategory.BI)
    AWS_BATCH = ("aws-batch", AtlanConnectionCategory.ELT)
    AWS_ECS = ("aws-ecs", AtlanConnectionCategory.ELT)
    AWS_LAMBDA = ("aws-lambda", AtlanConnectionCategory.ELT)
    AWS_SAGEMAKER = ("aws-sagemaker", AtlanConnectionCategory.ELT)
    CUSTOM = ("custom", AtlanConnectionCategory.CUSTOM)
    SHARED_DRIVE = ("shared-drive", AtlanConnectionCategory.OBJECT_STORE)
    SHARE_POINT = ("share-point", AtlanConnectionCategory.SAAS)
    RDS = ("rds", AtlanConnectionCategory.WAREHOUSE)
    CRATEDB = ("cratedb", AtlanConnectionCategory.DATABASE)
    KX = ("kx", AtlanConnectionCategory.DATABASE)
    DOCUMENTDB = ("documentdb", AtlanConnectionCategory.DATABASE)


class AtlanCustomAttributePrimitiveType(str, Enum):
    STRING = "string"
    INTEGER = "int"
    DECIMAL = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    OPTIONS = "enum"
    USERS = "users"
    GROUPS = "groups"
    URL = "url"
    SQL = "SQL"
    LONG = "long"


class AtlanDeleteType(str, Enum):
    HARD = "HARD"
    SOFT = "SOFT"
    PURGE = "PURGE"


class AtlanIcon(str, Enum):
    ACORN = "PhAcorn"
    ADDRESS_BOOK = "PhAddressBook"
    ADDRESS_BOOK_TABS = "PhAddressBookTabs"
    AIRPLANE = "PhAirplane"
    AIRPLANE_IN_FLIGHT = "PhAirplaneInFlight"
    AIRPLANE_LANDING = "PhAirplaneLanding"
    AIRPLANE_TAKEOFF = "PhAirplaneTakeoff"
    AIRPLANE_TAXIING = "PhAirplaneTaxiing"
    AIRPLANE_TILT = "PhAirplaneTilt"
    AIRPLAY = "PhAirplay"
    AIR_TRAFFIC_CONTROL = "PhAirTrafficControl"
    ALARM = "PhAlarm"
    ALIEN = "PhAlien"
    ALIGN_BOTTOM = "PhAlignBottom"
    ALIGN_BOTTOM_SIMPLE = "PhAlignBottomSimple"
    ALIGN_CENTER_HORIZONTAL = "PhAlignCenterHorizontal"
    ALIGN_CENTER_HORIZONTAL_SIMPLE = "PhAlignCenterHorizontalSimple"
    ALIGN_CENTER_VERTICAL = "PhAlignCenterVertical"
    ALIGN_CENTER_VERTICAL_SIMPLE = "PhAlignCenterVerticalSimple"
    ALIGN_LEFT = "PhAlignLeft"
    ALIGN_LEFT_SIMPLE = "PhAlignLeftSimple"
    ALIGN_RIGHT = "PhAlignRight"
    ALIGN_RIGHT_SIMPLE = "PhAlignRightSimple"
    ALIGN_TOP = "PhAlignTop"
    ALIGN_TOP_SIMPLE = "PhAlignTopSimple"
    AMAZON_LOGO = "PhAmazonLogo"
    AMBULANCE = "PhAmbulance"
    ANCHOR = "PhAnchor"
    ANCHOR_SIMPLE = "PhAnchorSimple"
    ANDROID_LOGO = "PhAndroidLogo"
    ANGLE = "PhAngle"
    ANGULAR_LOGO = "PhAngularLogo"
    APERTURE = "PhAperture"
    APPLE_LOGO = "PhAppleLogo"
    APPLE_PODCASTS_LOGO = "PhApplePodcastsLogo"
    APPROXIMATE_EQUALS = "PhApproximateEquals"
    APP_STORE_LOGO = "PhAppStoreLogo"
    APP_WINDOW = "PhAppWindow"
    ARCHIVE = "PhArchive"
    ARCHIVE_BOX = "PhArchiveBox"
    ARCHIVE_TRAY = "PhArchiveTray"
    ARMCHAIR = "PhArmchair"
    ARROWS_CLOCKWISE = "PhArrowsClockwise"
    ARROWS_COUNTER_CLOCKWISE = "PhArrowsCounterClockwise"
    ARROWS_DOWN_UP = "PhArrowsDownUp"
    ARROWS_HORIZONTAL = "PhArrowsHorizontal"
    ARROWS_IN = "PhArrowsIn"
    ARROWS_IN_CARDINAL = "PhArrowsInCardinal"
    ARROWS_IN_LINE_HORIZONTAL = "PhArrowsInLineHorizontal"
    ARROWS_IN_LINE_VERTICAL = "PhArrowsInLineVertical"
    ARROWS_IN_SIMPLE = "PhArrowsInSimple"
    ARROWS_LEFT_RIGHT = "PhArrowsLeftRight"
    ARROWS_MERGE = "PhArrowsMerge"
    ARROWS_OUT = "PhArrowsOut"
    ARROWS_OUT_CARDINAL = "PhArrowsOutCardinal"
    ARROWS_OUT_LINE_HORIZONTAL = "PhArrowsOutLineHorizontal"
    ARROWS_OUT_LINE_VERTICAL = "PhArrowsOutLineVertical"
    ARROWS_OUT_SIMPLE = "PhArrowsOutSimple"
    ARROWS_SPLIT = "PhArrowsSplit"
    ARROWS_VERTICAL = "PhArrowsVertical"
    ARROW_ARC_LEFT = "PhArrowArcLeft"
    ARROW_ARC_RIGHT = "PhArrowArcRight"
    ARROW_BEND_DOUBLE_UP_LEFT = "PhArrowBendDoubleUpLeft"
    ARROW_BEND_DOUBLE_UP_RIGHT = "PhArrowBendDoubleUpRight"
    ARROW_BEND_DOWN_LEFT = "PhArrowBendDownLeft"
    ARROW_BEND_DOWN_RIGHT = "PhArrowBendDownRight"
    ARROW_BEND_LEFT_DOWN = "PhArrowBendLeftDown"
    ARROW_BEND_LEFT_UP = "PhArrowBendLeftUp"
    ARROW_BEND_RIGHT_DOWN = "PhArrowBendRightDown"
    ARROW_BEND_RIGHT_UP = "PhArrowBendRightUp"
    ARROW_BEND_UP_LEFT = "PhArrowBendUpLeft"
    ARROW_BEND_UP_RIGHT = "PhArrowBendUpRight"
    ARROW_CIRCLE_DOWN = "PhArrowCircleDown"
    ARROW_CIRCLE_DOWN_LEFT = "PhArrowCircleDownLeft"
    ARROW_CIRCLE_DOWN_RIGHT = "PhArrowCircleDownRight"
    ARROW_CIRCLE_LEFT = "PhArrowCircleLeft"
    ARROW_CIRCLE_RIGHT = "PhArrowCircleRight"
    ARROW_CIRCLE_UP = "PhArrowCircleUp"
    ARROW_CIRCLE_UP_LEFT = "PhArrowCircleUpLeft"
    ARROW_CIRCLE_UP_RIGHT = "PhArrowCircleUpRight"
    ARROW_CLOCKWISE = "PhArrowClockwise"
    ARROW_COUNTER_CLOCKWISE = "PhArrowCounterClockwise"
    ARROW_DOWN = "PhArrowDown"
    ARROW_DOWN_LEFT = "PhArrowDownLeft"
    ARROW_DOWN_RIGHT = "PhArrowDownRight"
    ARROW_ELBOW_DOWN_LEFT = "PhArrowElbowDownLeft"
    ARROW_ELBOW_DOWN_RIGHT = "PhArrowElbowDownRight"
    ARROW_ELBOW_LEFT = "PhArrowElbowLeft"
    ARROW_ELBOW_LEFT_DOWN = "PhArrowElbowLeftDown"
    ARROW_ELBOW_LEFT_UP = "PhArrowElbowLeftUp"
    ARROW_ELBOW_RIGHT = "PhArrowElbowRight"
    ARROW_ELBOW_RIGHT_DOWN = "PhArrowElbowRightDown"
    ARROW_ELBOW_RIGHT_UP = "PhArrowElbowRightUp"
    ARROW_ELBOW_UP_LEFT = "PhArrowElbowUpLeft"
    ARROW_ELBOW_UP_RIGHT = "PhArrowElbowUpRight"
    ARROW_FAT_DOWN = "PhArrowFatDown"
    ARROW_FAT_LEFT = "PhArrowFatLeft"
    ARROW_FAT_LINES_DOWN = "PhArrowFatLinesDown"
    ARROW_FAT_LINES_LEFT = "PhArrowFatLinesLeft"
    ARROW_FAT_LINES_RIGHT = "PhArrowFatLinesRight"
    ARROW_FAT_LINES_UP = "PhArrowFatLinesUp"
    ARROW_FAT_LINE_DOWN = "PhArrowFatLineDown"
    ARROW_FAT_LINE_LEFT = "PhArrowFatLineLeft"
    ARROW_FAT_LINE_RIGHT = "PhArrowFatLineRight"
    ARROW_FAT_LINE_UP = "PhArrowFatLineUp"
    ARROW_FAT_RIGHT = "PhArrowFatRight"
    ARROW_FAT_UP = "PhArrowFatUp"
    ARROW_LEFT = "PhArrowLeft"
    ARROW_LINE_DOWN = "PhArrowLineDown"
    ARROW_LINE_DOWN_LEFT = "PhArrowLineDownLeft"
    ARROW_LINE_DOWN_RIGHT = "PhArrowLineDownRight"
    ARROW_LINE_LEFT = "PhArrowLineLeft"
    ARROW_LINE_RIGHT = "PhArrowLineRight"
    ARROW_LINE_UP = "PhArrowLineUp"
    ARROW_LINE_UP_LEFT = "PhArrowLineUpLeft"
    ARROW_LINE_UP_RIGHT = "PhArrowLineUpRight"
    ARROW_RIGHT = "PhArrowRight"
    ARROW_SQUARE_DOWN = "PhArrowSquareDown"
    ARROW_SQUARE_DOWN_LEFT = "PhArrowSquareDownLeft"
    ARROW_SQUARE_DOWN_RIGHT = "PhArrowSquareDownRight"
    ARROW_SQUARE_IN = "PhArrowSquareIn"
    ARROW_SQUARE_LEFT = "PhArrowSquareLeft"
    ARROW_SQUARE_OUT = "PhArrowSquareOut"
    ARROW_SQUARE_RIGHT = "PhArrowSquareRight"
    ARROW_SQUARE_UP = "PhArrowSquareUp"
    ARROW_SQUARE_UP_LEFT = "PhArrowSquareUpLeft"
    ARROW_SQUARE_UP_RIGHT = "PhArrowSquareUpRight"
    ARROW_UP = "PhArrowUp"
    ARROW_UP_LEFT = "PhArrowUpLeft"
    ARROW_UP_RIGHT = "PhArrowUpRight"
    ARROW_U_DOWN_LEFT = "PhArrowUDownLeft"
    ARROW_U_DOWN_RIGHT = "PhArrowUDownRight"
    ARROW_U_LEFT_DOWN = "PhArrowULeftDown"
    ARROW_U_LEFT_UP = "PhArrowULeftUp"
    ARROW_U_RIGHT_DOWN = "PhArrowURightDown"
    ARROW_U_RIGHT_UP = "PhArrowURightUp"
    ARROW_U_UP_LEFT = "PhArrowUUpLeft"
    ARROW_U_UP_RIGHT = "PhArrowUUpRight"
    ARTICLE = "PhArticle"
    ARTICLE_MEDIUM = "PhArticleMedium"
    ARTICLE_NY_TIMES = "PhArticleNyTimes"
    ASCLEPIUS = "PhAsclepius"
    ASTERISK = "PhAsterisk"
    ASTERISK_SIMPLE = "PhAsteriskSimple"
    AT = "PhAt"
    ATLAN_METADATA = "atlanMetadata"
    ATLAN_SHIELD = "atlanShield"
    ATLAN_TAG = "atlanTags"
    ATOM = "PhAtom"
    AVOCADO = "PhAvocado"
    AXE = "PhAxe"
    BABY = "PhBaby"
    BABY_CARRIAGE = "PhBabyCarriage"
    BACKPACK = "PhBackpack"
    BACKSPACE = "PhBackspace"
    BAG = "PhBag"
    BAG_SIMPLE = "PhBagSimple"
    BALLOON = "PhBalloon"
    BANDAIDS = "PhBandaids"
    BANK = "PhBank"
    BARBELL = "PhBarbell"
    BARCODE = "PhBarcode"
    BARN = "PhBarn"
    BARRICADE = "PhBarricade"
    BASEBALL = "PhBaseball"
    BASEBALL_CAP = "PhBaseballCap"
    BASEBALL_HELMET = "PhBaseballHelmet"
    BASKET = "PhBasket"
    BASKETBALL = "PhBasketball"
    BATHTUB = "PhBathtub"
    BATTERY_CHARGING = "PhBatteryCharging"
    BATTERY_CHARGING_VERTICAL = "PhBatteryChargingVertical"
    BATTERY_EMPTY = "PhBatteryEmpty"
    BATTERY_FULL = "PhBatteryFull"
    BATTERY_HIGH = "PhBatteryHigh"
    BATTERY_LOW = "PhBatteryLow"
    BATTERY_MEDIUM = "PhBatteryMedium"
    BATTERY_PLUS = "PhBatteryPlus"
    BATTERY_PLUS_VERTICAL = "PhBatteryPlusVertical"
    BATTERY_VERTICAL_EMPTY = "PhBatteryVerticalEmpty"
    BATTERY_VERTICAL_FULL = "PhBatteryVerticalFull"
    BATTERY_VERTICAL_HIGH = "PhBatteryVerticalHigh"
    BATTERY_VERTICAL_LOW = "PhBatteryVerticalLow"
    BATTERY_VERTICAL_MEDIUM = "PhBatteryVerticalMedium"
    BATTERY_WARNING = "PhBatteryWarning"
    BATTERY_WARNING_VERTICAL = "PhBatteryWarningVertical"
    BEACH_BALL = "PhBeachBall"
    BEANIE = "PhBeanie"
    BED = "PhBed"
    BEER_BOTTLE = "PhBeerBottle"
    BEER_STEIN = "PhBeerStein"
    BEHANCE_LOGO = "PhBehanceLogo"
    BELL = "PhBell"
    BELL_RINGING = "PhBellRinging"
    BELL_SIMPLE = "PhBellSimple"
    BELL_SIMPLE_RINGING = "PhBellSimpleRinging"
    BELL_SIMPLE_SLASH = "PhBellSimpleSlash"
    BELL_SIMPLE_Z = "PhBellSimpleZ"
    BELL_SLASH = "PhBellSlash"
    BELL_Z = "PhBellZ"
    BELT = "PhBelt"
    BEZIER_CURVE = "PhBezierCurve"
    BICYCLE = "PhBicycle"
    BINARY = "PhBinary"
    BINOCULARS = "PhBinoculars"
    BIOHAZARD = "PhBiohazard"
    BIRD = "PhBird"
    BLUEPRINT = "PhBlueprint"
    BLUETOOTH = "PhBluetooth"
    BLUETOOTH_CONNECTED = "PhBluetoothConnected"
    BLUETOOTH_SLASH = "PhBluetoothSlash"
    BLUETOOTH_X = "PhBluetoothX"
    BOAT = "PhBoat"
    BOMB = "PhBomb"
    BONE = "PhBone"
    BOOK = "PhBook"
    BOOKMARK = "PhBookmark"
    BOOKMARKS = "PhBookmarks"
    BOOKMARKS_SIMPLE = "PhBookmarksSimple"
    BOOKMARK_SIMPLE = "PhBookmarkSimple"
    BOOKS = "PhBooks"
    BOOK_BOOKMARK = "PhBookBookmark"
    BOOK_OPEN = "PhBookOpen"
    BOOK_OPEN_TEXT = "PhBookOpenText"
    BOOK_OPEN_USER = "PhBookOpenUser"
    BOOT = "PhBoot"
    BOULES = "PhBoules"
    BOUNDING_BOX = "PhBoundingBox"
    BOWLING_BALL = "PhBowlingBall"
    BOWL_FOOD = "PhBowlFood"
    BOWL_STEAM = "PhBowlSteam"
    BOXING_GLOVE = "PhBoxingGlove"
    BOX_ARROW_DOWN = "PhBoxArrowDown"
    BOX_ARROW_UP = "PhBoxArrowUp"
    BRACKETS_ANGLE = "PhBracketsAngle"
    BRACKETS_CURLY = "PhBracketsCurly"
    BRACKETS_ROUND = "PhBracketsRound"
    BRACKETS_SQUARE = "PhBracketsSquare"
    BRAIN = "PhBrain"
    BRANDY = "PhBrandy"
    BREAD = "PhBread"
    BRIDGE = "PhBridge"
    BRIEFCASE = "PhBriefcase"
    BRIEFCASE_METAL = "PhBriefcaseMetal"
    BROADCAST = "PhBroadcast"
    BROOM = "PhBroom"
    BROWSER = "PhBrowser"
    BROWSERS = "PhBrowsers"
    BUG = "PhBug"
    BUG_BEETLE = "PhBugBeetle"
    BUG_DROID = "PhBugDroid"
    BUILDING = "PhBuilding"
    BUILDINGS = "PhBuildings"
    BUILDING_APARTMENT = "PhBuildingApartment"
    BUILDING_OFFICE = "PhBuildingOffice"
    BULLDOZER = "PhBulldozer"
    BUS = "PhBus"
    BUTTERFLY = "PhButterfly"
    CABLE_CAR = "PhCableCar"
    CACTUS = "PhCactus"
    CAKE = "PhCake"
    CALCULATOR = "PhCalculator"
    CALENDAR = "PhCalendar"
    CALENDAR_BLANK = "PhCalendarBlank"
    CALENDAR_CHECK = "PhCalendarCheck"
    CALENDAR_DOT = "PhCalendarDot"
    CALENDAR_DOTS = "PhCalendarDots"
    CALENDAR_HEART = "PhCalendarHeart"
    CALENDAR_MINUS = "PhCalendarMinus"
    CALENDAR_PLUS = "PhCalendarPlus"
    CALENDAR_SLASH = "PhCalendarSlash"
    CALENDAR_STAR = "PhCalendarStar"
    CALENDAR_X = "PhCalendarX"
    CALL_BELL = "PhCallBell"
    CAMERA = "PhCamera"
    CAMERA_PLUS = "PhCameraPlus"
    CAMERA_ROTATE = "PhCameraRotate"
    CAMERA_SLASH = "PhCameraSlash"
    CAMPFIRE = "PhCampfire"
    CAR = "PhCar"
    CARDHOLDER = "PhCardholder"
    CARDS = "PhCards"
    CARDS_THREE = "PhCardsThree"
    CARET_CIRCLE_DOUBLE_DOWN = "PhCaretCircleDoubleDown"
    CARET_CIRCLE_DOUBLE_LEFT = "PhCaretCircleDoubleLeft"
    CARET_CIRCLE_DOUBLE_RIGHT = "PhCaretCircleDoubleRight"
    CARET_CIRCLE_DOUBLE_UP = "PhCaretCircleDoubleUp"
    CARET_CIRCLE_DOWN = "PhCaretCircleDown"
    CARET_CIRCLE_LEFT = "PhCaretCircleLeft"
    CARET_CIRCLE_RIGHT = "PhCaretCircleRight"
    CARET_CIRCLE_UP = "PhCaretCircleUp"
    CARET_CIRCLE_UP_DOWN = "PhCaretCircleUpDown"
    CARET_DOUBLE_DOWN = "PhCaretDoubleDown"
    CARET_DOUBLE_LEFT = "PhCaretDoubleLeft"
    CARET_DOUBLE_RIGHT = "PhCaretDoubleRight"
    CARET_DOUBLE_UP = "PhCaretDoubleUp"
    CARET_DOWN = "PhCaretDown"
    CARET_LEFT = "PhCaretLeft"
    CARET_LINE_DOWN = "PhCaretLineDown"
    CARET_LINE_LEFT = "PhCaretLineLeft"
    CARET_LINE_RIGHT = "PhCaretLineRight"
    CARET_LINE_UP = "PhCaretLineUp"
    CARET_RIGHT = "PhCaretRight"
    CARET_UP = "PhCaretUp"
    CARET_UP_DOWN = "PhCaretUpDown"
    CARROT = "PhCarrot"
    CAR_BATTERY = "PhCarBattery"
    CAR_PROFILE = "PhCarProfile"
    CAR_SIMPLE = "PhCarSimple"
    CASH_REGISTER = "PhCashRegister"
    CASSETTE_TAPE = "PhCassetteTape"
    CASTLE_TURRET = "PhCastleTurret"
    CAT = "PhCat"
    CELL_SIGNAL_FULL = "PhCellSignalFull"
    CELL_SIGNAL_HIGH = "PhCellSignalHigh"
    CELL_SIGNAL_LOW = "PhCellSignalLow"
    CELL_SIGNAL_MEDIUM = "PhCellSignalMedium"
    CELL_SIGNAL_NONE = "PhCellSignalNone"
    CELL_SIGNAL_SLASH = "PhCellSignalSlash"
    CELL_SIGNAL_X = "PhCellSignalX"
    CELL_TOWER = "PhCellTower"
    CERTIFICATE = "PhCertificate"
    CHAIR = "PhChair"
    CHALKBOARD = "PhChalkboard"
    CHALKBOARD_SIMPLE = "PhChalkboardSimple"
    CHALKBOARD_TEACHER = "PhChalkboardTeacher"
    CHAMPAGNE = "PhChampagne"
    CHARGING_STATION = "PhChargingStation"
    CHART_BAR = "PhChartBar"
    CHART_BAR_HORIZONTAL = "PhChartBarHorizontal"
    CHART_DONUT = "PhChartDonut"
    CHART_LINE = "PhChartLine"
    CHART_LINE_DOWN = "PhChartLineDown"
    CHART_LINE_UP = "PhChartLineUp"
    CHART_PIE = "PhChartPie"
    CHART_PIE_SLICE = "PhChartPieSlice"
    CHART_POLAR = "PhChartPolar"
    CHART_SCATTER = "PhChartScatter"
    CHAT = "PhChat"
    CHATS = "PhChats"
    CHATS_CIRCLE = "PhChatsCircle"
    CHATS_TEARDROP = "PhChatsTeardrop"
    CHAT_CENTERED = "PhChatCentered"
    CHAT_CENTERED_DOTS = "PhChatCenteredDots"
    CHAT_CENTERED_SLASH = "PhChatCenteredSlash"
    CHAT_CENTERED_TEXT = "PhChatCenteredText"
    CHAT_CIRCLE = "PhChatCircle"
    CHAT_CIRCLE_DOTS = "PhChatCircleDots"
    CHAT_CIRCLE_SLASH = "PhChatCircleSlash"
    CHAT_CIRCLE_TEXT = "PhChatCircleText"
    CHAT_DOTS = "PhChatDots"
    CHAT_SLASH = "PhChatSlash"
    CHAT_TEARDROP = "PhChatTeardrop"
    CHAT_TEARDROP_DOTS = "PhChatTeardropDots"
    CHAT_TEARDROP_SLASH = "PhChatTeardropSlash"
    CHAT_TEARDROP_TEXT = "PhChatTeardropText"
    CHAT_TEXT = "PhChatText"
    CHECK = "PhCheck"
    CHECKERBOARD = "PhCheckerboard"
    CHECKS = "PhChecks"
    CHECK_CIRCLE = "PhCheckCircle"
    CHECK_FAT = "PhCheckFat"
    CHECK_SQUARE = "PhCheckSquare"
    CHECK_SQUARE_OFFSET = "PhCheckSquareOffset"
    CHEERS = "PhCheers"
    CHEESE = "PhCheese"
    CHEF_HAT = "PhChefHat"
    CHERRIES = "PhCherries"
    CHURCH = "PhChurch"
    CIGARETTE = "PhCigarette"
    CIGARETTE_SLASH = "PhCigaretteSlash"
    CIRCLE = "PhCircle"
    CIRCLES_FOUR = "PhCirclesFour"
    CIRCLES_THREE = "PhCirclesThree"
    CIRCLES_THREE_PLUS = "PhCirclesThreePlus"
    CIRCLE_DASHED = "PhCircleDashed"
    CIRCLE_HALF = "PhCircleHalf"
    CIRCLE_HALF_TILT = "PhCircleHalfTilt"
    CIRCLE_NOTCH = "PhCircleNotch"
    CIRCUITRY = "PhCircuitry"
    CITY = "PhCity"
    CLIPBOARD = "PhClipboard"
    CLIPBOARD_TEXT = "PhClipboardText"
    CLOCK = "PhClock"
    CLOCK_AFTERNOON = "PhClockAfternoon"
    CLOCK_CLOCKWISE = "PhClockClockwise"
    CLOCK_COUNTDOWN = "PhClockCountdown"
    CLOCK_COUNTER_CLOCKWISE = "PhClockCounterClockwise"
    CLOCK_USER = "PhClockUser"
    CLOSED_CAPTIONING = "PhClosedCaptioning"
    CLOUD = "PhCloud"
    CLOUD_ARROW_DOWN = "PhCloudArrowDown"
    CLOUD_ARROW_UP = "PhCloudArrowUp"
    CLOUD_CHECK = "PhCloudCheck"
    CLOUD_FOG = "PhCloudFog"
    CLOUD_LIGHTNING = "PhCloudLightning"
    CLOUD_MOON = "PhCloudMoon"
    CLOUD_RAIN = "PhCloudRain"
    CLOUD_SLASH = "PhCloudSlash"
    CLOUD_SNOW = "PhCloudSnow"
    CLOUD_SUN = "PhCloudSun"
    CLOUD_WARNING = "PhCloudWarning"
    CLOUD_X = "PhCloudX"
    CLOVER = "PhClover"
    CLUB = "PhClub"
    COAT_HANGER = "PhCoatHanger"
    CODA_LOGO = "PhCodaLogo"
    CODE = "PhCode"
    CODEPEN_LOGO = "PhCodepenLogo"
    CODESANDBOX_LOGO = "PhCodesandboxLogo"
    CODE_BLOCK = "PhCodeBlock"
    CODE_SIMPLE = "PhCodeSimple"
    COFFEE = "PhCoffee"
    COFFEE_BEAN = "PhCoffeeBean"
    COIN = "PhCoin"
    COINS = "PhCoins"
    COIN_VERTICAL = "PhCoinVertical"
    COLUMNS = "PhColumns"
    COLUMNS_PLUS_LEFT = "PhColumnsPlusLeft"
    COLUMNS_PLUS_RIGHT = "PhColumnsPlusRight"
    COMMAND = "PhCommand"
    COMPASS = "PhCompass"
    COMPASS_ROSE = "PhCompassRose"
    COMPASS_TOOL = "PhCompassTool"
    COMPUTER_TOWER = "PhComputerTower"
    CONFETTI = "PhConfetti"
    CONTACTLESS_PAYMENT = "PhContactlessPayment"
    CONTROL = "PhControl"
    COOKIE = "PhCookie"
    COOKING_POT = "PhCookingPot"
    COPY = "PhCopy"
    COPYLEFT = "PhCopyleft"
    COPYRIGHT = "PhCopyright"
    COPY_SIMPLE = "PhCopySimple"
    CORNERS_IN = "PhCornersIn"
    CORNERS_OUT = "PhCornersOut"
    COUCH = "PhCouch"
    COURT_BASKETBALL = "PhCourtBasketball"
    COW = "PhCow"
    COWBOY_HAT = "PhCowboyHat"
    CPU = "PhCpu"
    CRANE = "PhCrane"
    CRANE_TOWER = "PhCraneTower"
    CREDIT_CARD = "PhCreditCard"
    CRICKET = "PhCricket"
    CROP = "PhCrop"
    CROSS = "PhCross"
    CROSSHAIR = "PhCrosshair"
    CROSSHAIR_SIMPLE = "PhCrosshairSimple"
    CROWN = "PhCrown"
    CROWN_CROSS = "PhCrownCross"
    CROWN_SIMPLE = "PhCrownSimple"
    CUBE = "PhCube"
    CUBE_FOCUS = "PhCubeFocus"
    CUBE_TRANSPARENT = "PhCubeTransparent"
    CURRENCY_BTC = "PhCurrencyBtc"
    CURRENCY_CIRCLE_DOLLAR = "PhCurrencyCircleDollar"
    CURRENCY_CNY = "PhCurrencyCny"
    CURRENCY_DOLLAR = "PhCurrencyDollar"
    CURRENCY_DOLLAR_SIMPLE = "PhCurrencyDollarSimple"
    CURRENCY_ETH = "PhCurrencyEth"
    CURRENCY_EUR = "PhCurrencyEur"
    CURRENCY_GBP = "PhCurrencyGbp"
    CURRENCY_INR = "PhCurrencyInr"
    CURRENCY_JPY = "PhCurrencyJpy"
    CURRENCY_KRW = "PhCurrencyKrw"
    CURRENCY_KZT = "PhCurrencyKzt"
    CURRENCY_NGN = "PhCurrencyNgn"
    CURRENCY_RUB = "PhCurrencyRub"
    CURSOR = "PhCursor"
    CURSOR_CLICK = "PhCursorClick"
    CURSOR_TEXT = "PhCursorText"
    CYLINDER = "PhCylinder"
    DATABASE = "PhDatabase"
    DESK = "PhDesk"
    DESKTOP = "PhDesktop"
    DESKTOP_TOWER = "PhDesktopTower"
    DETECTIVE = "PhDetective"
    DEVICES = "PhDevices"
    DEVICE_MOBILE = "PhDeviceMobile"
    DEVICE_MOBILE_CAMERA = "PhDeviceMobileCamera"
    DEVICE_MOBILE_SLASH = "PhDeviceMobileSlash"
    DEVICE_MOBILE_SPEAKER = "PhDeviceMobileSpeaker"
    DEVICE_ROTATE = "PhDeviceRotate"
    DEVICE_TABLET = "PhDeviceTablet"
    DEVICE_TABLET_CAMERA = "PhDeviceTabletCamera"
    DEVICE_TABLET_SPEAKER = "PhDeviceTabletSpeaker"
    DEV_TO_LOGO = "PhDevToLogo"
    DIAMOND = "PhDiamond"
    DIAMONDS_FOUR = "PhDiamondsFour"
    DICE_FIVE = "PhDiceFive"
    DICE_FOUR = "PhDiceFour"
    DICE_ONE = "PhDiceOne"
    DICE_SIX = "PhDiceSix"
    DICE_THREE = "PhDiceThree"
    DICE_TWO = "PhDiceTwo"
    DISC = "PhDisc"
    DISCORD_LOGO = "PhDiscordLogo"
    DISCO_BALL = "PhDiscoBall"
    DIVIDE = "PhDivide"
    DNA = "PhDna"
    DOG = "PhDog"
    DOOR = "PhDoor"
    DOOR_OPEN = "PhDoorOpen"
    DOT = "PhDot"
    DOTS_NINE = "PhDotsNine"
    DOTS_SIX = "PhDotsSix"
    DOTS_SIX_VERTICAL = "PhDotsSixVertical"
    DOTS_THREE = "PhDotsThree"
    DOTS_THREE_CIRCLE = "PhDotsThreeCircle"
    DOTS_THREE_CIRCLE_VERTICAL = "PhDotsThreeCircleVertical"
    DOTS_THREE_OUTLINE = "PhDotsThreeOutline"
    DOTS_THREE_OUTLINE_VERTICAL = "PhDotsThreeOutlineVertical"
    DOTS_THREE_VERTICAL = "PhDotsThreeVertical"
    DOT_OUTLINE = "PhDotOutline"
    DOWNLOAD = "PhDownload"
    DOWNLOAD_SIMPLE = "PhDownloadSimple"
    DRESS = "PhDress"
    DRESSER = "PhDresser"
    DRIBBBLE_LOGO = "PhDribbbleLogo"
    DRONE = "PhDrone"
    DROP = "PhDrop"
    DROPBOX_LOGO = "PhDropboxLogo"
    DROP_HALF = "PhDropHalf"
    DROP_HALF_BOTTOM = "PhDropHalfBottom"
    DROP_SIMPLE = "PhDropSimple"
    DROP_SLASH = "PhDropSlash"
    EAR = "PhEar"
    EAR_SLASH = "PhEarSlash"
    EGG = "PhEgg"
    EGG_CRACK = "PhEggCrack"
    EJECT = "PhEject"
    EJECT_SIMPLE = "PhEjectSimple"
    ELEVATOR = "PhElevator"
    EMPTY = "PhEmpty"
    ENGINE = "PhEngine"
    ENVELOPE = "PhEnvelope"
    ENVELOPE_OPEN = "PhEnvelopeOpen"
    ENVELOPE_SIMPLE = "PhEnvelopeSimple"
    ENVELOPE_SIMPLE_OPEN = "PhEnvelopeSimpleOpen"
    EQUALIZER = "PhEqualizer"
    EQUALS = "PhEquals"
    ERASER = "PhEraser"
    ESCALATOR_DOWN = "PhEscalatorDown"
    ESCALATOR_UP = "PhEscalatorUp"
    EXAM = "PhExam"
    EXCLAMATION_MARK = "PhExclamationMark"
    EXCLUDE = "PhExclude"
    EXCLUDE_SQUARE = "PhExcludeSquare"
    EXPORT = "PhExport"
    EYE = "PhEye"
    EYEDROPPER = "PhEyedropper"
    EYEDROPPER_SAMPLE = "PhEyedropperSample"
    EYEGLASSES = "PhEyeglasses"
    EYES = "PhEyes"
    EYE_CLOSED = "PhEyeClosed"
    EYE_SLASH = "PhEyeSlash"
    FACEBOOK_LOGO = "PhFacebookLogo"
    FACE_MASK = "PhFaceMask"
    FACTORY = "PhFactory"
    FADERS = "PhFaders"
    FADERS_HORIZONTAL = "PhFadersHorizontal"
    FALLOUT_SHELTER = "PhFalloutShelter"
    FAN = "PhFan"
    FARM = "PhFarm"
    FAST_FORWARD = "PhFastForward"
    FAST_FORWARD_CIRCLE = "PhFastForwardCircle"
    FEATHER = "PhFeather"
    FEDIVERSE_LOGO = "PhFediverseLogo"
    FIGMA_LOGO = "PhFigmaLogo"
    FILE = "PhFile"
    FILES = "PhFiles"
    FILE_ARCHIVE = "PhFileArchive"
    FILE_ARROW_DOWN = "PhFileArrowDown"
    FILE_ARROW_UP = "PhFileArrowUp"
    FILE_AUDIO = "PhFileAudio"
    FILE_C = "PhFileC"
    FILE_CLOUD = "PhFileCloud"
    FILE_CODE = "PhFileCode"
    FILE_CPP = "PhFileCpp"
    FILE_CSS = "PhFileCss"
    FILE_CSV = "PhFileCsv"
    FILE_C_SHARP = "PhFileCSharp"
    FILE_DASHED = "PhFileDashed"
    FILE_DOC = "PhFileDoc"
    FILE_HTML = "PhFileHtml"
    FILE_IMAGE = "PhFileImage"
    FILE_INI = "PhFileIni"
    FILE_JPG = "PhFileJpg"
    FILE_JS = "PhFileJs"
    FILE_JSX = "PhFileJsx"
    FILE_LOCK = "PhFileLock"
    FILE_MAGNIFYING_GLASS = "PhFileMagnifyingGlass"
    FILE_MD = "PhFileMd"
    FILE_MINUS = "PhFileMinus"
    FILE_PDF = "PhFilePdf"
    FILE_PLUS = "PhFilePlus"
    FILE_PNG = "PhFilePng"
    FILE_PPT = "PhFilePpt"
    FILE_PY = "PhFilePy"
    FILE_RS = "PhFileRs"
    FILE_SQL = "PhFileSql"
    FILE_SVG = "PhFileSvg"
    FILE_TEXT = "PhFileText"
    FILE_TS = "PhFileTs"
    FILE_TSX = "PhFileTsx"
    FILE_TXT = "PhFileTxt"
    FILE_VIDEO = "PhFileVideo"
    FILE_VUE = "PhFileVue"
    FILE_X = "PhFileX"
    FILE_XLS = "PhFileXls"
    FILE_ZIP = "PhFileZip"
    FILM_REEL = "PhFilmReel"
    FILM_SCRIPT = "PhFilmScript"
    FILM_SLATE = "PhFilmSlate"
    FILM_STRIP = "PhFilmStrip"
    FINGERPRINT = "PhFingerprint"
    FINGERPRINT_SIMPLE = "PhFingerprintSimple"
    FINN_THE_HUMAN = "PhFinnTheHuman"
    FIRE = "PhFire"
    FIRE_EXTINGUISHER = "PhFireExtinguisher"
    FIRE_SIMPLE = "PhFireSimple"
    FIRE_TRUCK = "PhFireTruck"
    FIRST_AID = "PhFirstAid"
    FIRST_AID_KIT = "PhFirstAidKit"
    FISH = "PhFish"
    FISH_SIMPLE = "PhFishSimple"
    FLAG = "PhFlag"
    FLAG_BANNER = "PhFlagBanner"
    FLAG_BANNER_FOLD = "PhFlagBannerFold"
    FLAG_CHECKERED = "PhFlagCheckered"
    FLAG_PENNANT = "PhFlagPennant"
    FLAME = "PhFlame"
    FLASHLIGHT = "PhFlashlight"
    FLASK = "PhFlask"
    FLIP_HORIZONTAL = "PhFlipHorizontal"
    FLIP_VERTICAL = "PhFlipVertical"
    FLOPPY_DISK = "PhFloppyDisk"
    FLOPPY_DISK_BACK = "PhFloppyDiskBack"
    FLOWER = "PhFlower"
    FLOWER_LOTUS = "PhFlowerLotus"
    FLOWER_TULIP = "PhFlowerTulip"
    FLOW_ARROW = "PhFlowArrow"
    FLYING_SAUCER = "PhFlyingSaucer"
    FOLDER = "PhFolder"
    FOLDERS = "PhFolders"
    FOLDER_DASHED = "PhFolderDashed"
    FOLDER_LOCK = "PhFolderLock"
    FOLDER_MINUS = "PhFolderMinus"
    FOLDER_NOTCH = "PhFolderNotch"
    FOLDER_NOTCH_MINUS = "PhFolderNotchMinus"
    FOLDER_NOTCH_OPEN = "PhFolderNotchOpen"
    FOLDER_NOTCH_PLUS = "PhFolderNotchPlus"
    FOLDER_OPEN = "PhFolderOpen"
    FOLDER_PLUS = "PhFolderPlus"
    FOLDER_SIMPLE = "PhFolderSimple"
    FOLDER_SIMPLE_DASHED = "PhFolderSimpleDashed"
    FOLDER_SIMPLE_LOCK = "PhFolderSimpleLock"
    FOLDER_SIMPLE_MINUS = "PhFolderSimpleMinus"
    FOLDER_SIMPLE_PLUS = "PhFolderSimplePlus"
    FOLDER_SIMPLE_STAR = "PhFolderSimpleStar"
    FOLDER_SIMPLE_USER = "PhFolderSimpleUser"
    FOLDER_STAR = "PhFolderStar"
    FOLDER_USER = "PhFolderUser"
    FOOTBALL = "PhFootball"
    FOOTBALL_HELMET = "PhFootballHelmet"
    FOOTPRINTS = "PhFootprints"
    FORK_KNIFE = "PhForkKnife"
    FOUR_K = "PhFourK"
    FRAMER_LOGO = "PhFramerLogo"
    FRAME_CORNERS = "PhFrameCorners"
    FUNCTION = "PhFunction"
    FUNNEL = "PhFunnel"
    FUNNEL_SIMPLE = "PhFunnelSimple"
    FUNNEL_SIMPLE_X = "PhFunnelSimpleX"
    FUNNEL_X = "PhFunnelX"
    GAME_CONTROLLER = "PhGameController"
    GARAGE = "PhGarage"
    GAS_CAN = "PhGasCan"
    GAS_PUMP = "PhGasPump"
    GAUGE = "PhGauge"
    GAVEL = "PhGavel"
    GEAR = "PhGear"
    GEAR_FINE = "PhGearFine"
    GEAR_SIX = "PhGearSix"
    GENDER_FEMALE = "PhGenderFemale"
    GENDER_INTERSEX = "PhGenderIntersex"
    GENDER_MALE = "PhGenderMale"
    GENDER_NEUTER = "PhGenderNeuter"
    GENDER_NONBINARY = "PhGenderNonbinary"
    GENDER_TRANSGENDER = "PhGenderTransgender"
    GHOST = "PhGhost"
    GIF = "PhGif"
    GIFT = "PhGift"
    GITHUB_LOGO = "PhGithubLogo"
    GITLAB_LOGO = "PhGitlabLogo"
    GITLAB_LOGO_SIMPLE = "PhGitlabLogoSimple"
    GIT_BRANCH = "PhGitBranch"
    GIT_COMMIT = "PhGitCommit"
    GIT_DIFF = "PhGitDiff"
    GIT_FORK = "PhGitFork"
    GIT_MERGE = "PhGitMerge"
    GIT_PULL_REQUEST = "PhGitPullRequest"
    GLOBE = "PhGlobe"
    GLOBE_HEMISPHERE_EAST = "PhGlobeHemisphereEast"
    GLOBE_HEMISPHERE_WEST = "PhGlobeHemisphereWest"
    GLOBE_SIMPLE = "PhGlobeSimple"
    GLOBE_SIMPLE_X = "PhGlobeSimpleX"
    GLOBE_STAND = "PhGlobeStand"
    GLOBE_X = "PhGlobeX"
    GOGGLES = "PhGoggles"
    GOLF = "PhGolf"
    GOODREADS_LOGO = "PhGoodreadsLogo"
    GOOGLE_CARDBOARD_LOGO = "PhGoogleCardboardLogo"
    GOOGLE_CHROME_LOGO = "PhGoogleChromeLogo"
    GOOGLE_DRIVE_LOGO = "PhGoogleDriveLogo"
    GOOGLE_LOGO = "PhGoogleLogo"
    GOOGLE_PHOTOS_LOGO = "PhGooglePhotosLogo"
    GOOGLE_PLAY_LOGO = "PhGooglePlayLogo"
    GOOGLE_PODCASTS_LOGO = "PhGooglePodcastsLogo"
    GPS = "PhGps"
    GPS_FIX = "PhGpsFix"
    GPS_SLASH = "PhGpsSlash"
    GRADIENT = "PhGradient"
    GRADUATION_CAP = "PhGraduationCap"
    GRAINS = "PhGrains"
    GRAINS_SLASH = "PhGrainsSlash"
    GRAPH = "PhGraph"
    GRAPHICS_CARD = "PhGraphicsCard"
    GREATER_THAN = "PhGreaterThan"
    GREATER_THAN_OR_EQUAL = "PhGreaterThanOrEqual"
    GRID_FOUR = "PhGridFour"
    GRID_NINE = "PhGridNine"
    GUITAR = "PhGuitar"
    HAIR_DRYER = "PhHairDryer"
    HAMBURGER = "PhHamburger"
    HAMMER = "PhHammer"
    HAND = "PhHand"
    HANDBAG = "PhHandbag"
    HANDBAG_SIMPLE = "PhHandbagSimple"
    HANDSHAKE = "PhHandshake"
    HANDS_CLAPPING = "PhHandsClapping"
    HANDS_PRAYING = "PhHandsPraying"
    HAND_ARROW_DOWN = "PhHandArrowDown"
    HAND_ARROW_UP = "PhHandArrowUp"
    HAND_COINS = "PhHandCoins"
    HAND_DEPOSIT = "PhHandDeposit"
    HAND_EYE = "PhHandEye"
    HAND_FIST = "PhHandFist"
    HAND_GRABBING = "PhHandGrabbing"
    HAND_HEART = "PhHandHeart"
    HAND_PALM = "PhHandPalm"
    HAND_PEACE = "PhHandPeace"
    HAND_POINTING = "PhHandPointing"
    HAND_SOAP = "PhHandSoap"
    HAND_SWIPE_LEFT = "PhHandSwipeLeft"
    HAND_SWIPE_RIGHT = "PhHandSwipeRight"
    HAND_TAP = "PhHandTap"
    HAND_WAVING = "PhHandWaving"
    HAND_WITHDRAW = "PhHandWithdraw"
    HARD_DRIVE = "PhHardDrive"
    HARD_DRIVES = "PhHardDrives"
    HARD_HAT = "PhHardHat"
    HASH = "PhHash"
    HASH_STRAIGHT = "PhHashStraight"
    HEADLIGHTS = "PhHeadlights"
    HEADPHONES = "PhHeadphones"
    HEADSET = "PhHeadset"
    HEAD_CIRCUIT = "PhHeadCircuit"
    HEART = "PhHeart"
    HEARTBEAT = "PhHeartbeat"
    HEART_BREAK = "PhHeartBreak"
    HEART_HALF = "PhHeartHalf"
    HEART_STRAIGHT = "PhHeartStraight"
    HEART_STRAIGHT_BREAK = "PhHeartStraightBreak"
    HEXAGON = "PhHexagon"
    HIGHLIGHTER = "PhHighlighter"
    HIGHLIGHTER_CIRCLE = "PhHighlighterCircle"
    HIGH_DEFINITION = "PhHighDefinition"
    HIGH_HEEL = "PhHighHeel"
    HOCKEY = "PhHockey"
    HOODIE = "PhHoodie"
    HORSE = "PhHorse"
    HOSPITAL = "PhHospital"
    HOURGLASS = "PhHourglass"
    HOURGLASS_HIGH = "PhHourglassHigh"
    HOURGLASS_LOW = "PhHourglassLow"
    HOURGLASS_MEDIUM = "PhHourglassMedium"
    HOURGLASS_SIMPLE = "PhHourglassSimple"
    HOURGLASS_SIMPLE_HIGH = "PhHourglassSimpleHigh"
    HOURGLASS_SIMPLE_LOW = "PhHourglassSimpleLow"
    HOURGLASS_SIMPLE_MEDIUM = "PhHourglassSimpleMedium"
    HOUSE = "PhHouse"
    HOUSE_LINE = "PhHouseLine"
    HOUSE_SIMPLE = "PhHouseSimple"
    HURRICANE = "PhHurricane"
    ICE_CREAM = "PhIceCream"
    IDENTIFICATION_BADGE = "PhIdentificationBadge"
    IDENTIFICATION_CARD = "PhIdentificationCard"
    IMAGE = "PhImage"
    IMAGES = "PhImages"
    IMAGES_SQUARE = "PhImagesSquare"
    IMAGE_BROKEN = "PhImageBroken"
    IMAGE_SQUARE = "PhImageSquare"
    INFINITY = "PhInfinity"
    INFO = "PhInfo"
    INSTAGRAM_LOGO = "PhInstagramLogo"
    INTERSECT = "PhIntersect"
    INTERSECTION = "PhIntersection"
    INTERSECT_SQUARE = "PhIntersectSquare"
    INTERSECT_THREE = "PhIntersectThree"
    INVOICE = "PhInvoice"
    ISLAND = "PhIsland"
    JAR = "PhJar"
    JAR_LABEL = "PhJarLabel"
    JEEP = "PhJeep"
    JOYSTICK = "PhJoystick"
    KANBAN = "PhKanban"
    KEY = "PhKey"
    KEYBOARD = "PhKeyboard"
    KEYHOLE = "PhKeyhole"
    KEY_RETURN = "PhKeyReturn"
    KNIFE = "PhKnife"
    LADDER = "PhLadder"
    LADDER_SIMPLE = "PhLadderSimple"
    LAMP = "PhLamp"
    LAMP_PENDANT = "PhLampPendant"
    LAPTOP = "PhLaptop"
    LASSO = "PhLasso"
    LASTFM_LOGO = "PhLastfmLogo"
    LAYOUT = "PhLayout"
    LEAF = "PhLeaf"
    LECTERN = "PhLectern"
    LEGO = "PhLego"
    LEGO_SMILEY = "PhLegoSmiley"
    LESS_THAN = "PhLessThan"
    LESS_THAN_OR_EQUAL = "PhLessThanOrEqual"
    LETTER_CIRCLE_H = "PhLetterCircleH"
    LETTER_CIRCLE_P = "PhLetterCircleP"
    LETTER_CIRCLE_V = "PhLetterCircleV"
    LIFEBUOY = "PhLifebuoy"
    LIGHTBULB = "PhLightbulb"
    LIGHTBULB_FILAMENT = "PhLightbulbFilament"
    LIGHTHOUSE = "PhLighthouse"
    LIGHTNING = "PhLightning"
    LIGHTNING_A = "PhLightningA"
    LIGHTNING_SLASH = "PhLightningSlash"
    LINE_SEGMENT = "PhLineSegment"
    LINE_SEGMENTS = "PhLineSegments"
    LINE_VERTICAL = "PhLineVertical"
    LINK = "PhLink"
    LINKEDIN_LOGO = "PhLinkedinLogo"
    LINKTREE_LOGO = "PhLinktreeLogo"
    LINK_BREAK = "PhLinkBreak"
    LINK_SIMPLE = "PhLinkSimple"
    LINK_SIMPLE_BREAK = "PhLinkSimpleBreak"
    LINK_SIMPLE_HORIZONTAL = "PhLinkSimpleHorizontal"
    LINK_SIMPLE_HORIZONTAL_BREAK = "PhLinkSimpleHorizontalBreak"
    LINUX_LOGO = "PhLinuxLogo"
    LIST = "PhList"
    LIST_BULLETS = "PhListBullets"
    LIST_CHECKS = "PhListChecks"
    LIST_DASHES = "PhListDashes"
    LIST_HEART = "PhListHeart"
    LIST_MAGNIFYING_GLASS = "PhListMagnifyingGlass"
    LIST_NUMBERS = "PhListNumbers"
    LIST_PLUS = "PhListPlus"
    LIST_STAR = "PhListStar"
    LOCK = "PhLock"
    LOCKERS = "PhLockers"
    LOCK_KEY = "PhLockKey"
    LOCK_KEY_OPEN = "PhLockKeyOpen"
    LOCK_LAMINATED = "PhLockLaminated"
    LOCK_LAMINATED_OPEN = "PhLockLaminatedOpen"
    LOCK_OPEN = "PhLockOpen"
    LOCK_SIMPLE = "PhLockSimple"
    LOCK_SIMPLE_OPEN = "PhLockSimpleOpen"
    LOG = "PhLog"
    MAGIC_WAND = "PhMagicWand"
    MAGNET = "PhMagnet"
    MAGNET_STRAIGHT = "PhMagnetStraight"
    MAGNIFYING_GLASS = "PhMagnifyingGlass"
    MAGNIFYING_GLASS_MINUS = "PhMagnifyingGlassMinus"
    MAGNIFYING_GLASS_PLUS = "PhMagnifyingGlassPlus"
    MAILBOX = "PhMailbox"
    MAP_PIN = "PhMapPin"
    MAP_PIN_AREA = "PhMapPinArea"
    MAP_PIN_LINE = "PhMapPinLine"
    MAP_PIN_PLUS = "PhMapPinPlus"
    MAP_PIN_SIMPLE = "PhMapPinSimple"
    MAP_PIN_SIMPLE_AREA = "PhMapPinSimpleArea"
    MAP_PIN_SIMPLE_LINE = "PhMapPinSimpleLine"
    MAP_TRIFOLD = "PhMapTrifold"
    MARKDOWN_LOGO = "PhMarkdownLogo"
    MARKER_CIRCLE = "PhMarkerCircle"
    MARTINI = "PhMartini"
    MASK_HAPPY = "PhMaskHappy"
    MASK_SAD = "PhMaskSad"
    MASTODON_LOGO = "PhMastodonLogo"
    MATH_OPERATIONS = "PhMathOperations"
    MATRIX_LOGO = "PhMatrixLogo"
    MEDAL = "PhMedal"
    MEDAL_MILITARY = "PhMedalMilitary"
    MEDIUM_LOGO = "PhMediumLogo"
    MEGAPHONE = "PhMegaphone"
    MEGAPHONE_SIMPLE = "PhMegaphoneSimple"
    MEMBER_OF = "PhMemberOf"
    MEMORY = "PhMemory"
    MESSENGER_LOGO = "PhMessengerLogo"
    META_LOGO = "PhMetaLogo"
    METEOR = "PhMeteor"
    METRONOME = "PhMetronome"
    MICROPHONE = "PhMicrophone"
    MICROPHONE_SLASH = "PhMicrophoneSlash"
    MICROPHONE_STAGE = "PhMicrophoneStage"
    MICROSCOPE = "PhMicroscope"
    MICROSOFT_EXCEL_LOGO = "PhMicrosoftExcelLogo"
    MICROSOFT_OUTLOOK_LOGO = "PhMicrosoftOutlookLogo"
    MICROSOFT_POWERPOINT_LOGO = "PhMicrosoftPowerpointLogo"
    MICROSOFT_TEAMS_LOGO = "PhMicrosoftTeamsLogo"
    MICROSOFT_WORD_LOGO = "PhMicrosoftWordLogo"
    MINUS = "PhMinus"
    MINUS_CIRCLE = "PhMinusCircle"
    MINUS_SQUARE = "PhMinusSquare"
    MONEY = "PhMoney"
    MONEY_WAVY = "PhMoneyWavy"
    MONITOR = "PhMonitor"
    MONITOR_ARROW_UP = "PhMonitorArrowUp"
    MONITOR_PLAY = "PhMonitorPlay"
    MOON = "PhMoon"
    MOON_STARS = "PhMoonStars"
    MOPED = "PhMoped"
    MOPED_FRONT = "PhMopedFront"
    MOSQUE = "PhMosque"
    MOTORCYCLE = "PhMotorcycle"
    MOUNTAINS = "PhMountains"
    MOUSE = "PhMouse"
    MOUSE_LEFT_CLICK = "PhMouseLeftClick"
    MOUSE_MIDDLE_CLICK = "PhMouseMiddleClick"
    MOUSE_RIGHT_CLICK = "PhMouseRightClick"
    MOUSE_SCROLL = "PhMouseScroll"
    MOUSE_SIMPLE = "PhMouseSimple"
    MUSIC_NOTE = "PhMusicNote"
    MUSIC_NOTES = "PhMusicNotes"
    MUSIC_NOTES_MINUS = "PhMusicNotesMinus"
    MUSIC_NOTES_PLUS = "PhMusicNotesPlus"
    MUSIC_NOTES_SIMPLE = "PhMusicNotesSimple"
    MUSIC_NOTE_SIMPLE = "PhMusicNoteSimple"
    NAVIGATION_ARROW = "PhNavigationArrow"
    NEEDLE = "PhNeedle"
    NETWORK = "PhNetwork"
    NETWORK_SLASH = "PhNetworkSlash"
    NETWORK_X = "PhNetworkX"
    NEWSPAPER = "PhNewspaper"
    NEWSPAPER_CLIPPING = "PhNewspaperClipping"
    NOTCHES = "PhNotches"
    NOTE = "PhNote"
    NOTEBOOK = "PhNotebook"
    NOTEPAD = "PhNotepad"
    NOTE_BLANK = "PhNoteBlank"
    NOTE_PENCIL = "PhNotePencil"
    NOTIFICATION = "PhNotification"
    NOTION_LOGO = "PhNotionLogo"
    NOT_EQUALS = "PhNotEquals"
    NOT_MEMBER_OF = "PhNotMemberOf"
    NOT_SUBSET_OF = "PhNotSubsetOf"
    NOT_SUPERSET_OF = "PhNotSupersetOf"
    NUCLEAR_PLANT = "PhNuclearPlant"
    NUMBER_CIRCLE_EIGHT = "PhNumberCircleEight"
    NUMBER_CIRCLE_FIVE = "PhNumberCircleFive"
    NUMBER_CIRCLE_FOUR = "PhNumberCircleFour"
    NUMBER_CIRCLE_NINE = "PhNumberCircleNine"
    NUMBER_CIRCLE_ONE = "PhNumberCircleOne"
    NUMBER_CIRCLE_SEVEN = "PhNumberCircleSeven"
    NUMBER_CIRCLE_SIX = "PhNumberCircleSix"
    NUMBER_CIRCLE_THREE = "PhNumberCircleThree"
    NUMBER_CIRCLE_TWO = "PhNumberCircleTwo"
    NUMBER_CIRCLE_ZERO = "PhNumberCircleZero"
    NUMBER_EIGHT = "PhNumberEight"
    NUMBER_FIVE = "PhNumberFive"
    NUMBER_FOUR = "PhNumberFour"
    NUMBER_NINE = "PhNumberNine"
    NUMBER_ONE = "PhNumberOne"
    NUMBER_SEVEN = "PhNumberSeven"
    NUMBER_SIX = "PhNumberSix"
    NUMBER_SQUARE_EIGHT = "PhNumberSquareEight"
    NUMBER_SQUARE_FIVE = "PhNumberSquareFive"
    NUMBER_SQUARE_FOUR = "PhNumberSquareFour"
    NUMBER_SQUARE_NINE = "PhNumberSquareNine"
    NUMBER_SQUARE_ONE = "PhNumberSquareOne"
    NUMBER_SQUARE_SEVEN = "PhNumberSquareSeven"
    NUMBER_SQUARE_SIX = "PhNumberSquareSix"
    NUMBER_SQUARE_THREE = "PhNumberSquareThree"
    NUMBER_SQUARE_TWO = "PhNumberSquareTwo"
    NUMBER_SQUARE_ZERO = "PhNumberSquareZero"
    NUMBER_THREE = "PhNumberThree"
    NUMBER_TWO = "PhNumberTwo"
    NUMBER_ZERO = "PhNumberZero"
    NUMPAD = "PhNumpad"
    NUT = "PhNut"
    NY_TIMES_LOGO = "PhNyTimesLogo"
    OCTAGON = "PhOctagon"
    OFFICE_CHAIR = "PhOfficeChair"
    ONIGIRI = "PhOnigiri"
    OPEN_AI_LOGO = "PhOpenAiLogo"
    OPTION = "PhOption"
    ORANGE = "PhOrange"
    ORANGE_SLICE = "PhOrangeSlice"
    OVEN = "PhOven"
    PACKAGE = "PhPackage"
    PAINT_BRUSH = "PhPaintBrush"
    PAINT_BRUSH_BROAD = "PhPaintBrushBroad"
    PAINT_BRUSH_HOUSEHOLD = "PhPaintBrushHousehold"
    PAINT_BUCKET = "PhPaintBucket"
    PAINT_ROLLER = "PhPaintRoller"
    PALETTE = "PhPalette"
    PANORAMA = "PhPanorama"
    PANTS = "PhPants"
    PAPERCLIP = "PhPaperclip"
    PAPERCLIP_HORIZONTAL = "PhPaperclipHorizontal"
    PAPER_PLANE = "PhPaperPlane"
    PAPER_PLANE_RIGHT = "PhPaperPlaneRight"
    PAPER_PLANE_TILT = "PhPaperPlaneTilt"
    PARACHUTE = "PhParachute"
    PARAGRAPH = "PhParagraph"
    PARALLELOGRAM = "PhParallelogram"
    PARK = "PhPark"
    PASSWORD = "PhPassword"  # noqa: S105
    PATH = "PhPath"
    PATREON_LOGO = "PhPatreonLogo"
    PAUSE = "PhPause"
    PAUSE_CIRCLE = "PhPauseCircle"
    PAW_PRINT = "PhPawPrint"
    PAYPAL_LOGO = "PhPaypalLogo"
    PEACE = "PhPeace"
    PEN = "PhPen"
    PENCIL = "PhPencil"
    PENCIL_CIRCLE = "PhPencilCircle"
    PENCIL_LINE = "PhPencilLine"
    PENCIL_RULER = "PhPencilRuler"
    PENCIL_SIMPLE = "PhPencilSimple"
    PENCIL_SIMPLE_LINE = "PhPencilSimpleLine"
    PENCIL_SIMPLE_SLASH = "PhPencilSimpleSlash"
    PENCIL_SLASH = "PhPencilSlash"
    PENTAGON = "PhPentagon"
    PENTAGRAM = "PhPentagram"
    PEN_NIB = "PhPenNib"
    PEN_NIB_STRAIGHT = "PhPenNibStraight"
    PEPPER = "PhPepper"
    PERCENT = "PhPercent"
    PERSON = "PhPerson"
    PERSON_ARMS_SPREAD = "PhPersonArmsSpread"
    PERSON_SIMPLE = "PhPersonSimple"
    PERSON_SIMPLE_BIKE = "PhPersonSimpleBike"
    PERSON_SIMPLE_CIRCLE = "PhPersonSimpleCircle"
    PERSON_SIMPLE_HIKE = "PhPersonSimpleHike"
    PERSON_SIMPLE_RUN = "PhPersonSimpleRun"
    PERSON_SIMPLE_SKI = "PhPersonSimpleSki"
    PERSON_SIMPLE_SNOWBOARD = "PhPersonSimpleSnowboard"
    PERSON_SIMPLE_SWIM = "PhPersonSimpleSwim"
    PERSON_SIMPLE_TAI_CHI = "PhPersonSimpleTaiChi"
    PERSON_SIMPLE_THROW = "PhPersonSimpleThrow"
    PERSON_SIMPLE_WALK = "PhPersonSimpleWalk"
    PERSPECTIVE = "PhPerspective"
    PHONE = "PhPhone"
    PHONE_CALL = "PhPhoneCall"
    PHONE_DISCONNECT = "PhPhoneDisconnect"
    PHONE_INCOMING = "PhPhoneIncoming"
    PHONE_LIST = "PhPhoneList"
    PHONE_OUTGOING = "PhPhoneOutgoing"
    PHONE_PAUSE = "PhPhonePause"
    PHONE_PLUS = "PhPhonePlus"
    PHONE_SLASH = "PhPhoneSlash"
    PHONE_TRANSFER = "PhPhoneTransfer"
    PHONE_X = "PhPhoneX"
    PHOSPHOR_LOGO = "PhPhosphorLogo"
    PI = "PhPi"
    PIANO_KEYS = "PhPianoKeys"
    PICNIC_TABLE = "PhPicnicTable"
    PICTURE_IN_PICTURE = "PhPictureInPicture"
    PIGGY_BANK = "PhPiggyBank"
    PILL = "PhPill"
    PING_PONG = "PhPingPong"
    PINTEREST_LOGO = "PhPinterestLogo"
    PINT_GLASS = "PhPintGlass"
    PINWHEEL = "PhPinwheel"
    PIPE = "PhPipe"
    PIPE_WRENCH = "PhPipeWrench"
    PIX_LOGO = "PhPixLogo"
    PIZZA = "PhPizza"
    PLACEHOLDER = "PhPlaceholder"
    PLANET = "PhPlanet"
    PLANT = "PhPlant"
    PLAY = "PhPlay"
    PLAYLIST = "PhPlaylist"
    PLAY_CIRCLE = "PhPlayCircle"
    PLAY_PAUSE = "PhPlayPause"
    PLUG = "PhPlug"
    PLUGS = "PhPlugs"
    PLUGS_CONNECTED = "PhPlugsConnected"
    PLUG_CHARGING = "PhPlugCharging"
    PLUS = "PhPlus"
    PLUS_CIRCLE = "PhPlusCircle"
    PLUS_MINUS = "PhPlusMinus"
    PLUS_SQUARE = "PhPlusSquare"
    POKER_CHIP = "PhPokerChip"
    POLICE_CAR = "PhPoliceCar"
    POLYGON = "PhPolygon"
    POPCORN = "PhPopcorn"
    POPSICLE = "PhPopsicle"
    POTTED_PLANT = "PhPottedPlant"
    POWER = "PhPower"
    PRESCRIPTION = "PhPrescription"
    PRESENTATION = "PhPresentation"
    PRESENTATION_CHART = "PhPresentationChart"
    PRINTER = "PhPrinter"
    PROHIBIT = "PhProhibit"
    PROHIBIT_INSET = "PhProhibitInset"
    PROJECTOR_SCREEN = "PhProjectorScreen"
    PROJECTOR_SCREEN_CHART = "PhProjectorScreenChart"
    PULSE = "PhPulse"
    PUSH_PIN = "PhPushPin"
    PUSH_PIN_SIMPLE = "PhPushPinSimple"
    PUSH_PIN_SIMPLE_SLASH = "PhPushPinSimpleSlash"
    PUSH_PIN_SLASH = "PhPushPinSlash"
    PUZZLE_PIECE = "PhPuzzlePiece"
    QR_CODE = "PhQrCode"
    QUESTION = "PhQuestion"
    QUESTION_MARK = "PhQuestionMark"
    QUEUE = "PhQueue"
    QUOTES = "PhQuotes"
    RABBIT = "PhRabbit"
    RACQUET = "PhRacquet"
    RADICAL = "PhRadical"
    RADIO = "PhRadio"
    RADIOACTIVE = "PhRadioactive"
    RADIO_BUTTON = "PhRadioButton"
    RAINBOW = "PhRainbow"
    RAINBOW_CLOUD = "PhRainbowCloud"
    RANKING = "PhRanking"
    READ_CV_LOGO = "PhReadCvLogo"
    RECEIPT = "PhReceipt"
    RECEIPT_X = "PhReceiptX"
    RECORD = "PhRecord"
    RECTANGLE = "PhRectangle"
    RECTANGLE_DASHED = "PhRectangleDashed"
    RECYCLE = "PhRecycle"
    REDDIT_LOGO = "PhRedditLogo"
    REPEAT = "PhRepeat"
    REPEAT_ONCE = "PhRepeatOnce"
    REPLIT_LOGO = "PhReplitLogo"
    RESIZE = "PhResize"
    REWIND = "PhRewind"
    REWIND_CIRCLE = "PhRewindCircle"
    ROAD_HORIZON = "PhRoadHorizon"
    ROBOT = "PhRobot"
    ROCKET = "PhRocket"
    ROCKET_LAUNCH = "PhRocketLaunch"
    ROWS = "PhRows"
    ROWS_PLUS_BOTTOM = "PhRowsPlusBottom"
    ROWS_PLUS_TOP = "PhRowsPlusTop"
    RSS = "PhRss"
    RSS_SIMPLE = "PhRssSimple"
    RUG = "PhRug"
    RULER = "PhRuler"
    SAILBOAT = "PhSailboat"
    SCALES = "PhScales"
    SCAN = "PhScan"
    SCAN_SMILEY = "PhScanSmiley"
    SCISSORS = "PhScissors"
    SCOOTER = "PhScooter"
    SCREENCAST = "PhScreencast"
    SCREWDRIVER = "PhScrewdriver"
    SCRIBBLE = "PhScribble"
    SCRIBBLE_LOOP = "PhScribbleLoop"
    SCROLL = "PhScroll"
    SEAL = "PhSeal"
    SEAL_CHECK = "PhSealCheck"
    SEAL_PERCENT = "PhSealPercent"
    SEAL_QUESTION = "PhSealQuestion"
    SEAL_WARNING = "PhSealWarning"
    SEAT = "PhSeat"
    SEATBELT = "PhSeatbelt"
    SECURITY_CAMERA = "PhSecurityCamera"
    SELECTION = "PhSelection"
    SELECTION_ALL = "PhSelectionAll"
    SELECTION_BACKGROUND = "PhSelectionBackground"
    SELECTION_FOREGROUND = "PhSelectionForeground"
    SELECTION_INVERSE = "PhSelectionInverse"
    SELECTION_PLUS = "PhSelectionPlus"
    SELECTION_SLASH = "PhSelectionSlash"
    SHAPES = "PhShapes"
    SHARE = "PhShare"
    SHARE_FAT = "PhShareFat"
    SHARE_NETWORK = "PhShareNetwork"
    SHIELD = "PhShield"
    SHIELD_CHECK = "PhShieldCheck"
    SHIELD_CHECKERED = "PhShieldCheckered"
    SHIELD_CHEVRON = "PhShieldChevron"
    SHIELD_PLUS = "PhShieldPlus"
    SHIELD_SLASH = "PhShieldSlash"
    SHIELD_STAR = "PhShieldStar"
    SHIELD_WARNING = "PhShieldWarning"
    SHIPPING_CONTAINER = "PhShippingContainer"
    SHIRT_FOLDED = "PhShirtFolded"
    SHOOTING_STAR = "PhShootingStar"
    SHOPPING_BAG = "PhShoppingBag"
    SHOPPING_BAG_OPEN = "PhShoppingBagOpen"
    SHOPPING_CART = "PhShoppingCart"
    SHOPPING_CART_SIMPLE = "PhShoppingCartSimple"
    SHOVEL = "PhShovel"
    SHOWER = "PhShower"
    SHRIMP = "PhShrimp"
    SHUFFLE = "PhShuffle"
    SHUFFLE_ANGULAR = "PhShuffleAngular"
    SHUFFLE_SIMPLE = "PhShuffleSimple"
    SIDEBAR = "PhSidebar"
    SIDEBAR_SIMPLE = "PhSidebarSimple"
    SIGMA = "PhSigma"
    SIGNATURE = "PhSignature"
    SIGNPOST = "PhSignpost"
    SIGN_IN = "PhSignIn"
    SIGN_OUT = "PhSignOut"
    SIM_CARD = "PhSimCard"
    SIREN = "PhSiren"
    SKETCH_LOGO = "PhSketchLogo"
    SKIP_BACK = "PhSkipBack"
    SKIP_BACK_CIRCLE = "PhSkipBackCircle"
    SKIP_FORWARD = "PhSkipForward"
    SKIP_FORWARD_CIRCLE = "PhSkipForwardCircle"
    SKULL = "PhSkull"
    SKYPE_LOGO = "PhSkypeLogo"
    SLACK_LOGO = "PhSlackLogo"
    SLIDERS = "PhSliders"
    SLIDERS_HORIZONTAL = "PhSlidersHorizontal"
    SLIDESHOW = "PhSlideshow"
    SMILEY = "PhSmiley"
    SMILEY_ANGRY = "PhSmileyAngry"
    SMILEY_BLANK = "PhSmileyBlank"
    SMILEY_MEH = "PhSmileyMeh"
    SMILEY_MELTING = "PhSmileyMelting"
    SMILEY_NERVOUS = "PhSmileyNervous"
    SMILEY_SAD = "PhSmileySad"
    SMILEY_STICKER = "PhSmileySticker"
    SMILEY_WINK = "PhSmileyWink"
    SMILEY_X_EYES = "PhSmileyXEyes"
    SNAPCHAT_LOGO = "PhSnapchatLogo"
    SNEAKER = "PhSneaker"
    SNEAKER_MOVE = "PhSneakerMove"
    SNOWFLAKE = "PhSnowflake"
    SOCCER_BALL = "PhSoccerBall"
    SOCK = "PhSock"
    SOLAR_PANEL = "PhSolarPanel"
    SOLAR_ROOF = "PhSolarRoof"
    SORT_ASCENDING = "PhSortAscending"
    SORT_DESCENDING = "PhSortDescending"
    SOUNDCLOUD_LOGO = "PhSoundcloudLogo"
    SPADE = "PhSpade"
    SPARKLE = "PhSparkle"
    SPEAKER_HIFI = "PhSpeakerHifi"
    SPEAKER_HIGH = "PhSpeakerHigh"
    SPEAKER_LOW = "PhSpeakerLow"
    SPEAKER_NONE = "PhSpeakerNone"
    SPEAKER_SIMPLE_HIGH = "PhSpeakerSimpleHigh"
    SPEAKER_SIMPLE_LOW = "PhSpeakerSimpleLow"
    SPEAKER_SIMPLE_NONE = "PhSpeakerSimpleNone"
    SPEAKER_SIMPLE_SLASH = "PhSpeakerSimpleSlash"
    SPEAKER_SIMPLE_X = "PhSpeakerSimpleX"
    SPEAKER_SLASH = "PhSpeakerSlash"
    SPEAKER_X = "PhSpeakerX"
    SPEEDOMETER = "PhSpeedometer"
    SPHERE = "PhSphere"
    SPINNER = "PhSpinner"
    SPINNER_BALL = "PhSpinnerBall"
    SPINNER_GAP = "PhSpinnerGap"
    SPIRAL = "PhSpiral"
    SPLIT_HORIZONTAL = "PhSplitHorizontal"
    SPLIT_VERTICAL = "PhSplitVertical"
    SPOTIFY_LOGO = "PhSpotifyLogo"
    SPRAY_BOTTLE = "PhSprayBottle"
    SQUARE = "PhSquare"
    SQUARES_FOUR = "PhSquaresFour"
    SQUARE_HALF = "PhSquareHalf"
    SQUARE_HALF_BOTTOM = "PhSquareHalfBottom"
    SQUARE_LOGO = "PhSquareLogo"
    SQUARE_SPLIT_HORIZONTAL = "PhSquareSplitHorizontal"
    SQUARE_SPLIT_VERTICAL = "PhSquareSplitVertical"
    STACK = "PhStack"
    STACK_MINUS = "PhStackMinus"
    STACK_OVERFLOW_LOGO = "PhStackOverflowLogo"
    STACK_PLUS = "PhStackPlus"
    STACK_SIMPLE = "PhStackSimple"
    STAIRS = "PhStairs"
    STAMP = "PhStamp"
    STANDARD_DEFINITION = "PhStandardDefinition"
    STAR = "PhStar"
    STAR_AND_CRESCENT = "PhStarAndCrescent"
    STAR_FOUR = "PhStarFour"
    STAR_HALF = "PhStarHalf"
    STAR_OF_DAVID = "PhStarOfDavid"
    STEAM_LOGO = "PhSteamLogo"
    STEERING_WHEEL = "PhSteeringWheel"
    STEPS = "PhSteps"
    STETHOSCOPE = "PhStethoscope"
    STICKER = "PhSticker"
    STOOL = "PhStool"
    STOP = "PhStop"
    STOP_CIRCLE = "PhStopCircle"
    STOREFRONT = "PhStorefront"
    STRATEGY = "PhStrategy"
    STRIPE_LOGO = "PhStripeLogo"
    STUDENT = "PhStudent"
    SUBSET_OF = "PhSubsetOf"
    SUBSET_PROPER_OF = "PhSubsetProperOf"
    SUBTITLES = "PhSubtitles"
    SUBTITLES_SLASH = "PhSubtitlesSlash"
    SUBTRACT = "PhSubtract"
    SUBTRACT_SQUARE = "PhSubtractSquare"
    SUBWAY = "PhSubway"
    SUITCASE = "PhSuitcase"
    SUITCASE_ROLLING = "PhSuitcaseRolling"
    SUITCASE_SIMPLE = "PhSuitcaseSimple"
    SUN = "PhSun"
    SUNGLASSES = "PhSunglasses"
    SUN_DIM = "PhSunDim"
    SUN_HORIZON = "PhSunHorizon"
    SUPERSET_OF = "PhSupersetOf"
    SUPERSET_PROPER_OF = "PhSupersetProperOf"
    SWAP = "PhSwap"
    SWATCHES = "PhSwatches"
    SWIMMING_POOL = "PhSwimmingPool"
    SWORD = "PhSword"
    SYNAGOGUE = "PhSynagogue"
    SYRINGE = "PhSyringe"
    TABLE = "PhTable"
    TABS = "PhTabs"
    TAG = "PhTag"
    TAG_CHEVRON = "PhTagChevron"
    TAG_SIMPLE = "PhTagSimple"
    TARGET = "PhTarget"
    TAXI = "PhTaxi"
    TEA_BAG = "PhTeaBag"
    TELEGRAM_LOGO = "PhTelegramLogo"
    TELEVISION = "PhTelevision"
    TELEVISION_SIMPLE = "PhTelevisionSimple"
    TENNIS_BALL = "PhTennisBall"
    TENT = "PhTent"
    TERMINAL = "PhTerminal"
    TERMINAL_WINDOW = "PhTerminalWindow"
    TEST_TUBE = "PhTestTube"
    TEXTBOX = "PhTextbox"
    TEXT_AA = "PhTextAa"
    TEXT_ALIGN_CENTER = "PhTextAlignCenter"
    TEXT_ALIGN_JUSTIFY = "PhTextAlignJustify"
    TEXT_ALIGN_LEFT = "PhTextAlignLeft"
    TEXT_ALIGN_RIGHT = "PhTextAlignRight"
    TEXT_A_UNDERLINE = "PhTextAUnderline"
    TEXT_B = "PhTextB"
    TEXT_COLUMNS = "PhTextColumns"
    TEXT_H = "PhTextH"
    TEXT_H_FIVE = "PhTextHFive"
    TEXT_H_FOUR = "PhTextHFour"
    TEXT_H_ONE = "PhTextHOne"
    TEXT_H_SIX = "PhTextHSix"
    TEXT_H_THREE = "PhTextHThree"
    TEXT_H_TWO = "PhTextHTwo"
    TEXT_INDENT = "PhTextIndent"
    TEXT_ITALIC = "PhTextItalic"
    TEXT_OUTDENT = "PhTextOutdent"
    TEXT_STRIKETHROUGH = "PhTextStrikethrough"
    TEXT_SUBSCRIPT = "PhTextSubscript"
    TEXT_SUPERSCRIPT = "PhTextSuperscript"
    TEXT_T = "PhTextT"
    TEXT_T_SLASH = "PhTextTSlash"
    TEXT_UNDERLINE = "PhTextUnderline"
    THERMOMETER = "PhThermometer"
    THERMOMETER_COLD = "PhThermometerCold"
    THERMOMETER_HOT = "PhThermometerHot"
    THERMOMETER_SIMPLE = "PhThermometerSimple"
    THREADS_LOGO = "PhThreadsLogo"
    THREE_D = "PhThreeD"
    THUMBS_DOWN = "PhThumbsDown"
    THUMBS_UP = "PhThumbsUp"
    TICKET = "PhTicket"
    TIDAL_LOGO = "PhTidalLogo"
    TIKTOK_LOGO = "PhTiktokLogo"
    TILDE = "PhTilde"
    TIMER = "PhTimer"
    TIPI = "PhTipi"
    TIP_JAR = "PhTipJar"
    TIRE = "PhTire"
    TOGGLE_LEFT = "PhToggleLeft"
    TOGGLE_RIGHT = "PhToggleRight"
    TOILET = "PhToilet"
    TOILET_PAPER = "PhToiletPaper"
    TOOLBOX = "PhToolbox"
    TOOTH = "PhTooth"
    TORNADO = "PhTornado"
    TOTE = "PhTote"
    TOTE_SIMPLE = "PhToteSimple"
    TOWEL = "PhTowel"
    TRACTOR = "PhTractor"
    TRADEMARK = "PhTrademark"
    TRADEMARK_REGISTERED = "PhTrademarkRegistered"
    TRAFFIC_CONE = "PhTrafficCone"
    TRAFFIC_SIGN = "PhTrafficSign"
    TRAFFIC_SIGNAL = "PhTrafficSignal"
    TRAIN = "PhTrain"
    TRAIN_REGIONAL = "PhTrainRegional"
    TRAIN_SIMPLE = "PhTrainSimple"
    TRAM = "PhTram"
    TRANSLATE = "PhTranslate"
    TRASH = "PhTrash"
    TRASH_SIMPLE = "PhTrashSimple"
    TRAY = "PhTray"
    TRAY_ARROW_DOWN = "PhTrayArrowDown"
    TRAY_ARROW_UP = "PhTrayArrowUp"
    TREASURE_CHEST = "PhTreasureChest"
    TREE = "PhTree"
    TREE_EVERGREEN = "PhTreeEvergreen"
    TREE_PALM = "PhTreePalm"
    TREE_STRUCTURE = "PhTreeStructure"
    TREE_VIEW = "PhTreeView"
    TREND_DOWN = "PhTrendDown"
    TREND_UP = "PhTrendUp"
    TRIANGLE = "PhTriangle"
    TRIANGLE_DASHED = "PhTriangleDashed"
    TROLLEY = "PhTrolley"
    TROLLEY_SUITCASE = "PhTrolleySuitcase"
    TROPHY = "PhTrophy"
    TRUCK = "PhTruck"
    TRUCK_TRAILER = "PhTruckTrailer"
    TUMBLR_LOGO = "PhTumblrLogo"
    TWITCH_LOGO = "PhTwitchLogo"
    TWITTER_LOGO = "PhTwitterLogo"
    T_SHIRT = "PhTShirt"
    UMBRELLA = "PhUmbrella"
    UMBRELLA_SIMPLE = "PhUmbrellaSimple"
    UNION = "PhUnion"
    UNITE = "PhUnite"
    UNITE_SQUARE = "PhUniteSquare"
    UPLOAD = "PhUpload"
    UPLOAD_SIMPLE = "PhUploadSimple"
    USB = "PhUsb"
    USER = "PhUser"
    USERS = "PhUsers"
    USERS_FOUR = "PhUsersFour"
    USERS_THREE = "PhUsersThree"
    USER_CHECK = "PhUserCheck"
    USER_CIRCLE = "PhUserCircle"
    USER_CIRCLE_CHECK = "PhUserCircleCheck"
    USER_CIRCLE_DASHED = "PhUserCircleDashed"
    USER_CIRCLE_GEAR = "PhUserCircleGear"
    USER_CIRCLE_MINUS = "PhUserCircleMinus"
    USER_CIRCLE_PLUS = "PhUserCirclePlus"
    USER_FOCUS = "PhUserFocus"
    USER_GEAR = "PhUserGear"
    USER_LIST = "PhUserList"
    USER_MINUS = "PhUserMinus"
    USER_PLUS = "PhUserPlus"
    USER_RECTANGLE = "PhUserRectangle"
    USER_SOUND = "PhUserSound"
    USER_SQUARE = "PhUserSquare"
    USER_SWITCH = "PhUserSwitch"
    VAN = "PhVan"
    VAULT = "PhVault"
    VECTOR_THREE = "PhVectorThree"
    VECTOR_TWO = "PhVectorTwo"
    VIBRATE = "PhVibrate"
    VIDEO = "PhVideo"
    VIDEO_CAMERA = "PhVideoCamera"
    VIDEO_CAMERA_SLASH = "PhVideoCameraSlash"
    VIDEO_CONFERENCE = "PhVideoConference"
    VIGNETTE = "PhVignette"
    VINYL_RECORD = "PhVinylRecord"
    VIRTUAL_REALITY = "PhVirtualReality"
    VIRUS = "PhVirus"
    VISOR = "PhVisor"
    VOICEMAIL = "PhVoicemail"
    VOLLEYBALL = "PhVolleyball"
    WALL = "PhWall"
    WALLET = "PhWallet"
    WAREHOUSE = "PhWarehouse"
    WARNING = "PhWarning"
    WARNING_CIRCLE = "PhWarningCircle"
    WARNING_DIAMOND = "PhWarningDiamond"
    WARNING_OCTAGON = "PhWarningOctagon"
    WASHING_MACHINE = "PhWashingMachine"
    WATCH = "PhWatch"
    WAVEFORM = "PhWaveform"
    WAVEFORM_SLASH = "PhWaveformSlash"
    WAVES = "PhWaves"
    WAVE_SAWTOOTH = "PhWaveSawtooth"
    WAVE_SINE = "PhWaveSine"
    WAVE_SQUARE = "PhWaveSquare"
    WAVE_TRIANGLE = "PhWaveTriangle"
    WEBCAM = "PhWebcam"
    WEBCAM_SLASH = "PhWebcamSlash"
    WEBHOOKS_LOGO = "PhWebhooksLogo"
    WECHAT_LOGO = "PhWechatLogo"
    WHATSAPP_LOGO = "PhWhatsappLogo"
    WHEELCHAIR = "PhWheelchair"
    WHEELCHAIR_MOTION = "PhWheelchairMotion"
    WIFI_HIGH = "PhWifiHigh"
    WIFI_LOW = "PhWifiLow"
    WIFI_MEDIUM = "PhWifiMedium"
    WIFI_NONE = "PhWifiNone"
    WIFI_SLASH = "PhWifiSlash"
    WIFI_X = "PhWifiX"
    WIND = "PhWind"
    WINDMILL = "PhWindmill"
    WINDOWS_LOGO = "PhWindowsLogo"
    WINE = "PhWine"
    WRENCH = "PhWrench"
    X = "PhX"
    X_CIRCLE = "PhXCircle"
    X_LOGO = "PhXLogo"
    X_SQUARE = "PhXSquare"
    YARN = "PhYarn"
    YIN_YANG = "PhYinYang"
    YOUTUBE_LOGO = "PhYoutubeLogo"


class AtlanTagColor(str, Enum):
    GREEN = "Green"
    YELLOW = "Yellow"
    RED = "Red"
    GRAY = "Gray"


class AtlanTypeCategory(str, Enum):
    ENUM = "ENUM"
    STRUCT = "STRUCT"
    CLASSIFICATION = "CLASSIFICATION"
    ENTITY = "ENTITY"
    RELATIONSHIP = "RELATIONSHIP"
    CUSTOM_METADATA = "BUSINESS_METADATA"


class BadgeComparisonOperator(str, Enum):
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    EQ = "eq"
    NEQ = "neq"


class BadgeConditionColor(str, Enum):
    GREEN = "#047960"
    YELLOW = "#F7B43D"
    RED = "#BF1B1B"
    GREY = "#525C73"


class Cardinality(str, Enum):
    SINGLE = "SINGLE"
    LIST = "LIST"
    SET = "SET"


class DataAction(str, Enum):
    SELECT = "select"


class DataMaskingType(str, Enum):
    SHOW_FIRST_4 = "MASK_SHOW_FIRST_4"
    SHOW_LAST_4 = "MASK_SHOW_LAST_4"
    HASH = "MASK_HASH"
    NULLIFY = "MASK_NULL"
    REDACT = "MASK_REDACT"


class EntityStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"


class IndexType(str, Enum):
    DEFAULT = "DEFAULT"
    STRING = "STRING"


class KeycloakEventType(str, Enum):
    LOGIN = "LOGIN"
    LOGIN_ERROR = "LOGIN_ERROR"
    REGISTER = "REGISTER"
    REGISTER_ERROR = "REGISTER_ERROR"
    LOGOUT = "LOGOUT"
    LOGOUT_ERROR = "LOGOUT_ERROR"
    CODE_TO_TOKEN = "CODE_TO_TOKEN"  # noqa: S105
    CODE_TO_TOKEN_ERROR = "CODE_TO_TOKEN_ERROR"  # noqa: S105
    CLIENT_LOGIN = "CLIENT_LOGIN"
    CLIENT_LOGIN_ERROR = "CLIENT_LOGIN_ERROR"
    REFRESH_TOKEN = "REFRESH_TOKEN"  # noqa: S105
    REFRESH_TOKEN_ERROR = "REFRESH_TOKEN_ERROR"  # noqa: S105
    VALIDATE_ACCESS_TOKEN = "VALIDATE_ACCESS_TOKEN"  # noqa: S105
    VALIDATE_ACCESS_TOKEN_ERROR = "VALIDATE_ACCESS_TOKEN_ERROR"  # noqa: S105
    INTROSPECT_TOKEN = "INTROSPECT_TOKEN"  # noqa: S105
    INTROSPECT_TOKEN_ERROR = "INTROSPECT_TOKEN_ERROR"  # noqa: S105
    FEDERATED_IDENTITY_LINK = "FEDERATED_IDENTITY_LINK"
    FEDERATED_IDENTITY_LINK_ERROR = "FEDERATED_IDENTITY_LINK_ERROR"
    REMOVE_FEDERATED_IDENTITY = "REMOVE_FEDERATED_IDENTITY"
    REMOVE_FEDERATED_IDENTITY_ERROR = "REMOVE_FEDERATED_IDENTITY_ERROR"
    UPDATE_EMAIL = "UPDATE_EMAIL"
    UPDATE_EMAIL_ERROR = "UPDATE_EMAIL_ERROR"
    UPDATE_PROFILE = "UPDATE_PROFILE"
    UPDATE_PROFILE_ERROR = "UPDATE_PROFILE_ERROR"
    UPDATE_PASSWORD = "UPDATE_PASSWORD"  # noqa: S105
    UPDATE_PASSWORD_ERROR = "UPDATE_PASSWORD_ERROR"  # noqa: S105
    UPDATE_TOTP = "UPDATE_TOTP"
    UPDATE_TOTP_ERROR = "UPDATE_TOTP_ERROR"
    VERIFY_EMAIL = "VERIFY_EMAIL"
    VERIFY_EMAIL_ERROR = "VERIFY_EMAIL_ERROR"
    VERIFY_PROFILE = "VERIFY_PROFILE"
    VERIFY_PROFILE_ERROR = "VERIFY_PROFILE_ERROR"
    REMOVE_TOTP = "REMOVE_TOTP"
    REMOVE_TOTP_ERROR = "REMOVE_TOTP_ERROR"
    GRANT_CONSENT = "GRANT_CONSENT"
    GRANT_CONSENT_ERROR = "GRANT_CONSENT_ERROR"
    UPDATE_CONSENT = "UPDATE_CONSENT"
    UPDATE_CONSENT_ERROR = "UPDATE_CONSENT_ERROR"
    REVOKE_GRANT = "REVOKE_GRANT"
    REVOKE_GRANT_ERROR = "REVOKE_GRANT_ERROR"
    SEND_VERIFY_EMAIL = "SEND_VERIFY_EMAIL"
    SEND_VERIFY_EMAIL_ERROR = "SEND_VERIFY_EMAIL_ERROR"
    SEND_RESET_PASSWORD = "SEND_RESET_PASSWORD"  # noqa: S105
    SEND_RESET_PASSWORD_ERROR = "SEND_RESET_PASSWORD_ERROR"  # noqa: S105
    SEND_IDENTITY_PROVIDER_LINK = "SEND_IDENTITY_PROVIDER_LINK"
    SEND_IDENTITY_PROVIDER_LINK_ERROR = "SEND_IDENTITY_PROVIDER_LINK_ERROR"
    RESET_PASSWORD = "RESET_PASSWORD"  # noqa: S105
    RESET_PASSWORD_ERROR = "RESET_PASSWORD_ERROR"  # noqa: S105
    RESTART_AUTHENTICATION = "RESTART_AUTHENTICATION"
    RESTART_AUTHENTICATION_ERROR = "RESTART_AUTHENTICATION_ERROR"
    INVALID_SIGNATURE = "INVALID_SIGNATURE"
    INVALID_SIGNATURE_ERROR = "INVALID_SIGNATURE_ERROR"
    REGISTER_NODE = "REGISTER_NODE"
    REGISTER_NODE_ERROR = "REGISTER_NODE_ERROR"
    UNREGISTER_NODE = "UNREGISTER_NODE"
    UNREGISTER_NODE_ERROR = "UNREGISTER_NODE_ERROR"
    USER_INFO_REQUEST = "USER_INFO_REQUEST"
    USER_INFO_REQUEST_ERROR = "USER_INFO_REQUEST_ERROR"
    IDENTITY_PROVIDER_LINK_ACCOUNT = "IDENTITY_PROVIDER_LINK_ACCOUNT"
    IDENTITY_PROVIDER_LINK_ACCOUNT_ERROR = "IDENTITY_PROVIDER_LINK_ACCOUNT_ERROR"
    IDENTITY_PROVIDER_LOGIN = "IDENTITY_PROVIDER_LOGIN"
    IDENTITY_PROVIDER_LOGIN_ERROR = "IDENTITY_PROVIDER_LOGIN_ERROR"
    IDENTITY_PROVIDER_FIRST_LOGIN = "IDENTITY_PROVIDER_FIRST_LOGIN"
    IDENTITY_PROVIDER_FIRST_LOGIN_ERROR = "IDENTITY_PROVIDER_FIRST_LOGIN_ERROR"
    IDENTITY_PROVIDER_POST_LOGIN = "IDENTITY_PROVIDER_POST_LOGIN"
    IDENTITY_PROVIDER_POST_LOGIN_ERROR = "IDENTITY_PROVIDER_POST_LOGIN_ERROR"
    IDENTITY_PROVIDER_RESPONSE = "IDENTITY_PROVIDER_RESPONSE"
    IDENTITY_PROVIDER_RESPONSE_ERROR = "IDENTITY_PROVIDER_RESPONSE_ERROR"
    IDENTITY_PROVIDER_RETRIEVE_TOKEN = "IDENTITY_PROVIDER_RETRIEVE_TOKEN"  # noqa: S105
    IDENTITY_PROVIDER_RETRIEVE_TOKEN_ERROR = "IDENTITY_PROVIDER_RETRIEVE_TOKEN_ERROR"  # noqa: S105
    IMPERSONATE = "IMPERSONATE"
    IMPERSONATE_ERROR = "IMPERSONATE_ERROR"
    CUSTOM_REQUIRED_ACTION = "CUSTOM_REQUIRED_ACTION"
    CUSTOM_REQUIRED_ACTION_ERROR = "CUSTOM_REQUIRED_ACTION_ERROR"
    EXECUTE_ACTIONS = "EXECUTE_ACTIONS"
    EXECUTE_ACTIONS_ERROR = "EXECUTE_ACTIONS_ERROR"
    EXECUTE_ACTION_TOKEN = "EXECUTE_ACTION_TOKEN"  # noqa: S105
    EXECUTE_ACTION_TOKEN_ERROR = "EXECUTE_ACTION_TOKEN_ERROR"  # noqa: S105
    CLIENT_INFO = "CLIENT_INFO"
    CLIENT_INFO_ERROR = "CLIENT_INFO_ERROR"
    CLIENT_REGISTER = "CLIENT_REGISTER"
    CLIENT_REGISTER_ERROR = "CLIENT_REGISTER_ERROR"
    CLIENT_UPDATE = "CLIENT_UPDATE"
    CLIENT_UPDATE_ERROR = "CLIENT_UPDATE_ERROR"
    CLIENT_DELETE = "CLIENT_DELETE"
    CLIENT_DELETE_ERROR = "CLIENT_DELETE_ERROR"
    CLIENT_INITIATED_ACCOUNT_LINKING = "CLIENT_INITIATED_ACCOUNT_LINKING"
    CLIENT_INITIATED_ACCOUNT_LINKING_ERROR = "CLIENT_INITIATED_ACCOUNT_LINKING_ERROR"
    TOKEN_EXCHANGE = "TOKEN_EXCHANGE"  # noqa: S105
    TOKEN_EXCHANGE_ERROR = "TOKEN_EXCHANGE_ERROR"  # noqa: S105
    OAUTH2_DEVICE_AUTH = "OAUTH2_DEVICE_AUTH"
    OAUTH2_DEVICE_AUTH_ERROR = "OAUTH2_DEVICE_AUTH_ERROR"
    OAUTH2_DEVICE_VERIFY_USER_CODE = "OAUTH2_DEVICE_VERIFY_USER_CODE"
    OAUTH2_DEVICE_VERIFY_USER_CODE_ERROR = "OAUTH2_DEVICE_VERIFY_USER_CODE_ERROR"
    OAUTH2_DEVICE_CODE_TO_TOKEN = "OAUTH2_DEVICE_CODE_TO_TOKEN"  # noqa: S105
    OAUTH2_DEVICE_CODE_TO_TOKEN_ERROR = "OAUTH2_DEVICE_CODE_TO_TOKEN_ERROR"  # noqa: S105
    AUTHREQID_TO_TOKEN = "AUTHREQID_TO_TOKEN"  # noqa: S105
    AUTHREQID_TO_TOKEN_ERROR = "AUTHREQID_TO_TOKEN_ERROR"  # noqa: S105
    PERMISSION_TOKEN = "PERMISSION_TOKEN"  # noqa: S105
    PERMISSION_TOKEN_ERROR = "PERMISSION_TOKEN_ERROR"  # noqa: S105
    DELETE_ACCOUNT = "DELETE_ACCOUNT"
    DELETE_ACCOUNT_ERROR = "DELETE_ACCOUNT_ERROR"
    PUSHED_AUTHORIZATION_REQUEST = "PUSHED_AUTHORIZATION_REQUEST"
    PUSHED_AUTHORIZATION_REQUEST_ERROR = "PUSHED_AUTHORIZATION_REQUEST_ERROR"


class LineageDirection(str, Enum):
    UPSTREAM = "INPUT"
    DOWNSTREAM = "OUTPUT"
    BOTH = "BOTH"


class PersonaGlossaryAction(str, Enum):
    CREATE = "persona-glossary-create"
    READ = "persona-glossary-read"
    UPDATE = "persona-glossary-update"
    DELETE = "persona-glossary-delete"
    UPDATE_CUSTOM_METADATA = "persona-glossary-update-custom-metadata"
    ADD_ATLAN_TAG = "persona-glossary-add-classifications"
    UPDATE_ATLAN_TAG = "persona-glossary-update-classifications"
    REMOVE_ATLAN_TAG = "persona-glossary-delete-classifications"


class PersonaMetadataAction(str, Enum):
    CREATE = "persona-api-create"
    READ = "persona-asset-read"
    UPDATE = "persona-asset-update"
    DELETE = "persona-api-delete"
    UPDATE_CUSTOM_METADATA = "persona-business-update-metadata"
    ADD_ATLAN_TAG = "persona-entity-add-classification"
    UPDATE_ATLAN_TAG = "persona-entity-update-classification"
    REMOVE_ATLAN_TAG = "persona-entity-remove-classification"
    ATTACH_TERMS = "persona-add-terms"
    DETACH_TERMS = "persona-remove-terms"


class PersonaDomainAction(str, Enum):
    CREATE_DOMAIN = "persona-domain-create"
    READ_DOMAIN = "persona-domain-read"
    UPDATE_DOMAIN = "persona-domain-update"
    DELETE_DOMAIN = "persona-domain-delete"
    CREATE_SUBDOMAIN = "persona-domain-sub-domain-create"
    READ_SUBDOMAIN = "persona-domain-sub-domain-read"
    UPDATE_SUBDOMAIN = "persona-domain-sub-domain-update"
    DELETE_SUBDOMAIN = "persona-domain-sub-domain-delete"
    CREATE_PRODUCTS = "persona-domain-product-create"
    READ_PRODUCTS = "persona-domain-product-read"
    UPDATE_PRODUCTS = "persona-domain-product-update"
    DELETE_PRODUCTS = "persona-domain-product-delete"
    UPDATE_DOMAIN_CUSTOM_METADATA = "persona-domain-business-update-metadata"
    UPDATE_SUBDOMAIN_CUSTOM_METADATA = (
        "persona-domain-sub-domain-business-update-metadata"
    )
    UPDATE_PRODUCT_CUSTOM_METADATA = "persona-domain-product-business-update-metadata"


class PurposeMetadataAction(str, Enum):
    CREATE = "entity-create"
    READ = "entity-read"
    UPDATE = "entity-update"
    DELETE = "entity-delete"
    UPDATE_CUSTOM_METADATA = "entity-update-business-metadata"
    ADD_ATLAN_TAG = "entity-add-classification"
    READ_ATLAN_TAG = "entity-read-classification"
    UPDATE_ATLAN_TAG = "entity-update-classification"
    REMOVE_ATLAN_TAG = "entity-remove-classification"
    ATTACH_TERMS = "purpose-add-terms"
    DETACH_TERMS = "purpose-remove-terms"


class QueryParserSourceType(str, Enum):
    ANSI = "ansi"
    BIGQUERY = "bigquery"
    HANA = "hana"
    HIVE = "hive"
    MSSQL = "mssql"
    MYSQL = "mysql"
    ORACLE = "oracle"
    POSTGRESQL = "postgresql"
    REDSHIFT = "redshift"
    SNOWFLAKE = "snowflake"
    SPARKSQL = "sparksql"
    ATHENA = "athena"


class SortOrder(str, Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"


class TagIconType(str, Enum):
    IMAGE = "image"
    ICON = "icon"
    EMOJI = "emoji"
    NONE = ""


class TypeName(str, Enum):
    STRING = "string"
    ARRAY_STRING = "array<string>"


class AtlanWorkflowPhase(str, Enum):
    SUCCESS = "Succeeded"
    RUNNING = "Running"
    FAILED = "Failed"
    ERROR = "Error"
    PENDING = "Pending"


class ChildScoreMode(str, Enum):
    NONE = "none"
    AVG = "avg"
    SUM = "sum"
    MAX = "max"
    MIN = "min"


class WorkflowPackage(str, Enum):
    AIRFLOW = "atlan-airflow"
    ATHENA = "atlan-athena"
    AWS_LAMBDA_TRIGGER = "atlan-aws-lambda-trigger"
    AZURE_EVENT_HUB = "atlan-azure-event-hub"
    BIGQUERY = "atlan-bigquery"
    BIGQUERY_MINER = "atlan-bigquery-miner"
    CONNECTION_DELETE = "atlan-connection-delete"
    DATABRICKS = "atlan-databricks"
    DATABRICKS_LINEAGE = "atlan-databricks-lineage"
    DYNAMODB = "atlan-dynamodb"
    DBT = "atlan-dbt"
    FIVETRAN = "atlan-fivetran"
    GLUE = "atlan-glue"
    HIVE = "atlan-hive"
    HIVE_MINER = "atlan-hive-miner"
    KAFKA = "atlan-kafka"
    KAFKA_AIVEN = "atlan-kafka-aiven"
    KAFKA_CONFLUENT_CLOUD = "atlan-kafka-confluent-cloud"
    KAFKA_REDPANDA = "atlan-kafka-redpanda"
    LOOKER = "atlan-looker"
    MATILLION = "atlan-matillion"
    METABASE = "atlan-metabase"
    MICROSTRATEGY = "atlan-microstrategy"
    MODE = "atlan-mode"
    MONTE_CARLO = "atlan-monte-carlo"
    MSSQL = "atlan-mssql"
    MSSQL_MINER = "atlan-mssql-miner"
    MYSQL = "atlan-mysql"
    ORACLE = "atlan-oracle"
    POSTGRES = "atlan-postgres"
    POWERBI = "atlan-powerbi"
    POWERBI_MINER = "atlan-powerbi-miner"
    PRESTO = "atlan-presto"
    QLIK_SENSE = "atlan-qlik-sense"
    QLIK_SENSE_ENTERPRISE_WINDOWS = "atlan-qlik-sense-enterprise-windows"
    QUICKSIGHT = "atlan-quicksight"
    REDASH = "atlan-redash"
    REDSHIFT = "atlan-redshift"
    REDSHIFT_MINER = "atlan-redshift-miner"
    SALESFORCE = "atlan-salesforce"
    DATAVERSE = "atlan-dataverse"
    SAP_HANA = "atlan-sap-hana"
    SCHEMA_REGISTRY_CONFLUENT = "atlan-schema-registry-confluent"
    SIGMA = "atlan-sigma"
    SNOWFLAKE = "atlan-snowflake"
    SNOWFLAKE_MINER = "atlan-snowflake-miner"
    MONGODB = "atlan-mongodb"
    SODA = "atlan-soda"
    SYNAPSE = "atlan-synapse"
    TABLEAU = "atlan-tableau"
    TERADATA = "atlan-teradata"
    TERADATA_MINER = "atlan-teradata-miner"
    THOUGHTSPOT = "atlan-thoughtspot"
    TRINO = "atlan-trino"
    # CSA packages
    ASSET_IMPORT = "csa-asset-import"
    ASSET_EXPORT_BASIC = "csa-asset-export-basic"
    RELATIONAL_ASSETS_BUILDER = "csa-relational-assets-builder"
    LINEAGE_BUILDER = "csa-lineage-builder"
    LINEAGE_GENERATOR = "csa-lineage-generator"
    API_TOKEN_CONNECTION_ADMIN = "csa-api-token-connection-admin"  # noqa: S105


class AssetInputHandling(str, Enum):
    UPSERT = "upsert"
    PARTIAL = "partial"
    UPDATE = "update"


class AssetCreationHandling(str, Enum):
    FULL = "upsert"
    PARTIAL = "partial"
    NONE = "update"


class AssetDeltaHandling(str, Enum):
    FULL_REPLACEMENT = "full"
    INCREMENTAL = "delta"


class AssetRemovalType(str, Enum):
    ARCHIVE = "archive"
    PURGE = "purge"


class UTMTags(str, Enum):
    # PAGE_ entries indicate where the action was taken.
    # Search was made from the home page.
    PAGE_HOME = "page_home"
    # Search was made from the assets (discovery) page.
    PAGE_ASSETS = "page_assets"
    # Asset was viewed from within a glossary.
    PAGE_GLOSSARY = "page_glossary"
    # Asset was viewed from within insights.
    PAGE_INSIGHTS = "page_insights"

    # PROJECT_ entries indicate how (via what application) the action was taken.
    # Search was made via the webapp (UI).
    PROJECT_WEBAPP = "project_webapp"
    # Search was made via the Java SDK.
    PROJECT_SDK_JAVA = "project_sdk_java"
    # Search was made via the Python SDK.
    PROJECT_SDK_PYTHON = "project_sdk_python"

    # ACTION_ entries dictate the specific action that was taken.
    # Assets were searched.
    ACTION_SEARCHED = "action_searched"
    # Search was run through the Cmd-K popup.
    ACTION_CMD_K = "action_cmd_k"
    # Search was through changing a filter in the UI (discovery).
    ACTION_FILTER_CHANGED = "action_filter_changed"
    # Search was through changing a type filter (pill) in the UI (discovery).
    ACTION_ASSET_TYPE_CHANGED = "action_asset_type_changed"
    # Asset was viewed, rather than an explicit search.
    ACTION_ASSET_VIEWED = "action_asset_viewed"

    # Others indicate any special mechanisms used for the action.
    # Search was run using the UI popup searchbar.
    UI_POPUP_SEARCHBAR = "ui_popup_searchbar"
    # Search was through a UI filter (discovery).
    UI_FILTERS = "ui_filters"
    # View was done via the UI's sidebar.
    UI_SIDEBAR = "ui_sidebar"
    # View was done of the full asset profile, not only sidebar.
    UI_PROFILE = "ui_profile"
    # Listing of assets, usually by a particular type, in the discovery page.
    UI_MAIN_LIST = "ui_main_list"


class HekaFlow(str, Enum):
    BYPASS = "BYPASS_FLOW"
    REWRITE = "REWRITE_FLOW"
    PASSTHROUGH = "PASSTHROUGH_FLOW"


class ParsingFlow(str, Enum):
    GUDUSOFT = "GUDUSOFT_FLOW"
    EXPLAIN_CALL = "EXPLAIN_CALL_FLOW"
    CALCITE = "CALCITE_FLOW"
    JSQL = "JSQL_FLOW"
    NONE = "NO_PARSING"


class QueryStatus(str, Enum):
    # Query run has been requested, but not yet started or completed.
    STARTED = "started"
    # Query run is in progress (running).
    IN_PROGRESS = "in-progress"
    # Query has completed running, successfully.
    COMPLETED = "completed"
    # Some other operation on the query has completed successfully.
    # For example: it has been aborted or was only testing a connection.
    OK = "ok"
    # There was an error running the query.
    ERROR = "error"


class SaveSemantic(Enum):
    REPLACE = "REPLACE"
    APPEND = "APPEND"
    REMOVE = "REMOVE"


class AtlanTaskStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    DELETED = "DELETED"


class AtlanTaskType(str, Enum):
    CLASSIFICATION_PROPAGATION_ADD = "CLASSIFICATION_PROPAGATION_ADD"
    CLASSIFICATION_PROPAGATION_DELETE = "CLASSIFICATION_PROPAGATION_DELETE"
    CLASSIFICATION_ONLY_PROPAGATION_DELETE = "CLASSIFICATION_ONLY_PROPAGATION_DELETE"
    CLASSIFICATION_ONLY_PROPAGATION_DELETE_ON_HARD_DELETE = (
        "CLASSIFICATION_ONLY_PROPAGATION_DELETE_ON_HARD_DELETE"
    )
    CLASSIFICATION_REFRESH_PROPAGATION = "CLASSIFICATION_REFRESH_PROPAGATION"
    CLASSIFICATION_PROPAGATION_RELATIONSHIP_UPDATE = (
        "CLASSIFICATION_PROPAGATION_RELATIONSHIP_UPDATE"
    )
    UPDATE_ENTITY_MEANINGS_ON_TERM_UPDATE = "UPDATE_ENTITY_MEANINGS_ON_TERM_UPDATE"
    UPDATE_ENTITY_MEANINGS_ON_TERM_SOFT_DELETE = (
        "UPDATE_ENTITY_MEANINGS_ON_TERM_SOFT_DELETE"
    )
    UPDATE_ENTITY_MEANINGS_ON_TERM_HARD_DELETE = (
        "UPDATE_ENTITY_MEANINGS_ON_TERM_HARD_DELETE"
    )


class AtlanMeshColor(str, Enum):
    INDIGO = "#3940E1"
    VIOLET = "#7F83EC"
    MAGENTA = "#F34D77"
    PINK = "#F78BA7"
    BLUE = "#0CD1FA"
    GREEN = "#00A680"
    YELLOW = "#FFB119"
    GRAY = "#525C73"


class DataContractStatus(Enum):
    DRAFT = "draft"
    VERIFIED = "verified"


class OpenLineageEventType(Enum):
    """
    Current transition of the run state.
    It is required to issue 1 START event
    and 1 of [COMPLETE, ABORT, FAIL ] event per run.
    """

    START = "START"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    ABORT = "ABORT"
    FAIL = "FAIL"
    OTHER = "OTHER"


# **************************************
# CODE BELOW IS GENERATED NOT MODIFY  **
# **************************************


class ADLSAccessTier(str, Enum):
    COOL = "Cool"
    HOT = "Hot"
    ARCHIVE = "Archive"


class ADLSAccountStatus(str, Enum):
    AVAILABLE = "Available"
    UNAVAILABLE = "Unavailable"


class ADLSEncryptionTypes(str, Enum):
    MICROSOFT_STORAGE = "Microsoft.Storage"
    MICROSOFT_KEYVAULT = "Microsoft.Keyvault"


class ADLSLeaseState(str, Enum):
    AVAILABLE = "Available"
    LEASED = "Leased"
    EXPIRED = "Expired"
    BREAKING = "Breaking"
    BROKEN = "Broken"


class ADLSLeaseStatus(str, Enum):
    LOCKED = "Locked"
    UNLOCKED = "Unlocked"


class ADLSObjectArchiveStatus(str, Enum):
    REHYDRATE_PENDING_TO_HOT = "rehydrate-pending-to-hot"
    REHYDRATE_PENDING_TO_COOL = "rehydrate-pending-to-cool"


class ADLSObjectType(str, Enum):
    BLOCK_BLOB = "BlockBlob"
    PAGE_BLOB = "PageBlob"
    APPEND_BLOB = "AppendBlob"


class ADLSPerformance(str, Enum):
    STANDARD = "Standard"
    PREMIUM = "Premium"


class ADLSProvisionState(str, Enum):
    CREATING = "Creating"
    RESOLVING_DNS = "ResolvingDNS"
    SUCCEEDED = "Succeeded"


class ADLSReplicationType(str, Enum):
    LRS = "LRS"
    ZRS = "ZRS"
    GRS = "GRS"
    GZRS = "GZRS"
    RA_GRS = "RA-GRS"


class ADLSStorageKind(str, Enum):
    BLOB_STORAGE = "BlobStorage"
    BLOCK_BLOB_STORAGE = "BlockBlobStorage"
    FILE_STORAGE = "FileStorage"
    STORAGE = "Storage"
    STORAGE_V2 = "StorageV2"


class AIApplicationDevelopmentStage(str, Enum):
    PROPOSAL = "PROPOSAL"
    DEVELOPMENT = "DEVELOPMENT"
    PRODUCTION = "PRODUCTION"
    ARCHIVED = "ARCHIVED"


class AIDatasetType(str, Enum):
    TRAINING = "TRAINING"
    TESTING = "TESTING"
    INFERENCE = "INFERENCE"
    VALIDATION = "VALIDATION"
    OUTPUT = "OUTPUT"


class AIModelStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class APIQueryParamTypeEnum(str, Enum):
    INPUT = "Input"
    OUTPUT = "Output"


class AdfActivityState(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class AtlasGlossaryCategoryType(str, Enum):
    DOCUMENT_FOLDER = "DOCUMENT_FOLDER"


class AtlasGlossaryTermAssignmentStatus(str, Enum):
    DISCOVERED = "DISCOVERED"
    PROPOSED = "PROPOSED"
    IMPORTED = "IMPORTED"
    VALIDATED = "VALIDATED"
    DEPRECATED = "DEPRECATED"
    OBSOLETE = "OBSOLETE"
    OTHER = "OTHER"


class AtlasGlossaryTermRelationshipStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    OBSOLETE = "OBSOLETE"
    OTHER = "OTHER"


class AtlasGlossaryTermType(str, Enum):
    DOCUMENT = "DOCUMENT"


class AtlasGlossaryType(str, Enum):
    KNOWLEDGE_HUB = "KNOWLEDGE_HUB"


class AtlasOperation(str, Enum):
    OTHERS = "OTHERS"
    PURGE = "PURGE"
    EXPORT = "EXPORT"
    IMPORT = "IMPORT"
    IMPORT_DELETE_REPL = "IMPORT_DELETE_REPL"
    TYPE_DEF_CREATE = "TYPE_DEF_CREATE"
    TYPE_DEF_UPDATE = "TYPE_DEF_UPDATE"
    TYPE_DEF_DELETE = "TYPE_DEF_DELETE"
    SERVER_START = "SERVER_START"
    SERVER_STATE_ACTIVE = "SERVER_STATE_ACTIVE"


class AuthPolicyCategory(str, Enum):
    BOOTSTRAP = "bootstrap"
    PERSONA = "persona"
    PURPOSE = "purpose"


class AuthPolicyResourceCategory(str, Enum):
    ENTITY = "ENTITY"
    RELATIONSHIP = "RELATIONSHIP"
    TAG = "TAG"
    CUSTOM = "CUSTOM"
    TYPEDEFS = "TYPEDEFS"
    ADMIN = "ADMIN"


class AuthPolicyType(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    ALLOW_EXCEPTIONS = "allowExceptions"
    DENY_EXCEPTIONS = "denyExceptions"
    DATA_MASK = "dataMask"
    ROW_FILTER = "rowFilter"


class CertificateStatus(str, Enum):
    DEPRECATED = "DEPRECATED"
    DRAFT = "DRAFT"
    VERIFIED = "VERIFIED"


class DataProductCriticality(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class DataProductLineageStatus(str, Enum):
    COMPLETED = "Completed"
    IN_PROGRESS = "InProgress"
    PENDING = "Pending"
    FAILED = "Failed"


class DataProductSensitivity(str, Enum):
    PUBLIC = "Public"
    INTERNAL = "Internal"
    CONFIDENTIAL = "Confidential"


class DataProductStatus(str, Enum):
    ACTIVE = "Active"
    SUNSET = "Sunset"
    ARCHIVED = "Archived"
    DRAFT = "Draft"


class DataProductVisibility(str, Enum):
    PRIVATE = "Private"
    PROTECTED = "Protected"
    PUBLIC = "Public"


class DocumentDBCollectionValidationAction(str, Enum):
    ERROR = "ERROR"
    WARN = "WARN"


class DocumentDBCollectionValidationLevel(str, Enum):
    OFF = "OFF"
    STRICT = "STRICT"
    MODERATE = "MODERATE"


class DomoCardType(str, Enum):
    DOC = "DOC"
    DOC_CARD = "DOC CARD"
    CHART = "CHART"
    DRILL_VIEW = "DRILL VIEW"
    NOTEBOOK = "NOTEBOOK"


class DynamoDBSecondaryIndexProjectionType(str, Enum):
    KEYS_ONLY = "KEYS_ONLY"
    INCLUDE = "INCLUDE"
    ALL = "ALL"


class DynamoDBStatus(str, Enum):
    CREATING = "CREATING"
    UPDATING = "UPDATING"
    DELETING = "DELETING"
    ACTIVE = "ACTIVE"
    INACCESSIBLE_ENCRYPTION_CREDENTIALS = "INACCESSIBLE_ENCRYPTION_CREDENTIALS"
    ARCHIVING = "ARCHIVING"
    ARCHIVED = "ARCHIVED"


class EthicalAIAccountabilityConfig(str, Enum):
    HAS_OWNER = "HAS_OWNER"
    SUBJECT_TO_HUMAN_OVERSIGHT = "SUBJECT_TO_HUMAN_OVERSIGHT"


class EthicalAIBiasMitigationConfig(str, Enum):
    INEFFECTIVE = "INEFFECTIVE"
    PARTIAL = "PARTIAL"
    EFFECTIVE = "EFFECTIVE"


class EthicalAIEnvironmentalConsciousnessConfig(str, Enum):
    LOW_RISK = "LOW_RISK"
    MEDIUM_RISK = "MEDIUM_RISK"
    HIGH_RISK = "HIGH_RISK"


class EthicalAIFairnessConfig(str, Enum):
    LOW_RISK = "LOW_RISK"
    MODERATE_RISK = "MODERATE_RISK"
    HIGH_RISK = "HIGH_RISK"


class EthicalAIPrivacyConfig(str, Enum):
    PERSONAL_DATA = "PERSONAL_DATA"
    NO_PERSONAL_DATA = "NO_PERSONAL_DATA"


class EthicalAIReliabilityAndSafetyConfig(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"


class EthicalAITransparencyConfig(str, Enum):
    LIMITED_DISCLOSURE = "LIMITED_DISCLOSURE"
    PARTIAL_DISCLOSURE = "PARTIAL_DISCLOSURE"
    FULL_DISCLOSURE = "FULL_DISCLOSURE"


class FileType(str, Enum):
    PDF = "pdf"
    DOC = "doc"
    XLS = "xls"
    PPT = "ppt"
    CSV = "csv"
    TXT = "txt"
    JSON = "json"
    XML = "xml"
    ZIP = "zip"
    YXDB = "yxdb"
    XLSM = "xlsm"
    HYPER = "hyper"


class FivetranConnectorStatus(str, Enum):
    SUCCESSFUL = "SUCCESSFUL"
    FAILURE = "FAILURE"
    FAILURE_WITH_TASK = "FAILURE_WITH_TASK"
    RESCHEDULED = "RESCHEDULED"
    NO_STATUS = "NO_STATUS"


class FormFieldDimension(str, Enum):
    SINGLE = "SINGLE"
    MULTI = "MULTI"


class FormFieldType(str, Enum):
    INT = "INT"
    STRING = "STRING"
    DATE = "DATE"
    BOOLEAN = "BOOLEAN"
    LONG = "LONG"
    JSON = "JSON"


class GoogleDatastudioAssetType(str, Enum):
    REPORT = "REPORT"
    DATA_SOURCE = "DATA_SOURCE"


class IconType(str, Enum):
    IMAGE = "image"
    EMOJI = "emoji"


class IncidentSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class KafkaTopicCleanupPolicy(str, Enum):
    COMPACT = "compact"
    DELETE = "delete"


class KafkaTopicCompressionType(str, Enum):
    UNCOMPRESSED = "uncompressed"
    ZSTD = "zstd"
    LZ4 = "lz4"
    SNAPPY = "snappy"
    GZIP = "gzip"
    PRODUCER = "producer"


class MatillionJobType(str, Enum):
    ORCHESTRATION = "ORCHESTRATION"
    TRANSFORMATION = "TRANSFORMATION"


class ModelCardinalityType(str, Enum):
    ONE_TO_ONE = "ONE-TO-ONE"
    ONE_TO_MANY = "ONE-TO-MANY"
    MANY_TO_ONE = "MANY-TO-ONE"
    MANY_TO_MANY = "MANY-TO-MANY"


class MongoDBCollectionValidationAction(str, Enum):
    ERROR = "ERROR"
    WARN = "WARN"


class MongoDBCollectionValidationLevel(str, Enum):
    OFF = "OFF"
    STRICT = "STRICT"
    MODERATE = "MODERATE"


class OpenLineageRunState(str, Enum):
    START = "START"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    ABORT = "ABORT"
    FAIL = "FAIL"
    OTHER = "OTHER"


class PowerbiEndorsement(str, Enum):
    PROMOTED = "Promoted"
    CERTIFIED = "Certified"


class QueryUsernameStrategy(str, Enum):
    CONNECTION_USERNAME = "connectionUsername"
    ATLAN_USERNAME = "atlanUsername"


class QuickSightAnalysisStatus(str, Enum):
    CREATION_IN_PROGRESS = "CREATION_IN_PROGRESS"
    CREATION_SUCCESSFUL = "CREATION_SUCCESSFUL"
    CREATION_FAILED = "CREATION_FAILED"
    UPDATE_IN_PROGRESS = "UPDATE_IN_PROGRESS"
    UPDATE_SUCCESSFUL = "UPDATE_SUCCESSFUL"
    UPDATE_FAILED = "UPDATE_FAILED"
    DELETED = "DELETED"


class QuickSightDatasetFieldType(str, Enum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    DATETIME = "DATETIME"


class QuickSightDatasetImportMode(str, Enum):
    SPICE = "SPICE"
    DIRECT_QUERY = "DIRECT_QUERY"


class QuickSightFolderType(str, Enum):
    SHARED = "SHARED"


class SchemaRegistrySchemaCompatibility(str, Enum):
    BACKWARD = "BACKWARD"
    BACKWARD_TRANSITIVE = "BACKWARD_TRANSITIVE"
    FORWARD = "FORWARD"
    FORWARD_TRANSITIVE = "FORWARD_TRANSITIVE"
    FULL = "FULL"
    FULL_TRANSITIVE = "FULL_TRANSITIVE"
    NONE = "NONE"


class SchemaRegistrySchemaType(str, Enum):
    AVRO = "AVRO"
    JSON = "JSON"
    PROTOBUF = "PROTOBUF"


class SourceCostUnitType(str, Enum):
    CREDITS = "Credits"
    BYTES = "bytes"
    SLOT_MS = "slot-ms"


class TableType(str, Enum):
    TEMPORARY = "TEMPORARY"
    ICEBERG = "ICEBERG"
    KUDU = "KUDU"


class WorkflowRunStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    WITHDRAWN = "WITHDRAWN"
    EXPIRED = "EXPIRED"
    TERMINATED = "TERMINATED"


class WorkflowRunType(str, Enum):
    DATA_ACCESS = "DATA_ACCESS"
    POLICY = "POLICY"
    CHANGE_MANAGEMENT = "CHANGE_MANAGEMENT"
    PUBLICATION_MANAGEMENT = "PUBLICATION_MANAGEMENT"
    IMPACT_ANALYSIS = "IMPACT_ANALYSIS"
    REVOKE_DATA_ACCESS = "REVOKE_DATA_ACCESS"


class WorkflowStatus(str, Enum):
    PUBLISHED = "PUBLISHED"
    DRAFT = "DRAFT"
    DISABLED = "DISABLED"


class WorkflowType(str, Enum):
    DATA_ACCESS = "DATA_ACCESS"
    POLICY = "POLICY"
    CHANGE_MANAGEMENT = "CHANGE_MANAGEMENT"
    PUBLICATION_MANAGEMENT = "PUBLICATION_MANAGEMENT"
    IMPACT_ANALYSIS = "IMPACT_ANALYSIS"
    REVOKE_DATA_ACCESS = "REVOKE_DATA_ACCESS"
