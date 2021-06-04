import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import simulation as sm
from graphing_utils import *
import dash_table
import pandas as pd
import io
from base64 import b64encode, b64decode
from constants import *
import time


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, assets_folder="assets")
server = app.server

fig = build_figure([], [], add_frames=False)

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
            children=[html.Div(id='graph2_parent', children=[
                            dcc.Graph(figure=go.Figure(), id='analysis-graph'),
                            dcc.Graph(figure=go.Figure(), id='analysis-heatmap')],
                            style={'display': 'none'}),
                      html.Div(id='graph_parent', children=[
                            dcc.Graph(figure=fig, id='live-graph', animate=True)]),
                      dcc.Interval(id='graph-update', interval=1 * 1000),
                      html.Div(id='button_parent', children=[
                            html.Button('Run quick simulation!', id='simulate', n_clicks=0),
                            dcc.Upload([
                                  'Got simulation results in a csv file? ',
                                  html.A(' Upload it here!'),
                              ], id='upload',
                                style={
                                  'width': '100%',
                                  'height': '100%',
                                  'lineHeight': '100px',
                                  'borderWidth': '1px',
                                  'borderStyle': 'dashed',
                                  'borderRadius': '5px',
                                  'textAlign': 'center',
                              })
                      ]),
                    ]
                ),
        html.Div(
            id="right_col",
            children=[
                        html.Div(id="input_T_parent", children=[
                            html.Label("Quick simulation time", style={'font-size': '20px'}),
                            dcc.Input(
                                id="input_T", type="number", placeholder=100, value=100,
                                min=1, max=5000, step=1,
                                    ),
                            html.Label(
                                "Traffic intensity", style={'font-size': '20px',
                                                            'margin-top': '20px',
                                                            'margin-bottom': '10px'},

                                title='Responsible for the intensity of the appearance of new cars. \n '
                                      'Note that high intensity can slow down computation considerably!'
                            ),
                            dcc.Slider(
                                id='traffic_intensity',
                                min=1,
                                max=50,
                                step=None,
                                marks={num: str(num) for num in range(5, 51, 5)},
                                value=5
                            )
                        ]),
                        html.Div(id="input_dir1_parent", children=[
                            table,
                            html.Button("  Show the analysis / Show the animation⠀", id="show_analysis_btn", n_clicks=0),
                            html.A(
                               html.Button("⠀Download⠀the⠀animation⠀as⠀an⠀HTML⠀file⠀"),
                               id="download",
                               href="data:text/html;base64,",
                               download="plotly_graph.html"
                                ),
                        ]),
                        html.Div(id="box"),
                        dcc.Store(id='simulation_state'),
                        dcc.Store(id='chain_analysis')
                     ]
                )
        ]
)

table.columns[0]['editable'] = False


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), converters={'traffic': eval, 'light_colors': eval})
            return df
    except Exception as e:  # TODO exception handling
        pass


@app.callback(Output('graph_parent', 'children'),
              Output('simulation_state', 'data'),
              Output('chain_analysis', 'data'),
              Output('upload', 'contents'),
              Output('upload', 'filename'),
              Input('simulate', 'n_clicks'),
              Input('upload', 'contents'),
              State('upload', 'filename'),
              State('input_T', 'value'),
              State('traffic_intensity', 'value'),
              State('table-parameters', 'data'))
def simulate(n, file_content, filename, T, intensity, params):
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'] == 'upload.contents':
        # print('start loading')
        df = parse_contents(file_content, filename)
        # print('parsed')
        traffic = df['traffic'].to_list()
        light_colors = df['light_colors'].to_list()
        new_fig = build_figure(traffic, light_colors)
        # print('figure built')
    else:
        # print('start simulating')
        traffic, light_colors = sm.simulation(int(T), 50/intensity, params)
        new_fig = build_figure(traffic, light_colors)
    return dcc.Graph(figure=new_fig, id=f'live-graph_{time.time()}', animate=True), \
        pd.DataFrame(traffic).to_json(date_format='iso', orient='split'), time.time(), '0', '0'


