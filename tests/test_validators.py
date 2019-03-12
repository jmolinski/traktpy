# flake8: noqa: F403, F405

import pytest
from trakt.core.restpaths import AuthRequiredValidator


class A:
    pass


def test_auth_validator():
    client = A()
    client.authenticated = True

    assert AuthRequiredValidator().validate(client=client) is True

    client.authenticated = False

    assert AuthRequiredValidator().validate(client=client) is False
