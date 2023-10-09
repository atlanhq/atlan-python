from typing import Protocol, runtime_checkable


@runtime_checkable
class ApiCaller(Protocol):
    def _call_api(
        self, api, query_params=None, request_obj=None, exclude_unset: bool = True
    ):
        pass
