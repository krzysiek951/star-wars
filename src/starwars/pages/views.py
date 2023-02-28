import logging
from time import time

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import petl

from starwars.settings import (COLLECTIONS_DIR, DEFAULT_PER_PAGE, QUERY_PER_PAGE, QUERY_COLUMN,
                               QUERY_SORT_BY)
from .models.director import DisplayedDataDirector, StoredPeopleDataDirector
from .models.db_models import UserCollection

from starwars.starwars_explorer.models.exceptions import ResourceDoesNotExist
from starwars.starwars_explorer.models.importer import get_data_importer
from starwars.starwars_explorer.models.resource import SwapiResourceType, SwapiResource
from starwars.starwars_explorer.models.exporter import get_data_exporter
from starwars.starwars_explorer.models.client import ApiClient

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
    displayed_data = DisplayedDataDirector(
        collection_data=imported_data,
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


def fetch_starwars_people(request):
    resource: SwapiResourceType = 'people'
    client = ApiClient()
    try:
        with client:
            start_timer = time()
            collection = SwapiResource(resource, client)
            collection_exported = StoredPeopleDataDirector(collection, client).transform()
            data_exporter = get_data_exporter('csv')
            data_exporter.export(collection_exported, COLLECTIONS_DIR)
            user_collection = UserCollection(name=resource, filepath=data_exporter.filepath).save()  # noqa
            end_timer = time()
            fetch_time = end_timer - start_timer

        messages.success(request, f'Created new resource collection of "{resource}" in {fetch_time:.2f} s.')
        logger.info(f'Created new resource collection of "{resource}".')

    except ResourceDoesNotExist:
        messages.error(request, 'An error occurred while collecting data from API. Please try again later.')
        logger.error(f'Unable to fetch the "{resource}" data from SWAPI.')

    return redirect('home')
