# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        connection_qualified_name: str,
        s3_bucket_name: str,
        s3_bucket_qualified_name: str,
        prefix: str,
        name: str | None = None,
    ) -> "S3Prefix":
        """
        Create a new S3Prefix asset.

        The qualified name is ``{s3_bucket_qualified_name}/{prefix}/`` — the full
        key from the bucket root, always with a trailing slash (native S3
        convention, shared by every app that builds prefixes).

        The parent prefix is recorded by qualified name
        (``s3_parent_prefix_qualified_name`` and ``s3_prefix_hierarchy``); the
        ``s3_parent_prefix`` relationship is left for the caller to set once the
        parent prefix exists.

        Args:
            connection_qualified_name: Unique name of the connection
            s3_bucket_name: Simple name of the bucket
            s3_bucket_qualified_name: Unique name of the bucket
            prefix: Full key of the prefix from the bucket root, e.g. ``a/b/``
                (leading and trailing slashes are optional)
            name: Name of the prefix; defaults to the last segment of ``prefix``

        Returns:
            S3Prefix instance ready to be created

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(
            [
                "connection_qualified_name",
                "s3_bucket_name",
                "s3_bucket_qualified_name",
                "prefix",
            ],
            [
                connection_qualified_name,
                s3_bucket_name,
                s3_bucket_qualified_name,
                prefix,
            ],
        )
        fields = connection_qualified_name.split("/")
        if len(fields) != 3:
            raise ValueError("Invalid connection_qualified_name")
        if fields[0].replace(" ", "") == "" or fields[2].replace(" ", "") == "":
            raise ValueError("Invalid connection_qualified_name")
        if fields[1].lower() != "s3":
            raise ValueError("Invalid connection_qualified_name")

        segments = prefix.strip("/").split("/")
        if any(segment.strip() == "" for segment in segments):
            raise ValueError("prefix cannot contain empty segments")
        if name is None:
            name = segments[-1]
        validate_required_fields(["name"], [name])

        def _prefix_qn(depth: int) -> str:
            return f"{s3_bucket_qualified_name}/{'/'.join(segments[:depth])}/"

        # Ancestors from immediate parent up to the root prefix.
        hierarchy = [
            {"name": segments[depth - 1], "qualifiedName": _prefix_qn(depth)}
            for depth in range(len(segments) - 1, 0, -1)
        ]
        return cls(
            name=name,
            qualified_name=_prefix_qn(len(segments)),
            connection_qualified_name=connection_qualified_name,
            connector_name=fields[1],
            s3_bucket_name=s3_bucket_name,
            s3_bucket_qualified_name=s3_bucket_qualified_name,
            s3_bucket=RelatedS3Bucket(qualified_name=s3_bucket_qualified_name),
            s3_parent_prefix_qualified_name=(
                hierarchy[0]["qualifiedName"] if hierarchy else UNSET
            ),
            s3_prefix_hierarchy=hierarchy or UNSET,
        )
