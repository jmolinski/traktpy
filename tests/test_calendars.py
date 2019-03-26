from tests.client import get_mock_http_component
from tests.test_data.calendars import SEASON_PREMIERES
from trakt import Trakt


def test_get_season_premieres():
    http = get_mock_http_component({".*": [SEASON_PREMIERES, 200]})
    client = Trakt("", "", http_component=http)

    premieres = client.calendars.get_season_premieres()

    assert len(premieres) == 1

    premiere = premieres[0]

    assert all(i in premiere for i in ["first_aired", "episode", "show"])

    assert premiere["episode"].title == "Episode 1"
    assert premiere["show"].title == "Make Or Break?"
