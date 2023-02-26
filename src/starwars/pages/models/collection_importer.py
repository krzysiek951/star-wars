from __future__ import annotations
from abc import abstractmethod

import petl
from django.db.models.fields.files import FieldFile

from starwars.pages.exceptions import NotSupportedFileExtension
from starwars.pages.utils.utils import get_file_extension
from petl.util.base import Table as petl_Table


def get_collection_importer(filepath: FieldFile) -> AbstractImporter:
    extension = get_file_extension(filepath)
    factories = {
        "csv": CSVImporter(filepath)
    }
    if extension in factories.keys():
        return factories[extension]
    else:
        raise NotSupportedFileExtension(extension)


class AbstractImporter:
    def __init__(self, filepath: FieldFile):
        self.filepath = filepath

    @abstractmethod
    def import_data(self) -> petl_Table:
        ...


class CSVImporter(AbstractImporter):

    def import_data(self) -> petl_Table:
        return petl.fromcsv(self.filepath)
