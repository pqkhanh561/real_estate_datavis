from django.shortcuts import render
from .forms import HouseFilterInfo
from .models import House


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
            num_bed = data['num_bed']
            num_bath = data['num_bath']
            print(House.objects.all())
        context = {
            "filter_form": filter_form
        }
    else:
        context = {
            "filter_form": filter_form
        }
    return render(request, "search.html", context)
