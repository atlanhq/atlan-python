# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from abc import ABC
from datetime import date
from enum import Enum
from typing import List, Union, overload

from pydantic.v1 import StrictBool, StrictFloat, StrictInt, StrictStr

from pyatlan.errors import ErrorCode
from pyatlan.model.aggregation import Aggregation
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlanComparisonOperator, SortOrder
from pyatlan.model.search import (
    Exists,
    Match,
    Prefix,
    Query,
    Range,
    Regexp,
    SearchFieldType,
    SortItem,
    Term,
    Terms,
    Wildcard,
)
from pyatlan.model.typedef import AttributeDef
from pyatlan.utils import ComparisonCategory, is_comparable_type


class AtlanField(ABC):
    """
    Base enumeration of all attributes that exist in Atlan, so you do not have to remember their
    exact spelling or capitalization.
    """

    atlan_field_name: StrictStr


class RelationField(AtlanField):
    """
    Represents any field used to capture a relationship in Atlan, which is not inherently
    searchable.
    """

    def __init__(self, atlan_field_name: StrictStr):
        """
        Default constructor.

        :param atlan_field_name: name of the attribute in the metastore
        """
        self.atlan_field_name = atlan_field_name


class SearchableField(AtlanField):
    """
    Base class for any field in Atlan that can be searched.
    """

    elastic_field_name: StrictStr

    def __init__(self, atlan_field_name: StrictStr, elastic_field_name: StrictStr):
        """
        Default constructor.

        :param atlan_field_name: name of the attribute in the metastore
        :param elastic_field_name: name of the field in the search index
        """
        self.atlan_field_name = atlan_field_name
        self.elastic_field_name = elastic_field_name

    @property
    def internal_field_name(self):
        return self.atlan_field_name

    def has_any_value(self) -> Query:
        """
        Returns a query that will only match assets that have some non-null, non-empty value
        (no matter what actual value) for the field.

        :returns: a query that will only match assets that have some non-null, non-empty value for the field
        """
        return Exists(field=self.elastic_field_name)

    def order(self, order: SortOrder = SortOrder.ASCENDING) -> SortItem:
        """
        Returns a condition to sort results by the field, in the specified order.

        :param order: in which to sort the results
        :returns: sort condition for the field, in the specified order
        """
        return SortItem(field=self.elastic_field_name, order=order)

    def bucket_by(
        self,
        size: int = 10,
    ) -> Aggregation:
        """Return criteria to bucket results based on the provided field.
           :param size: the number of buckets to include results across.
           :returns: criteria to bucket results by the provided field, across a maximum number of buckets defined by
           the provided size
        */"""
        return Aggregation(
            __root__={"terms": {"field": self.elastic_field_name, "size": size}}
        )


class BooleanField(SearchableField):
    """
    Represents any field in Atlan that can be searched only by truthiness.
    """

    def __init__(self, atlan_field_name: StrictStr, boolean_field_name: StrictStr):
        """
        Default constructor.

        :param atlan_field_name: name of the attribute in the metastore
        :param boolean_field_name: name of the bool field in the search index
        """
        super().__init__(atlan_field_name, boolean_field_name)

    @property
    def boolean_field_name(self) -> str:
        """
        Returns the name of the boolean field index for this attribute in Elastic.

        :returns: the field name for the boolean index on this attribute
        """
        return self.elastic_field_name

    @property
    def in_lineage(self) -> "LineageFilterFieldBoolean":
        """Returns a proxy which can be used a lineage filter with the appropriate subset of conditions"""
        return LineageFilterFieldBoolean(self)

    def eq(self, value: StrictBool) -> Query:
        """
        Returns a query that will match all assets whose field has a value that exactly equals
        the provided boolean value.

        :param value: the value (bool) to check the field's value is exactly equal to
        :returns: a query that will only match assets whose value for the field is exactly equal to the boolean value
                  provided
        """
        return Term(field=self.boolean_field_name, value=value)


