import logging
from time import time

from starwars.api_explorer.models.client import ApiClient
from starwars.api_explorer.models.exceptions import ResourceDoesNotExist
from starwars.api_explorer.models.exporter import AbstractExporter, CSVExporter
from starwars.api_explorer.models.connector import AbstractAPIConnector
from starwars.pages.models.db_models import UserCollection
from starwars.pages.models.storage_director import AbstractStorageDirector, DefaultStorageDirector
from starwars.settings import COLLECTIONS_DIR
from django.contrib import messages

logger = logging.getLogger('__main__.' + __name__)


def fetch_api_data(
        request,
        resource: str,
        connector: AbstractAPIConnector,
        exporter: AbstractExporter = CSVExporter(),
        storage_director: AbstractStorageDirector = DefaultStorageDirector(),
) -> None:
    client = ApiClient()
    try:
        with client:
            start_timer = time()
            connector.client = client
            connector.resource = resource

            collection = connector
            collection_exported = storage_director.transform(client, collection)
            exporter.export(collection_exported, COLLECTIONS_DIR)

            user_collection = UserCollection(  # noqa
                api=collection.api_name,
                resource=resource,
                filepath=exporter.filepath
            ).save()
            end_timer = time()
            fetch_time = end_timer - start_timer

        messages.success(request, f'Created new collection of "{resource}" in {fetch_time:.2f} s.')
        logger.info(f'Created new collection of "{resource}".')

    except ResourceDoesNotExist:
        messages.error(request, 'An error occurred while collecting data from API. Please try again later.')
        logger.error(f'Unable to fetch the "{resource}" data from {collection.api_name}.')
