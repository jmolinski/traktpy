# flake8: noqa: F403, F405

import pytest
from trakt.core.restpaths import AuthRequiredValidator


def test_validators():
    class A:
        pass

    client = A()
    client.authenticated = True

    assert AuthRequiredValidator().validate(client=client) == True

    client.authenticated = False

    assert AuthRequiredValidator().validate(client=client) == False
