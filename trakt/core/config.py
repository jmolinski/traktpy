from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, Union

__all__ = ("Config", "DefaultConfig", "TraktCredentials")


ConfigEntryType = Union[int, str, Dict[str, Union[str, int]]]
InternalConfigType = Dict[str, ConfigEntryType]


def _update_dict_recursive(org, new):
    for k, v in new.items():
        if k not in org:
            org[k] = v
        else:
            if isinstance(org[k], dict):
                _update_dict_recursive(org[k], v)
            else:
                org[k] = v


class Config:
    _config: InternalConfigType

    def __init__(self, config: InternalConfigType) -> None:
        self._config = config

    def __getitem__(self, name: str) -> Any:
        return self._config.get(name)

    def __setitem__(self, name: str, value: Any) -> None:
        self._config[name] = value


DEFAULT_CONFIG: InternalConfigType = {
    "http": {"base_url": "https://api.trakt.tv", "max_retries": 3},
    "oauth": {
        "default_redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "refresh_token_s": 30 * 24 * 60 * 60,
    },
    "cache": {"cache_level": "basic", "cache_timeout": 60 * 60},
}


class DefaultConfig(Config):
    def __init__(self, **custom_config: ConfigEntryType) -> None:
        config = deepcopy(DEFAULT_CONFIG)

        if custom_config:
            _update_dict_recursive(config, custom_config)

        super().__init__(config)


@dataclass
class TraktCredentials:
    access_token: str
    refresh_token: str
    scope: str
    expires_at: int
