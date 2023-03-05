from abc import ABC, abstractmethod

import petl

from starwars.api_explorer.utils import transformations as trans


class AbstractViewDirector(ABC):
    def __init__(self, collection_data: petl.Table, sort_by: str, columns: list[str], per_page: str):
        self.collection_data = collection_data
        self.sort_by = sort_by
        self.columns = columns
        self.per_page = per_page

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