@app.callback(Output('graph2_parent', 'children'), Input('chain_analysis', 'data'), State('simulation_state', 'data'))
def build_analysis(simulation_finished, traffic):
    # print("starting analysis")
    if traffic:
        traffic = pd.read_json(traffic, orient='split')
        frames = traffic.values
        frames = [i[i != None] for i in frames]
        traffic_by_roads = dict((road, []) for road in named_roads)

        for cars in frames:
            d = dict((road, 0) for road in traffic_by_roads)
            for car in cars:
                for road in named_roads:
                    if tuple(car) in named_roads[road]:
                        d[road] += 1
            for road, cars2 in list(zip(traffic_by_roads.keys(), d.values())):
                traffic_by_roads[road].append(cars2)
        fig3 = go.Figure()
        fig3.update_layout(width=1000, height=450, title={
            'text': "Analysis",
            'y': 0.95,
            'x': 0.5,
            'font': {'size': 40},
            'xanchor': 'center',
            'yanchor': 'top'},
            margin=dict(t=100),
            xaxis_title="time",
            yaxis_title="cars",
            legend_title="Roads",
        )
        for road in traffic_by_roads:
            fig3.add_trace(go.Scatter(x=list(range(len(traffic_by_roads[road]))), y=traffic_by_roads[road], name=road))

        x_c = []
        y_c = []
        for cars in frames:
            for car in cars:
                x_c.append(car[0])
                y_c.append(car[1])
        fig4 = go.Figure()
        fig4.add_trace(go.Histogram2d(
            x=x_c, y=y_c, autobinx=False,
            xbins=dict(start=1, end=41, size=1),
            autobiny=False,
            ybins=dict(start=1, end=28, size=1),
            colorscale=[[0.00, "rgb(229,236,246)"],
                        [0.11, "rgb(171,217,233)"],
                        [0.22, "rgb(254,224,144)"],
                        [0.44, "rgb(253,174,97)"],
                        [0.77, "rgb(244,109,67)"],
                        [1.0, "rgb(215,48,39)"]],
        )
        )
        fig4.update_layout(width=1000, height=450, margin=dict(t=30))
        # print("analyzed")
        return [dcc.Graph(figure=fig3), dcc.Graph(figure=fig4)]
    else:
        fig3 = go.Figure()
        fig4 = go.Figure()
        fig3.update_layout(width=1000, height=450)
        fig4.update_layout(width=1000, height=450)
        # print("analyzed")
        return [dcc.Graph(figure=fig3), dcc.Graph(figure=fig4)]


@app.callback(Output('table-parameters', 'data'),
              Input('table-parameters', 'data'))
def fill_zeros(data):
    data[0]['P(🡲)'] = 0
    data[1]['P(🡲)'] = 0
    data[10]['P(🡳)'] = 0
    data[11]['P(🡳)'] = 0
    data[12]['P(🡳)'] = 0
    return data


@app.callback(Output('download', 'href'),
              Input('graph_parent', 'children'),
              Input('download', 'n_clicks'),
              Input('simulation_state', 'data'))
def load_graph(graph, n, traffic):
    fig_ = go.Figure(graph['props']['figure'])
    buffer = io.StringIO()
    fig_.write_html(buffer)
    html_bytes = buffer.getvalue().encode()
    encoded = b64encode(html_bytes).decode()
    return "data:text/html;base64," + encoded


@app.callback(Output('graph_parent', 'style'),
              Output('graph2_parent', 'style'),
              Output('button_parent', 'style'),
              Input('show_analysis_btn', 'n_clicks'),
              Input('simulation_state', 'data'))
def show_analysis(clicks, traffic):

    if clicks % 2 > 0:
        return {'display': 'none'}, \
               {'display': 'block', 'margin-top': '10px', 'padding-top': '10px'}, \
               {'display': 'none'}
    else:
        return {'display': 'block', 'margin-top': '10px', 'padding-top': '10px'}, \
               {'display': 'none'}, \
               {'display': 'flex', 'justify-content': 'center',
                'align-items': 'center', 'height': '200px', 'padding-right': '100px'}


if __name__ == '__main__':
    app.run_server(debug=True)
