from django.shortcuts import render
from .forms import InterestForm, BankForm
import pandas as pd
import numpy as np
import plotly.express as px
import numpy_financial as npf
from .models import Bank

def home_view(request):

    return render(request, "home.html", {})

def bank_view(request):
    bank_form = BankForm(request.POST or None)
    if request.method == "POST":
        if bank_form.is_valid():
            lai_suat_NH = bank_form.cleaned_data.get("ten_ngan_hang")

        if request.POST.get("form_type") == "sosanh":
            sosanhbutton = request.POST.get("sosanh")
            bank = Bank.objects.all()
            fig = px.bar(
                x=[b.ten_ngan_hang for b in bank],
                y=[b.lai_suat for b in bank],
                width=800, height=400,
                title="Biểu đồ so sánh lãi suất giữa các ngân hàng",
                labels={'y': ' lãi suất % ', 'x': ''},
                text_auto=True,
                color_discrete_sequence=["green"]
            )
            chart = fig.to_html()
        context = {
            'bank_form': bank_form,
            "sosanhbutton": sosanhbutton,
            'chart': chart,
            'lai_suat_NH': lai_suat_NH
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
                    df, summary_df = ky_khoan_giam_dan(so_tien_vay, ky_han, lai_suat)
                    table_data = df.to_html(table_id="table_example")
                    summary_table = summary_df.to_html(table_id="summary_table")
                elif (loai_hinh == '2'):
                    df, summary_df = ky_khoan_co_dinh(so_tien_vay, ky_han, lai_suat)
                    table_data = df.to_html(table_id="table_example")
                    summary_table = summary_df.to_html(table_id="summary_table")

        context = {
            "form": form,
            "so_tien_vay": so_tien_vay,
            "ky_han": ky_han,
            "submitbutton": submitbutton,
            "lai_suat": lai_suat,
            'table_data': table_data,
            'summary_table': summary_table,
        }
    else:
        context = {
            'form': form,
        }

    return render(request, "interest/laisuat.html", context)


def ky_khoan_giam_dan(so_tien_vay, ky_han, lai_suat):

    lai_suat_thang = lai_suat / 12 /100

    df = pd.DataFrame(
        index=range(0, ky_han + 1),
        columns=[
            "Số kỳ trả",
            "Dư nợ đầu kỳ<br>VND",
            "Vốn phải trả<br>VND",
            "Lãi phải trả<br>VND",
            "Vốn + Lãi<br>VND",
        ],
        dtype="int",
    )
    df["Số kỳ trả"] = range(0, ky_han + 1)
    df.loc[0, "Dư nợ đầu kỳ<br>VND"] = so_tien_vay
    df.loc[0, "Vốn phải trả<br>VND"] = 0
    df.loc[0, "Lãi phải trả<br>VND"] = 0
    df.loc[0, "Vốn + Lãi<br>VND"] = 0

    for i in range(1, ky_han + 1):
        df.loc[i, "Vốn phải trả<br>VND"] = so_tien_vay / ky_han
        df.loc[i, "Dư nợ đầu kỳ<br>VND"] = so_tien_vay - (i-1) * (so_tien_vay / ky_han)
        df.loc[i, "Lãi phải trả<br>VND"] = (
                so_tien_vay * lai_suat_thang * (ky_han + 1 - i) / ky_han
        )
        df.loc[i, "Vốn + Lãi<br>VND"] = (
                so_tien_vay * (ky_han * lai_suat_thang + 1 - lai_suat_thang * (i - 1)) / ky_han
        )

    df = df.loc[1:, :]

    tong_lai = np.sum(df["Lãi phải trả<br>VND"])
    tong_von_lai = np.sum(df["Vốn + Lãi<br>VND"])
    d = {'Vốn vay ban đầu<br>(VND)': [so_tien_vay], 'Tổng lãi<br>(VND)': [tong_lai],
         'Tổng vốn và lãi<br>cần trả (VND)': [tong_von_lai]}
    summary_df = pd.DataFrame(data=d, dtype="int")

    cell_hover = {
        "selector": "td:hover",
        "props": [("background-color", "#FFFFE0")]
    }
    detail_headers = {
        "selector": "th:not(.index_name)",
        "props": "background-color: darkgrey; color: black; text-align: center; font-size: 12px; height: 30px",

    }
    detail_properties = {"font-size": "11px", "text-align": "center", "height": "16px", "width": "100px"}
    headers = {
        "selector": "th:not(.index_name)",
        "props": "color: #686868; text-align: center; font-size: 18px; height: 30px"}
    properties = {"font-size": "22px", "color": "green", "text-align": "center",
                  "height": "30px", "width": "180px", "font-weight": "bold",
                 }

    return (df.style.format("{:,.0f}").hide_index()\
            .set_table_styles([cell_hover, detail_headers])\
            .set_properties(**detail_properties),
            summary_df.style.format("{:,.0f}").hide_index().set_table_styles([headers])
            .set_properties(**properties))

def ky_khoan_co_dinh(so_tien_vay, ky_han, lai_suat):

    so_tien_vay_amount = -(so_tien_vay)
    interest_rate = (lai_suat / 100) / 12
    #periods = years * 12

    n_periods = np.arange(ky_han) + 1
    interest_monthly = npf.ipmt(interest_rate, n_periods, ky_han, so_tien_vay_amount)

    principal_monthly = npf.ppmt(interest_rate, n_periods, ky_han, so_tien_vay_amount)

    df_initialize = list(zip(n_periods, interest_monthly, principal_monthly))
    df = pd.DataFrame(df_initialize, columns=['Số kỳ trả', 'Lãi phải trả<br>VND', 'Vốn phải trả<br>VND'])

    df['Vốn + Lãi<br>VND'] = df['Lãi phải trả<br>VND'] + df['Vốn phải trả<br>VND']

    df.loc[0, 'Dư nợ đầu kỳ<br>VND'] = so_tien_vay
    for i in range(1, ky_han + 1):
        df.loc[i, "Dư nợ đầu kỳ<br>VND"] = df.loc[i-1, "Dư nợ đầu kỳ<br>VND"] - df.loc[i-1, 'Vốn phải trả<br>VND']

    columns = [
        "Số kỳ trả",
        "Dư nợ đầu kỳ<br>VND",
        "Vốn phải trả<br>VND",
        "Lãi phải trả<br>VND",
        "Vốn + Lãi<br>VND",
    ]
    df = df[columns].iloc[:-1,:]

    tong_lai = np.sum(df["Lãi phải trả<br>VND"])
    tong_von_lai = np.sum(df["Vốn + Lãi<br>VND"])
    d = {'Vốn vay ban đầu<br>(VND)': [so_tien_vay], 'Tổng lãi<br>(VND)': [tong_lai],
         'Tổng vốn và lãi<br>cần trả (VND)': [tong_von_lai]}
    summary_df = pd.DataFrame(data=d, dtype="int")

    cell_hover = {
        "selector": "td:hover",
        "props": [("background-color", "#FFFFE0")]
    }
    detail_headers = {
        "selector": "th:not(.index_name)",
        "props": "background-color: darkgrey; color: black; text-align: center; font-size: 12px; height: 30px",

    }
    detail_properties = {"font-size": "11px", "text-align": "center", "height": "16px", "width": "100px"}

    headers = {
        "selector": "th:not(.index_name)",
        "props": "color: #686868; text-align: center; font-size: 18px; height: 30px"}
    properties = {"font-size": "22px", "color": "green", "text-align": "center",
                  "height": "30px", "width": "180px", "font-weight": "bold",
                  }
    return (df.style.format("{:,.0f}").hide_index() \
            .set_table_styles([cell_hover, detail_headers]) \
            .set_properties(**detail_properties),
            summary_df.style.format("{:,.0f}").hide_index().set_table_styles([headers])
            .set_properties(**properties))
