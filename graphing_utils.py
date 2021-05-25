import plotly.graph_objs as go


def build_figure(traffic, light_colors, add_frames=True):
    colors = {'road': 'black', 'car': 'blue'}
    fig = go.Figure()

    fig.update_xaxes(range=[0, 42], showgrid=True)
    fig.update_yaxes(range=[0, 29], showgrid=True)

    fig.add_shape(
        type="rect",
        x0=10, y0=0, x1=12, y1=29,
        fillcolor=colors['road'],
        layer="below"
    )

    fig.add_shape(
        type="rect",
        x0=26, y0=0, x1=28, y1=29,
        fillcolor=colors['road'],
        layer="below"
    )

    fig.add_shape(
        type="rect",
        x0=0, y0=18, x1=49, y1=20,
        fillcolor=colors['road'],
        layer="below"
    )

    fig.add_shape(
        type="rect",
        x0=0, y0=6, x1=10, y1=7,
        fillcolor=colors['road'],
        layer="below"
    )

    fig.add_shape(
        type="rect",
        x0=35, y0=20, x1=37, y1=29,
        fillcolor=colors['road'],
        layer="below"
    )

    fig.add_shape(
        type="line",
        x0=27, y0=0, x1=27, y1=30,
        line=dict(
            color="white",
            width=3,
            dash="dash"
        )
    )

    fig.add_shape(
        type="line",
        x0=11, y0=0, x1=11, y1=30,
        line=dict(
            color="white",
            width=3,
            dash="dash"
        )
    )

    fig.add_shape(
        type="line",
        x0=0, y0=19, x1=43, y1=19,
        line=dict(
            color="white",
            width=3,
            dash="dash"
        )
    )

    fig.add_shape(
        type="line",
        x0=36, y0=19, x1=36, y1=40,
        line=dict(
            color="white",
            width=3,
            dash="dash"
        )
    )

    fig.update_shapes(layer="below")
    fig.add_trace(go.Scatter())  # preventing other shapes from disappearing (probably plotly bug)
    fig.add_trace(go.Scatter())
    fig.add_trace(go.Scatter(
        x=[14, 30, 40, 2, 8, 24, 33],
        y=[1, 1, 17, 17, 28, 28, 28],
        text=["A: λ1",
              "B: λ2",
              "C: λ3",
              "D: λ4",
              "E: λ5",
              "F: λ6",
              "G: λ7"],
        mode="text",
    ))

    fig.add_trace(go.Scatter(
        x=[14, 8, 14, 8, 8, 14, 30, 24, 24, 30, 33, 33, 39],
        y=[6, 8, 17, 17, 21, 21, 17, 17, 21, 21, 17, 21, 21],
        text=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"],
        mode="text",
    ))

    fig.update_xaxes(fixedrange=True, dtick=1, showgrid=False)
    fig.update_yaxes(fixedrange=True, dtick=1, showgrid=False)

    fig.update_layout(
        showlegend=False,
        autosize=False,
        width=1000,
        height=700,
        updatemenus=[
                    dict(
                         type="buttons",
                         buttons=[dict(
                                      label="                   ▶                   ",
                                      method="animate",
                                      args=[
                                            None,
                                            {"frame": {"duration": 100, "redraw": False},
                                             "fromcurrent": True,
                                             "transition": {"duration": 10000}}
                                            ]
                                      ),
                             {
                                 "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                                   "mode": "immediate",
                                                   "transition": {"duration": 0}}],
                                 "label": "                   ❚❚                   ",
                                 "method": "animate"
                             },
                                  ],

                         showactive=True,
                         direction='left',
                         x=0.1,
                         xanchor="left",
                         y=-0.2,
                         yanchor="bottom",
                         font={'size': 20}
                         ),

                    ],
        title={
            'text': "Road traffic simulation",
            'y': 0.95,
            'x': 0.5,
            'font' : {'size' : 40},
            'xanchor': 'center',
            'yanchor': 'top'}

                    )

    if add_frames is True:
        fig.frames = [go.Frame(
                        data=[
                            go.Scatter(
                                x=[x for x, y in state],
                                y=[y for x, y in state],
                                mode="markers",
                                marker=dict(color="blue", size=20, symbol='square')),
                            go.Scatter(
                                x=[13, 9, 13, 9, 9, 13, 29, 25, 25, 29, 34, 34, 38],
                                y=[6, 8, 17, 17, 21, 21, 17, 17, 21, 21, 17, 21, 21],
                                mode="markers",
                                marker=dict(color=colors,
                                            size=15, symbol='circle')  # #17a323 green "#f55d67" red
                            )]) for state, colors in zip(traffic, light_colors)
                      ]
    return fig
