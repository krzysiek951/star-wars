import petl

from starwars.pages.models.director import AbstractStorageDirector, SwapiPeopleStorageDirector, DefaultStorageDirector, \
    SwapiPeopleViewDirector, DefaultViewDirector, AbstractViewDirector
from starwars.settings import SUPPORTED_API
from starwars.starwars_explorer.models.client import ApiClient
from starwars.starwars_explorer.models.exceptions import NotSupportedAPI
from starwars.starwars_explorer.models.resource import SwapiResourceType, SwapiResource, AbstractAPIResource, \
    TripAwayResource

EXPORTED_DATA_FACTORIES = {
    "swapi": {
        "people": SwapiPeopleStorageDirector,
    },
}

DISPLAYED_DATA_FACTORIES = {
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
        resource: SwapiResourceType,
        collection: petl.Table,
) -> AbstractStorageDirector:
    if api in EXPORTED_DATA_FACTORIES.keys() and resource in EXPORTED_DATA_FACTORIES[api].keys():
        return EXPORTED_DATA_FACTORIES[api][resource](collection, client)
    else:
        return DefaultStorageDirector(collection, client)


def get_dataview_director(
        api: SUPPORTED_API,
        resource: SwapiResourceType,
        collection: petl.Table,
        sort_by: str,
        columns: list[str],
        per_page: str,
) -> AbstractViewDirector:
    if api in DISPLAYED_DATA_FACTORIES.keys() and resource in DISPLAYED_DATA_FACTORIES[api].keys():
        return DISPLAYED_DATA_FACTORIES[api][resource](collection, sort_by, columns, per_page)
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
