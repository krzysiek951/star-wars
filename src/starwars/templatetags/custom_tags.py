from django import template

from starwars.settings import DEFAULT_PER_PAGE, DEFAULT_DISPLAY_MORE, QUERY_PER_PAGE, QUERY_COLUMN, QUERY_SORT_BY

register = template.Library()


@register.simple_tag
def sort_by(request, field):
    query = request.GET.copy()
    query_sort_by = query.get(QUERY_SORT_BY, '')
    new_sort_by = field if not field == query_sort_by else f'-{query_sort_by}'
    query[QUERY_SORT_BY] = new_sort_by
    return query.urlencode()


@register.simple_tag
def select_column(request, field):
    query = request.GET.copy()
    query_column_list = query.getlist(QUERY_COLUMN)
    query_sort_by = query.get(QUERY_SORT_BY, '').replace('-', '')
    columns_selected = bool(query_column_list)

    if field not in query_column_list:
        query_column_list.append(field)
    else:
        query_column_list.remove(field)

    if columns_selected:
        if field == query_sort_by:
            del query[QUERY_SORT_BY]
    else:
        if query_sort_by and field != query_sort_by:
            del query[QUERY_SORT_BY]

    if not query_column_list and query_sort_by == 'count':
        del query[QUERY_SORT_BY]

    query.setlist(QUERY_COLUMN, query_column_list)
    return query.urlencode()


@register.simple_tag
def display_more(request):
    query = request.GET.copy()
    query_per_page = query.get(QUERY_PER_PAGE, '')
    try:
        query[QUERY_PER_PAGE] = int(query_per_page) + DEFAULT_DISPLAY_MORE
    except ValueError:
        query[QUERY_PER_PAGE] = DEFAULT_PER_PAGE + DEFAULT_DISPLAY_MORE
    return query.urlencode()
