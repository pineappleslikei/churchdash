import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pco_utils as util

app = dash.Dash(__name__)

# dummy data
df = pd.DataFrame({
    'Songs': ['Yes I Will', 'Belong To You', 'Fierce', 'Come To the Altar'],
    'x Played': [6, 5, 1, 3]
})

fig = px.bar(df, x='Songs', y='x Played', width=400, height=250)
fig2 = px.pie(df, values='x Played', names='Songs')

app.layout = html.Div(className='container', children=[
    html.Nav(className='title', children=[
        html.H1(f'Welcome, {util.dash_display_name}!')
    ]),
    html.Div([
        dcc.Graph(id='bar-graph', figure=fig),
    ]),
    html.Div([
        dcc.Graph(id='pie-chart', figure=fig2)
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)
