from trakt.core.abstract import AbstractComponent


class DefaultOauthComponent(AbstractComponent):
    name = "oauth"
    token = ""

    url = "https://api.trakt.tv/oauth/authorize?response_type=response_type&client_id=client_id&redirect_uri=redirect_uri&state=state"
