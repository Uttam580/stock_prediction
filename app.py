from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
import datetime
import pandas as pd
import requests
from pandas_datareader import data, wb
import datetime
import urllib
import time
import csv
from  models.prophet import prophet_predict, stock_extractor
import os
import os.path
from os import path



start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()



app = Dash(__name__)

colors = {
    'background': '#f0e6e6',
    'text': '#ffffff'
}


app.layout = html.Div([
    html.Div([
        html.H2("Stock Prediction"),
        html.Img(src="assets/images.jpg")
    ], className="banner"),

    html.Div([
        dcc.Input(id="stock-input", value="IOC.NS", type="text"),
        html.Button(id="submit-button", n_clicks=0, children="Submit")
    ]),

    html.Div([
        html.Div([
            dcc.Graph(
                id="graph_close",
            )
        ], className="six columns"),

    ],className="row")
])

app.css.append_css({
    "external_url":"https://codepen.io/chriddyp/pen/bWLwgP.css"
})



@app.callback(Output('graph_close', 'figure'),
              [Input("submit-button", "n_clicks")],
              [State("stock-input", "value")]
              )

def update_fig(n_clicks, symbol):
    from pandas_datareader import data, wb

    # checking for stock file 
    if path.exists(f"./src/stock_price_{symbol}.csv"):
        df= pd.read_csv(f'./src/stock_price_{symbol}.csv')
        print(f'raw file already exist for date : {end}')
    else:
        stock_extractor(symbol) 
        print('data generated')
        df= pd.read_csv(f'./src/stock_price_{symbol}.csv')
        
    # checking for prediction file 
    if path.exists(f'./out/pred_prophet_{symbol}.csv'):
        df_pred = pd.read_csv(f'out/pred_prophet_{symbol}.csv')
        print('prediction file already existed')
    else:
        print('Generating prediction file')
        prophet_predict(symbol)
        time.sleep(3)
        df_pred = pd.read_csv(f'out/pred_prophet_{symbol}.csv')


    trace_line = go.Scatter(x=list(df.Date),
                                y=list(df.Close),
                                #visible=False,
                                name="Close",
                                showlegend=False)

    trace_candle = go.Candlestick(x=df.Date,
                           open=df.Open,
                           high=df.High,
                           low=df.Low,
                           close=df.Close,
                           #increasing=dict(line=dict(color="#00ff00")),
                           #decreasing=dict(line=dict(color="white")),
                           visible=False,
                           showlegend=False)
    pred_line = go.Scatter(x=list(df_pred.ds),
                                y=list(df_pred.yhat_upper),
                                #visible=False,
                                name="Prediction",
                                showlegend=False)

    data = [trace_line, trace_candle, pred_line]

    updatemenus = list([
        dict(
            buttons=list([
                dict(
                    args=[{'visible': [True, False, False]}],
                    label='Line',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, True, False]}],
                    label='Candle',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, True]}],
                    label='Bar',
                    method='update'
                ),
            ]),
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=True,
            x=0,
            xanchor='left',
            y=1.05,
            yanchor='top'
        ),
    ])

    layout = dict(
        title=symbol,
        updatemenus=updatemenus,
        autosize=False,
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        xaxis_title='Time stamp',
        yaxis_title='stock Price',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                         label='YTD',
                         step='year',
                         stepmode='todate'),
                    dict(count=1,
                         label='1y',
                         step='year',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type='date'
        )
    )

    return {
        "data": data,
        "layout": layout
    }

if __name__=="__main__":
    app.run_server(debug=True, port=5001)
