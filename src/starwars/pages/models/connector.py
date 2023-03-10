from __future__ import annotations

import requests_cache

from starwars.api_explorer.models.client import ApiClient
from starwars.api_explorer.models.connector import AbstractAPIConnector
from starwars.settings import SwapiResourceType, SWAPI_BASE_URL, TripAwayResourceType, TRIPAWAY_BASE_URL

requests_cache.install_cache('cache_starwars')


class SwapiConnector(AbstractAPIConnector):
    api_name = 'SWAPI'

    def __init__(self, client: ApiClient = None, resource: SwapiResourceType = None):
        super().__init__(client, resource)
        self.api_url = SWAPI_BASE_URL

    def __iter__(self):
        next_api_query = self.resource_url
        response = self.client.get(next_api_query)
        header = tuple(response['results'][0].keys())
        yield header
        while next_api_query:
            response = self.client.get(next_api_query)
            next_api_query = response['next']
            for resource in response['results']:
                resource_data = tuple(resource.values())
                yield resource_data


class TripAwayConnector(AbstractAPIConnector):
    api_name = 'TripAway'

    def __init__(self, client: ApiClient = None, resource: TripAwayResourceType = None):
        super().__init__(client, resource)
        self.api_url = TRIPAWAY_BASE_URL

    def __iter__(self):
        next_api_query = self.resource_url
        response = self.client.get(next_api_query)
        header = tuple(response['results'][0].keys())
        yield header
        while next_api_query:
            response = self.client.get(next_api_query)
            next_api_query = response['links']['next']
            for resource in response['results']:
                resource_data = tuple(resource.values())
                yield resource_data
