from ..utils import transformations as trans
from petl.util.base import Table as PetlTable


class TransformationsDirector:
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
