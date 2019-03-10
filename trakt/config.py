from copy import deepcopy
from typing import Dict


class Config:
    _config: Dict[str, str]

    def __init__(self, config: Dict[str, str]) -> None:
        self._config = config

    def update(self, config: Dict[str, str]) -> None:
        self._config.update(config)


DEFAULT_CONFIG: Dict[str, str] = {"base_url": "https://api.trakt.tv"}


class DefaultConfig(Config):
    def __init__(self, **custom_config: str) -> None:
        config = deepcopy(DEFAULT_CONFIG)

        if custom_config:
            config.update(custom_config)

        super().__init__(config)
