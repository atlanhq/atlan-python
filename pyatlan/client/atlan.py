# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)
import contextlib
import copy
import json
import logging
import os
from typing import ClassVar, Generator, Optional, Type, TypeVar, Union

import requests
from pydantic import (
    BaseSettings,
    HttpUrl,
    PrivateAttr,
    parse_obj_as,
    validate_arguments,
)
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from pyatlan.client.constants import (
    ADD_BUSINESS_ATTRIBUTE_BY_ID,
    BULK_UPDATE,
    CREATE_TYPE_DEFS,
    DELETE_ENTITY_BY_ATTRIBUTE,
    DELETE_ENTITY_BY_GUID,
    DELETE_TYPE_DEF_BY_NAME,
    GET_ALL_TYPE_DEFS,
    GET_ENTITY_BY_GUID,
    GET_ENTITY_BY_UNIQUE_ATTRIBUTE,
    GET_ROLES,
    INDEX_SEARCH,
    PARTIAL_UPDATE_ENTITY_BY_ATTRIBUTE,
    UPDATE_ENTITY_BY_ATTRIBUTE,
)
from pyatlan.error import AtlanError, NotFoundError
from pyatlan.exceptions import AtlanServiceException, InvalidRequestException
from pyatlan.model.assets import (
    Asset,
    AtlasGlossary,
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    Connection,
    Database,
    MaterialisedView,
    Referenceable,
    Schema,
    Table,
    View,
)
from pyatlan.model.core import (
    Announcement,
    AssetRequest,
    AssetResponse,
    AtlanObject,
    BulkRequest,
    Classification,
    ClassificationName,
    Classifications,
    CustomMetadata,
    CustomMetadataReqest,
)
from pyatlan.model.enums import AtlanDeleteType, AtlanTypeCategory, CertificateStatus
from pyatlan.model.response import AssetMutationResponse
from pyatlan.model.role import RoleResponse
from pyatlan.model.search import IndexSearchRequest
from pyatlan.model.typedef import (
    ClassificationDef,
    CustomMetadataDef,
    TypeDef,
    TypeDefResponse,
)
from pyatlan.utils import HTTPStatus, get_logger

LOGGER = get_logger()
T = TypeVar("T", bound=Referenceable)
A = TypeVar("A", bound=Asset)
Assets = Union[
    AtlasGlossary,
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    Connection,
    Database,
    Schema,
    Table,
    View,
    MaterialisedView,
]
Asset_Types = Union[
    Type[AtlasGlossary],
    Type[AtlasGlossaryCategory],
    Type[AtlasGlossaryTerm],
    Type[Connection],
    Type[Database],
    Type[Schema],
    Type[Table],
    Type[View],
    Type[MaterialisedView],
]


