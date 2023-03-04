from typing import Literal

from django.db.models.fields.files import FieldFile

from starwars.api_explorer.models.exporter import AbstractExporter, CSVExporter
from starwars.api_explorer.models.importer import AbstractImporter, CSVImporter
from starwars.api_explorer.utils.utils import get_file_extension
from starwars.api_explorer.models.exceptions import NotSupportedFileExtension

ExportedFileExtension = Literal['csv']

IMPORTER_FACTORY = {
    "csv": CSVImporter
}

EXPORTER_FACTORY = {
    "csv": CSVExporter
}


def get_data_importer(filepath: FieldFile) -> AbstractImporter:
    extension = get_file_extension(filepath)
    if extension in IMPORTER_FACTORY.keys():
        return IMPORTER_FACTORY[extension](filepath)
    else:
        raise NotSupportedFileExtension(extension)


def get_data_exporter(extension: ExportedFileExtension) -> AbstractExporter:
    if extension in EXPORTER_FACTORY.keys():
        return EXPORTER_FACTORY[extension]()
    else:
        raise NotSupportedFileExtension(extension)
