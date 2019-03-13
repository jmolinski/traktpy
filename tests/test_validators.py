# flake8: noqa: F403, F405

from trakt.core.paths import Path
from trakt.core.paths.validators import (
    AuthRequiredValidator,
    OptionalArgsValidator,
    PerArgValidator,
    RequiredArgsValidator
)


class A:
    pass


def test_auth_validator():
    client = A()
    client.authenticated = True

    assert AuthRequiredValidator().validate(client=client) is True

    client.authenticated = False

    assert AuthRequiredValidator().validate(client=client) is False


def test_required_args_validator():
    p = Path("a/!b/!c/?d", {})

    assert RequiredArgsValidator().validate(path=p, b="b", c="c")
    assert not RequiredArgsValidator().validate(path=p, c="c")
    assert not RequiredArgsValidator().validate(path=p, b="b")
    assert not RequiredArgsValidator().validate(path=p, d="d")


def test_optional_args_validator():
    p = Path("a/?b/?c/?d", {})

    assert OptionalArgsValidator().validate(path=p)
    assert OptionalArgsValidator().validate(path=p, b="b", c="c")
    assert not OptionalArgsValidator().validate(path=p, c="c")
    assert not OptionalArgsValidator().validate(path=p, b="b", d="d")


def test_per_arg_validator():
    b_validator = PerArgValidator("b", lambda b: b in ["abc", "xyz"])
    c_validator = PerArgValidator("c", lambda c: "x" in c)
    p = Path("a/!b/?c", {}, validators=[b_validator, c_validator])

    assert b_validator.validate(path=p, b="xyz")
    assert not b_validator.validate(path=p, b="any")

    assert c_validator.validate(path=p, b="xyz")
    assert c_validator.validate(path=p, b="any")
    assert not c_validator.validate(path=p, b="any", c="y")
