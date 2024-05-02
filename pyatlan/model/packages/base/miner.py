from pyatlan import utils
from pyatlan.model.packages.base.package import AbstractPackage


class AbstractMiner(AbstractPackage):
    """
    Abstract class for miners

    :param connection_qualified_name: unique name of
    the connection whose assets should be mined
    """

    def __init__(
        self,
        connection_qualified_name: str,
    ):
        super().__init__()
        self._epoch = int(utils.get_epoch_timestamp())
        self._parameters.append(
            dict(name="connection-qualified-name", value=connection_qualified_name)
        )