class KeywordField(SearchableField):
    """
    Represents any field in Atlan that can be searched only by keyword (no text-analyzed fuzziness).
    """

    def __init__(self, atlan_field_name: StrictStr, keyword_field_name: StrictStr):
        """
        Default constructor.

        :param atlan_field_name: name of the attribute in the metastore
        :param keyword_field_name: name of the keyword field in the search index
        """
        super().__init__(atlan_field_name, keyword_field_name)

    @property
    def keyword_field_name(self) -> str:
        """
        Returns the name of the keyword field index for this attribute in Elastic.

        :returns: the field name for the keyword index on this attribute
        """
        return self.elastic_field_name

    @property
    def in_lineage(self) -> "LineageFilterFieldString":
        """Returns a proxy which can be used a lineage filter with the appropriate subset of conditions"""
        return LineageFilterFieldString(self)

    def startswith(self, value: StrictStr, case_insensitive: bool = False) -> Query:
        """
        Returns a query that will match all assets whose field has a value that starts with
        the provided value. Note that this can also be a case-insensitive match.

        :param value: the value (prefix) to check the field's value starts with
        :param case_insensitive: if True, will match the value irrespective of case, otherwise will be a case-sensitive
                                 match
        :returns: a query that will only match assets whose value for the field starts with the value provided
        """
        return Prefix(
            field=self.keyword_field_name,
            value=value,
            case_insensitive=case_insensitive,
        )

    def eq(self, value: StrictStr, case_insensitive: bool = False) -> Query:
        """
        Returns a query that will match all assets whose field has a value that exactly matches
        the provided string value.

        :param value: the value (string) to check the field's value is exactly equal to
        :param case_insensitive: if True, will match the value irrespective of case, otherwise will be a case-sensitive
                                 match
        :returns: a query that will only match assets whose value for the field is exactly equal to the value provided
        """
        return Term(
            field=self.keyword_field_name,
            value=value,
            case_insensitive=case_insensitive,
        )

    def within(self, values: List[str]) -> Query:
        """
        Returns a query that will match all assets whose field has a value that exactly matches
        at least one of the provided string values.

        :param values: the values (strings) to check the field's value is exactly equal to
        :returns: a query that will only match assets whose value for the field is exactly equal to at least one of
                  the values provided
        """
        return Terms(field=self.keyword_field_name, values=values)

    def wildcard(self, value: StrictStr, case_insensitive: bool = False) -> Query:
        """
        Returns a query that retrieves assets whose attribute value matches the
        provided wildcard pattern. This function is particularly useful for searching
        based on simple naming conventions.

        :param value: The wildcard pattern to match against the asset's attribute value.
        :param case_insensitive: If `True`, performs a case-insensitive match. Defaults to `False`.
        :return: A query that matches assets with the specified wildcard pattern for the designated attribute.
        """
        return Wildcard(
            field=self.keyword_field_name,
            value=value,
            case_insensitive=case_insensitive,
        )

    def regexp(self, value: StrictStr, case_insensitive: bool = False) -> Query:
        """
        Returns a query that retrieves assets whose attribute value matches the
        provided regular expression. This function is particularly useful for
        searching based on more complicated naming conventions.

        :param value: The regular expression to match against the asset's attribute value.
        :param case_insensitive: If `True`, performs a case-insensitive match. Defaults to `False`.
        :return: A query that matches assets with the specified regex pattern for the designated attribute.
        """
        return Regexp(
            field=self.keyword_field_name,
            value=value,
            case_insensitive=case_insensitive,
        )


class TextField(SearchableField):
    """
    Represents any field in Atlan that can only be searched using text-related search operations.
    """

    def __init__(self, atlan_field_name: StrictStr, text_field_name: StrictStr):
        """
        Default constructor.

        :param atlan_field_name: name of the attribute in the metastore
        :param text_field_name: name of the text field in the search index
        """
        super().__init__(atlan_field_name, text_field_name)

    @property
    def text_field_name(self) -> str:
        """
        Returns the name of the text field index for this attribute in Elastic.

        :returns: the field name for the text index on this attribute
        """
        return self.elastic_field_name

    @property
    def in_lineage(self) -> "LineageFilterFieldString":
        """Returns a proxy which can be used a lineage filter with the appropriate subset of conditions"""
        return LineageFilterFieldString(self)

    def match(self, value: StrictStr) -> Query:
        """
        Returns a query that will textually match the provided value against the field. This
        analyzes the provided value according to the same analysis carried out on the field
        (for example, tokenization, stemming, and so on).

        :param value: the string value to match against
        :returns: a query that will only match assets whose analyzed value for the field matches the value provided
                  (which will also be analyzed)
        """
        return Match(
            field=self.text_field_name,
            query=value,
        )


class InternalKeywordField(KeywordField):
    """
    Represents any field in Atlan that can be searched only by keyword (no text-analyzed fuzziness), and can also be
    searched against a special internal field directly within Atlan.
    """

    _internal_field_name: StrictStr

    def __init__(
        self,
        atlan_field_name: StrictStr,
        keyword_field_name: StrictStr,
        internal_field_name: StrictStr,
    ):
        """
        Default constructor.

        :param atlan_field_name: name of the attribute in the metastore
        :param keyword_field_name: name of the keyword field in the search index
        :param internal_field_name: internal name of the internal searchable attribute in the metastore
        """
        super().__init__(atlan_field_name, keyword_field_name)
        self._internal_field_name = internal_field_name

    @property
    def internal_field_name(self):
        return self._internal_field_name


