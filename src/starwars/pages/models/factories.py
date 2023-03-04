from enum import Enum
from typing import Any

import petl

from starwars.pages.models.director import (
    AbstractStorageDirector,
    SwapiPeopleStorageDirector,
    DefaultStorageDirector,
    SwapiPeopleViewDirector,
    DefaultViewDirector,
    AbstractViewDirector
)
from starwars.pages.models.resource import SwapiResource, TripAwayResource
from starwars.settings import SUPPORTED_API
from starwars.api_explorer.models.client import ApiClient
from starwars.api_explorer.models.exceptions import NotSupportedAPI
from starwars.api_explorer.models.resource import (
    AbstractAPIResource,
)


class SupportedApi(Enum):
    SWAPI = 'swapi'
    TRIPAWAY = 'tripaway'


class SwapiResourceName(Enum):
    PEOPLE = 'people'
    PLANETS = 'planets'
    FILMS = 'films'
    SPECIES = 'species'
    VEHICLES = 'vehicles'
    STARSHIPS = 'starships'


class TripAwayResourceName(Enum):
    PLACES = 'places'


RESOURCE_FACTORY = {
    SupportedApi.SWAPI.value: SwapiResource,
    SupportedApi.TRIPAWAY.value: TripAwayResource
}

STORAGE_DIRECTOR_FACTORY = {
    SupportedApi.SWAPI.value: {
        SwapiResourceName.PEOPLE.value: SwapiPeopleStorageDirector,
    },
}

VIEW_DIRECTOR_FACTORY = {
    SupportedApi.SWAPI.value: {
        SwapiResourceName.PEOPLE.value: SwapiPeopleViewDirector,
    },
}


def get_storage_director(
        client: ApiClient,
        api: SUPPORTED_API,
        resource: str,
        collection: petl.Table,
) -> AbstractStorageDirector:
    if resource in STORAGE_DIRECTOR_FACTORY.get(api, {}).keys():
        return STORAGE_DIRECTOR_FACTORY[api][resource](collection, client)
    else:
        return DefaultStorageDirector(collection, client)


def get_view_director(
        api: SUPPORTED_API,
        resource: str,
        collection: petl.Table,
        sort_by: str,
        columns: list[str],
        per_page: str,
) -> AbstractViewDirector:
    if resource in VIEW_DIRECTOR_FACTORY.get(api, {}).keys():
        return VIEW_DIRECTOR_FACTORY[api][resource](collection, sort_by, columns, per_page)
    else:
        return DefaultViewDirector(collection, sort_by, columns, per_page)


def get_api_resources(
        client: ApiClient,
        api: Any,
        resource: str,
) -> AbstractAPIResource:
    if api in RESOURCE_FACTORY.keys():
        return RESOURCE_FACTORY[api](client, resource)
    else:
        raise NotSupportedAPI(f'Unable to fetch resources from "{api}". Provided API is not currently supported.')
