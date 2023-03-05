import logging

from django.shortcuts import render, redirect, get_object_or_404
import petl

from starwars.settings import (
    DEFAULT_PER_PAGE,
    QUERY_PER_PAGE,
    QUERY_COLUMN,
    QUERY_SORT_BY
)
from .utils.fetch import fetch_api_data
from .models.db_models import UserCollection
from .models.connector import SwapiConnector, TripAwayConnector
from .models.storage_director import SwapiPeopleStorageDirector
from .models.factories import get_view_director
from starwars.api_explorer.models.factories import get_data_importer

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
    displayed_data = get_view_director(
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


def swapi_default_fetch(request, resource):
    fetch_api_data(
        request,
        resource,
        connector=SwapiConnector(),
    )
    return redirect('home')


def swapi_custom_fetch(request, resource):
    fetch_api_data(
        request,
        resource,
        connector=SwapiConnector(),
        storage_director=SwapiPeopleStorageDirector()
    )
    return redirect('home')


def tripaway_default_fetch(request, resource):
    fetch_api_data(
        request,
        resource,
        connector=TripAwayConnector(),
    )
    return redirect('home')