class NumericField(SearchableField):
    """
    Represents any field in Atlan that can be searched using only numeric search operations.
    """

    def __init__(self, atlan_field_name: StrictStr, numeric_field_name: StrictStr):
        """
        Default constructor.

        :param atlan_field_name: name of the attribute in the metastore
        :param numeric_field_name: name of the numeric field in the search index
        """
        super().__init__(atlan_field_name, numeric_field_name)

    @property
    def numeric_field_name(self) -> str:
        """
        Returns the name of the numeric field index for this attribute in Elastic.

        :returns: the field name for the numeric index on this attribute
        """
        return self.elastic_field_name

    @property
    def in_lineage(self) -> "LineageFilterFieldNumeric":
        """Returns a proxy which can be used a lineage filter with the appropriate subset of conditions"""
        return LineageFilterFieldNumeric(self)

    def eq(self, value: Union[StrictInt, StrictFloat]) -> Query:
        """
        Returns a query that will match all assets whose field has a value that exactly
        matches the provided numeric value.

        :param: value the numeric value to exactly match
        :returns: a query that will only match assets whose value for the field is exactly the numeric value provided
        """
        return Term(field=self.numeric_field_name, value=value)

    def gt(self, value: Union[StrictInt, StrictFloat]) -> Query:
        """
        Returns a query that will match all assets whose field has a value that is strictly
        greater than the provided numeric value.

        :param value: the numeric value to compare against
        :returns: a query that will only match assets whose value for the field is strictly greater than the numeric
                  value provided
        """
        return Range(field=self.numeric_field_name, gt=value)

    def gte(self, value: Union[StrictInt, StrictFloat]) -> Query:
        """
        Returns a query that will match all assets whose field has a value that is greater
        than or equal to the provided numeric value.

        :param value: the numeric value to compare against
        :returns: a query that will only match assets whose value for the field is greater than or equal to the numeric
                  value provided
        """
        return Range(field=self.numeric_field_name, gte=value)

    def lt(self, value: Union[StrictInt, StrictFloat]) -> Query:
        """
        Returns a query that will match all assets whose field has a value that is strictly
        less than the provided numeric value.

        :param value: the numeric value to compare against
        :returns: a value that will only match assets whose value for the field is strictly less than the numeric
                  value provided
        """
        return Range(field=self.numeric_field_name, lt=value)

    def lte(self, value: Union[StrictInt, StrictFloat]) -> Query:
        """
        Returns a query that will match all assets whose field has a value that is less
        than or equal to the provided numeric value.

        :param value: the numeric value to compare against
        :returns: a query that will only match assets whose value for the field is less than or equal to the numeric
                  value provided
        """
        return Range(field=self.numeric_field_name, lte=value)

    def between(
        self,
        minimum: Union[StrictInt, StrictFloat],
        maximum: Union[StrictInt, StrictFloat],
    ) -> Query:
        """
        Returns a query that will match all assets whose field has a value between the minimum and
        maximum specified values, inclusive.
        """
        return Range(field=self.numeric_field_name, gte=minimum, lte=maximum)

    def avg(self) -> Aggregation:
        """Returns criteria to calculate the average value of the provided field across all results."""
        return Aggregation(__root__={"avg": {"field": self.elastic_field_name}})

    def sum(self) -> Aggregation:
        """Returns criteria to calculate the sum value of the provided field across all results."""
        return Aggregation(__root__={"sum": {"field": self.elastic_field_name}})

    def min(self) -> Aggregation:
        """Returns criteria to calculate the minimum value of the provided field across all results."""
        return Aggregation(__root__={"min": {"field": self.elastic_field_name}})

    def max(self) -> Aggregation:
        """Returns criteria to calculate the maximum value of the provided field across all results."""
        return Aggregation(__root__={"max": {"field": self.elastic_field_name}})


class InternalNumericField(NumericField):
    def __init__(
        self,
        atlan_field_name: StrictStr,
        numeric_field_name: StrictStr,
        internal_field_name: StrictStr,
    ):
        """
        Default constructor.

        :param atlan_field_name: name of the attribute in the metastore
        :param numeric_field_name: name of the numeric field in the search index
        :param internal_field_name: internal name of the internal searchable attribute in the metastore
        """
        super().__init__(atlan_field_name, numeric_field_name)
        self._internal_field_name = internal_field_name

    @property
    def internal_field_name(self):
        return self._internal_field_name


class NumericRankField(NumericField):
    """
    Represents any field in Atlan that can be searched using only numeric search operations,
    but also has a rank-orderable index.
    """

    rank_field_name: StrictStr

    def __init__(
        self,
        atlan_field_name: StrictStr,
        numeric_field_name: StrictStr,
        rank_field_name: StrictStr,
    ):
        """
        Default constructor.

        :param atlan_field_name: name of the attribute in the metastore
        :param numeric_field_name: name of the numeric field in the search index
        :param rank_field_name: name of the rank orderable field in the search index
        """
        super().__init__(atlan_field_name, numeric_field_name)
        self.rank_field_name = rank_field_name


class KeywordTextField(KeywordField, TextField):
    """
    Represents any field in Atlan that can be searched by keyword or text-based search operations.
    """

    _text_field_name: StrictStr

    def __init__(
        self,
        atlan_field_name: StrictStr,
        keyword_field_name: StrictStr,
        text_field_name: StrictStr,
    ):
        """
        Default constructor.

        :param atlan_field_name: name of the attribute in the metastore
        :param keyword_field_name: name of the keyword field in the search index
        :param text_field_name: name of the text field in the search index
        """
        super(KeywordField, self).__init__(atlan_field_name, keyword_field_name)
        self._text_field_name = text_field_name

    @property
    def text_field_name(self) -> str:
        return self._text_field_name


class InternalKeywordTextField(KeywordTextField):
    """Represents any field in Atlan that can be searched by keyword or text-based search operations, and can also
    be searched against a special internal field directly within Atlan."""

    _internal_field_name: StrictStr

    def __init__(
        self,
        atlan_field_name: StrictStr,
        keyword_field_name: StrictStr,
        text_field_name: StrictStr,
        internal_field_name: StrictStr,
    ):
        """
        Default constructor.

        :param atlan_field_name: name of the attribute in the metastore
        :param keyword_field_name: name of the keyword field in the search index
        :param text_field_name: name of the text field in the search index
        """
        super().__init__(atlan_field_name, keyword_field_name, text_field_name)
        self._internal_field_name = internal_field_name

    @property
    def internal_field_name(self) -> StrictStr:
        return self._internal_field_name


class KeywordTextStemmedField(KeywordTextField):
    """
    Represents any field in Atlan that can be searched by keyword or text-based search operations,
    including a stemmed variation of the text analyzers.
    """

    stemmed_field_name: StrictStr

    def __init__(
        self,
        atlan_field_name: StrictStr,
        keyword_field_name: StrictStr,
        text_field_name: StrictStr,
        stemmed_field_name: StrictStr,
    ):
        """
        Default constructor.

        :param atlan_field_name: name of the attribute in the metastore
        :param keyword_field_name: name of the keyword field in the search index
        :param text_field_name: name of the text field in the search index
        :param stemmed_field_name: name of the stemmed text field in the search index
        """
        super().__init__(atlan_field_name, keyword_field_name, text_field_name)
        self.stemmed_field_name = stemmed_field_name

    def match_stemmed(self, value: StrictStr) -> Query:
        """
        Returns a query that will textually match the provided value against the field. This
        analyzes the provided value according to the same analysis carried out on the field
        (for example, tokenization and stemming).

        :param value: the string value to match against
        :returns: a query that will only match assets whose analyzed value for the field matches the value provided
                  (which will also be analyzed)
        """
        return Match(field=self.stemmed_field_name, query=value)


