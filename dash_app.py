import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pco_utils as util

app = dash.Dash(__name__)

# status pie chart
status_labels = ['Confirmed', 'Unconfirmed', 'Declined']
status_values = [
    util.people_stats['confirmed'],
    util.people_stats['unconfirmed'],
    util.people_stats['declined']
]

status_fig = px.pie(
    labels=status_labels,
    values=status_values,
    color=status_labels,
    color_discrete_map={'Confirmed': '#84AB57',
                        'Unconfirmed': '#F8D525',
                        'Declined': '#DC3318'},
    title='PCO Status',
    hole=.5,
    width=400,
)


# dashboard html layout
app.layout = html.Div(className='container', children=[
    html.Nav(className='title', children=[
        html.H1(f'Welcome, {util.dash_display_name}!')
    ]),
    html.Div([
        dcc.Graph(id='status-chart', figure=status_fig)
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)
