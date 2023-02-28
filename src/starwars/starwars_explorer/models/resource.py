from __future__ import annotations
from abc import ABC
from typing import Literal

import petl
import requests_cache

from starwars.starwars_explorer.models.client import ApiClient

requests_cache.install_cache('starwars_cache')
SwapiResourceType = Literal['people', 'planets', 'films', 'species', 'vehicles', 'starships']
SWAPI_BASE_URL = 'https://swapi.dev/api'


class AbstractAPIResource(ABC, petl.Table):
    def __init__(self, client: ApiClient, resource: SwapiResourceType):
        self.client = client
        self.resource = resource
        self.api_url = None

    @property
    def resource_url(self):
        return f'{self.api_url}/{self.resource}'


class SwapiResource(AbstractAPIResource):
    def __init__(self, resource: SwapiResourceType, client: ApiClient):
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
