import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import pco_utils as util

app = dash.Dash(__name__)


# status pie chart
status_data = {
    'status':util.people_stats,
    'count':[1 for stat in util.people_stats]
}

status_df = pd.DataFrame(data=status_data)
status_fig = px.pie(
    data_frame=status_df,
    values='count',
    names='status',
    color='status',
    color_discrete_map={'C': '#84AB57',
                        'U': '#F8D525',
                        'D': '#DC3318'},
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
