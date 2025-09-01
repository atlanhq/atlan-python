## 8.0.2 (September 1, 2025)

### Bug Fixes

- Fixed `AsyncWorkflowSearchResponse` async iterator.

## 8.0.1 (August 25, 2025)

### New Features

- Added `get_client_async()` for initializing `AsyncAtlanClient` when using packages.
- Added optional parameter `set_pkg_headers()` to set package headers on the client (defaults to `False`).

### Bug Fixes

- Fixed `httpcore.LocalProtocolError` exception in `get_client()` that occurred when `ATLAN_API_KEY` environment variable was not configured (commonly encountered during package impersonation with empty `API` key strings).

### QOL Improvements

- Added `pyatlan-wolfi-base` Docker image workflow with enhanced capabilities:
  - **Automatic release builds**: Workflow now triggers automatically on GitHub releases using latest Python (3.13) and SDK versions
  - **Git branch support**: Added ability to install SDK from any git branch for development/testing purposes via `pyatlan_branch` parameter
  - **Smart installation logic**: Automatically chooses between PyPI (stable) or git (development) installation methods
  - **Enhanced tagging**: Branch builds tagged as `branch-{branchname}-{python}-{commit}` for easy identification
  - **Build metadata**: Images include labels tracking installation source, version/branch, and Python version
  - **Conditional PyPI checks**: Skips PyPI availability checks when installing from git branches
  - **Improved logging**: Shows installation method, branch info, and trigger source in build outputs

## 8.0.0 (August 20, 2025)

### New Features

#### Full `async/await` support

- Added `async/await` support to the SDK. All existing `clients` and `caches` now have async variants, plus new models (mainly search result models that require `async` iteration). Following `aio` directory convention for all async components.
- Implemented `AsyncAtlanClient` for all async operations (extends `AtlanClient` for reusability).
- For methods that accept client parameters, we've added corresponding `*_async()` variants:

| sync method | async method |
|------------|--------------|
| `Connection.creator()` | `Connection.creator_async()` |
| `Badge.creator()` | `Badge.creator_async()` |
| `FluentSearch.execute()` | `FluentSearch.execute_async()` |
| `AtlanTag.of()` | `AtlanTag.of_async()` |
| `SourceTagAttachment.by_name()` | `SourceTagAttachment.by_name_async()` |
| `CompoundQuery.tagged_with_value()` | `CompoundQuery.tagged_with_value_async()` |
| `Referenceable.json()` | `Referenceable.json_async()` |
| `Referenceable.get_custom_metadata()` | `Referenceable.get_custom_metadata_async()` |
| `Referenceable.set_custom_metadata()` | `Referenceable.set_custom_metadata_async()` |
| `Referenceable.flush_custom_metadata()` | `Referenceable.flush_custom_metadata_async()` |

#### Shared business logic architecture

- Extracted common functionality (request preparation and response processing) into a separate `common` sub-package. This enables reuse across both sync and async operations - only the middle layer (API calling with respective clients) differs.

Example:
```python
from pyatlan.client.common import FindPurposesByName

@validate_arguments
async def find_purposes_by_name(
    self,
    name: str,
    attributes: Optional[List[str]] = None,
) -> List[Purpose]:
    """
    Async find purposes by name using shared business logic.
    :param name: of the purpose
    :param attributes: (optional) collection of attributes to retrieve for the purpose
    :returns: all purposes with that name, if found
    :raises NotFoundError: if no purpose with the provided name exists
    """
    search_request = FindPurposesByName.prepare_request(name, attributes)
    search_results = await self.search(search_request)
    return FindPurposesByName.process_response(
        search_results, name, allow_multiple=True
    )
```

### Documentation

- **Asynchronous SDK operations**: https://developer.atlan.com/sdks/python/#asynchronous-sdk-operations

### Breaking Changes

While these aren't direct breaking changes to the SDK API, they may affect your code if you depend on these libraries:

