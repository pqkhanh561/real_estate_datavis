import numpy as np
from django.shortcuts import render
from .forms import InterestForm, BankForm, TaxForm
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from .models import Bank
from .calculator import Calculator
from .plot import Plot

def home_view(request):

    return render(request, "home.html", {})

def tax_view(request):
    tax_form = TaxForm(request.POST or None)
    if request.method == "POST":
        thuebutton = request.POST.get("thuephi")
        thue_thu_nhap = ""
        phi_table = []

        if request.POST.get("form_type") == "thuephi":
            if tax_form.is_valid():
                gia_chuyen_nhuong = tax_form.cleaned_data.get("gia_chuyen_nhuong")
                thue_thu_nhap, df = Calculator.thue_phi_nha_dat(gia_chuyen_nhuong)
                phi_table = df.to_html(table_id="phi_table")

        context = {
            'tax_form': tax_form,
            'thuebutton': thuebutton,
            'phi_table': phi_table,
            'thue_thu_nhap': thue_thu_nhap
        }
    else:
        context = {
            'tax_form': tax_form,
        }

    return render(request, "interest/thue.html", context)

def bank_view(request):
    bank_form = BankForm(request.POST or None)
    if request.method == "POST":
        if bank_form.is_valid():
            lai_suat_NH = bank_form.cleaned_data.get("ten_ngan_hang")

        if request.POST.get("form_type") == "sosanh":
            sosanhbutton = request.POST.get("sosanh")
            bank = Bank.objects.all()
            fig = Plot.plot_lai_suat(bank)
            chart = fig.to_html()

            bank_list = Bank.objects.values_list('ten_ngan_hang', 'lai_suat').order_by('lai_suat')

        context = {
            'bank_form': bank_form,
            "sosanhbutton": sosanhbutton,
            'chart': chart,
            'lai_suat_NH': lai_suat_NH,
            'min_ten_NH': bank_list.first()[0],
            'min_lai': bank_list.first()[1],
            'max_ten_NH': bank_list.last()[0],
            'max_lai': bank_list.last()[1],
        }
    else:
        context = {
            'bank_form': bank_form,
        }

    return render(request, "interest/tracuu.html", context)

def interest_view(request):

    form = InterestForm(request.POST or None)
    if request.method == "POST":
        so_tien_vay = ""
        ky_han = ""
        lai_suat = ""
        table_data = []
        summary_table = []
        submitbutton = request.POST.get("laisuat")
        if request.POST.get("form_type") == "laisuat":
            if form.is_valid():
                so_tien_vay = form.cleaned_data.get("so_tien_vay")
                ky_han = form.cleaned_data.get("ky_han")
                lai_suat = form.cleaned_data.get("lai_suat")
                loai_hinh = form.cleaned_data.get("loai_hinh")
                if (loai_hinh == '1'):
                    df, df_style, summary_df = Calculator.ky_khoan_giam_dan(so_tien_vay, ky_han, lai_suat)
                    table_data = df_style.to_html(table_id="table_example")
                    summary_table = summary_df.to_html(table_id="summary_table")

                elif (loai_hinh == '2'):
                    df, df_style, summary_df = Calculator.ky_khoan_co_dinh(so_tien_vay, ky_han, lai_suat)
                    table_data = df_style.to_html(table_id="table_example")
                    summary_table = summary_df.to_html(table_id="summary_table")

                von = list(np.cumsum(df['Vốn phải trả<br>VND']))
                lai = list(np.cumsum(df['Lãi phải trả<br>VND']))
                fig_2 = Plot.plot_tich_luy(von, lai, df['Dư nợ đầu kỳ<br>VND'], df['Số kỳ trả'])
                chart_2 = fig_2.to_html()

                fig_1 = Plot.plot_vonlai_theoky(df['Vốn phải trả<br>VND'], df['Lãi phải trả<br>VND'],
                                                df['Số kỳ trả'])
                chart_1 = fig_1.to_html()

        context = {
            "form": form,
            "so_tien_vay": so_tien_vay,
            "ky_han": ky_han,
            "submitbutton": submitbutton,
            "lai_suat": lai_suat,
            'table_data': table_data,
            'summary_table': summary_table,
            'chart_2': chart_2,
            'chart_1': chart_1,
        }
    else:
        context = {
            'form': form,
        }

    return render(request, "interest/laisuat.html", context)
