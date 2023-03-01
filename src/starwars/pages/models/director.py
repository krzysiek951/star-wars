from abc import ABC, abstractmethod
from dataclasses import dataclass

import petl

from starwars.api_explorer.models.client import ApiClient
from starwars.api_explorer.utils import transformations as trans

from starwars.api_explorer.utils.utils import str_date_to_iso


@dataclass
class AbstractStorageDirector(ABC):
    collection_data: petl.Table
    client: ApiClient

    def transform(self, **kwargs) -> petl.Table:
        data = self.collection_data
        data = self._init_hook(data, **kwargs)
        return data

    @abstractmethod
    def _init_hook(self, data: petl.Table, **kwargs) -> petl.Table:
        ...


class DefaultStorageDirector(AbstractStorageDirector):

    def _init_hook(self, data: petl.Table, **kwargs) -> petl.Table:
        return data


class SwapiPeopleStorageDirector(AbstractStorageDirector):

    def _init_hook(self, data: petl.Table, **kwargs) -> petl.Table:
        data = trans.resolve_url(data, self.client, 'homeworld', 'name')
        data = trans.add_column(data, 'date', str_date_to_iso, 'edited')
        data = trans.drop_fields(data, ['url', 'films', 'species', 'vehicles', 'starships', 'created', 'edited'])
        return data


@dataclass
class AbstractViewDirector(ABC):
    collection_data: petl.Table
    sort_by: str = None
    columns: list[str] = None
    per_page: str = None

    def transform(self, **kwargs) -> petl.Table:
        data = self.collection_data
        data = self._init_hook(data, **kwargs)
        data = trans.group_by(data, self.columns)
        data = trans.sort_by(data, self.sort_by)
        data = trans.limit_to(data, self.per_page)
        data = self._post_hook(data, **kwargs)
        return data

    @abstractmethod
    def _init_hook(self, data: petl.Table, **kwargs) -> petl.Table:
        ...

    @abstractmethod
    def _post_hook(self, data: petl.Table, **kwargs) -> petl.Table:
        ...


class DefaultViewDirector(AbstractViewDirector):

    def _init_hook(self, data: petl.Table, **kwargs) -> petl.Table:
        return data

    def _post_hook(self, data: petl.Table, **kwargs) -> petl.Table:
        return data


class SwapiPeopleViewDirector(AbstractViewDirector):

    def _init_hook(self, data: petl.Table, **kwargs) -> petl.Table:
        data = trans.to_number(data, 'height')
        data = trans.to_number(data, 'mass')
        return data

    def _post_hook(self, data: petl.Table, **kwargs) -> petl.Table:
        return data
