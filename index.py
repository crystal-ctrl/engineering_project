import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np

from app import app
from app import server
from apps import state, county

cases = pd.read_csv('data/cases.csv')
cases['report_date']=pd.to_datetime(cases.report_date)


top_layout = html.Div([
    #links to other pages
    html.Div([
        html.Nav(className = "nav nav-pills", children=[
            html.A('State', className="nav-item nav-link btn", href='/apps/state',
                    style={"font-size": "2rem",
                            "box-shadow": "4px 4px 2px #e3e3e3",
                            "padding": "5px",
                            'marginTop':'-15px'}),
            html.H5(""),
            html.A('County', className="nav-item nav-link active btn", href='/apps/county',
                    style={"font-size": "2rem",
                        "box-shadow": "4px 4px 2px #e3e3e3",
                        "padding": "5px",
                        'marginTop':'-15px'})
            ],style = {'marginTop':'-15px'}),
    ], className='one-third column', id = 'links', style={'textAlign':'center'}),

    #title
    html.Div([
        html.Div([
            html.H2('VA x COVID',
                style={'marginBottom': '10','marginTop':'-15px'}),
            html.H3('Virginia COVID-19 Dashboard',
                style={'marginTop':'-15px'})
        ], style={'textAlign':'center'})
    ], className='one-third column', id='title'),

    # last update date
    html.Div([
        html.H6('Last Updated: ',
                style={'marginTop':'-15px'}),
        html.H6(str(cases['report_date'].iloc[-1].strftime('%B %d, %Y')) + ' 13:00 (EST)')

    ], className='one-third column', id = 'title1', style={'textAlign':'center'})

], id='header',className='row flex-display', style={'margin-bottom': '10px','marginTop':'-15px'})

app.layout = html.Div([
    dcc.Location(id='url',refresh=False),
    top_layout,
    html.Div(id='page-content',children=[])
], id='mainContainer', style={'display': 'flex','flex-direction':'column'})

@app.callback(Output('page-content', 'children'),
            [Input('url','pathname')])
def display_page(pathname):
    if pathname == '/apps/state':
        return state.layout
    if pathname == '/apps/county':
        return county.layout
    else:
        return state.layout











if __name__ == '__main__':
    app.run_server(debug=True)
