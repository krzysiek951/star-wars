from __future__ import annotations

import uuid
import os
from abc import abstractmethod

import petl


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
