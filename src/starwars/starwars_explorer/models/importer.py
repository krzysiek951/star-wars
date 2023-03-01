from __future__ import annotations
from abc import abstractmethod

import petl
from django.db.models.fields.files import FieldFile


class AbstractImporter:
    def __init__(self, filepath: FieldFile):
        self.filepath = filepath

    @abstractmethod
    def import_data(self) -> petl.Table:
        ...


class CSVImporter(AbstractImporter):

    def import_data(self) -> petl.Table:
        return petl.fromcsv(self.filepath)
