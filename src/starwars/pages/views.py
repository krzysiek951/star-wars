import logging
from time import time

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import petl

from starwars.settings import (COLLECTIONS_DIR, DEFAULT_PER_PAGE, QUERY_PER_PAGE, QUERY_COLUMN,
                               QUERY_SORT_BY)
from .models.db_models import UserCollection

from starwars.starwars_explorer.models.exceptions import ResourceDoesNotExist
from starwars.starwars_explorer.models.factories import get_data_importer
from starwars.starwars_explorer.models.resource import SwapiResourceType, SwapiResource
from starwars.starwars_explorer.models.factories import get_data_exporter
from starwars.starwars_explorer.models.client import ApiClient
from .models.factories import get_storage_director, get_dataview_director, get_api_resources

logger = logging.getLogger('__main__.' + __name__)


def home(request):
    collections = UserCollection.objects.order_by('-created_at')
    query_results = {
        'collections': collections,
    }
    return render(request, 'home.html', query_results)


def collection_details(request, collection_id):
    collection = get_object_or_404(UserCollection, pk=collection_id)
    imported_data = get_data_importer(collection.filepath).import_data()
    displayed_data = get_dataview_director(
        api=collection.api,
        resource=collection.resource,
        collection=imported_data,
        columns=request.GET.getlist(QUERY_COLUMN),
        per_page=request.GET.get(QUERY_PER_PAGE, DEFAULT_PER_PAGE),
        sort_by=request.GET.get(QUERY_SORT_BY, None),
    ).transform()
    query_results = {
        'collection': collection,
        'collection_header': petl.header(imported_data),
        'displayed_header': petl.header(displayed_data),
        'displayed_data': petl.data(displayed_data),
        'is_more_results': petl.nrows(displayed_data) < petl.nrows(imported_data),
    }
    return render(request, 'collection.html', query_results)


def fetch(request, api, resource):
    resource: SwapiResourceType
    client = ApiClient()
    try:
        with client:
            start_timer = time()
            collection = get_api_resources(client, api, resource)
            collection_exported = get_storage_director(client, api, resource, collection).transform()
            data_exporter = get_data_exporter('csv')
            data_exporter.export(collection_exported, COLLECTIONS_DIR)
            user_collection = UserCollection(api=api, resource=resource, filepath=data_exporter.filepath).save()  # noqa
            end_timer = time()
            fetch_time = end_timer - start_timer

        messages.success(request, f'Created new resource collection of "{resource}" in {fetch_time:.2f} s.')
        logger.info(f'Created new resource collection of "{resource}".')

    except ResourceDoesNotExist:
        messages.error(request, 'An error occurred while collecting data from API. Please try again later.')
        logger.error(f'Unable to fetch the "{resource}" data from {collection.api_name}.')

    return redirect('home')
