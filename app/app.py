#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('~/Documents/#dev&work/#pystuff/statflicker/points.csv')


def generate_table(dataframe):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(len(dataframe))]
    )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div([
    html.Div([ 
    html.H1('Walkytalky NBA League'), 
    html.P("League analysis tool.")
    ], style={
    'textAlign': 'center',
    'color': colors['text']
    }),
    
  
    
    dcc.Graph(
        id='avg-ftps',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['team'] == i]['week'],
                    y=df[df['team'] == i]['points'],
                    text=df[df['team'] == i]['player_name'],
                    mode='markers',
                    opacity=0.5,
                    marker={
                        'size': 10,
                        'line': {'width': 1, 'color': 'black'}
                    },
                    name=i
                ) for i in df.team.unique()
            ],
            'layout': go.Layout(
                xaxis={'title': 'week'},
                yaxis={'title': 'avg ftps'},
                margin={'l':50, 'b': 40, 't': 30, 'r': 50},
                legend={'x': -0.2, 'y': 1},
                legend_orientation='v',
                hovermode='closest'
            )
        }
    ),

    generate_table(df),
])


if __name__ == '__main__':
    app.run_server(debug=True)
