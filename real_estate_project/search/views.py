from django.shortcuts import render
from .forms import HouseFilterInfo
from .models import House, Property, Utility


def handle_post_search(num_bedroom, num_bath):
    return House.objects.select_related().filter(property_id__num_bedroom__gte=num_bedroom, property_id__num_bathroom=num_bath)


def search_view(request):
    filter_form = HouseFilterInfo(request.POST or None)
    context = None
    if request.method == "POST":  # Press submit filter
        if filter_form.is_valid():
            data = filter_form.data
            start_price = data['start_price']
            end_price = data['end_price']
            start_area = data['start_area']
            end_area = data['end_area']
            num_bedroom = data['num_bed']
            num_bath = data['num_bath']
            db = handle_post_search(num_bedroom, num_bath)[0:32]
        context = {
            "filter_form": filter_form,
            "house_data": db
        }
    else:
        context = {
            "filter_form": filter_form
        }
    return render(request, "search.html", context)
