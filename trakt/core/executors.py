from typing import List

from trakt.core.abstract import AbstractApi


class Executor:
    params: List[str]
    client: AbstractApi

    def __init__(self, client, module):
        self.params = [module]
        self.client = client

    def __getattr__(self, param):
        self.params.append(param)

        return self

    def __call__(self, *args, **kwargs):
        return repr(self)

    def __repr__(self):
        return f'Executor(params={".".join(self.params)})'
