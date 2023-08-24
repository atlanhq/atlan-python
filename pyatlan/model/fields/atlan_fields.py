from abc import ABC
from typing import Union

from pydantic import StrictBool, StrictFloat, StrictInt, StrictStr

from pyatlan.model.enums import SortOrder
from pyatlan.model.search import (
    Exists,
    Match,
    Prefix,
    Query,
    Range,
    SearchFieldType,
    SortItem,
    Term,
    Terms,
)
from pyatlan.model.typedef import AttributeDef


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

    def within(self, values: list[str]) -> Query:
        """
        Returns a query that will match all assets whose field has a value that exactly matches
        at least one of the provided string values.

        :param values: the values (strings) to check the field's value is exactly equal to
        :returns: a query that will only match assets whose value for the field is exactly equal to at least one of
                  the values provided
        """
        return Terms(field=self.keyword_field_name, values=values)


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

    def within(self, values: list[str]) -> Query:
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
