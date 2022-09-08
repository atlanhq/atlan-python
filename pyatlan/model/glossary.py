#!/usr/bin/env/python
# Copyright 2022 Atlan Pte, Ltd
# Copyright [2015-2021] The Apache Software Foundation
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pyatlan.model.misc import AtlanBase, AtlanBaseModelObject
from pyatlan.utils import type_coerce, type_coerce_dict, type_coerce_list


class AtlanGlossaryBaseObject(AtlanBaseModelObject):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanBaseModelObject.__init__(self, attrs)

        self.qualifiedName = attrs.get("qualifiedName")
        self.name = attrs.get("name")
        self.shortDescription = attrs.get("shortDescription")
        self.longDescription = attrs.get("longDescription")
        self.additionalAttributes = attrs.get("additionalAttributes")
        self.classifications = attrs.get("classifications")

    def type_coerce_attrs(self):
        # This is to avoid the circular dependencies that instance.py and glossary.py has.
        import pyatlan.model.instance as instance

        super(AtlanGlossaryBaseObject, self).type_coerce_attrs()
        self.classifications = type_coerce_list(
            self.classifications, instance.AtlanClassification
        )


class AtlanGlossary(AtlanGlossaryBaseObject):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanGlossaryBaseObject.__init__(self, attrs)

        self.language = attrs.get("language")
        self.usage = attrs.get("usage")
        self.terms = attrs.get("terms")
        self.categories = attrs.get("categories")

    def type_coerce_attrs(self):
        super(AtlanGlossary, self).type_coerce_attrs()

        self.terms = type_coerce_list(self.classifications, AtlanRelatedTermHeader)
        self.categories = type_coerce_list(self.categories, AtlanRelatedCategoryHeader)


class AtlanGlossaryExtInfo(AtlanGlossary):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanGlossary.__init__(self, attrs)

        self.termInfo = attrs.get("termInfo")
        self.categoryInfo = attrs.get("categoryInfo")

    def type_coerce_attrs(self):
        super(AtlanGlossaryExtInfo, self).type_coerce_attrs()

        self.termInfo = type_coerce_dict(self.termInfo, AtlanGlossaryTerm)
        self.categoryInfo = type_coerce_dict(self.categoryInfo, AtlanGlossaryCategory)


class AtlanGlossaryCategory(AtlanGlossaryBaseObject):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanGlossaryBaseObject.__init__(self, attrs)

        # Inherited attributes from relations
        self.anchor = attrs.get("anchor")

        # Category hierarchy links
        self.parentCategory = attrs.get("parentCategory")
        self.childrenCategories = attrs.get("childrenCategories")

        # Terms associated with this category
        self.terms = attrs.get("terms")

    def type_coerce_attrs(self):
        super(AtlanGlossaryCategory, self).type_coerce_attrs()

        self.anchor = type_coerce(self.anchor, AtlanGlossaryHeader)
        self.parentCategory = type_coerce(
            self.parentCategory, AtlanRelatedCategoryHeader
        )
        self.childrenCategories = type_coerce_list(
            self.childrenCategories, AtlanRelatedCategoryHeader
        )
        self.terms = type_coerce_list(self.terms, AtlanRelatedTermHeader)


