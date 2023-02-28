from typing import Union, Optional, Callable
import petl
from dateutil import parser

from starwars.starwars_explorer.models.client import ApiClient
from starwars.starwars_explorer.utils.utils import get_sort_name, is_order_reversed, str_to_digit
from starwars.settings import DEFAULT_PER_PAGE


def sort_by(collection: petl.Table, field: str = None) -> petl.Table:
    if not field or get_sort_name(field) not in petl.header(collection):
        return collection
    else:
        return petl.sort(collection, get_sort_name(field), reverse=is_order_reversed(field))


def group_by(collection: petl.Table, selected_column: list[str] = None) -> petl.Table:
    columns = [c for c in petl.header(collection) if c in selected_column]  # to keep original header order
    return collection if not selected_column else petl.valuecounts(petl.cut(collection, columns), *columns).cutout(
        'frequency')


def limit_to(collection: petl.Table, per_page: str = None) -> petl.Table:
    try:
        results_per_page = int(per_page)
    except ValueError:
        results_per_page = DEFAULT_PER_PAGE
    return petl.head(collection, results_per_page)


def to_number(collection: petl.Table, field: str) -> petl.Table:
    return petl.convert(collection, field, lambda x: str_to_digit(x))


def drop_fields(collection: petl.Table, dropped_fields: list[str]) -> petl.Table:
    return petl.cutout(collection, *dropped_fields)


def resolve_url(collection: petl.Table, client: ApiClient, from_: str, to_: str) -> petl.Table:
    return petl.convert(collection, from_, lambda x: client.get(x).get(to_, None))


def add_column(collection: petl.Table, new_column_name: str, func: Callable, func_arg: str):
    return petl.addfield(collection, new_column_name, lambda x: func(x[func_arg]))
