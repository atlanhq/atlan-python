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
