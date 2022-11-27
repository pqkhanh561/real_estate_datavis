from django.shortcuts import render
from django.core.paginator import Paginator

from .forms import HouseFilterInfo
from .models import House, Property, Utility

DATA_SEARCH = None
PRICE_SHOW = []
FILTER_FORM = None


def handle_post_search(**kwargs):
    global PRICE_SHOW
    PRICE_SHOW = []
    try:
        start_price = int(kwargs.get("start_price"))
    except TypeError:
        start_price = ''
    try:
        end_price = int(kwargs.get("end_price"))
    except TypeError:
        end_price = ''

    filter_input = {
        "property_id__num_bedroom":     kwargs.get("num_bedroom"),
        "property_id__num_bathroom":    kwargs.get("num_bathroom"),
        "property_id__area__gte":       kwargs.get("start_area"),
        "property_id__area__lte":       kwargs.get("end_area"),
        "total_price__gte":             start_price,
        "total_price__lte":             end_price,
    }
    drop_keys = []
    ret = None
    for k, v in filter_input.items():
        try:
            if v is None:
                drop_keys.append(k)
            elif len(v) == 0:
                drop_keys.append(k)
        except:
            pass
    for k in drop_keys:
        filter_input.pop(k)
    houses = House.objects.select_related().filter(**filter_input)
    for h in houses:
        if float(h.total_price)/1000 > 1:
            PRICE_SHOW.append(str(round(float(h.total_price)/1000, 1)) + ' tỷ')
        else:
            PRICE_SHOW.append(str(round(float(h.total_price), 1)) + ' triệu')
    return houses


def search_view(request):
    global DATA_SEARCH
    global FILTER_FORM
    global PRICE_SHOW
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
            DATA_SEARCH = handle_post_search(start_price=start_price,
                                             end_price=end_price,
                                             num_bedroom=num_bedroom,
                                             num_bathroom=num_bathroom,
                                             start_area=start_area,
                                             end_area=end_area)
    web_data = list(zip(PRICE_SHOW, DATA_SEARCH))
    db_paginator = Paginator(web_data, 27)
    page_num = request.GET.get('page')
    page = db_paginator.get_page(page_num)
    context = {
        "filter_form": FILTER_FORM,
        # "house_data": page,
        'page': page,
    }
    return render(request, "search.html", context)
