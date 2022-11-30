from django.shortcuts import render
import plotly.io as pio
from .plot import PlotData, LoadData

# Create your views here.
def home_view(request):
    df = LoadData.get_data_from_csv()

    chart_1 = PlotData.area_statistic(df)
    chart_2 = PlotData.unit_statistic(df)
    chart_3 = PlotData.bubble_chart(df)
    chart_4 = PlotData.area_used_statistic(df)
    chart_5 = PlotData.price_statistic(df)
    context = {
        'chart_1': pio.to_html(chart_1, validate=False),
        'chart_2': pio.to_html(chart_2, validate=False),
        'chart_3': pio.to_html(chart_3, validate=False),
        'chart_4': pio.to_html(chart_4, validate=False),
        'chart_5': pio.to_html(chart_5, validate=False),
    }
    return render(request, "home.html", context)
