from abc import ABC, abstractmethod
from dataclasses import dataclass

from starwars.starwars_explorer.models.client import ApiClient
from starwars.starwars_explorer.utils import transformations as trans
from petl.util.base import Table as PetlTable

from starwars.starwars_explorer.utils.utils import str_date_to_iso


@dataclass
class AbstractStorageDirector(ABC):
    collection_data: PetlTable
    client: ApiClient

    @abstractmethod
    def transform(self) -> PetlTable:
        ...


class DefaultStorageDirector(AbstractStorageDirector):
    def transform(self) -> PetlTable:
        return self.collection_data


class SwapiPeopleStorageDirector(AbstractStorageDirector):
    def transform(self) -> PetlTable:
        data = self.collection_data
        data = trans.resolve_url(data, self.client, 'homeworld', 'name')
        data = trans.add_column(data, 'date', str_date_to_iso, 'edited')
        data = trans.drop_fields(data, ['url', 'films', 'species', 'vehicles', 'starships', 'created', 'edited'])
        return data


@dataclass
class AbstractViewDirector(ABC):
    collection_data: PetlTable
    sort_by: str = None
    columns: list[str] = None
    per_page: str = None

    @abstractmethod
    def transform(self, **kwargs) -> PetlTable:
        ...


class DefaultViewDirector(AbstractViewDirector):

    def transform(self) -> PetlTable:
        data = self.collection_data
        data = trans.group_by(data, self.columns)
        data = trans.sort_by(data, self.sort_by)
        data = trans.limit_to(data, self.per_page)
        return data


class SwapiPeopleViewDirector(AbstractViewDirector):

    def transform(self) -> PetlTable:
        data = self.collection_data
        data = trans.to_number(data, 'height')
        data = trans.to_number(data, 'mass')
        data = trans.group_by(data, self.columns)
        data = trans.sort_by(data, self.sort_by)
        data = trans.limit_to(data, self.per_page)
        return data
