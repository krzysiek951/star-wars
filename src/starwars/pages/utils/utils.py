import pathlib

from django.db.models.fields.files import FieldFile


def get_file_extension(filepath: FieldFile) -> str:
    return pathlib.Path(filepath.path).suffix.lstrip('.')


def get_sort_name(field: str):
    return field.lstrip('-')


def is_order_reversed(field: str):
    return field.startswith('-')
