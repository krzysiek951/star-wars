from __future__ import annotations
import csv
import os
from abc import ABC, abstractmethod
from typing import Iterable, Iterator, Literal, Optional

import requests_cache
import uuid
from dateutil import parser
from starwars.settings import DROPPED_FIELDS
from starwars.pages.client import ApiClient

requests_cache.install_cache('starwars_cache')
ResourceType = Literal['people']


def get_api_resources(client: ApiClient, url: str, resource: ResourceType) -> list[dict]:
    api_query = f'{url}/{resource}'
    api_resources = []
    is_next = True
    while is_next:
        response = client.get(api_query)
        for resource in response['results']:
            api_resources.append(resource)
        if bool(response['next']):
            api_query = response['next']
        else:
            is_next = False
    return api_resources


def format_date(date: str) -> Optional[str]:
    if not date:
        return None
    date_time = parser.isoparse(date)
    return date_time.date().isoformat()


class AbstractResource(ABC):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def exported_fields(self):
        return {k: v for k, v in self.__dict__.items() if k not in DROPPED_FIELDS}


class StarWarsPlanet(AbstractResource):
    def __init__(self, **kwargs):
        self.name: str = ''
        super().__init__(**kwargs)

    def __repr__(self):
        return f'Planet: {self.name}'


class StarWarsPerson(AbstractResource):

    def __init__(self, client: ApiClient, **kwargs):
        self.client: ApiClient = client
        self.name: str = ''
        self.created: str = ''
        super().__init__(**kwargs)

        self.homeworld = self.get_homeworld().name
        self.date = format_date(self.created)

    def __repr__(self):
        return f'Person: {self.name}'

    def get_homeworld(self) -> StarWarsPlanet:
        response = self.client.get(self.homeworld)
        return StarWarsPlanet(**response)


class ApiOrderIterator(Iterator):
    def __init__(self, collection: list[AbstractResource]) -> None:
        self._collection: list[AbstractResource] = collection
        self._position: int = 0

    def __next__(self) -> AbstractResource:
        try:
            value = self._collection[self._position]
            self._position += 1
        except IndexError:
            raise StopIteration()
        return value


class AbstractCollection(Iterable):
    type = None

    def __init__(self, client: ApiClient, collection: list[AbstractResource] = None, raw_data: list[dict] = None):
        self.client: ApiClient = client
        self._collection: list[AbstractResource] = collection
        if raw_data:
            for data_item in raw_data:
                self.add_item(**data_item)

    @abstractmethod
    def add_item(self, item: dict) -> None:
        ...

    @abstractmethod
    def __getitem__(self, value: int) -> AbstractResource:
        ...

    def __iter__(self) -> ApiOrderIterator:
        return ApiOrderIterator(self._collection)

    def __call__(self) -> list[AbstractResource]:
        return self._collection


class PeopleCollection(AbstractCollection):
    type = 'people'

    def __init__(self, client: ApiClient, collection: list[StarWarsPerson] = None, raw_data: list[dict] = None):
        super().__init__(client, collection, raw_data)

    def add_item(self, **kwargs) -> None:
        if not self._collection:
            self._collection = []
        self._collection.append(StarWarsPerson(client=self.client, **kwargs))

    def __getitem__(self, value: int) -> StarWarsPerson:
        return self._collection[value]


class CsvExporter:
    def __init__(self, collection: AbstractCollection):
        self.collection: AbstractCollection = collection
        self.filepath: str = ''

    def export(self, export_dir: str = None) -> None:
        filename = f'{uuid.uuid4().hex}.csv'
        self.filepath = os.path.join(export_dir, filename)
        collection_keys = self.collection[0].exported_fields().keys()
        with open(self.filepath, 'w', encoding='utf8', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=collection_keys)
            csv_writer.writeheader()
            for resource in self.collection:
                csv_writer.writerow(resource.exported_fields())
