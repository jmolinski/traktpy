from copy import deepcopy
from typing import Any, Dict

InternalConfigType = Dict[str, Any]


class Config:
    _config: InternalConfigType

    def __init__(self, config: InternalConfigType) -> None:
        self._config = config

    def __getitem__(self, name: str) -> Any:
        return self._config[name]


DEFAULT_CONFIG: InternalConfigType = {
    "http": {"base_url": "https://api.trakt.tv", "max_retries": 3},
    "oauth": {"default_redirect_uri": "urn:ietf:wg:oauth:2.0:oob"},
}


class DefaultConfig(Config):
    def __init__(self, **custom_config: str) -> None:
        config = deepcopy(DEFAULT_CONFIG)

        if custom_config:
            config.update(custom_config)

        super().__init__(config)
