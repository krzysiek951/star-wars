from typing import Literal

from django.db.models.fields.files import FieldFile

from starwars.api_explorer.models.exporter import AbstractExporter, CSVExporter
from starwars.api_explorer.models.importer import AbstractImporter, CSVImporter
from starwars.api_explorer.utils.utils import get_file_extension
from starwars.api_explorer.models.exceptions import NotSupportedFileExtension

ExportedFileExtension = Literal['csv']

IMPORTER_FACTORIES = {
    "csv": CSVImporter
}

EXPORTER_FACTORIES = {
    "csv": CSVExporter
}


def get_data_importer(filepath: FieldFile) -> AbstractImporter:
    extension = get_file_extension(filepath)  # TODO: Move to utils
    if extension in IMPORTER_FACTORIES.keys():
        return IMPORTER_FACTORIES[extension](filepath)
    else:
        raise NotSupportedFileExtension(extension)


def get_data_exporter(extension: ExportedFileExtension) -> AbstractExporter:
    if extension in EXPORTER_FACTORIES.keys():
        return EXPORTER_FACTORIES[extension]()
    else:
        raise NotSupportedFileExtension(extension)