class CustomMetadataField(SearchableField):
    """
    Utility class to simplify searching for values on custom metadata attributes.
    """

    set_name: str
    attribute_name: str
    attribute_def: AttributeDef

    def __init__(self, set_name: str, attribute_name: str):
        from pyatlan.cache.custom_metadata_cache import CustomMetadataCache

        super().__init__(
            StrictStr(
                CustomMetadataCache.get_attribute_for_search_results(
                    set_name, attribute_name
                )
            ),
            StrictStr(
                CustomMetadataCache.get_attr_id_for_name(set_name, attribute_name)
            ),
        )
        self.set_name = set_name
        self.attribute_name = attribute_name
        self.attribute_def = CustomMetadataCache.get_attribute_def(
            self.elastic_field_name
        )

    def eq(self, value: SearchFieldType, case_insensitive: bool = False) -> Query:
        """
        Returns a query that will match all assets whose field has a value that exactly equals
        the provided value.

        :param value: the value to check the field's value is exactly equal to
        :param case_insensitive: if True, will match the value irrespective of case, otherwise will be a case-sensitive
                                 match
        :returns: a query that will only match assets whose value for the field is exactly equal to the value provided
        """
        return Term(
            field=self.elastic_field_name,
            value=value,
            case_insensitive=case_insensitive,
        )

    def startswith(self, value: StrictStr, case_insensitive: bool = False) -> Query:
        """
        Returns a query that will match all assets whose field has a value that starts with
        the provided value. Note that this can also be a case-insensitive match.

        :param value: the value (prefix) to check the field's value starts with
        :param case_insensitive: if True, will match the value irrespective of case, otherwise will be a case-sensitive
                                 match
        :returns: a query that will only match assets whose value for the field starts with the value provided
        """
        return Prefix(
            field=self.elastic_field_name,
            value=value,
            case_insensitive=case_insensitive,
        )

    def within(self, values: List[str]) -> Query:
        """
        Returns a query that will match all assets whose field has a value that exactly matches
        at least one of the provided string values.

        :param values: the values (strings) to check the field's value is exactly equal to
        :returns: a query that will only match assets whose value for the field is exactly equal to at least one of
                  the values provided
        """
        return Terms(field=self.elastic_field_name, values=values)

    def match(self, value: StrictStr) -> Query:
        """
        Returns a query that will textually match the provided value against the field. This
        analyzes the provided value according to the same analysis carried out on the field
        (for example, tokenization, stemming, and so on).

        :param value: the string value to match against
        :returns: a query that will only match assets whose analyzed value for the field matches the value provided
                  (which will also be analyzed)
        """
        return Match(
            field=self.elastic_field_name,
            query=value,
        )

    def gt(self, value: Union[StrictInt, StrictFloat]) -> Query:
        """
        Returns a query that will match all assets whose field has a value that is strictly
        greater than the provided numeric value.

        :param value: the numeric value to compare against
        :returns: a query that will only match assets whose value for the field is strictly greater than the numeric
                  value provided
        """
        return Range(field=self.elastic_field_name, gt=value)

    def gte(self, value: Union[StrictInt, StrictFloat]) -> Query:
        """
        Returns a query that will match all assets whose field has a value that is greater
        than or equal to the provided numeric value.

        :param value: the numeric value to compare against
        :returns: a query that will only match assets whose value for the field is greater than or equal to the numeric
                  value provided
        """
        return Range(field=self.elastic_field_name, gte=value)

    def lt(self, value: Union[StrictInt, StrictFloat]) -> Query:
        """
        Returns a query that will match all assets whose field has a value that is strictly
        less than the provided numeric value.

        :param value: the numeric value to compare against
        :returns: a value that will only match assets whose value for the field is strictly less than the numeric
                  value provided
        """
        return Range(field=self.elastic_field_name, lt=value)

    def lte(self, value: Union[StrictInt, StrictFloat]) -> Query:
        """
        Returns a query that will match all assets whose field has a value that is less
        than or equal to the provided numeric value.

        :param value: the numeric value to compare against
        :returns: a query that will only match assets whose value for the field is less than or equal to the numeric
                  value provided
        """
        return Range(field=self.elastic_field_name, lte=value)

    def between(
        self,
        minimum: Union[StrictInt, StrictFloat],
        maximum: Union[StrictInt, StrictFloat],
    ) -> Query:
        """
        Returns a query that will match all assets whose field has a value between the minimum and
        maximum specified values, inclusive.
        """
        return Range(field=self.elastic_field_name, gte=minimum, lte=maximum)


class LineageFilter(AtlanObject):
    """Class used to define how to filter assets and relationships when fetching lineage"""

    field: SearchableField
    operator: AtlanComparisonOperator
    value: str

    class Config:
        arbitrary_types_allowed = True


