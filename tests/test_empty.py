# flake8: noqa: F403, F405
from typing import List

import jsons
import pytest
from tests.client import config as secrets
from trakt import Trakt
from trakt.core.models import Country


def test_data_deserialization():
    data = {"name": "Poland", "code": "pl"}

    client = Trakt("", "")
    client.noop()  # initialize
    country = Country.from_json(data)

    assert country.name == data["name"]
    assert country.code == data["code"]

    data = [{"name": "Poland", "code": "pl"}, {"name": "Germany", "code": "de"}]

    cts: List[Country] = jsons.load(data, List[Country])

    assert cts[0].client == cts[1].client


def test_client():
    client = Trakt(**secrets)

    x = client.request("countries", type="shows")

    # print(x)
