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

dash_display_name = 'Chris'

# status pie chart
status_data = {
    'status': util.people_stats,
    'count': [1 for stat in util.people_stats]
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
    title='PCO Status (14-day Forecast)',
    hole=.5,
    width=400,
)
status_fig.update_layout(
    font=dict(
        family='Josefin Sans',
        size=16,
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    title=dict(
        x=0.5
    )
)

# people table


def make_people_fig(plan):
    plan_data = {
        'Person': [person['name'] for person in plan['people']],
        'Position': [person['position'] for person in plan['people']]
    }
    df = pd.DataFrame(data=plan_data)
    plan_people_figure = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=['Person', 'Position'],
                    font=dict(family='Josefin Sans'),
                ),
                cells=dict(values=[df.Person, df.Position])
            )
        ]
    )
    plan_people_figure.update_layout(
        title=dict(
            text=f'{plan["pretty_date"]}',
            x=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        autosize=True,
    )
    return plan_people_figure


def make_people_html(list_of_plans):
    graphs = []
    for plan in list_of_plans:
        graphs.append(
            html.Div(
                children=[
                    dcc.Graph(className='people-charts',
                              figure=make_people_fig(plan)),
                ],
                className='people-chart-wrappers'
            )
        )
    return graphs


# song graph
songs_df = pd.DataFrame.from_dict(util.songs, orient='index').reset_index()
songs_df = songs_df.rename(columns={'index': 'Song', 0: 'Services'})
songs_fig = px.bar(songs_df, x='Services', y='Song')
songs_fig.update_layout(
    title=dict(
        text='Song Usage',
        x=0.5
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    autosize=False,
)

# dashboard html layout
app.layout = html.Div(className='container', children=[
    html.Nav(className='title', children=[
        html.H1(f'Welcome, {dash_display_name}!')
    ]),
    html.Div(id='main-wrapper', children=[
        html.Div(id='charts-wrapper', children=[
            dcc.Graph(
                className='charts',
                id='status-chart',
                figure=status_fig
            ),
            dcc.Graph(
                className='charts',
                id='songs-graph',
                figure=songs_fig
            )
        ]),
        html.Div(children=make_people_html(
            util.two_weeks_sorted), id='people-container'),
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)
