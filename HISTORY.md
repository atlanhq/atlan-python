## 1.6.0 (November 2, 2023)

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
