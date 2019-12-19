import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('./data/diamonds.csv')

cuts = df['cut'].unique()
clarity = df['clarity'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in cuts],
                value='Ideal'
            )],
            style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in clarity],
                value='SI2'
            )],
            style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='diamond-graphic'),

    dcc.Slider(
        id='carat--slider',
        min=df['carat'].min(),
        max=df['carat'].max(),
        value=df['carat'].max(),
        marks={str(carat): str(carat) for carat in range(1, 6)},
        step=None
    )
])

@app.callback(
    Output('diamond-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('carat--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name, carat_value):
    dff = df[df['carat'] <= carat_value]

    return {
        'data': [dict(
            x=dff[dff['cut'] == xaxis_column_name]['price'],
            y=dff[dff['color'] == yaxis_column_name]['price'],
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
                'title': xaxis_column_name,
            },
            yaxis={
                'title': yaxis_column_name,
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)