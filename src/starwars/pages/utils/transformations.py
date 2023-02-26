from typing import Union

import petl

from starwars.pages.exceptions import MissingTableField
from starwars.pages.utils.utils import get_sort_name, is_order_reversed

from starwars.settings import DEFAULT_PER_PAGE
from petl.util.base import Table as PetlTable


def sort_by(collection: PetlTable, field: str = None) -> PetlTable:
    if field:
        field_name = get_sort_name(field)
        if field_name not in petl.header(collection):
            raise MissingTableField(field)
        return petl.sort(collection, get_sort_name(field), reverse=is_order_reversed(field))
    else:
        return collection


def group_by(collection: PetlTable, selected_column: list[str] = None) -> PetlTable:
    columns = [c for c in petl.header(collection) if c in selected_column]  # to keep original header order
    return collection if not selected_column else petl.valuecounts(petl.cut(collection, columns), *columns).cutout(
        'frequency')


def limit_to(collection: PetlTable, per_page: str = None) -> PetlTable:
    try:
        results_per_page = int(per_page)
    except ValueError:
        results_per_page = DEFAULT_PER_PAGE
    return petl.head(collection, results_per_page)


def str_to_digit(value: str) -> Union[float, int, str]:
    try:
        number = float(value.replace(",", ""))
        return number if not number.is_integer() else int(number)
    except ValueError:
        return value


def to_number(collection: PetlTable, field: str) -> PetlTable:
    return petl.convert(collection, field, lambda x: str_to_digit(x))
