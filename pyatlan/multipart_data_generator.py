# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
# Based on original code from https://github.com/stripe/stripe-python (under MIT license)
from __future__ import absolute_import, division, print_function

import io
import uuid


class MultipartDataGenerator(object):
    _CONTENT_TYPES = {
        ".png": "image/png",
        ".gif": "image/gif",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".jfif": "image/jpeg",
        ".pjpeg": "image/jpeg",
        ".pjp": "image/jpeg",
        ".svg": "image/svg+xml",
        ".apng": "image/apng",
        ".avif": "image/avif",
        ".webp": "image/webp",
    }

    def __init__(self, chunk_size=1028):
        self.data = io.BytesIO()
        self.line_break = "\r\n"
        self.boundary = uuid.uuid4()
        self.chunk_size = chunk_size

    def add_file(self, file, filename):
        # Write the 'name' part (name="image")
        self._write(self.param_header())
        self._write(self.line_break)
        self._write('Content-Disposition: form-data; name="name"')
        self._write(self.line_break)
        self._write(self.line_break)
        self._write("image")
        self._write(self.line_break)

        # Write the file part with the correct 'name="file"'
        self._write(self.param_header())
        self._write(self.line_break)
        self._write(
            f'Content-Disposition: form-data; name="file"; filename="{filename}"'
        )
        self._write(self.line_break)

        # Get content type from dictionary, default to 'application/octet-stream'
        content_type = self._CONTENT_TYPES.get(
            filename[filename.rfind(".") :], "application/octet-stream"  # noqa: E203
        )
        self._write(f"Content-Type: {content_type}")
        self._write(self.line_break)
        self._write(self.line_break)

        # Write the file content
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