def get_session():
    retry_strategy = Retry(
        total=6,
        backoff_factor=1,
        status_forcelist=[403, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.session()
    session.mount("https://", adapter)
    session.headers.update({"x-atlan-agent": "sdk", "x-atlan-agent-id": "python"})
    return session


class AtlanClient(BaseSettings):
    _default_client: "ClassVar[Optional[AtlanClient]]" = None
    base_url: HttpUrl
    api_key: str
    _session: requests.Session = PrivateAttr(default_factory=get_session)
    _request_params: dict = PrivateAttr()

    class Config:
        env_prefix = "atlan_"

    class SearchResults:
        def __init__(
            self,
            client: "AtlanClient",
            criteria: IndexSearchRequest,
            start: int,
            size: int,
            count: int,
            assets: list[Asset],
        ):
            self._client = client
            self._criteria = criteria
            self._start = start
            self._size = size
            self.count = count
            self._assets = assets

        def current_page(self) -> list[Asset]:
            return self._assets

        def next_page(self, start=None, size=None) -> bool:
            self._start = start or self._start + self._size
            if size:
                self._size = size
            return self._get_next_page() if self._assets else False

        # TODO Rename this here and in `next_page`
        def _get_next_page(self):
            self._criteria.dsl.from_ = self._start
            self._criteria.dsl.size = self._size
            raw_json = self._client._call_api(
                INDEX_SEARCH,
                request_obj=self._criteria,
            )
            if "entities" not in raw_json:
                self._assets = []
                return False
            self._assets = parse_obj_as(list[Asset], raw_json["entities"])
            return True

        def __iter__(self) -> Generator[Asset, None, None]:
            while True:
                yield from self.current_page()
                if not self.next_page():
                    break

    @classmethod
    def register_client(cls, client: "AtlanClient"):
        if not isinstance(client, AtlanClient):
            raise ValueError("client must be an instance of AtlanClient")
        cls._default_client = client

    @classmethod
    def get_default_client(cls) -> "Optional[AtlanClient]":
        return cls._default_client

    def __init__(self, **data):
        super().__init__(**data)
        self._request_params = {"headers": {"authorization": f"Bearer {self.api_key}"}}

    def _call_api(
        self, api, query_params=None, request_obj=None, exclude_unset: bool = True
    ):
        params, path = self._create_params(
            api, query_params, request_obj, exclude_unset
        )
        response = self._session.request(api.method.value, path, **params)
        if response is not None:
            LOGGER.debug("HTTP Status: %s", response.status_code)
        if response is None:
            return None
        if response.status_code == api.expected_status:
            try:
                if (
                    response.content is None
                    or response.status_code == HTTPStatus.NO_CONTENT
                ):
                    return None
                if LOGGER.isEnabledFor(logging.DEBUG):
                    LOGGER.debug(
                        "<== __call_api(%s,%s,%s), result = %s",
                        vars(api),
                        params,
                        request_obj,
                        response,
                    )
                    LOGGER.debug(response.json())
                return response.json()
            except Exception as e:
                print(e)
                LOGGER.exception(
                    "Exception occurred while parsing response with msg: %s", e
                )
                raise AtlanServiceException(api, response) from e
        elif response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
            LOGGER.error(
                "Atlas Service unavailable. HTTP Status: %s",
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

            return None
        else:
            with contextlib.suppress(ValueError):
                error_info = json.loads(response.text)
                error_code = error_info.get("errorCode", 0)
                error_message = error_info.get("errorMessage", "")
                if error_code and error_message:
                    raise AtlanError(
                        message=error_message,
                        code=error_code,
                        status_code=response.status_code,
                    )
            raise AtlanServiceException(api, response)

    def _create_params(
        self, api, query_params, request_obj, exclude_unset: bool = True
    ):
        params = copy.deepcopy(self._request_params)
        path = os.path.join(self.base_url, api.path)
        params["headers"]["Accept"] = api.consumes
        params["headers"]["content-type"] = api.produces
        if query_params is not None:
            params["params"] = query_params
        if request_obj is not None:
            if isinstance(request_obj, AtlanObject):
                params["data"] = request_obj.json(
                    by_alias=True, exclude_unset=exclude_unset
                )
            else:
                params["data"] = json.dumps(request_obj)
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("------------------------------------------------------")
            LOGGER.debug("Call         : %s %s", api.method, path)
            LOGGER.debug("Content-type_ : %s", api.consumes)
            LOGGER.debug("Accept       : %s", api.produces)
        return params, path

    def get_roles(
        self,
        limit: int,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> RoleResponse:
        if post_filter is None:
            post_filter = ""
        if sort is None:
            sort = ""
        query_params = {
            "filter": post_filter,
            "sort": sort,
            "count": count,
            "offset": offset,
            "limit": limit,
        }
        raw_json = self._call_api(GET_ROLES.format_path_with_params(), query_params)
        return RoleResponse(**raw_json)

    def get_all_roles(self) -> RoleResponse:
        """
        Retrieve all roles defined in Atlan.
        """
        raw_json = self._call_api(GET_ROLES.format_path_with_params())
        return RoleResponse(**raw_json)

    @validate_arguments()
    def get_asset_by_qualified_name(
        self,
        qualified_name: str,
        asset_type: Type[A],
        min_ext_info: bool = False,
        ignore_relationships: bool = False,
    ) -> A:
        query_params = {
            "attr:qualifiedName": qualified_name,
            "minExtInfo": min_ext_info,
            "ignoreRelationships": ignore_relationships,
        }
        try:
            raw_json = self._call_api(
                GET_ENTITY_BY_UNIQUE_ATTRIBUTE.format_path_with_params(
                    asset_type.__name__
                ),
                query_params,
            )
            raw_json["entity"]["attributes"].update(
                raw_json["entity"]["relationshipAttributes"]
            )
            asset = self.handle_relationships(raw_json)
            if not isinstance(asset, asset_type):
                raise NotFoundError(
                    message=f"Asset with qualifiedName {qualified_name} "
                    f"is not of the type requested: {asset_type.__name__}.",
                    code="ATLAN-PYTHON-404-002",
                )
            return asset
        except AtlanError as ae:
            if ae.status_code == HTTPStatus.NOT_FOUND:
                raise NotFoundError(message=ae.user_message, code=ae.code) from ae
            raise ae

    @validate_arguments()
    def get_asset_by_guid(
        self,
        guid: str,
        asset_type: Type[A],
        min_ext_info: bool = False,
        ignore_relationships: bool = False,
    ) -> A:
        query_params = {
            "minExtInfo": min_ext_info,
            "ignoreRelationships": ignore_relationships,
        }

        try:
            raw_json = self._call_api(
                GET_ENTITY_BY_GUID.format_path_with_params(guid),
                query_params,
            )
            asset = self.handle_relationships(raw_json)
            if not isinstance(asset, asset_type):
                raise NotFoundError(
                    message=f"Asset with GUID {guid} is not of the type requested: {asset_type.__name__}.",
                    code="ATLAN-PYTHON-404-002",
                )
            return asset
        except AtlanError as ae:
            if ae.status_code == HTTPStatus.NOT_FOUND:
                raise NotFoundError(message=ae.user_message, code=ae.code) from ae
            raise ae

    def handle_relationships(self, raw_json):
        if (
            "relationshipAttributes" in raw_json["entity"]
            and raw_json["entity"]["relationshipAttributes"]
        ):
            raw_json["entity"]["attributes"].update(
                raw_json["entity"]["relationshipAttributes"]
            )
        raw_json["entity"]["relationshipAttributes"] = {}
        asset = AssetResponse[A](**raw_json).entity
        asset.is_incomplete = False
        return asset

    @validate_arguments()
    def retrieve_minimal(self, guid: str, asset_type: Type[A]) -> A:
        return self.get_asset_by_guid(
            guid=guid,
            asset_type=asset_type,
            min_ext_info=True,
            ignore_relationships=True,
        )

    def upsert(
        self,
        entity: Union[Asset, list[Asset]],
        replace_classifications: bool = False,
        replace_custom_metadata: bool = False,
        overwrite_custom_metadata: bool = False,
    ) -> AssetMutationResponse:
        query_params = {
            "replaceClassifications": replace_classifications,
            "replaceBusinessAttributes": replace_custom_metadata,
            "overwriteBusinessAttributes": overwrite_custom_metadata,
        }
        entities: list[Asset] = []
        if isinstance(entity, list):
            entities.extend(entity)
        else:
            entities.append(entity)
        for asset in entities:
            asset.validate_required()
        request = BulkRequest[Asset](entities=entities)
        raw_json = self._call_api(BULK_UPDATE, query_params, request)
        return AssetMutationResponse(**raw_json)

    def purge_entity_by_guid(self, guid) -> AssetMutationResponse:
        raw_json = self._call_api(
            DELETE_ENTITY_BY_GUID.format_path_with_params(guid),
            {"deleteType": AtlanDeleteType.HARD.value},
        )
        return AssetMutationResponse(**raw_json)

    def delete_entity_by_guid(self, guid) -> AssetMutationResponse:
        raw_json = self._call_api(
            DELETE_ENTITY_BY_GUID.format_path_with_params(guid),
            {"deleteType": AtlanDeleteType.SOFT.value},
        )
        return AssetMutationResponse(**raw_json)

    def search(self, criteria: IndexSearchRequest) -> SearchResults:
        raw_json = self._call_api(
            INDEX_SEARCH,
            request_obj=criteria,
        )
        if "entities" in raw_json:
            assets = parse_obj_as(list[Asset], raw_json["entities"])
        else:
            assets = []
        count = raw_json["approximateCount"] if "approximateCount" in raw_json else 0
        return AtlanClient.SearchResults(
            client=self,
            criteria=criteria,
            start=criteria.dsl.from_,
            size=criteria.dsl.size,
            count=count,
            assets=assets,
        )

    def get_all_typedefs(self) -> TypeDefResponse:
        raw_json = self._call_api(GET_ALL_TYPE_DEFS)
        return TypeDefResponse(**raw_json)

    def get_typedefs(self, type_category: AtlanTypeCategory) -> TypeDefResponse:
        query_params = {"type": type_category.value}
        raw_json = self._call_api(
            GET_ALL_TYPE_DEFS.format_path_with_params(),
            query_params,
        )
        return TypeDefResponse(**raw_json)

    def create_typedef(self, typedef: TypeDef) -> TypeDefResponse:
        if isinstance(typedef, ClassificationDef):
            # Set up the request payload...
            payload = TypeDefResponse(
                classification_defs=[typedef],
                enum_defs=[],
                struct_defs=[],
                entity_defs=[],
                relationship_defs=[],
                custom_metadata_defs=[],
            )
        elif isinstance(typedef, CustomMetadataDef):
            # Set up the request payload...
            payload = TypeDefResponse(
                classification_defs=[],
                enum_defs=[],
                struct_defs=[],
                entity_defs=[],
                relationship_defs=[],
                custom_metadata_defs=[typedef],
            )
        else:
            raise InvalidRequestException(
                "Unable to create new type definitions of category: "
                + typedef.category.value,
                param="category",
            )
            # Throw an invalid request exception
        raw_json = self._call_api(
            CREATE_TYPE_DEFS, request_obj=payload, exclude_unset=False
        )
        return TypeDefResponse(**raw_json)

    def purge_typedef(self, internal_name: str) -> None:
        self._call_api(DELETE_TYPE_DEF_BY_NAME.format_path_with_params(internal_name))

    @validate_arguments()
    def add_classifications(
        self,
        asset_type: Type[A],
        qualified_name: str,
        classification_names: list[str],
        propagate: bool = True,
        remove_propagation_on_delete: bool = True,
        restrict_lineage_propagation: bool = True,
    ) -> None:
        classifications = Classifications(
            __root__=[
                Classification(
                    type_name=ClassificationName(display_text=name),
                    propagate=propagate,
                    remove_propagations_on_entity_delete=remove_propagation_on_delete,
                    restrict_propagation_through_lineage=restrict_lineage_propagation,
                )
                for name in classification_names
            ]
        )
        query_params = {"attr:qualifiedName": qualified_name}
        self._call_api(
            UPDATE_ENTITY_BY_ATTRIBUTE.format_path_with_params(
                asset_type.__name__, "classifications"
            ),
            query_params,
            classifications,
        )

    @validate_arguments()
    def remove_classification(
        self, asset_type: Type[A], qualified_name: str, classification_name: str
    ) -> None:
        from pyatlan.cache.classification_cache import ClassificationCache

        classification_id = ClassificationCache.get_id_for_name(classification_name)
        if not classification_id:
            raise ValueError(f"{classification_name} is not a valid Classification")
        query_params = {"attr:qualifiedName": qualified_name}
        self._call_api(
            DELETE_ENTITY_BY_ATTRIBUTE.format_path_with_params(
                asset_type.__name__, "classification", classification_id
            ),
            query_params,
        )

    @validate_arguments()
    def update_certificate(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        certificate_status: CertificateStatus,
        message: str,
    ) -> Optional[A]:
        asset = asset_type()
        asset.qualified_name = qualified_name
        asset.certificate_status = certificate_status
        asset.name = name
        asset.certificate_status_message = message
        return self._update_asset_by_attribute(asset, asset_type, qualified_name)

    def _update_asset_by_attribute(self, asset, asset_type, qualified_name: str):
        query_params = {"attr:qualifiedName": qualified_name}
        raw_json = self._call_api(
            PARTIAL_UPDATE_ENTITY_BY_ATTRIBUTE.format_path_with_params(
                asset_type.__name__
            ),
            query_params,
            AssetRequest[Asset](entity=asset),
        )
        response = AssetMutationResponse(**raw_json)
        if assets := response.assets_partially_updated(asset_type=asset_type):
            return assets[0]
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return None

    @validate_arguments()
    def remove_certificate(
        self, asset_type: Type[A], qualified_name: str, name: str
    ) -> Optional[A]:
        asset = asset_type()
        asset.qualified_name = qualified_name
        asset.name = name
        asset.remove_certificate()
        return self._update_asset_by_attribute(asset, asset_type, qualified_name)

    @validate_arguments()
    def update_announcement(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        announcement: Announcement,
    ) -> Optional[A]:
        asset = asset_type()
        asset.qualified_name = qualified_name
        asset.set_announcement(announcement)
        asset.name = name
        return self._update_asset_by_attribute(asset, asset_type, qualified_name)

    @validate_arguments()
    def remove_announcement(
        self, asset_type: Type[A], qualified_name: str, name: str
    ) -> Optional[A]:
        asset = asset_type()
        asset.qualified_name = qualified_name
        asset.name = name
        asset.remove_announcement()
        return self._update_asset_by_attribute(asset, asset_type, qualified_name)

    def replace_custom_metadata(self, guid: str, custom_metadata: CustomMetadata):
        # TODO: This endpoint is not currently functioning correctly on the server
        custom_metadata_request = CustomMetadataReqest(__root__=custom_metadata)
        self._call_api(
            ADD_BUSINESS_ATTRIBUTE_BY_ID.format_path(
                {"entity_guid": guid, "bm_id": custom_metadata._meta_data_type_id}
            ),
            None,
            custom_metadata_request,
        )

    @validate_arguments()
    def append_terms(
        self,
        asset_type: Type[A],
        terms: list[AtlasGlossaryTerm],
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        if guid:
            if qualified_name:
                raise ValueError(
                    "Either guid or qualified_name can be be specified not both"
                )
            asset = self.get_asset_by_guid(guid=guid, asset_type=asset_type)
        elif qualified_name:
            asset = self.get_asset_by_qualified_name(
                qualified_name=qualified_name, asset_type=asset_type
            )
        else:
            raise ValueError("Either guid or qualified name must be specified")
        if not terms:
            return asset
        replacement_terms: list[AtlasGlossaryTerm] = []
        if existing_terms := asset.terms:
            replacement_terms.extend(
                term for term in existing_terms if term.relationship_status != "DELETED"
            )
        replacement_terms.extend(terms)
        asset.terms = replacement_terms
        response = self.upsert(entity=asset)
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return asset

    @validate_arguments()
    def replace_terms(
        self,
        asset_type: Type[A],
        terms: list[AtlasGlossaryTerm],
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        if guid:
            if qualified_name:
                raise ValueError(
                    "Either guid or qualified_name can be be specified not both"
                )
            asset = self.get_asset_by_guid(guid=guid, asset_type=asset_type)
        elif qualified_name:
            asset = self.get_asset_by_qualified_name(
                qualified_name=qualified_name, asset_type=asset_type
            )
        else:
            raise ValueError("Either guid or qualified name must be specified")
        asset.terms = terms
        response = self.upsert(entity=asset)
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return asset

    @validate_arguments()
    def remove_terms(
        self,
        asset_type: Type[A],
        terms: list[AtlasGlossaryTerm],
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        if not terms:
            raise ValueError("A list of terms to remove must be specified")
        if guid:
            if qualified_name:
                raise ValueError(
                    "Either guid or qualified_name can be be specified not both"
                )
            asset = self.get_asset_by_guid(guid=guid, asset_type=asset_type)
        elif qualified_name:
            asset = self.get_asset_by_qualified_name(
                qualified_name=qualified_name, asset_type=asset_type
            )
        else:
            raise ValueError("Either guid or qualified name must be specified")
        replacement_terms: list[AtlasGlossaryTerm] = []
        guids_to_be_removed = {t.guid for t in terms}
        if existing_terms := asset.terms:
            replacement_terms.extend(
                term
                for term in existing_terms
                if term.relationship_status != "DELETED"
                and term.guid not in guids_to_be_removed
            )
        asset.terms = replacement_terms
        response = self.upsert(entity=asset)
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return asset
