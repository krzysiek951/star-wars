from starwars.starwars_explorer.models.client import ApiClient
from starwars.starwars_explorer.utils import transformations as trans
from petl.util.base import Table as PetlTable

from starwars.starwars_explorer.utils.utils import str_date_to_iso


class StoredPeopleDataDirector:
    def __init__(
            self,
            collection_data: PetlTable,
            client: ApiClient = None,
    ):
        self.collection_data = collection_data
        self.client = client

    def transform(self) -> PetlTable:
        data = self.collection_data
        data = trans.resolve_url(data, self.client, 'homeworld', 'name')
        data = trans.add_column(data, 'date', str_date_to_iso, 'edited')
        data = trans.drop_fields(data, ['url', 'films', 'species', 'vehicles', 'starships', 'created', 'edited'])

        return data


class DisplayedDataDirector:
    def __init__(
            self,
            collection_data: PetlTable,
            sort_by: str = None,
            columns: list[str] = None,
            per_page: str = None,
    ):
        self.collection_data = collection_data
        self.sort_by = sort_by
        self.columns = columns
        self.per_page = per_page

    def transform(self) -> PetlTable:
        data = self.collection_data
        data = trans.to_number(data, 'height')
        data = trans.to_number(data, 'mass')
        data = trans.group_by(data, self.columns)
        data = trans.sort_by(data, self.sort_by)
        data = trans.limit_to(data, self.per_page)

        return data
