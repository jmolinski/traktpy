from datetime import date

import pytest
from tests.client import get_mock_http_component
from tests.test_data.certifications import CERTIFICATIONS
from tests.test_data.countries import COUNTRIES
from tests.test_data.genres import GENRES
from tests.test_data.languages import LANGUAGES
from tests.test_data.lists import TRENDING_LISTS
from tests.test_data.networks import NETWORKS
from trakt import Trakt, TraktCredentials
from trakt.core.exceptions import ArgumentError

USER = TraktCredentials("", "", "", 10e14)


def mk_mock_client(endpoints, client_id="", client_secret="", user=None):
    http = get_mock_http_component(endpoints)
    return Trakt(client_id, client_secret, http_component=http, user=user or USER)


def test_countries():
    client = mk_mock_client({r".*countries.*": [COUNTRIES, 200]})

    with pytest.raises(ArgumentError):
        client.countries.get_countries(type="qwerty")

    countries = client.countries.get_countries(type="shows")

    assert countries[0].code == COUNTRIES[0]["code"]


def test_certifications():
    client = mk_mock_client({r".*certifications.*": [CERTIFICATIONS, 200]})

    with pytest.raises(ArgumentError):
        client.certifications.get_certifications(type="qwerty")

    certifications = client.certifications.get_certifications(type="shows")

    assert certifications[0].slug == CERTIFICATIONS["us"][0]["slug"]


def test_genres():
    client = mk_mock_client({r".*genres.*": [GENRES, 200]})
    genres = client.genres.get_genres(type="shows")
    assert genres[0].name == GENRES[0]["name"]


def test_languages():
    client = mk_mock_client({r".*languages.*": [LANGUAGES, 200]})
    languages = client.languages.get_languages(type="shows")
    assert languages[0].name == LANGUAGES[0]["name"]


def test_lists():
    resp = [TRENDING_LISTS, 200, {"X-Pagination-Page-Count": 1}]
    client = mk_mock_client({r".*lists/(trending|popular).*": resp})

    tre = list(client.lists.get_trending())
    pop = list(client.lists.get_popular())
    assert tre[0].like_count == pop[0].like_count == TRENDING_LISTS[0]["like_count"]


def test_networks():
    client = mk_mock_client({r".*networks.*": [NETWORKS, 200]})
    networks = client.networks.get_networks()
    assert networks[0].name == NETWORKS[0]["name"]
