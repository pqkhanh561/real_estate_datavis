from django.shortcuts import render
from .forms import HouseFilterInfo


def search_view(request):
    filter_form = HouseFilterInfo(request.POST or None)
    context = None
    if request.method == "POST": # Press submit filter
        context = {
            "filter_form": filter_form
        }
    else:
        context = {
            "filter_form": filter_form
        }
    return render(request, "search.html", context)