- **Migrated from [`requests`](https://requests.readthedocs.io/en/latest) to [`httpx`](https://www.python-httpx.org)**: Completely removed support for `requests` library and migrated to `httpx`, which provides similar API for `sync` operations plus `async` client support for async operations.
- **Replaced [`urllib3`](https://urllib3.readthedocs.io/en/stable) with [`httpx-retries`](https://will-ockmore.github.io/httpx-retries)**: Removed support for `urllib3` retry mechanism and implemented retries using `httpx-retries` library (API remains similar).

### QOL Improvements

- Generated latest typedef models.
- Removed redundant requirements files (no longer needed since migration to `uv` in previous releases).
- Updated GitHub workflows for Docker image builds to use `uv sync` (without dev dependencies).
- Added unit and integration tests for `async` SDK.
- Added `x-atlan-client-type: sync` or `x-atlan-client-type: async` to SDK headers and logging for better observability.
- Added `async-integration-tests` job to `pyatlan-pr.yaml` workflow. Triggers when there are changes to async SDK code or can be triggered manually via `run-async-tests` label on PR.
- Async SDK unit tests run by default on every commit push as they have minimal time impact on test suite.
- Used module-scoped asyncio test fixtures similar to sync integration tests:
  ```toml
  # pyproject.toml
  asyncio_mode = "auto"
  asyncio_default_test_loop_scope = "module"
  asyncio_default_fixture_loop_scope = "module"
  ```
- Used `token_client` fixtures when creating/deleting API tokens with `retry=0` to avoid token overpopulation in test tenants.

## 7.2.0 (August 13, 2025)

### New Features

- Added Python version info to SDK headers and API logger.

### Breaking Changes

- Dropped support for `Python 3.8`.

### QOL Improvements

- Bumped various `core` and `dev` dependencies to latest versions.
- Fixed conda publish and pyatlan publish GitHub workflows.
- Fixed integration test failures due to Elasticsearch eventual consistency using custom retries (`glossary_test`, `test_client`, `persona/purpose_test`)

## 7.1.6 (August 7, 2025)

### Experimental

- Added support for adding DQ rules schedule to an asset (i.e: `AssetClient.add_dq_rule_schedule()`).

## 7.1.5 (August 1, 2025)

### Experimental
- Added `creator()` and `updater()` methods for `alpha_DQRule` (data quality rule) asset.

### QOL Improvements
- Generated latest typedef models.

## 7.1.4 (July 29, 2025)

### New Features
- Added new connector types: `AI`, `SAP_ECC`.
- Added new connector categories: `AI`, `ERP`.
- Added `creator()` methods for AI-based assets.
- Added support for `applicable_ai_asset_types` to custom metadata `AttributeDef.Options`.

### Experimental
- Added support for `AtlanClient` initialization via API token `guid`.

### Bug Fixes
- Fixed handling of `source_tag` when no `attributes` present.

### QOL Improvements
- Generated latest typedef models.
- Updated Dockerfile to use `python:3.13.5-slim-bookworm`.
- Removed unused `requirements` files (now using `pyproject.toml`).

## 7.1.3 (July 21, 2025)

### Bug Fixes

- Fixed multi-value select bug in the CM attribute setter.

## 7.1.2 (July 11, 2025)

### QOL Improvements

- Fixed `suggestions_test` integration test.
- Generated latest typedefs models.
- Updated Dockerfile to use `python:3.11-slim`.
- Migrated SDK to use [`uv`](https://docs.astral.sh/uv) for development, building, and publishing the SDK.
- Added `delete_type:HARD` optional parameter to `AssetClient.purge_by_guid()` method.
- Made `FluentSearch` usage in `get_by_*()` methods consistent with `GET` API (return `active` and `archived` assets).

## 7.1.1 (June 30, 2025)

### QOL Improvements

- Regenerated latest typedef models.

## 7.1.0 (June 27, 2025)

###  New Features

- Added support for managing asset-to-asset relationships that include attributes. Atlan now allows setting attributes on specific relationship types, providing richer metadata and contextual information for how assets are connected.

- These relationships can now carry attributes, similar to how assets themselves have attributes. The SDK has been enhanced to deserialize, access, and serialize these relationship-level attributes correctly.

**Supported relationship types:**

1. `AtlasGlossaryAntonym`
2. `AtlasGlossarySynonym`
3. `AtlasGlossaryReplacementTerm`
4. `AtlasGlossarySemanticAssignment`
5. `AtlasGlossaryPreferredTerm`
6. `AtlasGlossaryRelatedTerm`
7. `AtlasGlossaryTermCategorization`
8. `AtlasGlossaryTranslation`
9. `AtlasGlossaryValidValue`
10. `AtlasGlossaryIsARelationship`
11. `CustomParentEntityCustomChildEntities`
12. `CustomRelatedFromEntitiesCustomRelatedToEntities`
13. `UserDefRelationship`


### Breaking Changes

`Referenceable.relationship_attributes` field type updated:

This field now supports:

  ```python
  Optional[Union[RelationshipAttributes, Dict[str, Any]]]
  ```

- If `typeName` is present in the relationship attributes, the SDK will attempt to deserialize using the correct subclass of `RelationshipAttributes`.
- If `typeName` is absent, it will fall back to a raw `Dict[str, Any]`.

  **Before:**

  ```python
  Optional[Dict[str, Any]]
  ```

- This change improves structure and typing for known relationship models while maintaining backward compatibility via fallback.

### Bug Fixes

- Fixed automatic `401` token refresh by using `ContextVar` for `AtlanClient._401_has_retried` (bool flag) to avoid race conditions when executing SDK code in multithreading environments.

## 7.0.1 (June 16, 2025)

### Bug Fixes

- Fixed `FluentSearch` criteria used for `get_by_qualified_name/guid` method to include asset `type_name`.

## 7.0.0 (June 12, 2025)

### New Features

- Added `long` as a new primitive type in the `AtlanCustomAttributePrimitiveType` enum.
- Support for `Unmodeled` Asset types: Introduced `IndistinctAsset` as a fallback model to handle asset types that are not explicitly modeled in the SDK. Previously, such assets would return `None` (e.g: for newly introduced typedefs). With this release, the SDK will now return an `IndistinctAsset` instance containing basic fields such as `guid`, `qualifiedName`, and `typeName`.

### Bug Fixes

- Fixed timestamp-based pagination in search log results when `from + size` exceeds the Elasticsearch window size (10,000 records) due to identical creation times for the first and last records in a retrieved page.

### Breaking Changes

This release includes a **major refactor** that eliminates all usage of `AtlanClient.get_current_client()` and `set_current_client()` (previously implemented using [ContextVar](https://docs.python.org/3/library/contextvars.html) / [thread-local storage](https://docs.python.org/3/library/threading.html#thread-local-data) a.k.a TLS). Although the earlier design was thread-safe, it still required users to explicitly use `PyAtlanThreadPoolExecutor` in multi-threaded environments, resulting in unintuitive patterns and frequent client initialization errors.

The new design simplifies usage by requiring the `client` to be passed explicitly to SDK operations that interact with the Atlan platform.

> [!IMPORTANT]
> ### Affected Areas
> All the following methods or constructors now require a `client` argument due to the removal of `AtlanClient.get_current_client()`:

##### `pyatlan.model.assets`:

- `Referenceable.flush_custom_metadata(client)`
- `Referenceable.get_custom_metadata(client, name)`
- `Referenceable.set_custom_metadata(client, custom_metadata)`
- `CustomMetadataProxy` is no longer initialized in `Referenceable.__init__()` (as it now requires a `client`).
- `Purpose.create_metadata_policy()`
- `Purpose.create_data_policy()`
- `DataProduct.get_assets()`
- `Badge.creator()`
- `Connection.creator()`

> [!NOTE]
> `user_cache.validate_names`, `role_cache.validate_idstrs`, and `group_cache.validate_aliases` are now invoked inside `Connection.creator()` instead of field validators.

##### `pyatlan.model.custom_metadata`:

- `CustomMetadataDict(client, name)`
- `CustomMetadataProxy(client, business_attributes)`

##### `pyatlan.model.structs`:

- `SourceTagAttachment.by_name()`
- `SourceTagAttachment.by_qualified_name()`
- `SourceTagName()` (constructor)

##### `pyatlan.model.suggestions`:

- `Suggestions.get()`
- `Suggestions.apply()`

##### `pyatlan.model.fluent_search`

- `FluentSearch.tagged()`
- `FluentSearch.tagged_with_value()`

##### `pyatlan.client.typedef`

- `EnumDef.update()`
- `AttributeDef.create()`

##### `pyatlan.model.search`

- `Exists.with_custom_metadata()`
- `Term.with_custom_metadata()`

##### `pyatlan.client.atlan`

- `client_connection()`

##### `pyatlan.model.open_lineage`

- `OpenLineageEvent.emit()`

##### `pyatlan.model.fields.atlan_fields`

- `CustomMetadataField()` (constructor)

##### `pyatlan.model.packages`

- All crawler class constructors

### Serialization & Deserialization

#### API Serialization:

- Now handled via the `AtlanRequest` wrapper, which takes a Pydantic model instance and a client.
- It automatically performs translation (e.g: converting human-readable Atlan tag names into hashed IDs using `AtlanTagRetranslator`).

#### API Response Deserialization:

- Responses are processed using the `AtlanResponse` wrapper.
- It translates raw JSON into readable formats via registered translators like `AtlanTagTranslator` (e.g: converting hashed tag IDs into human-readable names).

### AtlanTag / AtlanTagName Changes

- **Human-readable tag names** are now only available when deserializing through `AtlanResponse` (which requires a valid `client`). If skipped, tag names remain in **hashed ID format** or as plain strings.
- Deleted tags (e.g `AtlanTagName('(DELETED)')`) will only appear when using `AtlanResponse`, as the lookup requires a client to determine tag validity.
- The `.id` attribute on `AtlanTagName` has been **deprecated**. Use `AtlanTag.tag_id` to access the hashed ID instead.
- Fixed typo in `AtlanTag.source_tag_attachments` field name.

### Other Changes

- `AtlanClient._401_has_retried` is now marked as a `PrivateAttr`.
- `IndexSearchRequest.Metadata` has been moved to a separate class: `IndexSearchRequestMetadata`.
- Removed deprecated methods:

  - `AtlanClient.get_current_client()`
  - `AtlanClient.set_current_client()`
  - `PyAtlanThreadPoolExecutor` (SDK is now fully thread-safe without it)
- Updated `AssetClient.find_domain_by_name()` and `AssetClient.find_product_by_name()` to return only active `Domain` and `Product` assets. Previously, these methods returned both `active` and `archived` assets, which caused issues when assets with the same `name` existed in both states - the first match (possibly `archived`) was returned.

### QOL Improvements

- Regenerated latest typedef models.
- Refactored integration and unit tests to eliminate reliance on `AtlanClient.get_current_client()` / `set_current_client()`.

## 6.2.1 (May 30, 2025)

### Bug Fixes

- Extended the `applicable_asset_types` attribute definition to accept `Union[Set[str], AssetTypes]`.
- Fixed validation to ensure provided asset type names match existing SDK asset classes, replacing the previously hard-coded set of asset types.

### QOL Improvements

- Regenerated the latest typedef models.

## 6.2.0 (May 27, 2025)

### New Features

- Added support for `append_atlan_tags` in the `AssetClient.save()` method.
- Introduced `AssetClient.remove_atlan_tags()` to allow users to remove one or more Atlan tags from a given asset.
- Enhanced the SDK to use the `/bulk` endpoint for all tag mutation operations.

### Breaking Changes

- All tag mutation methods (`add_atlan_tags`, `update_atlan_tags`, `remove_atlan_tag`, `remove_atlan_tags`) now use the `/bulk` endpoint. As a result, these methods will now return an `AssetMutationResponse` instead of `None`, reflecting the updated API response structure.

### Bug Fixes

- Added default `typeName=Referenceable` to `Bool`(must) clauses when `typeName` is not explicitly provided in the search request. This ensures the SDK retrieves only assets that inherit from the `Referenceable` supertype.

### QOL Improvements

- Regenerated the latest typedef models.

## 6.1.1 (May 21, 2025)

### New Features

- Added a utility method (`AssetClient.process_assets()`) to simplify processing (e.g: updating) assets while iterating through search results.

### Bug Fixes

- Fixed an issue where the search pagination loop would break due to invalid assets.
- If `typeName` is not explicitly provided in the search request, the SDK now defaults to retrieving only assets with the `Referenceable` supertype. This avoids including non-asset records in the response.

### QOL Improvements

- Regenerated the latest typedef models.
- Added a retry loop to ensure the token is fully active before retrying the original request after a `401` response.

## 6.1.0 (May 13, 2025)

### New Features

- Added support for dynamic extension of `AtlanConnectorType` to enable custom connectors.
- Migrated from `TLS` to `ContextVars` to support both multithreaded and asynchronous environments.
- Introduced `PyAtlanThreadPoolExecutor` in `pyatlan.utils`, which preserves context variables across threads—useful for running SDK methods in multithreaded or asynchronous environments.
- Implemented iterative pagination in `WorkflowClient` search methods.

### Bug Fixes

- Resolved pagination issues in `UserClient` and `GroupClient` search methods.

### QOL Improvements

- Regenerated the latest typedef models.
- Simplified the `creator()` methods in both `AtlasGlossaryTerm` and `AtlasGlossaryCategory`.

## 6.0.6 (April 29, 2025)

### New Features

- Added optional `description` parameter to `CustomMetadataDef/AttributeDef.create()` methods.

### QOL Improvements

- Added issue and pull request templates.
- Added support for [`vcrpy`](https://vcrpy.readthedocs.io/en/latest) to enable easy mocking/patching of HTTP interactions, especially useful for 3rd-party API testing.

## 6.0.5 (April 25, 2025)

### New Features

- Added a public method `AtlanClient.init_for_multithreading()` to allow users to prepare the given client for use in multi-threaded environments.

### QOL Improvements

- Regenerated the latest typedef models.

## 6.0.4 (April 22, 2025)

### New Features

- Added a new optional parameter `source_tag_qualified_name` to `tagged_with_value()`, allowing users to explicitly provide the qualified name of the source tag to match (useful when multiple tags share the same name).
- Added support for undefined fields in `DataContract` models by allowing extra fields in `AtlanYamlModel` (`Extra.allow`).
- Added a new method `WorkflowClient.find_runs_by_status_and_time_range()` to search workflow runs based on their status and a specified time range (`started_at` / `finished_at`).

### QOL Improvements

- Regenerated the latest typedef models.
- Fixed an indentation issue in the `DocumentDB` generator Jinja templates.

## 6.0.3 (April 15, 2025)

### New Features

- Added `creator()` methods for `DocumentDB` assets.
- Added support for `purpose` and `persona` in `IndexSearchRequest`.
- Added an optional `workflow_name` parameter to the `WorkflowClient.monitor()` method.
- Added an optional `workflow_name` parameter to the `CredentialClient.get_all()` method.

### QOL Improvements

- Generated the latest typedef models.

## 6.0.2 (April 07, 2025)

### QOL Improvements

- Updated SDK generator templates to align with `Pyatlan v6` changes.
- Added a delay after token refresh to avoid empty (`[]`) typedef responses.

### Bug Fixes

- Reset `has_retried` if the last retry wasn't a `401` to allow future token refresh attempts.

## 6.0.1 (March 28, 2025)

### QOL Improvements

- Migrated the boolean field `AtlanClient.401_tls.has_retried` to thread-local storage (`TLS`) to enhance `401` token handling in a multithreaded environment.

## 6.0.0 (March 20, 2025)

### New Features

- Added a new connector type: `DOCUMENTDB`.

### Breaking Changes

- `DataProduct.get_assets()` method now raises `InvalidRequestError` when there is a missing value for `data_product_assets_d_s_l`, which is required to retrieve product assets.
- Fixed SDK cache inconsistencies and unexpected behavior when running in concurrent/multi-threaded environments.

  - Completely migrated from `AtlanClient._default_client` to `AtlanClient._current_client_tls` (which uses thread-local storage) to prevent sharing this class variable across multiple threads. Previously, it was shared across threads, resulting in inconsistent behavior in SDK caches.
  - Removed `cache_key` maintenance that used to maintain cache instances per Atlan client hash (`cache_key(base_url, api_key)`).
  - Now, all caches are bound to an `AtlanClient` instance, requiring the migration of all cache methods from class methods to instance methods.
  - Caches remain tracked even in cases of automatic token refresh for the client.

  The following example illustrates the migration:

  ### Before

  ```py
  from pyatlan.cache.atlan_tag_cache import AtlanTagCache

  c1 = AtlanClient()
  tag_id = AtlanTagCache.get_id_for_name(atlan_tag_name)  # <-- Uses default client (c1), populates the caches (API call), and uses cache_key to store the cache instance
  tag_id = AtlanTagCache.get_id_for_name(atlan_tag_name)  # Returns the ID from the cache (no API call)

  c2 = AtlanClient()
  tag_id = AtlanTagCache.get_id_for_name(atlan_tag_name)  # <-- Uses default client (c2), populates the caches, and uses cache_key to store the cache instance
  tag_id = AtlanTagCache.get_id_for_name(atlan_tag_name)  # Returns the ID from the cache (no API call)

  c1 = AtlanClient()
  tag_id = AtlanTagCache.get_id_for_name(atlan_tag_name)  # <-- c1 initialized again. Since cache_key was used for c1 previously, the populated cache instance in memory is reused, avoiding an API call.
  tag_id = AtlanTagCache.get_id_for_name(atlan_tag_name)  # Returns the ID from the cache (no API call)
  ```

  ### Now (caches are bound to the client and maintained only upon the first client initialization):

  ```py
  c1 = AtlanClient()

  tag_id = c1.atlan_tag_cache.get_id_for_name(atlan_tag_name)  # <-- Uses default client (c1) and populates the caches (API call)

  # OR
  tag_id = AtlanClient.get_current_client().atlan_tag_cache.get_id_for_name(atlan_tag_name) # <-- Uses default client (c1) and populates the caches (API call)
  tag_id = AtlanTagCache.get_id_for_name(atlan_tag_name)  # Returns the ID from the cache (no API call)

  c2 = AtlanClient()
  tag_id = c2.atlan_tag_cache.get_id_for_name(atlan_tag_name)  # <-- Uses default client (c2) and populates the cache (API call)
  tag_id = c2.atlan_tag_cache.get_id_for_name(atlan_tag_name)  # Returns the ID from the cache (no API call)

  c1 = AtlanClient()
  tag_id = c1.atlan_tag_cache.get_id_for_name(atlan_tag_name)  # <-- c1 initialized again. Since no cache_key is used in the latest approach, the previously populated cache instance is gone, and we need to make an API call to populate the cache for c1.
  tag_id = c1.atlan_tag_cache.get_id_for_name(atlan_tag_name)  # Returns the ID from the cache (no API call)
  ```

## 5.0.2 (March 11, 2025)

### New Features

- Added handling for `doc` and `errorDoc` in `AtlanError`.
- Introduced secure agent support in `OracleCrawler`.

### QOL Improvements

- Fixed vulnerabilities reported by `dependabot`.

## 5.0.1 (March 03, 2025)

### New Features

- Added support for the `MatchPhase` query.

### Bug Fixes

- Fixed handling of `aggregations` in `AuditSearchResults`.
- Added `Asset.TYPE_NAME` condition in `FluentSearch` for append terms, replace terms, and remove terms methods to ensure an exact asset match. Previously, only `Asset.GUID/QUALIFIED_NAME` was used, which could return multiple assets if different asset types had the same qualified name.

### QOL Improvements

- Bumped `ruff` to the latest version (`0.9.9`).
- Removed redundant asset relationship fields.
- Updated the **"Installing for Development"** section in `README.md`.

## 5.0.0 (February 26, 2025)

### New Features

- Added a new method `DataProduct.get_assets()` that retrieves a list of all assets linked to the provided data product.
- Made `DSL.query` and `DSL.post_filter` more flexible to accept both raw dictionaries and Python objects, i.e: `Optional[Union[Dict[str, Any], Query]]`. This change allows users to construct `DSL` objects directly with raw DSL dictionaries, e.g: `DSL(**raw_dsl)`.
- Added `creator_with_prefix()` methods to `GCSObject` and `ADLSObject`.
- Added a model utility method (`construct_object_key()`) to construct a consistent `objectKey` for object store assets, which is currently used by `creator_with_prefix()`.

### Bug Fixes

- Fixed the `creator_with_prefix()` method to use an empty prefix `""` (representing the root path) for object store assets.
- Fixed `SearchLogResults` edge cases — when `entityGuidsAll` is empty `[]` or `"undefined"` in the request `DSL`.

### Breaking Changes

- `bucket_name` and `adls_container_name` are now mandatory for `GCSObject.creator()` and `ADLSObject.creator()`, respectively.
- Changed the default behavior for tag propagation to `False` by default. This means:
  - `remove_propagations_on_entity_delete` is now `True` by default.
  - `propagate`, `restrict_propagation_through_lineage`, and `restrict_propagation_through_hierarchy` are now `False` by default.

### QOL Improvements

- Generated the latest typedef models.
- Upgraded SDK dependencies (main, dev, and tooling) to the latest versions.
- Replaced the existing linter and formatter stack (`black`, `flake8`, `isort`, `autoflake8`) with `ruff`, significantly reducing development and QA check times while consolidating all configurations into a single file.

## 4.2.5 (February 19, 2025)

### New Features

- Added the SDK version number to the `_api_logger()` method.
- Added handling of the `errorCause` property to `AtlanError`.
- Added `creator()` methods for `Quicksight` assets.
- Added support for new connector types:
  - `KX`
  - `CRATEDB`

### QOL Improvements

- Updated GitHub Actions to the latest version.
- Fixed broken integration tests for adding, replacing, and removing glossary terms.
- Added a new job to the `pyatlan-publish.yml` workflow to publish the SDK image to Docker Hub.
- Introduced `dependabot.yml` to manage dependencies and actions, and removed unused secret variables.

## 4.2.4 (February 13, 2025)

### Bug Fixes

- Added safeguards for search pagination methods.

## 4.2.3 (February 13, 2025)

### QOL Improvements

- Refactored the `Asset._convert_to_real_type_()` method for improved clarity and robustness.
  In certain cases, asset types may be undefined or invalid—likely due to an unhandled backend edge case. To handle this gracefully, the method now ignores deserialization of `Asset` API responses in such scenarios instead of raising `AttributeError` or `TypeError` exceptions.

## 4.2.2 (February 11, 2025)

### New Features

- Added support for `AnaplanSystemDimension.creator()`.
- Added support for new connector types:
  - `RDS`
  - `SHARE_POINT`
  - `SHARED_DRIVE`

### QOL Improvements

- Generated the latest typedef models.
- Upgraded pre-commit `black` to `24.4.2`
- Enhanced `Credential.creator()` validation to prevent creating fake credentials when `test=False`.

## 4.2.1 (February 6, 2025)

### New Features

- Added an optional boolean parameter `test=True` to `CredentialClient.creator()` method.

## 4.2.0 (February 4, 2025)

### New Features

- Added support for `ApplicationField.creator()`.
- Added support for `CredentialClient.creator()`.
- Added support for optional parameters (`host` and `port`) in `Connection.creator()`.

### Breaking Changes

- Changed the default setting for tracking `IndexSearch` logs (`save_search_log=False`). Previously, it was set to `True`, which was causing frequent Out of Memory (OOM) issues in Metastore pods.

### QOL Improvements

- Generated the latest typedef models.
- Refactored `OpenLineageClient.create_connection()` to use the new `CredentialClient.creator()`.

## 4.1.0 (January 28, 2025)

### New Features

- Added support for the following workflow packages:

  **Connectors**
  - OracleCrawler

  **Utils**
  - LineageBuilder
  - LineageGenerator
  - APITokenConnectionAdmin

- Extended the `WorkflowClient.run()` method to accept raw workflow `JSON` strings.

### Bug Fixes

- Updated the maximum API token Time-to-Expire (TTE) to `5` years. Previously, the value was set to `13` years (`409,968,000` seconds), which was reverted to `5` years due to an integer overflow issue in Keycloak. For more details, see [Keycloak Issue #19671](https://github.com/keycloak/keycloak/issues/19671).

### QOL Improvements

- Added support for Python `3.10`, `3.11`, `3.12` and `3.13`.
- Increased the default read timeout for `AtlanClient` to `900` seconds (`15` minutes).

## 4.0.2 (January 22, 2025)

### New Features

- Added the ability to the custom package logger to log unhandled exceptions.
- Added support for creating `OpenLineage` connections (`OpenLineageClient.create_connection()`).

### Bug Fixes

- Fixed handling of deleted `AtlanTagName`s in `Purpose` asset deserialization. Previously, a `ValueError` was raised.

### QOL Improvements

- Added an "Installing for development" section to the `README.md`.
- Removed `pyatlan-codeql.yaml` in favor of using the organization-level CodeQL workflow to avoid configuration conflicts and failures.

## 4.0.1 (January 14, 2025)

### New Features

- Added a new connector type (`CUSTOM`).
- Added support for the `DatabricksCrawler` and `DatabricksMiner` workflow packages.
- Added the `creator()` method for the following assets:
  - `Custom`
  - `Dataverse`
  - `TablePartition`

### Bug Fixes

- Fixed `_user_id` handling issue in `pyatlan.pkg.utils.get_client()`.

### QOL Improvements

- Enhanced test coverage with additional unit tests for the `append_terms`, `replace_terms`, and `remove_terms` methods.

## 4.0.0 (January 7, 2025)

### New Features

- Added support for the `MongoDBCrawler` workflow package.
- Added `creator()` and `updater()` methods for the `Procedure` asset.

### Bug Fixes

- Fixed `WorkflowClient.find_by_type()` method to use regular expressions.
- Fixed `AttributeDef.cardinality` and `AttributeDef.type_name` handling for the new `multi_value_select` attribute option.
- Fixed issues with the `AssetClient.append_terms()`, `remove_terms()`, and `replace_terms()` methods:
  - These methods now use `SaveSemantic.APPEND/REPLACE/REMOVE`, which is more optimized and faster than the previous approach that required full asset retrieval with relationships for updates.
- Fixed `S3Object.create_with_prefix()` and `creator()` to ensure the `s3_bucket_name` field is correctly set.

### Breaking Changes

- The default behavior of `AssetClient.get_by_guid()` and `AssetClient.get_by_qualified_name()` has changed:

  - By default, these methods now ignore relationships during asset retrieval (`ignore_relationships: bool = True`). Previously, this was set to `False`.
  - This change is intentional, aiming to prevent users from retrieving more information than necessary, thereby reducing the overall runtime of requests.
  - Users can now use the `attributes` and `related_attributes` optional parameters to specify the exact details required for each search result. This ensures precise and efficient searches. See:
  [Advanced Examples - Read](https://developer.atlan.com/snippets/advanced-examples/read).

  ```python
  # In this example, we are retrieving the "userDescription" attribute
  # for both the glossary and its terms (related attribute).
  # You can also retrieve other attributes as illustrated below:

  glossary = client.asset.get_by_guid(
        guid="b4113341-251b-4adc-81fb-2420501c30e6",
        asset_type=AtlasGlossary,
        min_ext_info=False,
        ignore_relationships=True,
        attributes=[AtlasGlossary.USER_DESCRIPTION, AtlasGlossary.TERMS],
        related_attributes=[AtlasGlossaryTerm.USER_DESCRIPTION]
    )

  glossary = client.asset.get_by_qualified_name(
      asset_type=AtlasGlossary,
      qualified_name="pXkf3RUvsIOIG8xnn0W3O",
      min_ext_info=False,
      ignore_relationships=True,
      attributes=[AtlasGlossary.USER_DESCRIPTION, AtlasGlossary.TERMS],
      related_attributes=[AtlasGlossaryTerm.USER_DESCRIPTION]
  )
  ```

### QOL Improvements

- Added an [OSV](https://osv.dev) vulnerability-scan workflow job to GitHub Actions.

## 3.1.2 (December 31, 2024)

### New features

- Enabled the use of the `Retry-After` header for handling rate-limit retries.
- Added support for [OpenTelemetry](https://opentelemetry.io) logging in custom packages.
- Added `creator()` methods for Insights assets (`Collection`, `Folder`, `Query`).
- Added support for the following new connector types:
  - ANAPLAN
  - AWS_ECS
  - AWS_BATCH
  - AWS_LAMBDA
  - AWS_SAGEMAKER
  - DATAVERSE

### QOL improvements

- Generated the latest typedef models.
- Upgraded `jinja2` from `3.1.4` to `3.1.5` to address a security vulnerability.
- Fixed pagination assertions in `AuditSearch` unit tests and integration tests.

## 3.1.1 (December 26, 2024)

### Bug fixes

- Fixed a `ValidationError` caused by the private field (`_user_id`) in the `AtlanClient` constructor.

## 3.1.0 (December 26, 2024)

### New features

- Added support for automatic token refresh and retrying API requests upon receiving a `401` (Unauthorized) response.

  To enable this feature, the following constants must be configured:

  **1. Environment variables:**
  For regenerating the bearer access token:
  - `CLIENT_ID` (string)
  - `CLIENT_SECRET` (string)

  **2. Update `AtlanClient` field:**
  - `_user_id` (string, default: `None`): The unique identifier (GUID) of the user that the client impersonates.

  **Example:**
  ```python
  client = AtlanClient()
  client._user_id = "962c8f78-98a7-908f-9ec2-9e5b7ee7a09f"
  ```

### Breaking changes

- Introduced a new pagination approach in `SearchLogClient.search()` called **search log bulk search** (disabled by default). The SDK switches to this search operation automatically if results exceed a predefined threshold (e.g: `10,000` results). Alternatively, users can enable bulk search explicitly by setting `bulk=True` in `SearchLogClient.search()`. This breaking change affects searches that return more than `10,000` results — either the results will now be sorted differently or an error will be thrown.

- `SearchLogClient.search()` method will now raise an `InvalidRequestError` exception in the following scenarios:
  - when bulk search is enabled (`bulk=True`) and any user-specified sorting options are included in the search request.
  - when bulk search is disabled (`bulk=False`), the number of results exceeds the predefined threshold (e.g: `10,000` assets), and any user-specified sorting options are found in the search request.

  _This is because the bulk search approach for search logs ignores user-specified sorting and instead reorders results by the `createdAt` timestamps of log entries to efficiently handle large volumes of search logs._

## 3.0.0 (December 13, 2024)

### New features

- Added a new connector type (`BIGID`).
- Added support for the following options in `Batch` operations:
  - `update_only`: bool (default: `False`)
  - `track`: bool (default: `False`)
  - `case_insensitive`: bool (default: `False`)
  - `table_view_agnostic`: bool (default: `False`)
  - `creation_handling`: `AssetCreationHandling` (default: `AssetCreationHandling.FULL`)
- Added default timeouts (`read`, `connect`) to `AtlanClient`:
  - Total retries: 5
  - `AtlanClient.connect_timeout`: float (default: 30.0 seconds)
  - `AtlanClient.read_timeout`: float (default: 120.0 seconds)
- Added support for a new `parent_type` (`SnowflakeDynamicTable`) in `Column.creator()`.
- Added exposure for source-specific custom attributes (e.g: `Asset.custom_attributes`).
- Added handling for `error_cause` and `backend_error_id` in `ErrorInfo`.

### Bug fixes

- Fixed the generator to correctly handle the naming of the `Asset.DOMAIN_GUIDS` keyword search field.
- Fixed an issue where search pages (`IndexSearchResults` and `AuditSearchResults`) could overrun when the total results are just under the `_MASS_EXTRACT_THRESHOLD`.
- Fixed an issue with timestamp paging returning incomplete results when searching with a small page size (e.g: `2`) and assets with the same creation time.

### QOL improvements

- Generated the latest typedef models.
- Added the `@init_guid` decorator to the `updater()` method of assets to ensure that GUIDs are properly initialized and resolved in batch operations.
- Removed `type_name` validation from `Table`, `View`, and `Materialised View` to make them configurable when running `Batch` operations with `table_view_agnostic=True`.
- Removed deprecated `AssetClient.get_lineage()` integration tests.
- Updated integration test asset constants to align with the new tenant setup.

### Deprecated features

- Removed the deprecated `AssetClient.get_lineage()` method, which is slower and will no longer receive enhancements. Use the `AssetClient.get_lineage_list()` operation instead.

### Breaking changes

- `Batch` now accepts `AtlanClient` as the first parameter, replacing the previous use of `AssetClient`.

- Introduced a new pagination approach in `AuditClient.search()` called **audit bulk search** (disabled by default). The SDK switches to this search operation automatically if results exceed a predefined threshold (e.g: `10,000` results). Alternatively, users can enable bulk search explicitly by setting `bulk=True` in `AuditClient.search()`. This breaking change affects searches that return more than `10,000` results — either the results will now be sorted differently or an error will be thrown.

- `AuditClient.search()` method will now raise an `InvalidRequestError` exception in the following scenarios:
  - when bulk search is enabled (`bulk=True`) and any user-specified sorting options are included in the search request.
  - when bulk search is disabled (`bulk=False`), the number of results exceeds the predefined threshold (e.g: `10,000` assets), and any user-specified sorting options are found in the search request.

  _This is because the audit bulk search approach ignores user-specified sorting and instead reorders results based on the creation timestamps of assets to handle large volumes of assets efficiently._

## 2.7.0 (December 4, 2024)

### QOL improvements

- Renamed `CredentialResponseList` to `CredentialListResponse` to ensure consistent response model naming.
- Updated handling for (`{"records": null}`) in the response to populate the model with an empty list (`[]`) instead of `None`, which is non-iterable.
- Updated `level` and `connection` fields to use `Optional[Union[Dict[str, Any], str]]`, as they can be strings, preventing Pydantic validation errors, eg:

  ```
  "level": "user",
  "connection": "default/bigquery/1234567890"
  ```

## 2.6.2 (December 3, 2024)

### QOL improvements

- Added Column projection support to `group.get_all()`.
- Added retry on http code 429.

## 2.6.1 (November 25, 2024)

### New features

- Added the `"x-atlan-client-origin": "product_sdk"` header to the `AtlanClient`.
- Added a method to retrieve all credentials: `CredentialClient.get_all()`.

### QOL improvements

- Generated the latest typedef models.
  - Application typedef changes:
    - Replaced the `Application` supertype with `App`.
    - Renamed `ApplicationContainer` to `Application`.
    - Changed the level of the relationship from `Catalog` to `Asset`.
    - Updated the name of the de-normalized attribute.
- Added a wait to the integration test fixtures (atlan_tag_test, custom_metadata_test).

## 2.6.0 (November 21, 2024)

### New features

- Added the `creator()` method for `ApplicationContainer`.
- Added a new connector type (`APPLICATION`).
- Added support for a new method (`s3()`) in `TableauCrawler` to fetch metadata directly from S3 bucket extractions.
- Added support for the following CSA custom packages:
  - Asset import
  - Asset export (basic)
  - Relational assets builder
- Added `username` and `extras` fields to the `CredentialResponse` model.

### Bug fixes

- Fixed `Batch._track()` method to handle `AtlasGlossaryTerm` assets correctly.

### QOL improvements

- Fixed several issues related to tag deletion during integration test cleanups (e.g: `purpose_test`, `test_task_client`, and `suggestions_test`).
- Updated various response models in `pyatlan.model.workflow` to use `Optional` fields, ensuring complete capture of API response results.
- Removed `@validate_arguments` from `@overload` methods (`WorkflowClient`: `rerun()`, `add_schedule()`, `remove_schedule()`), as it unintentionally typecast arguments to different types, causing unexpected behavior when model fields were optional. Instead, replaced it with the utility function `validate_type()` to validate argument types in `@overload`ed methods.

## 2.5.8 (November 13, 2024)

### Bug fixes

- Fixed a typo in the IBM_DB2 connector type.

## 2.5.7 (November 13, 2024)

### New features

- Added support for new connector types:
  - IBM_DB2
  - SAP_GIGYA
  - SAP_HYBRIS
  - TREASURE_DATA
  - APACHE_PULSAR
  - ADOBE_TARGET
  - AZURE_ACTIVE_DIRECTORY
  - ADOBE_EXPERIENCE_MANAGER

### QOL improvements

- Generated the latest typedef models.

### Bug fixes

- Fixed generator to handle new core assets in the typedefs.

## 2.5.6 (October 24, 2024)

### Bug fixes

- Fixed `Readme.creator()` to use `asset.trim_to_reference()` instead of sending the complete `asset`, which was somehow breaking backend parsing for related assets.

### QOL improvements

- Generated the latest typedef models.

## 2.5.5 (October 23, 2024)

### Bug fixes

- Fixed `AtlanError` message for unescaped curly braces (`{}`) in `response.text`.

## 2.5.4 (October 22, 2024)

### New features

- Implemented cache management for `Connection` and `SourceTag`.
- Added support for assigning a `SourceTag` with a `value` to an asset.

## 2.5.3 (October 16, 2024)

### Bug fixes

- Added the missing `FluentLineage.includes_on_relations` method and the `LineageListRequest.relation_attributes` field.

### New features

- Added a new connector type (`INRIVER`).
- Added `APIObject`, `APIQuery`, and `APIField` assets, along with their `creator()` methods.
- Added a boolean field `immediate_neighbors` to the `LineageListRequest`, which allows users to include immediate neighbors of the starting `asset` in the response (`True`), or exclude them (`False` - default).

## 2.5.2 (October 11, 2024)

### Bug fixes

- Updated the type of `TableauDatasource.upstream_tables` and `upstream_datasources` to `Optional[List[Dict[str, Optional[str]]]]` to prevent Pydantic validation errors when a dict `value` in this field is mapped to `None`.

### QOL improvements

- Generated the latest typedef models.

## 2.5.1 (October 9, 2024)

### Bug fixes

- Fixed `ModuleNotFoundError` caused by the missing `PyYAML` dependency in the project’s `requirements.txt`.

## 2.5.0 (October 8, 2024)

### New features (experimental)

- Added support for sending `OpenLineage` events.
- Added support for serialization/deserialization (serde) of the `DataContract` spec.

### Breaking changes

- Updated the `ContractClient.generate_initial_spec()` method to directly accept the `asset` for which the initial contract spec is generated, similar to the Java SDK. Previously, you needed to pass the keyword arguments `asset_type` and `asset_qualified_name`.


## 2.4.8 (October 5, 2024)

### New features

- Added new connector types (`IICS`, `ABINITIO`, `SAP_S4_HANA`).

## 2.4.7 (September 30, 2024)

### New features

- Added `CompoundQuery.tagged_with_value()` method to search
for source-synced tags by assigned value eg: Snowflake tags.
- Added `ContractClient.generate_initial_spec()` method to generate
the initial contract specification for the provided asset `typeName` and `qualifiedName`.

### Experimental

- Added initial support for `Span`, `SpanNear`, `SpanWithin`, and `SpanTerm` queries for textual fields.

## 2.4.6 (September 24, 2024)

### New features

- Added a new connector type `MODEL` for data modeling assets.

### QOL improvements

- Generated latest typedefs models (`model`, `anomalo`, `powerbi`).

## 2.4.5 (September 18, 2024)

### New Features

- Added `username` property to the `ApiToken` model.
- Added functions for validating custom package files to `pyatlan.test_utils`.
- Added an optional parameter `asset_selection` to `DataProduct.updater()`, allowing users to update assets within the data product.
- Added the `DataProductsAssetsDSL.get_asset_selection()` method, which returns the asset selection DSL string for a data product based on the specified `IndexSearchRequest`.

### Bug Fixes

- Fixed pagination issues in `AuditSearchResults`.
- Fixed multipart form handling for `AtlanTag` image uploads.

## 2.4.4 (September 10, 2024)

### New features

- Added a new function (`pkg.utils.set_package_headers`) to configure the `AtlanClient` with the required custom package headers using environment variables.

### Bug fixes

- Fixed `pkg.utils.validate_connection()` to include other types (`Connection`, `Dict`).

### QOL improvements

- Moved `nanoid` from the `requirements-dev.txt`.
- Moved common test functions to a separate `test_utils` package.

## 2.4.3 (September 04, 2024)

### New features

- Added a new connector type `DM` for data modeling assets.

## 2.4.2 (August 28, 2024)

### New features

- Added support for `GCS` presigned URL file uploads.
- Added the `find_run_by_id` method to the `WorkflowClient`.

### QOL improvements

- Generated the latest typedef models.
- Added `pyatlan` to the Conda packages.

### Bug fixes

- Fixed the interpretation of `text-only` indexed fields for assets.

## 2.4.1 (August 12, 2024)

### New features

- Added support for `Azure Blob` presigned URL file uploads.

### QOL improvements

- Replaced `pyatlan.utils.HTTPStatus` with the standard library `http.HTTPStatus` (introduced in **Python 3.4**).

## 2.4.0 (August 06, 2024)

### QOL improvements

- **Implemented lazy imports for `pyatlan.model.assets`:** This change reduces the import time for assets by deferring the import of modules until they are actually needed. As a result, users will experience faster startup times and reduced memory usage when working with assets.

### Bug fixes

- Fixed missing check for `asset.guid` in the `Readme.creator()` method, which caused issues with updating `Readme` assets when the asset was passed using `Asset.ref_by_qualified_name()` instead of `Asset.ref_by_guid()`. The SDK now throws a `ValueError` if `asset.guid` is missing in the `Readme.creator()` method to prevent these issues.

## 2.3.3 (July 23, 2024)

### New features

- Added support for nested aggregations.
- Added support for trident suggestions.
- Added `Superset` assets `creator()` methods.

## 2.3.2 (July 16, 2024)

### New features

- Added a new ELT connector type: `PREFECT`.

### Bug fixes

- Fixed the `ErrorCode.CM_ATTR_NOT_FOUND_BY_NAME` error message in `CustomMetadataCache.get_attr_id_for_name()`, which was receiving the wrong parameters.

## 2.3.1 (July 9, 2024)

### New features

- Added `WorkflowClient.find_by_id()` method for workflow search/retrieval.

### OQL improvements

- Made `AtlanError` messages more descriptive.

## 2.3.0 (June 19, 2024)

### Breaking changes

- Introduced a new pagination approach in `AssetClient.search()` and `FluentSearch.execute()` called **bulk search** (disabled by default). It minimizes system impact when handling large result sets. The SDK switches to this search operation automatically if results exceed a predefined threshold (i.e: `100,000` results). Alternatively, users can enable bulk search explicitly by setting `bulk=True` in `AssetClient.search()` or `FluentSearch.execute()`. The breaking change is in regards to searches that return more than `100,000` results — either the results will now be sorted differently or an error will be thrown.

- The `AssetClient.search()` and `FluentSearch.execute()` methods will now raise an exception (`InvalidRequestError`) in the following scenarios:

  - when bulk search is enabled (`bulk=True`) and any user-specified sorting options are found in the search request.

  - when bulk search is disabled (`bulk=False`), the number of results exceeds the predefined threshold (i.e: `100,000` assets), and any user-specified sorting options are found in the search request.

  _This is because the bulk search approach ignores user-specified sorting and instead reorders the results based on the creation timestamps of assets to handle large numbers of assets efficiently._

### QOL improvements

- Pinned `urllib3>=1.26.0,<3` and moved `networkx` to the dev requirements to avoid potential version mismatches.

## 2.2.4 (June 11, 2024)

### New features

- Added the `creator()` method for `DataContract`.
- Overloaded the `creator()` methods to explicitly handle ancestral `qualified_name` and `name`. This enhancement allows users to create objects when the ancestral asset name contains `/`, which `creator()` was previously unable to handle.

### QOL improvements

- Generated the latest typedef models.
- Updated the latest set of Phosphor icons in the `AtlanIcon` enum.

## 2.2.3 (June 4, 2024)

### New features

- Added thread lock to cache methods (`get_cache()` and `_refresh_cache()`).
- Added support for the `Connection Delete` package.
- Added support for custom metadata handling for data domains and products.

### QOL improvements

- Generated the latest typedef models (`DatabricksUnityCatalogTag`).
- Updated `AtlanError` to include `user_action` when throwing an exception.

## 2.2.2 (May 28, 2024)

### New features

- Added creator methods to `Kafka` and `AzureEventHub` assets.
- Added support for `includeClassificationNames` in `IndexSearchRequest`.
- Expanded the functionality of the `WorkflowClient` with new methods for scheduled query workflows.

### Bug fixes

- Fixed the `AtlasGlossaryCategory.trim_to_required()` method to use `updater()` instead of `create_for_modification()`.

### QOL improvements

- Generated the latest typedef models, including `Workflow` and `WorkflowRun`.
- Updated the SSO provider in `test_sso_client.py` to check for `JUMPCLOUD` instead of `AZURE_AD`.
- Updated the Pydantic dependency (`pydantic>=2.0.0,<3.0.0`) to provide more flexibility for users.

## 2.2.1 (May 21, 2024)

### New features

- Added `find_domain_by_name()` and `find_product_by_name` methods to `AssetClient` to find data mesh objects by their human-readable names.
- Modified the type of the `attributes` and `related_attributes` keyword parameters in `asset.get_hierarchy()` to accept `str` in addition to `AtlanField`.

### Bug fixes

- Fixed issues with data domain and data product creation.
- Added the `AtlanConnectorType.get_connector_name()` method, which handles connection qualified name validation for assets and returns the connector name. Previously, this logic was repeated in most Asset `creator()` methods, which sometimes resulted in the `connector_name` field being mistakenly omitted (this bug was found in the `File` asset).

### QOL improvements

- Added data mesh integration tests.
- Added a fallback delete mechanism for API tokens in tests.
- Generated the latest typedef models, such as `Cognos`, `Stakeholder`, etc.

## 2.2.0 (May 15, 2024)

### Breaking changes

- Fixes typos and docstrings in IAM role methods of the `DynamoDB` and `PostgreSQL` crawlers. Previously, the method name was `iam_user_role_auth` instead of `iam_role_auth`.

## 2.1.9 (May 14, 2024)

### New features

- Added support for `BigQuery`, `DynamoDB` and `Postgres` crawlers.

### Bug fixes

- Fixed logic in the `Referenceable` model to determine the correct subtype.

### QOL improvements

- Utilized generated atlas core enums in the import template.
- Added a shell script (`pyatlan-formatter`) capable of handling code formatting for both tracked and untracked files.

## 2.1.8 (May 8, 2024)

### New features

- Added support for `Snowflake Miner`.
- Introduced new connector types: `COGNITE`, `SYNDIGO`, `NETEZZA`, and `AZURE_SERVICE_BUS`.
- Added an optional `depth` field to indicate the asset's depth within lineage in the `Referenceable` model.
- Added an optional parameter (`related_attributes`) to the `get_hierarchy()` method, allowing users to specify a list of attributes to retrieve for each related asset in the hierarchy.
- Expanded the functionality of the `WorkflowClient` with new methods for scheduling, stopping, and deleting workflows.

### QOL improvements

- Upgraded `jinja2` from `3.1.3` to `3.1.4` to address a security vulnerability: [GHSA-h75v-3vvj-5mfj](https://github.com/advisories/GHSA-h75v-3vvj-5mfj).

## 2.1.7 (April 30, 2024)

### New features

- Adds `FileClient` for uploading and downloading files from Atlan's tenant object storage via presigned URLs.

## 2.1.6 (April 23, 2024)

### New features

- Adds support for SSO group mapping.
- Adds `AtlanSSO` to enumerate the options for supported Atlan's SSO providers.

## 2.1.5 (April 18, 2024)

### Bug fixes

- Fixed an issue where explicit assignment of `None` to asset attributes in `BulkRequest` within the `client.asset.save()` method resulted in exclusion from the request payload.
- Fixed issues with **multiple remove/append relationships** where values were being overwritten inside append/remove dictionaries.

## 2.1.4 (April 16, 2024)

### New features

- Adds `AssetFilterGroup` enum for persona personalization.
- Adds creator method to `AirflowDag` and `AirflowTask` assets.

### Bug fixes

- Fixes `qualified_name` population for related entities in `Glossary` objects.
- Fixes logic for removing parent category relationship in `AtlasGlossaryCategory`.
- Fixes lineage list performance by considering the `hasMore` attribute to optimize lineage paging.

### QOL improvements

- Updates `networkx >= 3.1` and bumped development requirements to the latest version.

## 2.1.3 (April 3, 2024)

### Bug fixes

- Fixes field alias typo for `restrict_propagation_through_hierarchy` in the `AtlanTag` model.
- Fixes issues with `AtlanEvent` model deserialization. Previously, it threw a `ValidationError` for `ENTITY_DELETE`, `CLASSIFICATION_ADD`, and `CLASSIFICATION_DELETE` events.

## 2.1.2 (April 2, 2024)

### New features

- Adds `atlanMetadata` icon to `AtlanIcon` enum.
- Adds support for `restrict_propagation_through_hierarchy` to the `AtlanTag` model.
- Adds latest typedef models **(cube, cognite, spark, sparkjob, and multi-dimensional dataset)**.
- Adds support to limit the applicability of custom metadata attributes directly through the `AttributeDef.create()` method.

### Bug Fixes

- Fixes an issue with direct model deserialization of structs.

## 2.1.1 (March 28, 2024)

### Bug Fixes

- Fixes an issue where certain structs could cause errors during marshalling and unmarshalling.
- Fixes `Process.generate_qualified_name()` method to ensure that the generated process `qualified_name` includes the connection prefix. Previously, it only used the MD5 hash as the `qualified_name` for the `Process`.

## 2.1.0 (March 27, 2024)

### New features

- Adds `EnumDef.update()` method to update an existing enumeration with more valid values.
- Adds `get_by_name()` method to the `TypeDefClient` to retrieve a specific type definition from Atlan.
- Adds `propagation_only_through_lineage` field to the `AtlanTag`, allowing users to specify that
propagation will only occur downstream in the lineage and not within the hierarchy.

### Breaking changes

- `EnumCache.get_by_name()` method now raises `NotFoundError` if the enumeration with the given name does not exist. Previously the method would only return `None` in case the enumeration did not exist, rather than raising an error.

### QOL improvements

- Bump pre-commit black from `23.7.0` to `24.3.0` (Fixes [CVE security vulnerability](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-21503)).

## 2.0.4 (March 22, 2024)

### New features

- Adds model field (`__atlan_extra__`) to the `AtlanObject` model to accommodate extra properties from API responses.
- Adds an optional parameter (`return_info`) to the user creation method, allowing control over whether to return the list of created users or not.
- Adds an optional parameter (`exclude_users`) to the `SearchLogRequest` methods for excluding specific user data from search log results.

### Bug fixes

- Fixes issues related to creating data domains and data products.

### QOL improvements

- Bump black from `23.7.0` to `24.3.0` (Fixes [CVE security vulnerability](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-21503)).

## 2.0.3 (March 15, 2024)

### New features

- **(Experimental)** Adds support for `Sigma` and `SQL Server` crawlers.
- Adds AWS IoT connector types: `AWS_SITE_WISE` and `AWS_GREENGRASS`.
- Adds credential widget to package toolkit.

### Bug fixes

- Fixes `to_dict` method handling of `Range` queries for `datetime` attributes.
- Fixes `UserClient` create method throwing 500 (internal server error).

### QOL improvements

- Sets `asset_type` keyword argument default value to `Asset` in `get_by_guid` and `retrieve_minimal` methods.

## 2.0.2 (March 5, 2024)

### New features

- **(Experimental)** Adds the ability to search the background tasks queue.
- Adds the missing connector type for `MICROSTRATEGY`.

### Bug fixes

- Replaces spaces with underscores in generated enums.

## 2.0.1 (February 27, 2024)

### New features

- Adds pagination to listings for **user**, **group**, and **membership**.

### Bug fixes

- Fixes `LineageListResults` not including custom metadata.
- Avoid throwing `ValidationError` when aggregating an index search with no results.

### QOL improvements

- Improves the tests report experience by using pytest plugins (`pytest-sugar` and `pytest-timer`).

## 2.0.0 (February 22, 2024)

### New features

- Migrates to Pydantic 2.6
- Allows use of Python 3.8 as a minimum version supported by the SDK
- Adds file connector as a new connector type
- Adds Essbase connector as a new connector type
- Allows fluent lineage conditions to be configured for combining (AND) or any (OR)
- Adds an option to rerun workflows idempotently

### Breaking changes

Since this is a new major release, there are some breaking changes:

- The move to Pydantic 2.6 means we have a dependency on a different major release of this library than previously. We do not believe it will impact your use of any of our methods; however, it could impact you if you rely on Pydantic v1 elsewhere in your codebase and are not yet ready to move to Pydantic v2 yourself.
- The `find_personas_by_name`, `find_purposes_by_name` and `find_connections_by_name` methods previously returned an empty list if no requested object were found, despite being documented as throwing a `NotFoundError` in such cases. We have now made this consistent with the other `find_.._by_name` methods, so if a requested object does not found it will now throw a `NotFoundError`.
- To create consistency across our SDKs, we are also introducing new asset creation and modification methods. This is to reserve the use of verbs in a method name for server-side interactions (like `save`, `find`, etc) and instead use non-verbs to indicate that you are creating an instance of an object purely in-memory — but that it still needs to be acted upon (`save`d) in order to be persisted to Atlan. These offer identical functionality to the prior methods, and we will keep the prior methods around until at least the next major release but simply mark them as deprecated. (So no immediate change to any existing code should be needed.)

    | Old method | New method |
    |---|---|
    | `create()` | `creator()` |
    | `create_for_modification()` | `updater()` |

## 1.9.4 (February 13, 2024)

### New features

- Adds a way to specify replace, append, or removal of individual relationships during `save` operations

### Bug fixes

- Adds missing changes to code generation templates
- Corrects an erroneous use of the inverse operator

## 1.9.3 (January 30, 2024)

### Bug fixes

- raise exception if tag in query in FluentSearch does not exist
- (Experimental) fix defects custom package generation

### QOL Improvements

- add api to assign a token to a purpose
- add api to enable running sql queries

## 1.9.2 (January 24, 2024)

### Bug fixes

- Fix problem with AssetUpdatePayload not being returned from AtlanEvent
- Fix problem with sort order for AuditSearchRequest

## 1.9.1 (January 23, 2024)

### QOL Improvements

- Make `aws_arn` optional in S3 models
- Change default S3 file in package toolkit
- Update docstrings in package toolkit
- Add workflow `update` method
- Adds QA checks (black, flake8, mypy) to the CI
- Bump jinja2 from 3.1.2 to 3.1.3
- Add missing regex and wildcard methods to the `KeywordField`

### Bug fixes

- Make sure the name of the python file generated by the package toolkit does not contain any special characters
- Correct the description of fields in the `AttributeDef` model


## 1.9.0 (January 16, 2024)

### New Features

- Add ability to update certificate, announcement for GlossaryTerm and GlossaryCategory
- Add `create` method for `ColumnProcess`
- Always include sort by `GUID` as final criteria in `IndexSearch`
- (Experimental) Add classes to support custom package generation

### QOL Improvements

- Add an additional parameter to `create` method of `ADLSObject`
- Add type checking to AtlanClient save and other methods

## 1.8.4 (January 4, 2024)

### New Features

- Add credential management

### Bug fixes

- Fix workflow client monitor method
- Fix problem where Python SDK was not initializing applicableConnections and applicableGlossaries when creating new custom metadata sets
- Fix handling of archived custom metadata attributes

## 1.8.3 (December 27, 2023)

### New Features

- (Experimental) Define and run new workflows
- Added support for retrieval of `SourceTagAttachements` in `AtlanTags`

### Bug fixes

- Fix duplicate initial GUID on Windows. This was due to a lack of support for nano-second accuracy in timestamps in Python on Windows. Code has been changed to rectify this problem.

## 1.8.2 (December 21, 2023)

### New Features

### Bug fixes

- Fix problem parsing assets that contain SourceTagAttachements

### QOL improvements


## 1.8.1 (December 19, 2023)

### New Features

- Add support for search log access

### Breaking changes

### Bug fixes

- Modify constants like Referenceable.TYPE_NAME to use InternalKeywordField, InternalKeywordTextField or InternalNumericField
- Fix groups in purpose policies and remove data mesh slugs and abbreviations
- Added missing "templates" field to the WorkflowSpec model

### QOL improvements

- Change qualifiedName generation on Link to be deterministic

## 1.8.0 (December 13, 2023)

### New features

### Breaking changes

- `Asset.create_for_modification` now raises an exception. The `create_for_modification` method should not be invoked on the `Asset` class. Instead `create_for_modification` should be invoked on the class of the asset to be created, for example `Table.create_for_modification`.

### Bug fixes

- An exception was being raised when `client.asset.replace_custom_metadata` was invoked on a custom metadata set that contained archived attributes.
- The `ADLSObject.create()` was missing the parameter for `adls_account_qualified_name`. This was causing the `ADSLObject` to be displayed incorrectly in the UI.

### QOL improvements


## 1.7.0 (December 1, 2023)

### New features

- (Experimental) Adds initial support for data domains and data products

### Breaking changes

- Disables the `delete_by_guid()` and restore methods for categories. Categories can currently only be purged (hard-deleted), so even when previously calling the `delete_by_guid()` method the backend actually translated this to a hard-delete (purge). (Which also means there is no way to restore a category.) We have therefore opted to disable the `delete_by_guid()` and restore methods — only for categories — to make it clearer that categories can only be purged (hard-deleted).

### Bug fixes

- Fixes error shown on retry overrun to show the underlying error, not the retry limit
- Fixes a message that was logged as an error but was purely informational (debug-level)

### QOL improvements

- Adds a unique request ID to every request, and includes in logging
- Logging is now done in both plain text and JSON
- Bundles a reasonable default logging configuration to the base container image

### Background changes

- Consolidates Python-based code repositories into a single place

## 1.6.4 (November 21, 2023)

### Deprecations
* None
### Bug Fixes
* Fix problem with source_read_top_user_record_list not being read correctly in index search
* Correct problem with AuditSearch mis-identifying asset as deleted tag
### QOL Improvm
* Update enums with latest changes to persona preferences
* Bundle logging.conf file in Docker image
* Add ability to set icon during glossary creation

## 1.6.3 (November 14, 2023)

* Changed to support new custom metadata payload
* Add methods to manage Preset Assets
* Add in-cluster optimisation to use services URLs directly
* Changes the logic for generating Google Data Studio asset qualifiedNames

## 1.6.2 (November 7, 2023)

* Add filter to redact HTTP authorization header
* Add ability to traverse glossary hierarchy
* Publish docker image on release

## 1.6.1 (November 3, 2023)

* PARENT_CATEGORY of Glossary had the wrong atlan_field_name

## 1.6.0 (November 1, 2023)

* Rename exclude_classifications to exclude_atlan_tags in FluentLineage

## 1.5.0 (October 31, 2023)

* Add FluentLineage an abstraction mechanism, to simplify the most common lineage requests against Atlan (removing the need to understand the guts of Elastic).
* Add support for management of Google Data Studio assets

## 1.4.2 (October 30, 2023)

* Fix bug causing token_client.get_by_id to fail when when deprecated personas section present

## 1.4.1 (October 25, 2023)

* Fix bug causing client.user.add_as_admin to fail
* Add create methods for GCSBucket and GCSObject

## 1.4.0 (October 19, 2023)

* Create new helper client classes:
  * AdminClient
  * AssetClient
  * Add property atlan_tag_names to assets to provide human readable versions of classificationNames
  * Added Batch class for managing bulk updates in batches.

## 1.3.3 (October 12, 2023)

* Create new helper client classes:
  *  GroupClient
  *  RoleClient
  *  TokenClient
  *  TypeDefClient
  *  UserClient
* Add custom pre-commit hook
* Additional optional parameters for index searc
* Add capability to manage API Assets


## 1.3.2 (October 10, 2023)

* Fix bug preventing classifications with unexpected attributes from being read

## 1.3.1 (October 6, 2023)

* Fix bug preventing custom metadata from being read that were written with locked bug

## 1.3.0 (October 5, 2023)

* Correct issue with incorrect type on purpose_atlan_tags of Purpose
* Added support for searching audit logs
* Fixed bug preventing creation of locked custom metadata
* Fully-validate connection parameters on save
* Adds emojis and icons for both tags and custom metadata
* Fix bug on validating (internal) group names
* Manage ADLS assests
* Makes all options in AttributeDefs optional

## 1.2.0 (September 26, 2023)

* Add capability to do bucket and metric aggregations
* Mark lineage method (and others) deprecated, including DeprecationWarning

## 1.1.0 (September 20, 2023)

* Add capability to find and re-run workflows
* Fix Range query with 0 not generating expected request
* Adds Matillion, MongoDB, and time granularity for custom metadata
* Generates Sphinx documentation for the SDK
* Adds an API token check as part of cache refreshes

## 1.0.0 (September 13, 2023)
* Initial production release
* Adds column projections for listing users
* Renamed register_client method to set_default_client from AtlanClient
* Removed reset_default_client from AtlanClient

## 0.8.0 (September 11, 2023)
* Improve retry strategy for HTTP
* Adds generators for developer portal docs
* Adds create helper for Links
* Fixes bug in adding API tokens as admins and viewers
* Removes ability to activate and deactivate users
* Refactored Exception hierarchy

## 0.7.0 (September 4, 2023)
* Upgrade to pydantic 1.10.12

## 0.6.3 (August 31, 2023)
* Add ability to get, create and modify API tokens

## 0.6.2 (August 24, 2023)
* Fix bug in generating field class vars

## 0.6.1 (August 23, 2023)
* Adds a new FluentSearch approach to searching (no need to know Elastic anymore)
* Changes default inclusion operation for Bool queries to filter rather than must (for efficiency)

## 0.6.0 (August 17, 2023)
* Added:
  * Adds new purpose policy permissions (attaching / detaching terms from assets)
  * Fixes type for decentralized_role
  * Documents various public methods in client, caches, and event-handling classes
  * Add code generation for enums from enum-defs
  * split assets into multiple modules
  * Initial support for an X-Atlan-Request-Id header
* Breaking changes
  * find_category_by_name[_fast] now return a list of categories rather than a single category, since categories are not unique by name within a glossary.

## 0.5.0 (August 10, 2023)
* Added:
  * Bulk delete
  * Restore
  * Search by certificate
  * Activate / deactivate users
  * Search by any of multiple types
* regenerates model to include latest assets and structs
* Breaking change:
  * S3_bucket_qualified_name is now required for S3 object creation

## 0.4.3 (August 7, 2023)

* Add a creation-only semantic operation, and deprecate upsert in favour of save
*
## 0.4.2 (July 25, 2023)

* Add Alteyx to AtlanConnectorType enums

## 0.4.1 (July 24, 2023)

* Correct issue where custom metadata wasn't being returned after the first page in mult-page index search
* Avoid double zipping when producing lambda layer in build
* Correct problem with indexing error
* Removed redundant code related to custom metadata
* Add handling for log events
* Add constant for archived asset retrieval

## 0.4.0 (July 5, 2023)

* Pin dependency on pydantic==1.10.8
* Facilitate inclusion of custom metadata in index search
* Change lineage list response into a lazy-fetching generator

## 0.3.0 (July 3, 2023)

* Renamed AtlanClassificationColor to AtlanTagColor

## 0.2.0 (June 30, 2023)

* Renamed all references to Classification and classification to Tag and tag (TagDef, Tag, tags, tagNames, etc):
* Add ability to create Files as an asset directly on Atlan.
* Add Event-handling abstractions
* Add the following methods to pyatlan.client.atlan.AtlanClient
  * find_glossary_by_name
  * find_category_fast_by_name
  * find_category_by_name
  * find_term_fast_by_name
  * find_term_by_name

## 0.1.3 (June 19, 2023)

* Adds new persona and purpose policy handling
* Added trim_to_required method to assets

## 0.1.2 (June 14, 2023)

* Set status to Active when Badge is created

## 0.1.1 (June 12, 2023)

* Adds icons and images for classifications
* Migrates to easier to use uniqueness generator for testing
* Refactor Integration Tests to work on any server
* Remove incorrect required field validations for Connection


## 0.1.0 (June 6, 2023)

* Fixes connection creation and associated validations
* Adds further connectors (with icons)
* Adds SQL parser endpoint
* Add Lineage list API and integration tests
* Fix bug on locking custom metadata
* Refactor syntax for accessing custom metadata properties

  Previously the custom metadata property `First Name` would have been accessed as follows:
    ````cm.first_name````

  This could cause confusion how the name was converted so now the following syntax will be used:

    ```cm['First Name']```
## 0.0.33 (May 24, 2023)

* Added convenience properties for relationship_attributes
* Rename convenience property for glossary terms from terms to assigned_terms

* Add create method to Badge
* Add integrations tests for CustomMetaData

## 0.0.31 (May 15, 2023)

* Added the following classes to support lineage retrieval
  * LineageRelation
  * DirectedPair
  * LineageGraph
  * LineageResponse
* Added the get_lineage method to AtlanClient
* Modify create_typdef in client to handle creating EnumDef
* Refresh caches on any SDK-driven creates or deletes

## 0.0.30 (May 11, 2023)

* Fix problem where custom metadata created via the SDK failed to show up in the UI

## 0.0.29 (May 11, 2023)

* Fix problem where custom metadata created via the SDK failed to show up in the UI

## 0.0.28 (May 9, 2023)

* Add find_connections_by_name to AtlanClient

## 0.0.27 (May 8, 2023)

* Add a create method to Process

## 0.0.26 (May 4, 2023)

* Add remove_terms method to AtlanClient
* Add append_terms method to AtlanClient
* Add replace_terms method to AtlanClient

## 0.0.25 (May 2, 2023)

* Update create method for Readme asset

## 0.0.24 (Apr 27, 2023)

* Fix broken link in README.md

## 0.0.23 (Apr 27, 2023)

* Renamed get_business_attributes method get_custom_metadata in Referenceable.Attributes
* Renamed set_business_attributes method set_custom_metadata in Referenceable.Attributes
* Renamed BusinessAttributes to CustomMetadata
* Add parameter overwrite_custom_metadata to AtlanClient.upsert
* Add get_custom_metadata to CustomMetadataCache
* Update create functions

## 0.0.22 (Apr 12, 2023)

* Added create method to Column
* Updated Schema.create method to add schema to Database schemas collection
* Updated Table.create method to add table to Schema tables collection

## 0.0.21 (Apr 11, 2023)

* Added relation_attributes parameter to IndexSearchRequest to specify the attributes to be included in each relationship that is included in the results of the search
* Set assets to empty list when no entities are returned by search
* Add classmethod ref_by_guid to Referencable
* Add classmethod ref_by_qualified_name to Referencable

## 0.0.20 (Apr 5, 2023)

* Corrected issue with from, size and track_total_hits in DSL object not being sent to server if the defaults weren't changed
* Added relation_attributes parameter to IndexSearchRequest to specify the attributes to be included in each relationship that is included in the results of the search

## 0.0.19 (Mar 30, 2023)

* Renamed environment variable used to specify the Atlan URL from ATLAN_HOST to ATLAN_BASE_URL
* Renamed initialization parameter in pyatlan.client.atlan.AtlanClient from host to base_url

## 0.0.18 (Mar 27, 2023)

* Added workflow to run code scan with [CodeQl](https://codeql.github.com/)
* Added workflow to upload to [pypi](https://pypi.org) on release

## 0.0.17 (Mar 22, 2023)

* Initial public release
