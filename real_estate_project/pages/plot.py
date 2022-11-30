import plotly.io as pio
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

class LoadData():
    def get_data_from_csv():
        csv_filename = os.path.join(os.path.dirname(__file__), 'static/propzy_cleaned.csv')
        df = pd.read_csv(csv_filename)

        df['phân loại'] = df['phân loại'].replace({1: 'nhà ở', 2: 'chung cư', 3: 'đất nền'})

        df = df.sort_values(['Quận'])
        df['phân loại'] = pd.Categorical(df['phân loại'], ["nhà ở", "chung cư", "đất nền"])
        df = df.sort_values(['phân loại'], ascending=False)

        return df

class PlotData():
    def price_statistic(df):
        district = df['Quận']
        price = df['Giá']

        aggs = ["count","avg","median","min","max"]

        agg = []
        agg_func = []
        for i in range(0, len(aggs)):
            agg = dict(
                args=['transforms[0].aggregations[0].func', aggs[i]],
                label=aggs[i],
                method='restyle'
            )
            agg_func.append(agg)


        data = [dict(
          type = 'scatter',
          x = district,
          y = price,
          mode = 'markers+lines+text',
          transforms = [dict(
            type = 'aggregate',
            groups = district,
            aggregations = [dict(
                target = 'y', func = 'avg', enabled = True)
            ]
          )]
        )]

        layout = dict(
          title = '<span style="color: #686868; font-size: 16px; font-weight: 700;">Thống kê giá giữa các Quận</span>',
          xaxis = dict(title = '', tickangle=45),
          yaxis = dict(title = 'Giá (tỷ)', autorange = True),
          updatemenus = [dict(
                x = 0.9,
                y = 1.2,
                xref = 'paper',
                yref = 'paper',
                yanchor = 'top',
                active = 1,
                showactive = False,
                buttons = agg_func
          )]
        )

        fig_dict = dict(data=data, layout=layout)

        return fig_dict

    def area_used_statistic(df):
        district = df['Quận']
        area = df['Diện tích sử dụng']

        aggs = ["median","avg","min","max"]

        agg = []
        agg_func = []
        for i in range(0, len(aggs)):
            agg = dict(
                args=['transforms[0].aggregations[0].func', aggs[i]],
                label=aggs[i],
                method='restyle'
            )
            agg_func.append(agg)


        data = [dict(
          type = 'bar',
          x = district,
          y = area,
         #mode = 'markers+lines+text',
          transforms = [dict(
            type = 'aggregate',
            groups = district,
            aggregations = [dict(
                target = 'y', func = 'avg', enabled = True)
            ]
          )]
        )]

        layout = dict(
          title = '<span style="color: #686868; font-size: 16px; font-weight: 700;">Thống kê diện tích sử dụng giữa các Quận</span>',
          xaxis = dict(title = '', tickangle=45),
          yaxis = dict(title = 'Diện tích sử dụng', autorange = True),
          updatemenus = [dict(
                x = 1,
                y = 1.2,
                xref = 'paper',
                yref = 'paper',
                yanchor = 'top',
                active = 1,
                showactive = False,
                buttons = agg_func
          )]
        )

        fig_dict = dict(data=data, layout=layout)

        return fig_dict

    def area_statistic(df):
        district = df['Quận']
        area = df['Diện tích đất']
        kind = df['phân loại']

        aggs = ["median", "avg", "min", "max"]
        agg = []
        agg_func = []
        for i in range(0, len(aggs)):
            agg = dict(
                args=['transforms[0].aggregations[0].func', aggs[i]],
                label=aggs[i],
                method='restyle'
            )
            agg_func.append(agg)

        data = [
            dict(
                type='scatter',
                x=district,
                y=area,
                text = kind,
                mode='markers',
                opacity=0.8,
                marker=dict(
                    size=7,
                ),
                transforms=[dict(
                    type='aggregate',
                    groups=district,
                    aggregations=[dict(
                        target='y', func='avg', enabled=True)
                    ]),
                    dict(
                        type='groupby',
                        groups=kind
                    ),
                ]
        )]

        layout = dict(
            title='<span style="color: #686868; font-size: 16px; font-weight: 700;">Thống kê diện tích giữa các Quận</span>',
            xaxis=dict(title='', tickangle=45),
            yaxis=dict(title='Diện tích đất (m²)', autorange=True),
            updatemenus=[
                dict(
                    x=1,
                    y=1.2,
                    xref='paper',
                    yref='paper',
                    yanchor='top',
                    active=1,
                    showactive=False,
                    buttons=agg_func
                )
            ]
        )

        fig_dict = dict(data=data, layout=layout)

        return fig_dict

    def unit_statistic(df):
        district = df['Quận']
        unit = df['Đơn giá gộp']
        kind = df['phân loại']

        aggs = ["median", "avg", "min", "max"]
        agg = []
        agg_func = []
        for i in range(0, len(aggs)):
            agg = dict(
                args=['transforms[0].aggregations[0].func', aggs[i]],
                label=aggs[i],
                method='restyle'
            )
            agg_func.append(agg)

        data = [
            dict(
                type='scatter',
                x=district,
                y=unit,
                #text = kind,
                mode='markers',
                opacity=0.7,
                marker=dict(
                    size=10,
                ),
                transforms=[dict(
                    type='aggregate',
                    groups=district,
                    aggregations=[dict(
                        target='y', func='avg', enabled=True)
                    ]),
                    dict(
                        type='groupby',
                        groups=kind
                    ),
                ]
        )]

        layout = dict(
            title='<span style="color: #686868; font-size: 16px; font-weight: 700;">Thống kê đơn giá gộp giữa các Quận</span>',
            xaxis=dict(title='', tickangle=45),
            yaxis=dict(title='Đơn giá gộp (triệu/m²)', autorange=True),
            updatemenus=[
                dict(
                    x=1,
                    y=1.2,
                    xref='paper',
                    yref='paper',
                    yanchor='top',
                    active=1,
                    showactive=False,
                    buttons=agg_func
                )
            ]
        )

        fig_dict = dict(data=data, layout=layout)

        return fig_dict

    def bubble_chart(df):

        df["Gần chợ, siêu thị"] = df["Gần chợ, siêu thị"].astype(str)

        fig = px.scatter(df, x="Quận", y="Giá", animation_frame="phân loại",
                         color="Gần chợ, siêu thị",size="Diện tích đất",
                         hover_name="Quận",
                         size_max=60,
                         color_discrete_sequence=["orange", "black"],
                         hover_data={'Gần trường học': True,  # remove species from hover data
                                     'Giá': ':.2f',  # customize hover for column of y attribute
                                     'Diện tích đất': ':.2f',  # add other column, default formatting
                                     'Gần chợ, siêu thị': True,  # add other column, customized formatting
                                     # data not in dataframe, default formatting
                                     'Di chuyển thuận tiện ra trung tâm': True,
                                     # data not in dataframe, customized formatting
                                     'phân loại': True,
                                     })


        fig.update_layout(
            height=500,
            title_font_family="Quicksand",
            title={
                'text': '<span style="color: #686868; font-size: 16px; font-weight: 700;">'
                        'Mối liên quan giữa tiện ích gần chợ, siêu thị với giá cả và diện tích</span>',
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis_title="",
            sliders={
                'x': 0.5,
                'xanchor': 'center',
            },
            hoverlabel=dict(
                font_size=14,
            ),
            autosize=True
        )
        fig.update_xaxes(tickangle=45, autorange=True, fixedrange=False)
        fig.update_yaxes(autorange=True, fixedrange=False)
        fig["layout"].pop("updatemenus") # optional, drop animation buttons

        return fig


