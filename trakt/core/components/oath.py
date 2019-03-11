from typing import Any

from trakt.core.abstract import AbstractComponent


class OathComponent(AbstractComponent):
    name = "oath"

    url = "https://api.trakt.tv/oauth/authorize?response_type=response_type&client_id=client_id&redirect_uri=redirect_uri&state=state"
