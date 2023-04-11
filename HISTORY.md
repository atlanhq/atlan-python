## 0.0.21 (Apr 11, 2023)

* Added relation_attributes parameter to IndexSearchRequest to specify the attributes to be included in each relationship that is included in the results of the search
* Set assets to empty list when no entities are returned by search
* Add classmethod ref_by_guid to Referencable

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
