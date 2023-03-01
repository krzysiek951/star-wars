from typing import Literal

from django.db.models.fields.files import FieldFile

from starwars.starwars_explorer.models.exporter import AbstractExporter, CSVExporter
from starwars.starwars_explorer.models.importer import AbstractImporter, CSVImporter
from starwars.starwars_explorer.utils.utils import get_file_extension
from starwars.starwars_explorer.models.exceptions import NotSupportedFileExtension
ExportedFileExtension = Literal['csv']


def get_data_importer(filepath: FieldFile) -> AbstractImporter:
    extension = get_file_extension(filepath)
    factories = {
        "csv": CSVImporter(filepath)
    }
    if extension in factories.keys():
        return factories[extension]
    else:
        raise NotSupportedFileExtension(extension)


def get_data_exporter(extension: ExportedFileExtension) -> AbstractExporter:
    factories = {
        "csv": CSVExporter()
    }
    if extension in factories.keys():
        return factories[extension]
    else:
        raise NotSupportedFileExtension(extension)
