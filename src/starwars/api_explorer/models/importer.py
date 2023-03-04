from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass

import petl
from django.db.models.fields.files import FieldFile


@dataclass
class AbstractImporter:
    filepath: FieldFile

    @abstractmethod
    def import_data(self) -> petl.Table:
        ...


class CSVImporter(AbstractImporter):

    def import_data(self) -> petl.Table:
        return petl.fromcsv(self.filepath)
