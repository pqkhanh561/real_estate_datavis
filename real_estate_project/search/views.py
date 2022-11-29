from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

from .forms import HouseFilterInfo
from .models import House, Property, Utility

DATA_SEARCH = None
PRICE_SHOW = []
UTILITY = []
FILTER_FORM = None
ITEM1 = None
ITEM2 = None


def handle_post_search(**kwargs):
    global PRICE_SHOW
    PRICE_SHOW = []
    try:
        start_price = int(kwargs.get("start_price"))
    except (TypeError, ValueError):
        start_price = ''
    try:
        end_price = int(kwargs.get("end_price"))
    except (TypeError, ValueError):
        end_price = ''

    filter_input = {
        "property_id__num_bedroom": kwargs.get("num_bedroom"),
        "property_id__num_bathroom": kwargs.get("num_bathroom"),
        "property_id__area__gte": kwargs.get("start_area"),
        "property_id__area__lte": kwargs.get("end_area"),
        "total_price__gte": start_price,
        "total_price__lte": end_price,
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
        if float(h.total_price) / 1000 > 1:
            PRICE_SHOW.append(str(round(float(h.total_price) / 1000, 1)) + ' tỷ')
        else:
            PRICE_SHOW.append(str(round(float(h.total_price), 1)) + ' triệu')
    return houses


def get_utility():
    UTILITY = [
        "ID",
        "utility_Gần chợ, siêu thị",
        "utility_Gần trường học",
        "utility_Di chuyển thuận tiện ra trung tâm",
        "utility_Thiết kế thông thoáng",
        "utility_Khu vực an ninh, yên tĩnh",
        "utility_Gần mặt tiền đường",
        "utility_Gần bệnh viện",
        "utility_Gần công viên, trung tâm",
        "utility_Sân để xe rộng rãi",
        "utility_Hẻm thông",
        "utility_Cần bán gấp",
        "utility_Nở hậu",
        "utility_2 Mặt hẻm",
        "utility_2 Mặt đường chính"
    ]

    DB_UTILITY = [
        'id', 'near_market', 'near_school', 'near_center',
        'good_design', 'security', 'near_front_road', 'near_hospital',
        'near_park', 'parking', 'through_road', 'fast_trade', 'open_house', 'two_small_roads', 'two_roads'
    ]
    ret = []
    for data in DATA_SEARCH:
        utility = data.utility.__dict__
        utility_array = []
        for k, v in utility.items():
            if bool(v):
                if k in DB_UTILITY and k != 'id':
                    utility_array.append(UTILITY[DB_UTILITY.index(k)].split('_')[1])
        ret.append(utility_array)
    return ret


def handle_compare_item(code1, code2):
    global ITEM1
    global ITEM2
    ITEM1 = House.objects.select_related().filter(code=int(code1.replace(',', '')))
    ITEM2 = House.objects.select_related().filter(code=int(code2.replace(',', '')))


def compare_view(request):
    # return HttpResponse("www.google.com")
    # return request, "www.google.com"
    return render(request, "compare.html")

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

            if len(data['compare_no1']) > 0 and len(data['compare_no2']) > 0:
                handle_compare_item(data['compare_no1'], data['compare_no2'])
                return compare_view(request)
    utility = get_utility()
    web_data = list(zip(PRICE_SHOW, DATA_SEARCH, utility))
    db_paginator = Paginator(web_data, 27)
    page_num = request.GET.get('page')
    page = db_paginator.get_page(page_num)
    context = {
        "filter_form": FILTER_FORM,
        # "house_data": page,
        'page': page,
    }
    return render(request, "search.html", context)
