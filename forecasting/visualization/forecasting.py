from datetime import datetime, timedelta
import time
from collections import namedtuple
import pandas as pd
import requests
import matplotlib.pyplot as plt
import pandas_datareader as pdr
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.graph_objs as go
import datetime
import pandas as pd
from config import *



external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']

app = dash.Dash('vehicle-data',external_scripts=external_js,external_stylesheets=external_css)

features = ['humidityLow', 'humidityAvg', 'qcStatus', 'tempHigh', 'tempLow',
       'tempAvg', 'windspeedHigh', 'windspeedLow', 'windspeedAvg',
       'windgustHigh', 'windgustLow', 'windgustAvg', 'dewptHigh', 'dewptLow',
       'dewptAvg', 'windchillHigh', 'windchillLow', 'windchillAvg',
       'heatindexHigh', 'heatindexLow', 'heatindexAvg', 'pressureMax',
       'pressureMin', 'pressureTrend', 'precipRate', 'precipTotal']
DailySummary = namedtuple("DailySummary", features)

def extract_weather_data():
    print('Enter')
    BASE_URL = 'https://api.weather.com/v2/pws/observations/all/1day?stationId=KMAHANOV10&format=json&units=e&apiKey={}'
    request = BASE_URL.format(API_KEY)
    response = requests.get(request)
    #print(response.status_code)
    # for _ in range(days):
    if response.status_code == 200:
        x = [{key: val for key, val in i.items() if key != 'imperial'} for i in response.json()['observations']]
        y = [{key: val for key, val in i['imperial'].items()} for i in response.json()['observations']]
        [i.update(j) for i, j in zip(x, y)]
        df = pd.DataFrame(x)
    #time.sleep(60)
    #target_date += timedelta(days=1)
    print("enter Exit")
    return df



app.layout = html.Div([
    html.Div([
        html.H2('Weather Data',
                style={'float': 'left',
                       }),
        ]),
    dcc.Dropdown(id='weather-data-name',
                 options=[{'label': s, 'value': s}
                          for s in features],
                 value=['tempAvg'],
                 multi=True
                 ),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=1000,n_intervals = 0),
    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':5000})


@app.callback(
    Output('graphs','children'),
    [Input('weather-data-name', 'value')],[Input('graph-update', 'n_intervals')]
    )
def update_graph(data_names,n):
    graphs =[]
    df = extract_weather_data()
    #print(df.columns,df.shape)
    df['obsTimeUtc'] = pd.to_datetime((df['obsTimeUtc']))
    df['obsTimeLocal'] = pd.to_datetime((df['obsTimeLocal']))
    times = df['obsTimeLocal'].tolist()
    print(times)
    if len(data_names)>2:
        class_choice = 'col s12 m6 l4'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'
    for data_name in data_names:
        #print(df[data_name].tolist())
        data = go.Scatter(
            x=times,
            y=df[data_name].tolist(),
            name='Scatter',
            fill="tozeroy",
            fillcolor="#6897bb"
            )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=False,
            figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min( c/.),max(times)]),
                                                        yaxis=dict(range=[min(df[data_name]),max(df[data_name])]),
                                                        margin={'l':50,'r':1,'t':45,'b':1},
                                                        title='{}'.format(data_name))}
            ), className=class_choice))

    return graphs


if __name__ == '__main__':
    app.run_server(debug=True)