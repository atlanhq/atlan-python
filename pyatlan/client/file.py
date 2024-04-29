from pydantic.v1 import validate_arguments

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import (
    PRESIGNED_URL,
    PRESIGNED_URL_DOWNLOAD,
    PRESIGNED_URL_UPLOAD,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.file import PresignedURLRequest, PresignedURLResponse


class FileClient:
    """
    A client for operating on Atlan's tenant object storage.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @staticmethod
    def _detect_cloud_storage(url: str) -> str:
        if PresignedURLResponse.CloudStorageIdentifier.S3 in url:
            return PresignedURLResponse.CloudStorageIdentifier.S3.name
        else:
            return PresignedURLResponse.CloudStorageIdentifier.UNSUPPORTED.name

    @validate_arguments
    def generate_presigned_url(
        self, request: PresignedURLRequest
    ) -> PresignedURLResponse:
        """
        Generates a presigned URL based on Atlan's tenant object store.

        :param request: instance containing object key,
        expiry, and method (PUT: upload, GET: download).
        :raises AtlanError: on any error during API invocation.
        :returns: a response object containing a presigned URL with its cloud provider.
        """
        raw_json = self._client._call_api(PRESIGNED_URL, request_obj=request)
        presigned_url = raw_json and raw_json.get("url", "")
        cloud_storage = self._detect_cloud_storage(presigned_url)
        return PresignedURLResponse(url=presigned_url, cloud_storage=cloud_storage)

    @validate_arguments
    def upload_file(self, url_response: PresignedURLResponse, file_path: str) -> None:
        """
        Uploads a file to Atlan's object storage.

        :param url_response: instance of a generated PresignedURLResponse (method : PUT).
        :param file_path: path to the file to be uploaded.
        :raises AtlanError: on any error during API invocation.
        :raises InvalidRequestException: if the upload file path is invalid,
        or when the presigned URL cloud provider is unsupported.
        """
        try:
            upload_file = open(file_path, "rb")
        except FileNotFoundError as err:
            raise ErrorCode.INVALID_UPLOAD_FILE_PATH.exception_with_parameters(
                str(err.strerror), file_path
            )
        if (
            url_response.cloud_storage
            == PresignedURLResponse.CloudStorageIdentifier.S3.name
        ):
            return self._client._s3_presigned_url_file_upload(
                upload_file=upload_file,
                api=PRESIGNED_URL_UPLOAD.format_path(
                    {"presigned_url_put": url_response.url}
                ),
            )
        else:
            raise ErrorCode.UNSUPPORTED_PRESIGNED_URL.exception_with_parameters()

    @validate_arguments
    def download_file(
        self,
        url_response: PresignedURLResponse,
        file_path: str,
    ) -> str:
        """
        Downloads a file from Atlan's tenant object storage.

        :param url_response: instance of a generated PresignedURLResponse (method: GET).
        :param file_path: path to the file where you want to download the file.
        :raises InvalidRequestException: if unable to download the file.
        :raises AtlanError: on any error during API invocation.
        :returns: full path to the downloaded file.
        """
        return self._client._presigned_url_file_download(
            file_path=file_path,
            api=PRESIGNED_URL_DOWNLOAD.format_path(
                {"presigned_url_get": url_response.url}
            ),
        )
