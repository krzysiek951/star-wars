import logging
from time import time

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

import petl

from .client import ApiClient

from starwars.settings import (COLLECTIONS_DIR, DEFAULT_PER_PAGE, API_BASE_URL, QUERY_PER_PAGE, QUERY_COLUMN,
                               QUERY_SORT_BY)
from starwars.starwars_explorer.exceptions import ResourceDoesNotExist
from starwars.starwars_explorer.models import PeopleCollection, get_api_resources, get_collection_exporter, ResourceType

from .models.collection_importer import get_collection_importer
from .models.db_models import UserCollection
from .models.transformations_director import TransformationsDirector

logger = logging.getLogger('__main__.' + __name__)


def home(request):
    collections = UserCollection.objects.order_by('-created_at')
    query_results = {
        'collections': collections,
    }
    return render(request, 'home.html', query_results)


def collection_details(request, collection_id):
    collection = get_object_or_404(UserCollection, pk=collection_id)
    imported_data = get_collection_importer(collection.filepath).import_data()

    transformations_director = TransformationsDirector(
        collection_data=imported_data,
        columns=request.GET.getlist(QUERY_COLUMN),
        per_page=request.GET.get(QUERY_PER_PAGE, DEFAULT_PER_PAGE),
        sort_by=request.GET.get(QUERY_SORT_BY, None),
    )
    displayed_data = transformations_director.transform()
    query_results = {
        'collection': collection,
        'collection_header': petl.header(imported_data),
        'displayed_header': petl.header(displayed_data),
        'displayed_data': petl.data(displayed_data),
        'is_more_results': petl.nrows(displayed_data) < petl.nrows(imported_data),
    }
    return render(request, 'collection.html', query_results)


def fetch_starwars_people(request):
    resource: ResourceType = 'people'
    client = ApiClient()
    start_timer = time()
    try:
        with client:
            people = get_api_resources(client=client, url=API_BASE_URL, resource=resource)
            people_collection = PeopleCollection(client=client, raw_data=people)
        collection_exporter = get_collection_exporter('csv')
        collection_exporter.export(people_collection, COLLECTIONS_DIR)
        end_timer = time()

        user_collection = UserCollection(
            name=collection_exporter.collection.type,
            filepath=collection_exporter.filepath,
        )
        user_collection.save()

        messages.success(request,
                         f'Created new resource collection of "{resource}" in {end_timer - start_timer:.2f} s.')
        logger.info(f'Created new resource collection of "{resource}".')

    except ResourceDoesNotExist:
        messages.error(request, 'An error occurred while collecting data from API. Please try again later.')
        logger.error(f'Unable to fetch the "{resource}" data from SWAPI.')

    return redirect('home')
