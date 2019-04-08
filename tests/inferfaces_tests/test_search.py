from tests.test_data.search import ID_RESULTS, TEXT_RESULTS
from tests.utils import mk_mock_client

PAG_H = {"X-Pagination-Page-Count": 1}


def test_text_query():
    client = mk_mock_client({".*search.*": [TEXT_RESULTS, 200, PAG_H]})
    results = list(
        client.search.text_query(
            query="abc", type=["movie", "show"], fields=["title", "overview"]
        )
    )

    assert len(results) == 2
    assert results[1].type == TEXT_RESULTS[1]["type"]


def test_id_lookup():
    client = mk_mock_client({".*search.*": [ID_RESULTS, 200, PAG_H]})
    results = list(client.search.id_lookup(id_type="imdb", id="abc", type="movie"))

    assert len(results) == 1
    assert results[0].type == ID_RESULTS[0]["type"]