class LineageFilterField:
    """Class used to provide a proxy to building up a lineage filter with the appropriate
    subset of conditions available."""

    def __init__(self, field: SearchableField):
        """Create LineageFilterField

        :param field: Field on which filtering should be applied.
        """
        self._field = field

    @property
    def field(self) -> SearchableField:
        return self._field

    def has_any_value(self) -> LineageFilter:
        """
        Returns a filter that will match all assets whose provided field has any value at all (non-null).

        :returns:  a filter that will match all assets whose provided field has any value at all (non-null).
        """
        return LineageFilter(
            field=self._field, operator=AtlanComparisonOperator.NOT_NULL, value=""
        )

    def has_no_value(self) -> LineageFilter:
        """
        Returns a filter that will match all assets whose provided field has no value at all (is null).

        :returns:  a filter that will only match assets that have no value at all for the field (null).
        """
        return LineageFilter(
            field=self._field, operator=AtlanComparisonOperator.IS_NULL, value=""
        )


class LineageFilterFieldBoolean(LineageFilterField):
    """Class used to provide a proxy to building up a lineage filter with the appropriate
    subset of conditions available, for boolean fields."""

    def eq(self, value: bool) -> LineageFilter:
        """
        Returns a filter that will match all assets whose provided field has a value that is exactly
         the provided value.

        :param value: the value to check the field's value equals
        :returns:  a filter that will only match assets whose value for the field is exactly the value provided
        """
        return LineageFilter(
            field=self._field, operator=AtlanComparisonOperator.EQ, value=str(value)
        )

    def neq(self, value: bool) -> LineageFilter:
        """
        Returns a filter that will match all assets whose provided field has a value that is not exactly
         the provided value.

        :param value: the value to check the field's value does not equal
        :returns:  a filter that will only match assets whose value for the field is not exactly the value provided
        """
        return LineageFilter(
            field=self._field, operator=AtlanComparisonOperator.NEQ, value=str(value)
        )


