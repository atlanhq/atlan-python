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