class AtlanGlossaryTerm(AtlanGlossaryBaseObject):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanGlossaryBaseObject.__init__(self, attrs)

        # Core attributes
        self.examples = attrs.get("examples")
        self.abbreviation = attrs.get("abbreviation")
        self.usage = attrs.get("usage")

        # Attributes derived from relationships
        self.anchor = attrs.get("anchor")
        self.assignedEntities = attrs.get("assignedEntities")
        self.categories = attrs.get("categories")

        # Related Terms
        self.seeAlso = attrs.get("seeAlso")

        # Term Synonyms
        self.synonyms = attrs.get("synonyms")

        # Term antonyms
        self.antonyms = attrs.get("antonyms")

        # Term preference
        self.preferredTerms = attrs.get("preferredTerms")
        self.preferredToTerms = attrs.get("preferredToTerms")

        # Term replacements
        self.replacementTerms = attrs.get("replacementTerms")
        self.replacedBy = attrs.get("replacedBy")

        # Term translations
        self.translationTerms = attrs.get("translationTerms")
        self.translatedTerms = attrs.get("translatedTerms")

        # Term classification
        self.isA = attrs.get("isA")
        self.classifies = attrs.get("classifies")

        # Values for terms
        self.validValues = attrs.get("validValues")
        self.validValuesFor = attrs.get("validValuesFor")

    def type_coerce_attrs(self):
        super(AtlanGlossaryTerm, self).type_coerce_attrs()

        # This is to avoid the circular dependencies that instance.py and glossary.py has.
        import pyatlan.model.instance as instance

        self.anchor = type_coerce(self.anchor, AtlanGlossaryHeader)
        self.assignedEntities = type_coerce_list(
            self.assignedEntities, instance.AtlanRelatedObjectId
        )
        self.categories = type_coerce_list(
            self.categories, AtlanTermCategorizationHeader
        )
        self.seeAlso = type_coerce_list(self.seeAlso, AtlanRelatedTermHeader)
        self.synonyms = type_coerce_list(self.synonyms, AtlanRelatedTermHeader)
        self.antonyms = type_coerce_list(self.antonyms, AtlanRelatedTermHeader)
        self.preferredTerms = type_coerce_list(
            self.preferredTerms, AtlanRelatedTermHeader
        )
        self.preferredToTerms = type_coerce_list(
            self.preferredToTerms, AtlanRelatedTermHeader
        )
        self.replacementTerms = type_coerce_list(
            self.replacementTerms, AtlanRelatedTermHeader
        )
        self.replacedBy = type_coerce_list(self.replacedBy, AtlanRelatedTermHeader)
        self.translationTerms = type_coerce_list(
            self.translationTerms, AtlanRelatedTermHeader
        )
        self.isA = type_coerce_list(self.isA, AtlanRelatedTermHeader)
        self.classifies = type_coerce_list(self.classifies, AtlanRelatedTermHeader)
        self.validValues = type_coerce_list(self.validValues, AtlanRelatedTermHeader)
        self.validValuesFor = type_coerce_list(
            self.validValuesFor, AtlanRelatedTermHeader
        )


class AtlanGlossaryHeader(AtlanBase):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanBase.__init__(self, attrs)

        self.glossaryGuid = attrs.get("glossaryGuid")
        self.relationGuid = attrs.get("relationGuid")
        self.displayText = attrs.get("displayText")


class AtlanRelatedCategoryHeader(AtlanBase):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanBase.__init__(self, attrs)

        self.categoryGuid = attrs.get("categoryGuid")
        self.parentCategoryGuid = attrs.get("parentCategoryGuid")
        self.relationGuid = attrs.get("relationGuid")
        self.displayText = attrs.get("displayText")
        self.description = attrs.get("description")


class AtlanRelatedTermHeader(AtlanBase):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanBase.__init__(self, attrs)

        self.termGuid = attrs.get("termGuid")
        self.relationGuid = attrs.get("relationGuid")
        self.displayText = attrs.get("displayText")
        self.description = attrs.get("description")
        self.expression = attrs.get("expression")
        self.steward = attrs.get("steward")
        self.source = attrs.get("source")
        self.status = attrs.get("status")


class AtlanTermAssignmentHeader(AtlanBase):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanBase.__init__(self, attrs)

        self.termGuid = attrs.get("termGuid")
        self.relationGuid = attrs.get("relationGuid")
        self.description = attrs.get("description")
        self.displayText = attrs.get("displayText")
        self.expression = attrs.get("expression")
        self.createdBy = attrs.get("createdBy")
        self.steward = attrs.get("steward")
        self.source = attrs.get("source")
        self.confidence = attrs.get("confidence")


class AtlanTermCategorizationHeader(AtlanBase):
    def __init__(self, attrs=None):
        attrs = attrs or {}

        AtlanBase.__init__(self, attrs)

        self.categoryGuid = attrs.get("categoryGuid")
        self.relationGuid = attrs.get("relationGuid")
        self.description = attrs.get("description")
        self.displayText = attrs.get("displayText")
        self.status = attrs.get("status")
