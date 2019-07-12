# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
from datetime import datetime

input_factory_data = pd.read_csv("summerschool_dataset.csv", delimiter=";")
number_periods = 10000
input_factory_data = input_factory_data.head(number_periods)
start_datetime = datetime.fromtimestamp(datetime.now().timestamp() - number_periods).strftime("%Y-%m-%d %H:%M:%S")
data_df = input_factory_data.set_index(pd.date_range(start=start_datetime, periods=number_periods, freq='s'))
df_columns = data_df.columns.values
df = data_df.fillna(data_df.mean())
df["color"] = np.where(df["class"] == 'OK', 'green', 'red')

mapping = {}

for element in df_columns:
    mapping[element] = element

colors = {
    # 'background': '#111111',
    # 'text': '#7FDBFF'
    'background': 'white',
    'text': 'black'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'background-color': '#F8F8F8'}, children=[
    html.H1("INDUSTRY 4.0 - DATA ANALYTICS DASHBOARD", style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.H5("DATA EXPLORATION FOR VISUAL ANALYTICS", style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Div("This dashboards intends to provide data exploration capabilities. In the first diagram, you are able "
             "to select the different machine types and observe the sensor values that were measured in the last "
             "3 hours. Please zoom in by using the mouse in order to explore the data in more detail. Return to the "
             "full view by double-clicking on the diagram.", style={'margin-top': '10px', 'margin-bottom': '20px'}),
    html.Div(children="Select a Sensor "),

    dcc.Dropdown(
        id='Sensors_DropDown',
        options=[
            {'label': 'Drilling', 'value': '1'},
            {'label': 'Milling', 'value': '2'},
            {'label': 'Turning', 'value': '3'}
        ],
        value='1',
        style={'display': 'inline-block', 'width': '49%'}),
    html.Div(id='output-graph'),

    html.H5("SENSOR VALUES TIME PLOT", style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Div("The diagram below is a scatter plot of all available data variables that are collected throughout the "
             "simulation. Please pick a signal in each of the dropdown menus in order to visualize the relationship "
             "between the two signals. The color of the data points indicates whether the according product or "
             "component was an 'OK (green)' or a 'NOT OK (red) product. If the clusters of green and red points can "
             "be separated well, this means that the two selected features are well-suited as features for Machine "
             "Learning.",
             style={'margin-top': '20px', 'margin-bottom': '20px'}),

    html.Div(children="Select a Sensor"),
    dcc.Dropdown(
        id='Sensor_1_scatter',
        options=[{'label': k, 'value': k} for k in mapping.keys()],
        style={'display': 'inline-block', 'width': '49%'},
        value="Drill_Pressure"
    ),
    html.Div(children="Select a Sensor"),
    dcc.Dropdown(
        id='Sensor_2_scatter',
        options=[{'label': k, 'value': k} for k in mapping.keys()],
        style={'display': 'inline-block', 'width': '49%'},
        value="Drilling_Speed"
    ),
    html.Div(id='output_graph_scatter')

])


@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='Sensors_DropDown', component_property='value')]
)
def update_graph(value):
    if value == "1":
        return dcc.Graph(
            id='Drilling Sensors',
            figure={
                'data': [
                    {'x': df.index, 'y': df["Drill_Pressure"], 'type': 'line', 'name': 'Drill_Pressure'},
                    {'x': df.index, 'y': df["Drilling_Surf_Quality"], 'type': 'line', 'name': 'Drilling_Surf_Quality'},
                    {'x': df.index, 'y': df["Drilling_Speed"], 'type': 'line', 'name': 'Drilling_Speed'}

                ],
                'layout': {
                    'title': 'Drilling Machine Sensor Values',
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'height': 820
                },
                'style': {'display': 'inline-block', 'width': '30%'}
            }
        )

    if value == "2":
        return dcc.Graph(
            id='Milling Sensors',
            figure={
                'data': [
                    {'x': df.index, 'y': df["Milling_Gear_Depth"], 'type': 'line', 'name': 'Milling_Gear_Depth'},
                    {'x': df.index, 'y': df["Milling_Circle_Diameter"], 'type': 'line',
                     'name': 'Milling_Circle_Diameter'},

                ],
                'layout': {
                    'title': 'Miling Machine Sensor Values',
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'height': 820
                },
                'style': {'display': 'inline-block', 'width': '30%', 'height': '100%'}
            }
        )

    if value == "3":
        return dcc.Graph(
            id='Turning Sensors',
            figure={
                'data': [
                    {'x': df.index, 'y': df["Turning_Cut_Speed"], 'type': 'line', 'name': 'Turning_Cut_Speed'},
                    {'x': df.index, 'y': df["Turning_Cut_Depth"], 'type': 'line', 'name': 'Turning_Cut_Depth'},

                ],
                'layout': {
                    'title': 'Turning Sensor Graph',
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'height': 820
                },

                'style': {'display': 'inline-block', 'width': '30%'}
            }
        )


@app.callback(
    Output(component_id='output_graph_scatter', component_property='children'),
    [Input(component_id='Sensor_1_scatter', component_property='value'),
     Input(component_id='Sensor_2_scatter', component_property='value')]
)
def update_scatter(value1, value2):
    return dcc.Graph(
        id='Sactter Graph ID ',
        figure={
            'data': [go.Scatter(
                {'x': df[value1], 'y': df[value2], 'marker': dict(color=df["color"].values),
                 'mode': 'markers', 'name': 'Scatter Plot'})
            ],
            'layout': {
                'title': value1 + " " + "vs" + "  " + value2 + " " + "Scatter Plot",
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'xaxis': {
                    'title': value1,
                },
                'yaxis': {
                    'title': value2,
                },
                'height': 800
            },
            'style': {'display': 'inline-block', 'width': '30%'},
        }
    )


temp_layout = html.Div(children=[html.H1(children=' Smart Factory Floor1'),
     dcc.Graph(
         id='Drilling Sensors',
         figure={
             'data': [
                 {'x': df.index, 'y': df["Drill_Pressure"], 'type': 'line',
                  'name': 'Drill_Pressure'},
                 {'x': df.index, 'y': df["Drilling_Surf_Quality"], 'type': 'line',
                  'name': 'Drilling_Surf_Quality'},
                 {'x': df.index, 'y': df["Drilling_Speed"], 'type': 'line',
                  'name': 'Drilling_Speed'}
             ],
             'layout': {
                 'title': 'Drilling Machine Sensor Values'
             }
         }
     ),

     html.Div("Miling Sensor Graph"),

     dcc.Graph(
         id='Milling Sensors',
         figure={
             'data': [
                 {'x': df.index, 'y': df["Milling_Gear_Depth"], 'type': 'line',
                  'name': 'Milling_Gear_Depth'},
                 {'x': df.index, 'y': df["Milling_Circle_Diameter"], 'type': 'line',
                  'name': 'Milling_Circle_Diameter'},
             ],
             'layout': {
                 'title': 'Drilling Machine Sensor Values'
             }
         }
     ),

     html.Div("Turning Sensor Graph"),

     dcc.Graph(
         id='Turning Sensors',
         figure={
             'data': [
                 {'x': df.index, 'y': df["Turning_Cut_Speed"], 'type': 'line',
                  'name': 'Turning_Cut_Speed'},
                 {'x': df.index, 'y': df["Turning_Cut_Depth"], 'type': 'line',
                  'name': 'Turning_Cut_Depth'},
             ],
             'layout': {
                 'title': 'Turning Sensor Graph'
             }
         }
     )
     ])

if __name__ == '__main__':
    app.run_server(port=8051,
                   debug=True)
