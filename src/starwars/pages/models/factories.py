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

STORAGE_DIRECTOR_FACTORIES = {
    "swapi": {
        "people": SwapiPeopleStorageDirector,
    },
}

VIEW_DIRECTOR_FACTORIES = {
    "swapi": {
        "people": SwapiPeopleViewDirector,
    },
}

API_FACTORIES = {
    "swapi": SwapiResource,
    'tripaway': TripAwayResource,
}


def get_storage_director(
        client: ApiClient,
        api: SUPPORTED_API,
        resource: str,
        collection: petl.Table,
) -> AbstractStorageDirector:
    if resource in STORAGE_DIRECTOR_FACTORIES.get(api, {}).keys():
        return STORAGE_DIRECTOR_FACTORIES[api][resource](collection, client)
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
    if resource in VIEW_DIRECTOR_FACTORIES.get(api, {}).keys():
        return VIEW_DIRECTOR_FACTORIES[api][resource](collection, sort_by, columns, per_page)
    else:
        return DefaultViewDirector(collection, sort_by, columns, per_page)


def get_api_resources(
        client: ApiClient,
        api: SUPPORTED_API,
        resource: str,
) -> AbstractAPIResource:
    if api in API_FACTORIES.keys():
        return API_FACTORIES[api](client, resource)
    else:
        raise NotSupportedAPI(f'Unable to fetch resources from "{api}". Provided API is not currently supported.')
