from trakt.core.abstract import AbstractApi


class AbstractComponent:
    name: str = "base_component"
    client: AbstractApi

    def __init__(self, client: AbstractApi) -> None:
        self.client = client
