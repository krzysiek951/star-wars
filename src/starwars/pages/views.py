import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

import petl

from .models import UserCollection
from .client import ApiClient

from starwars.settings import COLLECTIONS_DIR, DEFAULT_PER_PAGE, API_BASE_URL, QUERY_PER_PAGE, QUERY_COLUMN, \
    QUERY_SORT_BY
from starwars.starwars_explorer.exceptions import ResourceDoesNotExist
from starwars.starwars_explorer.models import PeopleCollection, CsvExporter, get_api_resources

logger = logging.getLogger('__main__.' + __name__)


def home(request):
    collections = UserCollection.objects.order_by('-created_at')
    query_results = {
        'collections': collections,
    }
    return render(request, 'home.html', query_results)


def collection(request, collection_id):
    user_collection = get_object_or_404(UserCollection, pk=collection_id)
    collection_data = petl.fromcsv(user_collection.filepath)

    selected_columns = request.GET.getlist(QUERY_COLUMN)
    per_page = request.GET.get(QUERY_PER_PAGE, DEFAULT_PER_PAGE)
    sort_by = request.GET.get(QUERY_SORT_BY, None)

    collection_header = petl.header(collection_data)
    displayed_columns = [i for i in collection_header if i in selected_columns]

    if displayed_columns:
        collection_data_cut = petl.cut(collection_data, displayed_columns)
        collection_data = petl.valuecounts(collection_data_cut, *displayed_columns).cutout('frequency')

    if sort_by:
        reverse_order = sort_by.startswith('-')
        sort_by_field = sort_by if not reverse_order else sort_by[1:]
        collection_data = petl.sort(collection_data, sort_by_field, reverse=reverse_order)

    try:
        results_per_page = int(per_page)
    except ValueError:
        results_per_page = DEFAULT_PER_PAGE

    displayed_table = petl.head(collection_data, results_per_page)
    displayed_header = petl.header(displayed_table)
    displayed_data = petl.data(displayed_table)
    collection_count = petl.nrows(collection_data)
    is_more_results = results_per_page < collection_count

    query_results = {
        'user_collection': user_collection,
        'collection_header': collection_header,
        'displayed_columns': displayed_columns,
        'displayed_header': displayed_header,
        'displayed_data': displayed_data,
        'is_more_results': is_more_results,
    }
    return render(request, 'collection.html', query_results)


def fetch_starwars_people(request):
    resource = 'people'
    client = ApiClient()

    try:
        with client:
            people = get_api_resources(client=client, url=API_BASE_URL, resource=resource)
            people_collection = PeopleCollection(client=client, raw_data=people)
        collection_exporter = CsvExporter(people_collection)
        collection_exporter.export(COLLECTIONS_DIR)

        user_collection = UserCollection(
            name=collection_exporter.collection.type,
            filepath=collection_exporter.filepath)
        user_collection.save()

        messages.success(request, f'Created new resource collection of "{resource}".')
        logger.info(f'Created new resource collection of "{resource}".')

    except ResourceDoesNotExist:
        messages.error(request, 'An error occurred while collecting data from API. Please try again later.')
        logger.error(f'Unable to fetch the "{resource}" data from SWAPI.')

    return redirect('home')
