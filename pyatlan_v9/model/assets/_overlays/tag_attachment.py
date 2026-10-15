# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    _QN_STYLES: ClassVar[tuple[str, ...]] = (
        "tag_object",
        "tag_attachments_object",
        "object_tag",
    )

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        tag_qualified_name: str,
        object_qualified_name: str,
        qn_style: str = "tag_object",
        object_type_name: str | None = None,
        source_tag_type_name: str | None = None,
        value: str | None = None,
    ) -> "TagAttachment":
        """
        Create a new TagAttachment asset, linking a source tag to an asset.

        Apps already in production build the qualified name in different shapes,
        so ``qn_style`` selects one; changing it changes the attachment's identity:

        - ``tag_object`` (default): ``{tag_qualified_name}/{object_qualified_name}``
        - ``tag_attachments_object``:
          ``{tag_qualified_name}/attachments/{object_qualified_name}``
        - ``object_tag``: ``{object_qualified_name}/{name}``

        Args:
            name: Name of the source tag
            connection_qualified_name: Unique name of the connection
            tag_qualified_name: Unique name of the source tag
            object_qualified_name: Unique name of the asset the tag is attached to
            qn_style: Shape of the qualified name (see above)
            object_type_name: Type name of the asset the tag is attached to
            source_tag_type_name: Type name of the source tag
            value: String value of the tag on this asset, if any

        Returns:
            TagAttachment instance ready to be created

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(
            [
                "name",
                "connection_qualified_name",
                "tag_qualified_name",
                "object_qualified_name",
            ],
            [
                name,
                connection_qualified_name,
                tag_qualified_name,
                object_qualified_name,
            ],
        )
        fields = connection_qualified_name.split("/")
        if len(fields) != 3:
            raise ValueError("Invalid connection_qualified_name")
        if fields[0].replace(" ", "") == "" or fields[2].replace(" ", "") == "":
            raise ValueError("Invalid connection_qualified_name")

        if qn_style == "tag_object":
            qualified_name = f"{tag_qualified_name}/{object_qualified_name}"
        elif qn_style == "tag_attachments_object":
            qualified_name = f"{tag_qualified_name}/attachments/{object_qualified_name}"
        elif qn_style == "object_tag":
            qualified_name = f"{object_qualified_name}/{name}"
        else:
            raise ValueError(f"qn_style must be one of {cls._QN_STYLES}")

        return cls(
            name=name,
            qualified_name=qualified_name,
            connection_qualified_name=connection_qualified_name,
            connector_name=fields[1],
            tag_qualified_name=tag_qualified_name,
            source_tag_qualified_name=tag_qualified_name,
            source_tag_display_name=name,
            source_tag_type_name=(
                source_tag_type_name if source_tag_type_name is not None else UNSET
            ),
            object_qualified_name=object_qualified_name,
            object_type_name=object_type_name
            if object_type_name is not None
            else UNSET,
            value_type="NONE" if value is None else "STRING",
            value=value,
            tag_attachment_string_value=value if value is not None else UNSET,
            propagate=False,
        )
