from typing import Any, Dict, Optional

from pyatlan import utils
from pyatlan.model.packages.base.package import AbstractPackage


class AbstractCustomPackage(AbstractPackage):
    """
    Abstract class for custom packages
    """

    def __init__(
        self,
    ):
        super().__init__()
        self._epoch = int(utils.get_epoch_timestamp())

    def _add_optional_params(self, params: Dict[str, Optional[Any]]) -> None:
        """
        Helper method to add non-None params to `self._parameters`.

        :param params: dict of param names and values.
        """
        for name, value in params.items():
            if value is not None:
                self._parameters.append({"name": name, "value": value})
