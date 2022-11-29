import pandas as pd
import numpy as np
import numpy_financial as npf

class Calculator():

    def ky_khoan_giam_dan(so_tien_vay, ky_han, lai_suat):
        lai_suat_thang = lai_suat / 12 / 100

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
            df.loc[i, "Dư nợ đầu kỳ<br>VND"] = so_tien_vay - (i - 1) * (so_tien_vay / ky_han)
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

        return (df, df.style.format("{:,.0f}").hide_index() \
                .set_table_styles([cell_hover, detail_headers]) \
                .set_properties(**detail_properties),
                summary_df.style.format("{:,.0f}").hide_index().set_table_styles([headers])
                .set_properties(**properties))

    def ky_khoan_co_dinh(so_tien_vay, ky_han, lai_suat):

        so_tien_vay_amount = -(so_tien_vay)
        interest_rate = (lai_suat / 100) / 12
        # periods = years * 12

        n_periods = np.arange(ky_han) + 1
        interest_monthly = npf.ipmt(interest_rate, n_periods, ky_han, so_tien_vay_amount)

        principal_monthly = npf.ppmt(interest_rate, n_periods, ky_han, so_tien_vay_amount)

        df_initialize = list(zip(n_periods, interest_monthly, principal_monthly))
        df = pd.DataFrame(df_initialize, columns=['Số kỳ trả', 'Lãi phải trả<br>VND', 'Vốn phải trả<br>VND'])

        df['Vốn + Lãi<br>VND'] = df['Lãi phải trả<br>VND'] + df['Vốn phải trả<br>VND']

        df.loc[0, 'Dư nợ đầu kỳ<br>VND'] = so_tien_vay
        for i in range(1, ky_han + 1):
            df.loc[i, "Dư nợ đầu kỳ<br>VND"] = df.loc[i - 1, "Dư nợ đầu kỳ<br>VND"] - df.loc[
                i - 1, 'Vốn phải trả<br>VND']

        columns = [
            "Số kỳ trả",
            "Dư nợ đầu kỳ<br>VND",
            "Vốn phải trả<br>VND",
            "Lãi phải trả<br>VND",
            "Vốn + Lãi<br>VND",
        ]
        df = df[columns].iloc[:-1, :]

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
            "props": "background-color: darkgrey; "
                     "color: black; text-align: center; font-size: 12px; "
                     "height: 30px",

        }
        detail_properties = {"font-size": "11px", "text-align": "center", "height": "16px", "width": "100px"}

        headers = {
            "selector": "th:not(.index_name)",
            "props": "color: #686868; text-align: center; font-size: 18px; height: 30px"}
        properties = {"font-size": "22px", "color": "green", "text-align": "center",
                      "height": "30px", "width": "180px", "font-weight": "bold",
                      }
        return (df, df.style.format("{:,.0f}").hide_index() \
                .set_table_styles([cell_hover, detail_headers]) \
                .set_properties(**detail_properties),
                summary_df.style.format("{:,.0f}").hide_index().set_table_styles([headers])
                .set_properties(**properties))

    def thue_phi_nha_dat(gia_chuyen_nhuong):
        thue_thu_nhap = '{:,.0f}'.format((float(gia_chuyen_nhuong) * 0.02))
        phi_truoc_ba = float(gia_chuyen_nhuong) * 0.5 / 100
        phi_cong_chung = Calculator.le_phi_cong_chung(gia_chuyen_nhuong)
        phi_tham_dinh = Calculator.le_phi_tham_dinh(gia_chuyen_nhuong)
        tong_phi = phi_tham_dinh + phi_truoc_ba + phi_cong_chung

        d = {'Lệ phí trước bạ<br>(VND)': [phi_truoc_ba],
             'Phí công chứng<br>(VND)': [phi_cong_chung], 'Phí thẩm định<br>(VND)': [phi_tham_dinh],
             'Tổng phí<br>(VND)': [tong_phi]}
        df = pd.DataFrame(data=d)

        headers = {
            "selector": "th:not(.index_name)",
            "props": "border: 1px solid grey; color: #686868; text-align: center; "
                     "font-size: 14px;"}
        properties = {"border: solid grey; font-size": "14px",
                      "color": "green", "text-align": "center",
                      "width": "120px", "font-weight": "bold",
                      }
        return (thue_thu_nhap, df.style.format("{:,.0f}").hide_index()
                .set_table_styles([headers])
                .set_properties(**properties))

    def le_phi_tham_dinh(gia_chuyen_nhuong):
        phi_tham_dinh = float(gia_chuyen_nhuong) * 0.15 / 100
        if (phi_tham_dinh < 100000):
            phi_tham_dinh = 100000
        elif (phi_tham_dinh > 5000000):
            phi_tham_dinh = 5000000

        return phi_tham_dinh

    def le_phi_cong_chung(gia_chuyen_nhuong):
        gia_chuyen_nhuong = float(gia_chuyen_nhuong)
        phi_cong_chung = 0
        if gia_chuyen_nhuong <= 50000000:
            phi_cong_chung = 50000
        elif (50000000 < gia_chuyen_nhuong) and (gia_chuyen_nhuong <= 100000000):
            phi_cong_chung = 100000
        elif (100000000 < gia_chuyen_nhuong) and (gia_chuyen_nhuong <= 1000000000):
            phi_cong_chung = gia_chuyen_nhuong * 0.1 / 100
        elif (1000000000 < gia_chuyen_nhuong) and (gia_chuyen_nhuong <= 3000000000):
            phi_cong_chung = (gia_chuyen_nhuong * 0.06 / 100) + 1000000
        elif (3000000000 < gia_chuyen_nhuong) and (gia_chuyen_nhuong <= 5000000000):
            phi_cong_chung = (gia_chuyen_nhuong * 0.05 / 100) + 2200000
        elif (5000000000 < gia_chuyen_nhuong) and (gia_chuyen_nhuong <= 10000000000):
            phi_cong_chung = (gia_chuyen_nhuong * 0.04 / 100) + 3200000
        elif (10000000000 < gia_chuyen_nhuong) and (gia_chuyen_nhuong <= 100000000000):
            phi_cong_chung = (gia_chuyen_nhuong * 0.03 / 100) + 5200000
        elif (gia_chuyen_nhuong > 100000000000):
            phi_cong_chung = (gia_chuyen_nhuong * 0.02 / 100) + 32200000
            if (phi_cong_chung > 70000000):
                phi_cong_chung = 70000000
        return phi_cong_chung