import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('./data/diamonds.csv')

cuts = df['cut'].unique()
color = df['color'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='filter1',
                options=[{'label': i, 'value': i} for i in cuts],
                value='Ideal'
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='filter2',
                options=[{'label': i, 'value': i} for i in color],
                value='E'
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    ]),

    dcc.Graph(id='diamond-graphic'),

    # dcc.Slider(
    #     id='carat--slider',
    #     min=df['carat'].min(),
    #     max=df['carat'].max(),
    #     value=df['carat'].max(),
    #     marks={str(carat): str(carat) for carat in np.arange(0, 6.25, 0.25)},
    #     step=None
    # )
])

@app.callback(
    Output('diamond-graphic', 'figure'),
    [Input('filter1', 'value'),
     Input('filter2', 'value')])
def update_graph(filter1, filter2):
    dff = df[(df['cut'] == filter1) & (df['color'] == filter2)]

    return {
        'data': [dict(
            x=dff['carat'],
            y=dff['price'],
#            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': 'Carat',
            },
            yaxis={
                'title': 'Price',
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)