class LineageFilterFieldCM(LineageFilterField):
    """Class used to provide a proxy to building up a lineage filter with the appropriate
    subset of conditions available, for custom metadata fields."""

    def __init__(self, field: CustomMetadataField):
        """Create LineageFilterFieldCM

        :param field: Field on which filtering should be applied.
        """
        super().__init__(field)
        self._cm_field = field

    @property
    def cm_field(self) -> CustomMetadataField:
        return self._cm_field

    @overload
    def eq(self, value: str) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is exactly
        the provided value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""

    @overload
    def eq(self, value: Enum) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is exactly
        the provided value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""

    @overload
    def eq(self, value: int) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly equal to
        the provided value.

        :param value: the value to check the field's value is strictly equal to
        :return value: a filter that will only match assets whose value for the field is strictly equal to the value
        provided
        """

    @overload
    def eq(self, value: float) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly equal to
        the provided value.

        :param value: the value to check the field's value is strictly equal to
        :return value: a filter that will only match assets whose value for the field is strictly equal to the value
        provided
        """

    @overload
    def eq(self, value: date) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly equal to
        the provided value.

        :param value: the value to check the field's value is strictly equal to
        :return value: a filter that will only match assets whose value for the field is strictly equal to the value
        provided
        """

    def eq(self, value: Union[str, Enum, int, float, date]):
        if isinstance(value, Enum):
            return LineageFilter(
                field=self._field,
                operator=AtlanComparisonOperator.EQ,
                value=value.value,
            )
        if isinstance(value, str):
            return LineageFilter(
                field=self._field, operator=AtlanComparisonOperator.EQ, value=value
            )
        if isinstance(value, bool):
            if not is_comparable_type(
                self._cm_field.attribute_def.type_name or "", ComparisonCategory.BOOLEAN
            ):
                raise ErrorCode.INVALID_QUERY.exception_with_parameters(
                    AtlanComparisonOperator.EQ,
                    f"{self._cm_field.set_name}.{self._cm_field.attribute_name}",
                )
            return LineageFilter(
                field=self._field, operator=AtlanComparisonOperator.EQ, value=str(value)
            )
        return self._with_numeric_comparison(
            value=value,
            comparison_operator=AtlanComparisonOperator.EQ,
            expected_types="str, Enum, bool, int, float or date",
        )

    @overload
    def neq(self, value: str) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is not exactly
        the provided value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value does not equal (case-sensitive)
        """

    @overload
    def neq(self, value: Enum) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is not exactly
        the provided value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value does not equal (case-sensitive)
        """

    @overload
    def neq(self, value: int) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly not equal to
        the provided value.

        :param value: the value to check the field's value is strictly not equal to
        :return value: a filter that will only match assets whose value for the field is strictly not equal to the value
        provided
        """

    @overload
    def neq(self, value: float) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly not equal to
        the provided value.

        :param value: the value to check the field's value is strictly not equal to
        :return value: a filter that will only match assets whose value for the field is strictly not equal to the value
        provided
        """

    @overload
    def neq(self, value: date) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly not equal to
        the provided value.

        :param value: the value to check the field's value is strictly not equal to
        :return value: a filter that will only match assets whose value for the field is strictly not equal to the value
        provided
        """

    def neq(self, value: Union[str, Enum, int, float, date]):
        if isinstance(value, Enum):
            return LineageFilter(
                field=self._field,
                operator=AtlanComparisonOperator.NEQ,
                value=value.value,
            )
        if isinstance(value, str):
            return LineageFilter(
                field=self._field, operator=AtlanComparisonOperator.NEQ, value=value
            )
        if isinstance(value, bool):
            if not is_comparable_type(
                self._cm_field.attribute_def.type_name or "", ComparisonCategory.BOOLEAN
            ):
                raise ErrorCode.INVALID_QUERY.exception_with_parameters(
                    AtlanComparisonOperator.NEQ,
                    f"{self._cm_field.set_name}.{self._cm_field.attribute_name}",
                )
            return LineageFilter(
                field=self._field,
                operator=AtlanComparisonOperator.NEQ,
                value=str(value),
            )
        return self._with_numeric_comparison(
            value=value,
            comparison_operator=AtlanComparisonOperator.NEQ,
            expected_types="str, Enum, bool, int, float or date",
        )

    def starts_with(self, value: str) -> LineageFilter:
        """
        Returns a filter that will match all assets whose provided field has a value that starts with
        the provided value. Note that this is a case-sensitive match.

        :param value: the value (prefix) to check the field's value starts with (case-sensitive)
        :return: a filter that will only match assets whose value for the field starts with the value provided
        """
        return self._with_string_comparison(
            value=value, comparison_operator=AtlanComparisonOperator.STARTS_WITH
        )

    def ends_with(self, value: str) -> LineageFilter:
        """
        Returns a filter that will match all assets whose provided field has a value that ends with
        the provided value. Note that this is a case-sensitive match.

        :param value: the value (suffix) to check the field's value starts with (case-sensitive)
        :return: a filter that will only match assets whose value for the field ends with the value provided
        """
        return self._with_string_comparison(
            value=value, comparison_operator=AtlanComparisonOperator.ENDS_WITH
        )

    def contains(self, value: str) -> LineageFilter:
        """
        Returns a filter that will match all assets whose provided field has a value that contains
        the provided value. Note that this is a case-sensitive match.

        :param value: the value (suffix) to check the field's value contains (case-sensitive)
        :return: a filter that will only match assets whose value for the field contains the value provided
        """
        return self._with_string_comparison(
            value=value, comparison_operator=AtlanComparisonOperator.CONTAINS
        )

    def does_not_contain(self, value: str) -> LineageFilter:
        """
        Returns a filter that will match all assets whose provided field has a value that does not contain
        the provided value. Note that this is a case-sensitive match.

        :param value: the value (suffix) to check the field's value does not contain (case-sensitive)
        :return: a filter that will only match assets whose value for the field does not contain the value provided
        """
        return self._with_string_comparison(
            value=value, comparison_operator=AtlanComparisonOperator.NOT_CONTAINS
        )

    @overload
    def lt(self, value: int) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than
        the provided value.

        :param value: the value to check the field's value is strictly less than
        :return value: a filter that will only match assets whose value for the field is strictly less than the value
        provided
        """

    @overload
    def lt(self, value: float) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than
        the provided value.

        :param value: the value to check the field's value is strictly less than
        :return value: a filter that will only match assets whose value for the field is strictly less than the value
        provided
        """

    @overload
    def lt(self, value: date) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than
        the provided value.

        :param value: the value to check the field's value is strictly less than
        :return value: a filter that will only match assets whose value for the field is strictly less than the value
        provided
        """

    def lt(self, value: Union[int, float, date]) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than
        the provided value.

        :param value: the value to check the field's value is strictly less than
        :return value: a filter that will only match assets whose value for the field is strictly less than the value
        provided
        """
        return self._with_numeric_comparison(
            value=value, comparison_operator=AtlanComparisonOperator.LT
        )

    @overload
    def gt(self, value: int) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than
        the provided value.

        :param value: the value to check the field's value is strictly less than
        :return value: a filter that will only match assets whose value for the field is strictly less than the value
        provided
        """

    @overload
    def gt(self, value: float) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly greater than
        the provided value.

        :param value: the value to check the field's value is strictly less than
        :return value: a filter that will only match assets whose value for the field is strictly greater than the value
         provided
        """

    @overload
    def gt(self, value: date) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly greater than
        the provided value.

        :param value: the value to check the field's value is strictly greater than
        :return value: a filter that will only match assets whose value for the field is strictly greater than the value
         provided
        """

    def gt(self, value: Union[int, float, date]) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than
        the provided value.

        :param value: the value to check the field's value is strictly greater than
        :return value: a filter that will only match assets whose value for the field is strictly greater than the
        value provided
        """
        return self._with_numeric_comparison(
            value=value, comparison_operator=AtlanComparisonOperator.GT
        )

    @overload
    def lte(self, value: int) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than or
        equal to the provided value.

        :param value: the value to check the field's value is strictly less than or equal to
        :return value: a filter that will only match assets whose value for the field is strictly less than or equal
        to the value provided
        """

    @overload
    def lte(self, value: float) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than or
        equal to the provided value.

        :param value: the value to check the field's value is strictly less than or equal to
        :return value: a filter that will only match assets whose value for the field is strictly less than or equal
        to the value provided
        """

    @overload
    def lte(self, value: date) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than
        or equal to the provided value.

        :param value: the value to check the field's value is strictly less than or equal to
        :return value: a filter that will only match assets whose value for the field is strictly less than or equal
        to the value provided
        """

    def lte(self, value: Union[int, float, date]) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than or
        equal to the provided value.

        :param value: the value to check the field's value is strictly less than or equal to
        :return value: a filter that will only match assets whose value for the field is strictly less than or equal
        to the value provided
        """
        return self._with_numeric_comparison(
            value=value, comparison_operator=AtlanComparisonOperator.LTE
        )

    @overload
    def gte(self, value: int) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than or
        equal to the provided value.

        :param value: the value to check the field's value is strictly less than or equal to
        :return value: a filter that will only match assets whose value for the field is strictly less than or equal to
        the value provided
        """

    @overload
    def gte(self, value: float) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly greater than or
        equal to the provided value.

        :param value: the value to check the field's value is strictly less than or equal to
        :return value: a filter that will only match assets whose value for the field is strictly greater than or equal
         to the value provided
        """

    @overload
    def gte(self, value: date) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly greater than or
        equal to the provided value.

        :param value: the value to check the field's value is strictly greater than or equal to
        :return value: a filter that will only match assets whose value for the field is strictly greater than or equal
         to the value provided
        """

    def gte(self, value: Union[int, float, date]) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than or
        equal to the provided value.

        :param value: the value to check the field's value is strictly greater than or equal to
        :return value: a filter that will only match assets whose value for the field is strictly greater than or equal
        to the value provided
        """
        return self._with_numeric_comparison(
            value=value, comparison_operator=AtlanComparisonOperator.GTE
        )

    def _with_numeric_comparison(
        self,
        value: Union[int, float, date],
        comparison_operator: AtlanComparisonOperator,
        expected_types: str = "int, float or date",
    ):
        if isinstance(
            value,
            bool,  # needed because isinstance(value, int) evaluates to true when value is bool
        ) or (
            not isinstance(value, int)
            and not isinstance(value, float)
            and not isinstance(value, date)
        ):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                type(value).__name__, expected_types
            )
        if not is_comparable_type(
            self._cm_field.attribute_def.type_name or "", ComparisonCategory.NUMBER
        ):
            raise ErrorCode.INVALID_QUERY.exception_with_parameters(
                comparison_operator,
                f"{self._cm_field.set_name}.{self._cm_field.attribute_name}",
            )
        return LineageFilter(
            field=self._field, operator=comparison_operator, value=str(value)
        )

    def _with_string_comparison(
        self, value: str, comparison_operator: AtlanComparisonOperator
    ):
        if not isinstance(value, str):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                type(value).__name__, "str"
            )
        if not is_comparable_type(
            self._cm_field.attribute_def.type_name or "", ComparisonCategory.STRING
        ):
            raise ErrorCode.INVALID_QUERY.exception_with_parameters(
                comparison_operator,
                f"{self._cm_field.set_name}.{self._cm_field.attribute_name}",
            )
        return LineageFilter(
            field=self._field, operator=comparison_operator, value=value
        )


