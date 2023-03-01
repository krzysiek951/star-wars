from unittest.mock import patch
from requests import Session
import pytest

from starwars.api_explorer.models.client import ApiClient
from starwars.api_explorer.utils.utils import str_date_to_iso

TEST_API_URL = 'https://swapi.dev/api'

PEOPLE_PAGE_1 = {
    "next": "https://swapi.dev/api/people/?page=2",
    "results": [
        {
            "name": "Luke Skywalker",
            "height": "172"
        },
        {
            "name": "R2-D2",
            "height": "96"
        }
    ]
}
PEOPLE_PAGE_2 = {
    "next": "",
    "results": [
        {
            "name": "Obi-Wan Kenobi",
            "height": "182"
        },
        {
            "name": "R2-D2",
            "height": "96"
        }
    ]
}


@pytest.fixture
def test_client():
    return ApiClient()


def mocked_requests_get(*args, **kwargs):
    """ Represents mocked response from API. """

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == f'https://swapi.dev/api/people':
        return MockResponse(PEOPLE_PAGE_1, 200)
    elif args[0] == f'https://swapi.dev/api/people/?page=2':
        return MockResponse(PEOPLE_PAGE_2, 200)

    return MockResponse(None, 404)


# #
# @patch.object(Session, 'get', side_effect=mocked_requests_get)
# def test_get_api_resources(mock_get, test_client):
#     """ Test whether the data from API is fetched correctly. """
#     with test_client:
#         response = get_api_resources(client=test_client, url=TEST_API_URL, resource='people')
#     assert response == PEOPLE_PAGE_1['results'] + PEOPLE_PAGE_2['results']
#
#
# @patch.object(Session, 'get', side_effect=mocked_requests_get)
# def test_get_raises_exception(mock_get, test_client):
#     """ Test whether Client 'get' raises exception on wrong url. """
#     with pytest.raises(ResourceDoesNotExist):
#         with test_client:
#             test_client.get('https://swapi.dev/api/people/bad-url')


def test_format_date():
    """ Test whether date if properly formatted. """
    samples = {
        '2014-12-20T21:17:56.891000Z': '2014-12-20',
        '': None,
    }
    for sample, expected in samples.items():
        result = str_date_to_iso(sample)
        assert result == expected
