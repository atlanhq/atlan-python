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
    A client for operating on Atlan's tenant files.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    def _detect_cloud_storage(self, url: str) -> str:
        if "amazonaws.com" in url:
            return PresignedURLResponse.CloudStorageIdentifier.S3.name
        else:
            return PresignedURLResponse.CloudStorageIdentifier.UNSUPPORTED.name

    @validate_arguments
    def get_presigned_url(self, request: PresignedURLRequest) -> PresignedURLResponse:
        raw_json = self._client._call_api(PRESIGNED_URL, request_obj=request)
        presigned_url = raw_json and raw_json.get("url", "")
        cloud_storage = self._detect_cloud_storage(presigned_url)
        return PresignedURLResponse(url=presigned_url, cloud_storage=cloud_storage)

    @validate_arguments
    def upload_file(self, url_response: PresignedURLResponse, file_path: str) -> None:
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
        return self._client._presigned_url_file_download(
            file_path=file_path,
            api=PRESIGNED_URL_DOWNLOAD.format_path(
                {"presigned_url_get": url_response.url}
            ),
        )
