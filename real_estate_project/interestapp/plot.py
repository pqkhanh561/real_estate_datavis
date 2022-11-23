import plotly.express as px
import plotly.graph_objs as go

class Plot():
    def plot_lai_suat(data):
        fig = px.bar(
            x=[b.ten_ngan_hang for b in data],
            y=[b.lai_suat for b in data],
            labels={'y': 'Lãi suất', 'x': 'Ngân hàng'},
            text_auto=True,
            color_discrete_sequence=["green"],
        )

        fig.update_layout(
            width=700, height=400,
            title={'text':'<span style="color: #686868; font-size: 16px; font-weight: 700;">'
                  'Biểu đồ so sánh lãi suất giữa các ngân hàng</span>',
                   'y': 0.9,
                   'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
            title_font_family="Quicksand",
            hoverlabel=dict(
                bgcolor="white",
                font_size=14,
            )
        )
        return fig

    def plot_tich_luy(von, lai, du_no, so_ky):
        fig = go.Figure(go.Bar(
                x=so_ky,
                y=von,
                name='Vốn tích lũy',
                marker_color='#388E3C'
                ))
        fig.add_trace(go.Bar(x=so_ky, y=lai, marker_color='#F57F17',
                                     name='Lãi tích lũy'))
        fig.add_trace(go.Line(x=so_ky, y=du_no,
                                      name='Dư nợ', line_color='#2979FF'))

        fig.update_layout(barmode="overlay",
                            width=700, height=500,
                            title_font_family="Quicksand",
                            title={
                                  'text': '<span style="color: #686868; font-size: 16px; font-weight: 700;">'
                                          'Lãi và vốn cần trả tích lũy theo từng kỳ</span>',
                                  'y': 0.9,
                                  'x': 0.5,
                                  'xanchor': 'center',
                                  'yanchor': 'top'},
                            xaxis_title="Số kỳ trả",
                            yaxis_title="Số tiền",
                            hoverlabel=dict(
                                      bgcolor="white",
                                      font_size=14,
                                  ),
                            legend=dict(
                                      orientation="h",
                                      yanchor="bottom",
                                      y=1.02,
                                      xanchor="right",
                                      x=1)
                                  )

        return fig

    def plot_vonlai_theoky(von, lai, so_ky):
        fig = go.Figure(go.Bar(
                x=so_ky,
                y=von,
                name='Vốn',
                marker_color='#388E3C'
                ))
        fig.add_trace(go.Bar(x=so_ky, y=lai, marker_color='#F57F17',
                                     name='Lãi'))

        fig.update_layout(barmode="stack",
                          title_font_family="Quicksand",
                            width=700, height=500,
                            title={
                                  'text': '<span style="color: #686868; font-size: 16px; font-weight: 700;">'
                                          'Lãi và vốn cần trả theo từng kỳ</span>',
                                  'y': 0.9,
                                  'x': 0.5,
                                  'xanchor': 'center',
                                  'yanchor': 'top'},
                            xaxis_title="Số kỳ trả",
                            yaxis_title="Số tiền",
                            hoverlabel=dict(
                                      bgcolor="white",
                                      font_size=14,
                                  ),
                            legend=dict(
                                      orientation="h",
                                      yanchor="bottom",
                                      y=1.02,
                                      xanchor="right",
                                      x=1)
                                  )

        return fig