class LineageFilterFieldNumeric(LineageFilterField):
    """Class used to provide a proxy to building up a lineage filter with the appropriate
    subset of conditions available, for numeric fields."""

    @overload
    def eq(self, value: int) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly equal to
        the provided value.

        :param value: the value to check the field's value is strictly equal to
        :return value: a filter that will only match assets whose value for the field is strictly equal to the value
        provided
        """

    @overload
    def eq(self, value: float) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly equal to
        the provided value.

        :param value: the value to check the field's value is strictly equal to
        :return value: a filter that will only match assets whose value for the field is strictly equal to the value
        provided
        """

    @overload
    def eq(self, value: date) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly equal to
        the provided value.

        :param value: the value to check the field's value is strictly equal to
        :return value: a filter that will only match assets whose value for the field is strictly equal to the value
        provided
        """

    def eq(self, value: Union[int, float, date]):
        """Returns a filter that will match all assets whose provided field has a value that is strictly equal to
        the provided value.

        :param value: the value to check the field's value is strictly equal to
        :return value: a filter that will only match assets whose value for the field is strictly equal to the value
        provided
        """
        return self._get_filter(value=value, operator=AtlanComparisonOperator.EQ)

    @overload
    def neq(self, value: int) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly not equal to
        the provided value.

        :param value: the value to check the field's value is strictly not equal to
        :return value: a filter that will only match assets whose value for the field is strictly not equal to the value
        provided
        """

    @overload
    def neq(self, value: float) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly not equal to
        the provided value.

        :param value: the value to check the field's value is strictly not equal to
        :return value: a filter that will only match assets whose value for the field is strictly not equal to the value
        provided
        """

    @overload
    def neq(self, value: date) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly not equal to
        the provided value.

        :param value: the value to check the field's value is strictly not equal to
        :return value: a filter that will only match assets whose value for the field is strictly not equal to the value
        provided
        """

    def neq(self, value: Union[int, float, date]):
        """Returns a filter that will match all assets whose provided field has a value that is strictly not equal to
        the provided value.

        :param value: the value to check the field's value is strictly equal to
        :return value: a filter that will only match assets whose value for the field is strictly not equal to
        the value provided
        """
        return self._get_filter(value=value, operator=AtlanComparisonOperator.NEQ)

    @overload
    def lt(self, value: int) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than
        the provided value.

        :param value: the value to check the field's value is strictly less than
        :return value: a filter that will only match assets whose value for the field is strictly less than the value
        provided
        """

    @overload
    def lt(self, value: float) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than
        the provided value.

        :param value: the value to check the field's value is strictly less than
        :return value: a filter that will only match assets whose value for the field is strictly less than the value
        provided
        """

    @overload
    def lt(self, value: date) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than
        the provided value.

        :param value: the value to check the field's value is strictly less than
        :return value: a filter that will only match assets whose value for the field is strictly less than the value
        provided
        """

    def lt(self, value: Union[int, float, date]):
        """Returns a filter that will match all assets whose provided field has a value that is strictly not equal to
        the provided value.

        :param value: the value to check the field's value is strictly equal to
        :return value: a filter that will only match assets whose value for the field is strictly not equal to
        the value provided
        """
        return self._get_filter(value=value, operator=AtlanComparisonOperator.LT)

    @overload
    def lte(self, value: float) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than or
        equal to the provided value.

        :param value: the value to check the field's value is strictly less than or equal to
        :return value: a filter that will only match assets whose value for the field is strictly less than or equal
        to the value provided
        """

    @overload
    def lte(self, value: date) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than
        or equal to the provided value.

        :param value: the value to check the field's value is strictly less than or equal to
        :return value: a filter that will only match assets whose value for the field is strictly less than or equal
        to the value provided
        """

    def lte(self, value: Union[int, float, date]) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly less than or
        equal to the provided value.

        :param value: the value to check the field's value is strictly less than or equal to
        :return value: a filter that will only match assets whose value for the field is strictly less than or equal
        to the value provided
        """
        return self._get_filter(value=value, operator=AtlanComparisonOperator.LTE)

    @overload
    def gt(self, value: int) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly greater than
        the provided value.

        :param value: the value to check the field's value is strictly greater than
        :return value: a filter that will only match assets whose value for the field is strictly less than the value
        provided
        """

    @overload
    def gt(self, value: float) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly greater than
        the provided value.

        :param value: the value to check the field's value is strictly greater than
        :return value: a filter that will only match assets whose value for the field is strictly greater than the value
        provided
        """

    @overload
    def gt(self, value: date) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly greater than
        the provided value.

        :param value: the value to check the field's value is strictly greater than
        :return value: a filter that will only match assets whose value for the field is strictly greater than the value
        provided
        """

    def gt(self, value: Union[int, float, date]):
        """Returns a filter that will match all assets whose provided field has a value that is strictly not equal to
        the provided value.

        :param value: the value to check the field's value is strictly equal to
        :return value: a filter that will only match assets whose value for the field is strictly not equal to
        the value provided
        """
        return self._get_filter(value=value, operator=AtlanComparisonOperator.GT)

    @overload
    def gte(self, value: float) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly greater than or
        equal to the provided value.

        :param value: the value to check the field's value is strictly greater than or equal to
        :return value: a filter that will only match assets whose value for the field is strictly greater than or equal
        to the value provided
        """

    @overload
    def gte(self, value: date) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly greater than
        or equal to the provided value.

        :param value: the value to check the field's value is strictly greater than or equal to
        :return value: a filter that will only match assets whose value for the field is strictly greater than or equal
        to the value provided
        """

    def gte(self, value: Union[int, float, date]) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is strictly greater than or
        equal to the provided value.

        :param value: the value to check the field's value is strictly greater than or equal to
        :return value: a filter that will only match assets whose value for the field is strictly greater than or equal
        to the value provided
        """
        return self._get_filter(value=value, operator=AtlanComparisonOperator.GTE)

    def _get_filter(
        self, value: Union[int, float, date], operator: AtlanComparisonOperator
    ):
        if isinstance(
            value,
            bool,  # needed because isinstance(value, int) evaluates to true when value is bool
        ) or (
            not isinstance(value, int)
            and not isinstance(value, float)
            and not isinstance(value, date)
        ):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                type(value).__name__, "int, float or date"
            )
        return LineageFilter(field=self._field, operator=operator, value=str(value))


