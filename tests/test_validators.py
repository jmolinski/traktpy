# flake8: noqa: F403, F405

from trakt.core.paths.path import AuthRequiredValidator


class A:
    pass


def test_auth_validator():
    client = A()
    client.authenticated = True

    assert AuthRequiredValidator().validate(client=client) is True

    client.authenticated = False

    assert AuthRequiredValidator().validate(client=client) is False
