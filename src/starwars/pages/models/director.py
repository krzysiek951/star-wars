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

    @abstractmethod
    def transform(self) -> petl.Table:
        ...


class DefaultStorageDirector(AbstractStorageDirector):
    def transform(self) -> petl.Table:
        return self.collection_data


class SwapiPeopleStorageDirector(AbstractStorageDirector):
    def transform(self) -> petl.Table:
        data = self.collection_data
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

    @abstractmethod
    def transform(self, **kwargs) -> petl.Table:
        ...


class DefaultViewDirector(AbstractViewDirector):

    def transform(self) -> petl.Table:
        data = self.collection_data
        data = trans.group_by(data, self.columns)
        data = trans.sort_by(data, self.sort_by)
        data = trans.limit_to(data, self.per_page)
        return data


class SwapiPeopleViewDirector(AbstractViewDirector):

    def transform(self) -> petl.Table:
        data = self.collection_data
        data = trans.to_number(data, 'height')
        data = trans.to_number(data, 'mass')
        data = trans.group_by(data, self.columns)
        data = trans.sort_by(data, self.sort_by)
        data = trans.limit_to(data, self.per_page)
        return data
