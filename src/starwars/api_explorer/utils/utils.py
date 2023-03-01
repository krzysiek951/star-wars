import pathlib
from typing import Union, Optional

from dateutil import parser
from django.db.models.fields.files import FieldFile


def get_file_extension(filepath: FieldFile) -> str:
    return pathlib.Path(filepath.path).suffix.lstrip('.')


def get_sort_name(field: str):
    return field.lstrip('-')


def is_order_reversed(field: str):
    return field.startswith('-')


def str_to_digit(value: str) -> Union[float, int, str]:
    try:
        number = float(value.replace(",", ""))
        return number if not number.is_integer() else int(number)
    except ValueError:
        return value


def str_date_to_iso(date: str) -> Optional[str]:
    return None if not date else parser.isoparse(date).date().isoformat()
