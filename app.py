import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import simulation as sm
from graphing_utils import *
import dash_table
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, assets_folder="assets")

fig = build_figure([], [], add_frames=False)

ids = list(range(1, 14))
taus = [5 for _ in range(13)]
sigmas = [3 for _ in range(13)]
P_ups = 2 * [0.33] + 8 * [0.25] + 3 * [0.33]
P_downs = 2 * [0.33] + 8 * [0.25] + 3 * [0.0]
P_lefts = 2 * [0.33] + 8 * [0.25] + 3 * [0.33]
P_rights = 2 * [0.0] + 8 * [0.25] + 3 * [0.33]

parameters = {'Light id': ids, 'T(🟢)': taus, 'T(🔴...)': sigmas,
              'P(🡱)': P_ups, 'P(🡳)': P_downs, 'P(🡰)': P_lefts, 'P(🡲)': P_rights}

df = pd.DataFrame(parameters)

table = dash_table.DataTable(
            id='table-parameters',
            columns=[{"name": i, "id": i, 'type': 'numeric', 'on_change': {'action': 'coerce', 'failure': 'default'},
                      'validation': {'default': 0}} for i in df.columns],
            data=df.to_dict('records'),
            editable=True,
            style_data_conditional=[
                {'if': {
                                'row_index': [10, 11, 12],
                                'column_id': 'P(🡳)'
                            },
                 'color': '#d9d0d0',
                 },
                {'if': {
                                'row_index': [0, 1],
                                'column_id': 'P(🡲)'
                            },
                 'color': '#d9d0d0'
                 }
            ]
        )

app.layout = html.Div(id="page", children=[
        dcc.Store(id='value_T'),
        html.Div(
            id='left_col',
            children=[
                        html.Div(
                            id='graph_parent',
                            children=[dcc.Graph(figure=fig, id='live-graph', animate=True)]
                                ),
                        dcc.Interval(id='graph-update', interval=1 * 1000),
                        html.Div(id='button_parent', children=[
                        html.Button('Run simulation!', id='simulate', n_clicks=0)]),
                    ]
                ),
        html.Div(
            id="right_col",
            children=[
                        html.Div(id="input_T_parent", children=[
                        html.Label("Simulation time"),
                        dcc.Input(
                            id="input_T", type="number", placeholder=100, value=100,
                            min=1, max=5000, step=1,
                                )]),
                        html.Div(id="input_dir1_parent", children=[table]),
                        html.Div(id="box")
                     ]
                )
        ]
)

table.columns[0]['editable'] = False


@app.callback(Output('graph_parent', 'children'),
              Input('simulate', 'n_clicks'),
              State('input_T', 'value'),
              State('table-parameters', 'data'))
def simulate(n, T, params):
    traffic, light_colors = sm.simulation(int(T), params)
    new_fig = build_figure(traffic, light_colors)
    return dcc.Graph(figure=new_fig, id=f'live-graph_{n}', animate=True)


@app.callback(Output('table-parameters', 'data'),
              Input('table-parameters', 'data'))
def fill_zeros(data):
    data[0]['P(🡲)'] = 0
    data[1]['P(🡲)'] = 0
    data[10]['P(🡳)'] = 0
    data[11]['P(🡳)'] = 0
    data[12]['P(🡳)'] = 0
    return data


if __name__ == '__main__':
    app.run_server(debug=True)
