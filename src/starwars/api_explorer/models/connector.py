from __future__ import annotations
from abc import ABC
from typing import Literal

import petl
import requests_cache

from starwars.api_explorer.models.client import ApiClient

requests_cache.install_cache('cache_api_explorer')
SampleAPIResourceType = Literal['people', 'planets', 'films', 'species', 'vehicles', 'starships']
SAMPLE_API_URL = 'https://swapi.dev/api'


class AbstractAPIConnector(ABC, petl.Table):
    api_name = None

    def __init__(self, client: ApiClient, resource: str):
        self.client = client
        self.resource = resource
        self.api_url = None

    @property
    def resource_url(self):
        return f'{self.api_url}/{self.resource}'


class SampleAPIConnector(AbstractAPIConnector):
    api_name = 'SWAPI'

    def __init__(self, client: ApiClient, resource: SampleAPIResourceType):
        super().__init__(client, resource)
        self.api_url = SAMPLE_API_URL

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
