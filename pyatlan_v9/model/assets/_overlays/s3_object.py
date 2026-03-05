# IMPORT: from pyatlan.model.utils import construct_object_key
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        aws_arn: str,
        s3_bucket_name: str,
        s3_bucket_qualified_name: str,
    ) -> "S3Object":
        """
        Create a new S3Object asset with an AWS ARN.

        Args:
            name: Name of the object
            connection_qualified_name: Unique name of the connection
            aws_arn: Amazon Resource Name (ARN) for the object
            s3_bucket_name: Simple name of the bucket
            s3_bucket_qualified_name: Unique name of the bucket

        Returns:
            S3Object instance ready to be created

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(
            [
                "name",
                "connection_qualified_name",
                "aws_arn",
                "s3_bucket_name",
                "s3_bucket_qualified_name",
            ],
            [
                name,
                connection_qualified_name,
                aws_arn,
                s3_bucket_name,
                s3_bucket_qualified_name,
            ],
        )
        fields = connection_qualified_name.split("/")
        if len(fields) != 3:
            raise ValueError("Invalid connection_qualified_name")
        if fields[0].replace(" ", "") == "" or fields[2].replace(" ", "") == "":
            raise ValueError("Invalid connection_qualified_name")
        if fields[1].lower() != "s3":
            raise ValueError("Invalid connection_qualified_name")

        connector_name = fields[1]
        return cls(
            name=name,
            connection_qualified_name=connection_qualified_name,
            qualified_name=f"{connection_qualified_name}/{aws_arn}",
            connector_name=connector_name,
            aws_arn=aws_arn,
            s3_bucket_name=s3_bucket_name,
            s3_bucket_qualified_name=s3_bucket_qualified_name,
        )

    @classmethod
    @init_guid
    def creator_with_prefix(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        s3_bucket_name: str,
        s3_bucket_qualified_name: str,
        prefix: str = "",
    ) -> "S3Object":
        """
        Create a new S3Object asset using a prefix-based object key.

        Args:
            name: Name of the object
            connection_qualified_name: Unique name of the connection
            s3_bucket_name: Simple name of the bucket
            s3_bucket_qualified_name: Unique name of the bucket
            prefix: Prefix (folder path) for the object

        Returns:
            S3Object instance ready to be created

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(
            [
                "name",
                "connection_qualified_name",
                "s3_bucket_name",
                "s3_bucket_qualified_name",
            ],
            [
                name,
                connection_qualified_name,
                s3_bucket_name,
                s3_bucket_qualified_name,
            ],
        )
        fields = connection_qualified_name.split("/")
        if len(fields) != 3:
            raise ValueError("Invalid connection_qualified_name")
        if fields[0].replace(" ", "") == "" or fields[2].replace(" ", "") == "":
            raise ValueError("Invalid connection_qualified_name")
        if fields[1].lower() != "s3":
            raise ValueError("Invalid connection_qualified_name")

        connector_name = fields[1]
        object_key = construct_object_key(prefix, name)
        return cls(
            name=name,
            s3_object_key=object_key,
            connection_qualified_name=connection_qualified_name,
            qualified_name=f"{connection_qualified_name}/{s3_bucket_name}/{object_key}",
            connector_name=connector_name,
            s3_bucket_name=s3_bucket_name,
            s3_bucket_qualified_name=s3_bucket_qualified_name,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "S3Object":
        """
        Create an S3Object instance for modification.

        Args:
            qualified_name: Unique name of the S3Object to update
            name: Human-readable name of the S3Object

        Returns:
            S3Object instance ready for update

        Raises:
            ValueError: If required parameters are missing
        """
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "S3Object":
        """
        Return a copy of this S3Object with only the minimum required fields for update.

        Returns:
            S3Object with only qualified_name and name set
        """
        return S3Object.updater(qualified_name=self.qualified_name, name=self.name)
