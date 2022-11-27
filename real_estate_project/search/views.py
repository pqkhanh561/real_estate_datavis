from django.shortcuts import render
from django.core.paginator import Paginator

from .forms import HouseFilterInfo
from .models import House, Property, Utility

DATA_SEARCH = None
FILTER_FORM = None


def handle_post_search(**kwargs):
    filter_input = {
        "property_id__num_bedroom":     kwargs.get("num_bedroom"),
        "property_id__num_bathroom":    kwargs.get("num_bathroom"),
        "property_id__area__gte":       kwargs.get("start_area"),
        "property_id__area__lte":       kwargs.get("end_area"),
        "total_price__gte":             kwargs.get("start_price"),
        "total_price__lte":             kwargs.get("end_price"),
    }
    drop_keys = []
    for k, v in filter_input.items():
        if v is None:
            drop_keys.append(k)
        elif len(v) == 0:
            drop_keys.append(k)
    for k in drop_keys:
        filter_input.pop(k)
    if len(filter_input) > 0:
        return(House.objects.select_related().filter(**filter_input))
    return House.objects.select_related().all()


def search_view(request):
    global DATA_SEARCH
    global FILTER_FORM
    if DATA_SEARCH is None:
        DATA_SEARCH = handle_post_search()
        FILTER_FORM = HouseFilterInfo(None)

    if request.method == "POST":  # Press submit filter
        FILTER_FORM = HouseFilterInfo(request.POST)
        if FILTER_FORM.is_valid():
            data = FILTER_FORM.data
            start_price = data['start_price']
            end_price = data['end_price']
            start_area = data['start_area']
            end_area = data['end_area']
            num_bedroom = data['num_bed']
            num_bathroom = data['num_bath']
            DATA_SEARCH = handle_post_search(num_bedroom=num_bedroom,
                                             num_bathroom=num_bathroom,
                                             start_area=start_area,
                                             end_area=end_area)

    db_paginator = Paginator(DATA_SEARCH, 27)
    page_num = request.GET.get('page')
    page = db_paginator.get_page(page_num)
    context = {
        "filter_form": FILTER_FORM,
        # "house_data": page,
        'page': page
    }
    return render(request, "search.html", context)
