from __future__ import annotations

import uuid
import os
from abc import abstractmethod
from dataclasses import dataclass

import petl


@dataclass
class AbstractExporter:
    filepath: str = ''

    @abstractmethod
    def export(self, collection: petl.Table, export_dir) -> None:
        ...


class CSVExporter(AbstractExporter):

    def export(self, collection: petl.Table, export_dir: str) -> None:
        self.filepath = os.path.join(export_dir, f'{uuid.uuid4().hex}.csv')
        petl.tocsv(collection, self.filepath)