class LineageFilterFieldString(LineageFilterField):
    """Class used to provide a proxy to building up a lineage filter with the appropriate subset of conditions
    available, for string-searchable fields."""

    @overload
    def eq(self, value: str) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is exactly
        equal to the provided value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""

    @overload
    def eq(self, value: Enum) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is exactly
        equal to the provided value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""

    def eq(self, value: Union[str, Enum]) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is exactly
        equal to the provided value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""
        return self._get_filter(value=value, operator=AtlanComparisonOperator.EQ)

    @overload
    def neq(self, value: str) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is exactly
        not equal to the provided value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""

    @overload
    def neq(self, value: Enum) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is exactly
        not equal to the provided value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""

    def neq(self, value: Union[str, Enum]) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that is exactly
        not equal to the provided value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""
        return self._get_filter(value=value, operator=AtlanComparisonOperator.NEQ)

    @overload
    def starts_with(self, value: str) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that starts with the provided
        value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""

    @overload
    def starts_with(self, value: Enum) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that starts with the provided
        value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""

    def starts_with(self, value: Union[str, Enum]) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that starts with the provided
        value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""
        return self._get_filter(
            value=value, operator=AtlanComparisonOperator.STARTS_WITH
        )

    @overload
    def ends_with(self, value: str) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that ends with the provided
        value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""

    @overload
    def ends_with(self, value: Enum) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that ends with the provided
        value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""

    def ends_with(self, value: Union[str, Enum]) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that ends with the provided
        value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""
        return self._get_filter(value=value, operator=AtlanComparisonOperator.ENDS_WITH)

    @overload
    def contains(self, value: str) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that contains the provided
        value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""

    @overload
    def contains(self, value: Enum) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that contains the provided
        value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""

    def contains(self, value: Union[str, Enum]) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that contains the provided
        value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""
        return self._get_filter(value=value, operator=AtlanComparisonOperator.CONTAINS)

    @overload
    def does_not_contain(self, value: str) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that does not contain the
        provided value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""

    @overload
    def does_not_contain(self, value: Enum) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that does not contain the
        provided value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""

    def does_not_contain(self, value: Union[str, Enum]) -> LineageFilter:
        """Returns a filter that will match all assets whose provided field has a value that does not contain the
        provided value. Note that this is a case-sensitive match.

        :param value: the value to check the field's value equals (case-sensitive)"""
        return self._get_filter(
            value=value, operator=AtlanComparisonOperator.NOT_CONTAINS
        )

    def _get_filter(self, value: Union[str, Enum], operator: AtlanComparisonOperator):
        if isinstance(value, Enum):
            return LineageFilter(
                field=self._field, operator=operator, value=value.value
            )
        if isinstance(value, str):
            return LineageFilter(field=self._field, operator=operator, value=value)
        raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
            type(value).__name__, "int, float or date"
        )
