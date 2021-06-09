import pandas_datareader.data as web
import pandas_datareader as pdr
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from config import *
import datetime
import pandas as pd



#df = web.DataReader('F', 'iex', start, end)
# df = pdr.get_data_tiingo('goog', api_key=os.getenv('TIINGO_API_KEY'))
# df.reset_index(inplace=True)
# df['date'] = pd.to_datetime((df['date']))
# print(df.columns)
#'symbol', 'date', 'close', 'high', 'low', 'open', 'volume', 'adjClose','adjHigh', 'adjLow', 'adjOpen', 'adjVolume', 'divCash', 'splitFactor']

app = dash.Dash()
app.layout = html.Div(children=[html.H1('StockPrice'),
                                html.Div(children='Company name'),
                                dcc.Input(id = 'input',value='',type='text'),
                                html.Div(children='Chart Type'),
                                dcc.Dropdown(
                                    id='chart',
                                    options=[
                                        {'label': 'Time series', 'value': 'timeseries'},
                                        {'label': 'Area Between high and low', 'value': 'area'},
                                    ],
                                    value='timeseries'
                                ),
                                html.Div(id = 'output-graph')
                                ])


@app.callback(Output(component_id ='output-graph',component_property='children'),
             [Input(component_id ='input',component_property='value'),Input(component_id ='chart',component_property='value')])
def update_graph(input_date,chart_type):
    start = datetime.datetime(2018, 1, 1)
    end = datetime.datetime.now()
    print(input_date)

    df = pdr.get_data_tiingo(input_date, api_key=os.getenv('TIINGO_API_KEY'))
    df.reset_index(inplace=True)
    df['date'] = pd.to_datetime((df['date']))
    #print(df.columns)
    print(chart_type)
    print(type(chart_type))
    #chart_type = int(chart_type)
    df.set_index('date', inplace=True)
    if chart_type == 'timeseries':
        return dcc.Graph(id='example',
                  figure={
                      'data': [
                          {'x': df.index, 'y': df.close, 'type': 'area', 'name': 'Stock'}
                      ],
                      'layout': {'title': input_date}
                  })
    elif chart_type == 'area':
        return dcc.Graph(id='example',
                  figure={
                      'data': [
                          {'x': df.index, 'y': df.high, 'type': 'scatter', 'name': 'high','fill':'tozeroy'},
                          {'x': df.index, 'y': df.low, 'type': 'scatter', 'name': 'low','fill':'tozeroy'}
                      ],
                      'layout': {'title': input_date}
                  })

if __name__ =='__main__':
    app.run_server(debug=True)