# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


class Synonym:
    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        instance[self.storage_name] = value

    def __get__(self, instance, owner):
        if self.storage_name in instance:
            return instance[self.storage_name]
        return None
