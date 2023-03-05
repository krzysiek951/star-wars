from enum import Enum

import petl

from starwars.pages.models.view_director import (
    SwapiPeopleViewDirector,
    DefaultViewDirector,
    AbstractViewDirector
)

from starwars.settings import SUPPORTED_API


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


VIEW_DIRECTOR_FACTORY = {
    SupportedApi.SWAPI.value: {
        SwapiResourceName.PEOPLE.value: SwapiPeopleViewDirector,
    },
}


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
