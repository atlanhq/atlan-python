# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
# Based on original code from https://github.com/stripe/stripe-python (under MIT license)
from __future__ import absolute_import, division, print_function

import io
import uuid


class MultipartDataGenerator(object):
    def __init__(self, chunk_size=1028):
        self.data = io.BytesIO()
        self.line_break = "\r\n"
        self.boundary = uuid.uuid4()
        self.chunk_size = chunk_size

    def add_file(self, file, filename):
        self._write(self.param_header())
        self._write(self.line_break)
        self._write('Content-Disposition: form-data; name="file"; filename="')
        self._write(filename)
        self._write('"')
        self._write(self.line_break)
        if filename.endswith(".png"):
            self._write("Content-Type: image/png")
        elif filename.endswith(".gif"):
            self._write("Content-Type: image/gif")
        elif (
            filename.endswith(".jpg")
            or filename.endswith(".jpeg")
            or filename.endswith(".jfif")
            or filename.endswith(".pjpeg")
            or filename.endswith(".pjp")
        ):
            self._write("Content-Type: image/jpeg")
        elif filename.endswith(".svg"):
            self._write("Content-Type: image/svg+xml")
        elif filename.endswith(".apng"):
            self._write("Content-Type: image/apng")
        elif filename.endswith(".avif"):
            self._write("Content-Type: image/avif")
        elif filename.endswith(".webp"):
            self._write("Content-Type: image/webp")
        else:
            self._write("Content-Type: application/octet-stream")
        self._write(self.line_break)
        self._write(self.line_break)
        self._write_file(file)
        self._write(self.line_break)

    def param_header(self):
        return f"--{self.boundary}"

    def get_post_data(self):
        self._write(f"--{self.boundary}--")
        self._write(self.line_break)
        return self.data.getvalue()

    def _write(self, value):
        if isinstance(value, bytes):
            array = bytearray(value)
        elif isinstance(value, str):
            array = bytearray(value, encoding="utf-8")
        else:
            raise TypeError(
                "unexpected type: {value_type}".format(value_type=type(value))
            )

        self.data.write(array)

    def _write_file(self, f):
        while file_contents := f.read(self.chunk_size):
            self._write(file_contents)
