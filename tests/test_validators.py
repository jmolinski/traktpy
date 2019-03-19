# flake8: noqa: F403, F405

import pytest
from trakt.core.exceptions import ArgumentError, NotAuthenticated
from trakt.core.paths import Path
from trakt.core.paths.validators import (
    AuthRequiredValidator,
    OptionalArgsValidator,
    PerArgValidator,
    RequiredArgsValidator,
)


class A:
    pass


def test_auth_validator():
    client = A()
    client.user = "not none"

    assert AuthRequiredValidator().validate(client=client) is None

    client.user = None

    with pytest.raises(NotAuthenticated):
        AuthRequiredValidator().validate(client=client)


def test_required_args_validator():
    p = Path("a/!b/!c/?d", {})

    assert RequiredArgsValidator().validate(path=p, b="b", c="c") is None

    with pytest.raises(ArgumentError):
        RequiredArgsValidator().validate(path=p, c="c")

    with pytest.raises(ArgumentError):
        RequiredArgsValidator().validate(path=p, b="b")

    with pytest.raises(ArgumentError):
        RequiredArgsValidator().validate(path=p, d="d")


def test_optional_args_validator():
    p = Path("a/?b/?c/?d", {})

    assert OptionalArgsValidator().validate(path=p) is None
    assert OptionalArgsValidator().validate(path=p, b="b", c="c") is None

    with pytest.raises(ArgumentError):
        OptionalArgsValidator().validate(path=p, c="c")

    with pytest.raises(ArgumentError):
        OptionalArgsValidator().validate(path=p, b="b", d="d")


def test_per_arg_validator():
    b_validator = PerArgValidator("b", lambda b: b in ["abc", "xyz"])
    c_validator = PerArgValidator("c", lambda c: "x" in c)
    p = Path("a/!b/?c", {}, validators=[b_validator, c_validator])

    assert b_validator.validate(path=p, b="xyz") is None

    with pytest.raises(ArgumentError):
        b_validator.validate(path=p, b="any")

    assert c_validator.validate(path=p, b="xyz") is None
    assert c_validator.validate(path=p, b="any") is None

    with pytest.raises(ArgumentError):
        c_validator.validate(path=p, b="any", c="y")


def test_extended_validator():
    pass


def test_filters_validator():
    pass
