# INTERNAL_IMPORT: from pyatlan.utils import init_guid

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        aws_arn: str | None = None,
    ) -> "S3Bucket":
        """
        Create a new S3Bucket asset.

        Args:
            name: Name of the bucket
            connection_qualified_name: Unique name of the connection in which this bucket exists
            aws_arn: Amazon Resource Name (ARN) for the bucket (optional)

        Returns:
            S3Bucket instance ready to be created

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        if name is None:
            raise ValueError("name is required")
        if connection_qualified_name is None:
            raise ValueError("connection_qualified_name is required")

        if name.strip() == "":
            raise ValueError("name cannot be blank")
        if connection_qualified_name.strip() == "":
            raise ValueError("connection_qualified_name cannot be blank")

        fields = connection_qualified_name.split("/")
        if len(fields) != 3:
            raise ValueError("Invalid connection_qualified_name")

        if fields[0].replace(" ", "") == "" or fields[2].replace(" ", "") == "":
            raise ValueError("Invalid connection_qualified_name")

        if fields[1].lower() != "s3":
            raise ValueError("Invalid connection_qualified_name")

        connector_name = fields[1]
        qualified_name = f"{connection_qualified_name}/{aws_arn if aws_arn else name}"

        return cls(
            name=name,
            qualified_name=qualified_name,
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            aws_arn=aws_arn,
        )
