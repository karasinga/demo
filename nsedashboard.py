import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

df = pd.read_excel('NSE.xlsx')
# print(df[:15])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

server = app.server
# Layout section: Bootstrap (https://hackerthemes.com/bootstrap-cheatsheet/)
# ************************************************************************
app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(html.H1("NSE Stock Market Dashboard",
                        className='text-center text-primary mb-4'),
                width=12)
    ),

    dbc.Row([

        dbc.Col([
            dcc.Dropdown(id='my-dpdn', multi=False, value='KCB', searchable=True,
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df['CODE'].unique())],
                         style={'height': 'height',
                                'margin-top': '0px',
                                'margin-left': '10px',
                                'font-size': '9px',
                                'width': '50%'},
                         placeholder="Select a company ticker",
                         clearable=False,
                         ),
            dcc.Graph(id='line-fig', figure={})
        ],  # width={'size':5, 'offset':1, 'order':1},
            xs=12, sm=12, md=12, lg=12, xl=12
        ),
    ], no_gutters=True, justify='start'),  # Horizontal:start,center,end,between,

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='my-dpdn2', multi=True,
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df['CODE'].unique())],
                         value=['SASN'],
                         clearable=True,
                         searchable=True,
                         persistence=True,
                         persistence_type='session',  # memory, local,session
                         placeholder="Select one or more company ticker",

                         ),
            dcc.Graph(id='line-fig2', figure={})
        ],  # width={'size':5, 'offset':0, 'order':2},
            xs=12, sm=12, md=12, lg=12, xl=12
        )
    ])
], fluid=True)


# Callback section: connecting the components
# ************************************************************************
# Line chart - Single
@app.callback(
    Output('line-fig', 'figure'),
    Input('my-dpdn', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['CODE'] == stock_slctd]
    dff['MA200'] = dff.Close.rolling(200).mean()
    latest_close = dff['Close'].iloc[-1]
    latest_date = dff['Date'].iloc[-1]
    latest_200_ma = round(dff['MA200'].iloc[-1], 2)
    figln = px.line(dff, x='Date', y=['Close', 'MA200'])
    # figln.update_xaxes(showticklabels=True)
    figln.update_xaxes(
        title=f"{stock_slctd} closing price as on {latest_date} was {latest_close}, while it's 200MA was {latest_200_ma}",
                visible=True, showticklabels=False)
    return figln


# Line chart - multiple
@app.callback(
    Output('line-fig2', 'figure'),
    Input('my-dpdn2', 'value')
)
def update_graph_2(stock_slctd):
    if len(stock_slctd) == 0:
        dff = df[df['CODE'].isin(['KCB', 'SBIC', 'EQTY'])]
        figln2 = px.line(dff, x='Date', y='Close', color='CODE')
        figln2.update_xaxes(showticklabels=False)
    else:
        dff = df[df['CODE'].isin(stock_slctd)]
        figln2 = px.line(dff, x='Date', y='Close', color='CODE')
        figln2.update_xaxes(showticklabels=False)
    return figln2


if __name__ == '__main__':
    app.run_server(debug=False)
