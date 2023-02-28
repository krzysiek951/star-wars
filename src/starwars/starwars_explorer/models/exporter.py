from __future__ import annotations

import uuid
import os
from abc import abstractmethod
from typing import Literal

import petl

from starwars.starwars_explorer.models.exceptions import NotSupportedFileExtension

ExportedFileExtension = Literal['csv']


def get_data_exporter(extension: ExportedFileExtension) -> AbstractExporter:
    factories = {
        "csv": CSVExporter()
    }
    if extension in factories.keys():
        return factories[extension]
    else:
        raise NotSupportedFileExtension(extension)


class AbstractExporter:
    def __init__(self):
        self.filepath: str = ''

    @abstractmethod
    def export(self, collection: petl.Table, export_dir) -> None:
        ...


class CSVExporter(AbstractExporter):
    def __init__(self):
        super().__init__()

    def export(self, collection: petl.Table, export_dir: str) -> None:
        self.filepath = os.path.join(export_dir, f'{uuid.uuid4().hex}.csv')
        petl.tocsv(collection, self.filepath)
