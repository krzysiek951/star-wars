from abc import ABC, abstractmethod

import petl

from starwars.api_explorer.models.client import ApiClient
from starwars.api_explorer.utils import transformations as trans

from starwars.api_explorer.utils.utils import str_date_to_iso


class AbstractStorageDirector(ABC):

    def transform(self, client: ApiClient, collection_data: petl.Table) -> petl.Table:
        data = collection_data
        data = self._init_hook(client, data)
        return data

    @abstractmethod
    def _init_hook(self, client: ApiClient, data: petl.Table) -> petl.Table:
        ...


class DefaultStorageDirector(AbstractStorageDirector):

    def _init_hook(self, client: ApiClient, data: petl.Table) -> petl.Table:
        return data


class SwapiPeopleStorageDirector(AbstractStorageDirector):

    def _init_hook(self, client: ApiClient, data: petl.Table) -> petl.Table:
        data = trans.resolve_url(data, client, 'homeworld', 'name')
        data = trans.add_column(data, 'date', str_date_to_iso, 'edited')
        data = trans.drop_fields(data, ['url', 'films', 'species', 'vehicles', 'starships', 'created', 'edited'])
        return data
