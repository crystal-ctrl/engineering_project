import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from urllib.request import urlopen
import json
import pathlib
from app import app

##############
##   Data   ##
##############
#map Counties
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

#setup path
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
# Load case data
cases = pd.read_csv(DATA_PATH.joinpath('cases.csv'))
cases['report_date']=pd.to_datetime(cases.report_date)
#cases dfs
cases_1 = cases.groupby(['report_date'])[['total_cases','hospitalizations','deaths']]\
            .sum().reset_index()
cases_map = cases.groupby(['fips','locality'])[['total_cases','hospitalizations','deaths',
                        'total_cases_rate','hospitalizations_rate','deaths_rate']].max().reset_index()
cases_plot = cases.groupby(['report_date'])[['new_cases','weekly_rolling_avg_cases']].sum().reset_index()
#cases stats nums
total_cases = cases_1.total_cases.iloc[-1]
new_cases = total_cases - cases_1.total_cases.iloc[-2]
total_hosp = cases_1.hospitalizations.iloc[-1]
new_hosp = total_hosp - cases_1.hospitalizations.iloc[-2]
total_deaths = cases_1.deaths.iloc[-1]
new_deaths = total_deaths - cases_1.deaths.iloc[-2]
# Load vax data
vax = pd.read_csv(DATA_PATH.joinpath('vax.csv'))
vax['administration_date'] = pd.to_datetime(vax.administration_date)

vax_map = pd.read_csv(DATA_PATH.joinpath('vax_map.csv'))

vax2 = pd.read_csv(DATA_PATH.joinpath('county_vax.csv'))
vax2['administration_date'] = pd.to_datetime(vax2.administration_date)
#vax dfs
vax_plot = vax2.groupby(['administration_date'])[['vaccine_doses_administered']].sum().reset_index()
vax_plot['weekly_rolling_avg_dose'] = vax_plot.vaccine_doses_administered.rolling(7).mean()
#vax stat nums
total_doses = vax.vaccine_doses_administered.sum()
new_total_doses = vax[(vax.administration_date.notnull())].groupby(['administration_date']).vaccine_doses_administered.sum().iloc[-1]
one_dose = vax[vax.dose_number ==1].vaccine_doses_administered.sum()
va_pop = vax[(vax.administration_date.notnull())].groupby(['fips']).Population.max().sum()
full_vax = vax[vax.dose_number ==2].vaccine_doses_administered.sum()+vax[(vax.dose_number ==1) & (vax.vaccine_manufacturer =='J&J')].vaccine_doses_administered.sum()

##############
##  Layout  ##
##############

layout = html.Div([

    #subheaders
    html.Div([
        html.H4('Virginia State At a Glance',style={'color':'white'})
    ], style={'textAlign':'center','marginTop':'-15px'},id='subheader', className='subheader'),
    html.Div([
        html.Div([
            html.H5('Cases Summary')
        ], style={'textAlign':'center'},id='smallheader1',className='six columns smallheader'),
        html.Div([
            html.H5('Vaccine Summary')
        ], style={'textAlign':'center'},id='smallheader2',className='six columns smallheader')
    ],className='row flex-display'),
#-----------------------------------------------------------------------------------------------#
    # row of cards (row 2)
    html.Div([
        # case card
        html.Div([
            html.H6(children='Total Cases',
                    style={'textAlign': 'center'}),
            html.P(f"{total_cases:,.0f}",
                    style={'textAlign': 'center', 'fontSize': 40}),
            html.P('new: ' + f"{new_cases:,.0f}"
                   + ' (' + str(round((new_cases /total_cases) * 100, 2)) + '%)',
                   style={'textAlign': 'center',
                          'fontSize': 15,
                          'margin-top': '-18px'})
        ], className='card_container two columns'), # case card ends

        # hospital card
        html.Div([
            html.H6(children='Hospitalizations',
                    style={'textAlign': 'center'}),
            html.P(f"{total_hosp:,.0f}",
                    style={'textAlign': 'center',
                            'fontSize': 40,
                            'color':'orange'}),
            html.P('new: ' + f"{new_hosp:,.0f}"
                   + ' (' + str(round((new_hosp / total_hosp) * 100, 2)) + '%)',
                   style={'textAlign': 'center',
                          'fontSize': 15,
                          'color':'orange',
                          'margin-top': '-18px'})
        ], className='card_container two columns'), # hospital card ends

        # death card
        html.Div([
            html.H6(children='Total Deaths',
                    style={'textAlign': 'center'}),
            html.P(f"{total_deaths:,.0f}",
                    style={'textAlign': 'center',
                            'fontSize': 40,
                            'color':'red'}),
            html.P('new: ' + f"{new_deaths:,.0f}"
                   + ' (' + str(round((new_deaths / total_deaths) * 100, 2)) + '%)',
                   style={'textAlign': 'center',
                          'fontSize': 15,
                          'color':'red',
                          'margin-top': '-18px'})
        ], className='card_container two columns'), # death card ends

        # total vax card
        html.Div([
            html.H6(children='Total Doses',
                    style={'textAlign': 'center'}),
            html.P(f"{total_doses:,.0f}",
                    style={'textAlign': 'center',
                            'fontSize': 40}),
            html.P('new: ' + f"{new_total_doses:,.0f}"
                   + ' (' + str(round(((new_total_doses) /
                            total_doses) * 100, 2)) + '%)',
                   style={'textAlign': 'center',
                          'fontSize': 15,
                          'margin-top': '-18px'})
        ], className='card_container two columns'), # total vax card ends

        # one dose vax card
        html.Div([
            html.H6(children='At Least 1 Dose',
                    style={'textAlign': 'center'}),
            html.P(f"{one_dose:,.0f}",
                    style={'textAlign': 'center',
                            'fontSize': 40,
                            'color':'#3498DB'}),
            html.P(str(round(one_dose/va_pop *100,1))+'%'+' of population',
                   style={'textAlign': 'center',
                          'fontSize': 15,
                          'color':'#3498DB',
                          'margin-top': '-18px'})
        ], className='card_container two columns'), # one dose card ends

        # fully vax card
        html.Div([
            html.H6(children='Fully Vaccinated',
                    style={'textAlign': 'center'}),
            html.P(f"{full_vax:,.0f}",
                    style={'textAlign': 'center',
                            'fontSize': 40,
                            'color':'green'}),
            html.P(str(round(full_vax/va_pop *100,1))+'%'+' of population',
                   style={'textAlign': 'center',
                          'fontSize': 15,
                          'color':'green',
                          'margin-top': '-18px'})
        ], className='card_container two columns'), # two doses card ends
    ], className='row flex display'), #row 2 ends
#-----------------------------------------------------------------------------------------------#
    # Map cards (row 3)
    html.Div([
        # cases map
        html.Div([
            html.Div([
                html.Div([
                    html.P("Select Measure:"),
                    dcc.RadioItems(
                        id='measure',
                        options=[{'value':'total_cases', 'label': 'Cases'},
                                {'value':'hospitalizations', 'label': 'Hospitalization'},
                                {'value':'deaths', 'label': 'Deaths'}],
                        value= 'total_cases',
                        labelStyle={'display':'inline-block'}
                    ),
                ],className='eight columns'),
                html.Div([
                    html.P("Select Method:"),
                    dcc.RadioItems(
                        id='method',
                        options=[{'value':'count', 'label': 'Counts'},
                                {'value':'rate', 'label': 'Rates per 100,000'}],
                        value= 'count',
                        labelStyle={'display':'inline-block'}
                    ),
                ],className='four columns'),
            ],className='row flex display'),
            dcc.Graph(id = 'case_map', config={'displayModeBar': 'hover'})
        ], className='card_container six columns'),


        # vax map
        html.Div([
            html.Div([
                html.Div([
                    html.P("Select Vaccination Status:"),
                    dcc.RadioItems(
                        id='status',
                        options=[{'value':'One_dose','label':'At Least One Dose'},
                                {'value':'Fully_vaccinated','label':'Fully Vaccinated'},
                                {'value':'Total_doses','label':'Total Doses'}],
                        value="Fully_vaccinated",
                        labelStyle={'display':'inline-block'}
                    ),
                ],className='eight columns'),
                html.Div([
                    html.P("Select Method:"),
                    dcc.RadioItems(
                        id='method_vax',
                        options=[{'value':'count', 'label': 'Counts'},
                                {'value':'rate', 'label': 'Rates per 100,000'}],
                        value= 'count',
                        labelStyle={'display':'inline-block'}
                    ),
                ],className='four columns'),
            ],className='row flex display'),

            dcc.Graph(id = 'vax_map', config={'displayModeBar': 'hover'})
        ], className='card_container six columns'),

    ], className='row flex display'),# row 3 ends
#-----------------------------------------------------------------------------------------------#
    # boxplots(row4)
    html.Div([
        # case plot
        html.Div([
            dcc.Dropdown(id="slct_days",
                        options=[
                            {"value":30, "label": "Past 30 Days"},
                            {"value":90, "label": "Past 90 Days"},
                            {"value":180,"label": "Past 180 Days"},
                            {"value":0, "label": "All Reporting"}],
                        multi=False,
                        value=180
                        ),

            dcc.Graph(id='case_plot', config={'displayModeBar':'hover'})
        ],className='card_container six columns'),

        #vax plot
        html.Div([
            dcc.Dropdown(id="slct_days_vax",
                        options=[
                            {"value":30, "label": "Past 30 Days"},
                            {"value":90, "label": "Past 90 Days"},
                            {"value":180,"label": "Past 180 Days"},
                            {"value":0, "label": "All Reporting"}],
                        multi=False,
                        value=180
                        ),

            dcc.Graph(id='vax_plot', config={'displayModeBar':'hover'})
        ],className='card_container six columns'),

    ], className='row flex display')# row 4 ends
], id='stateContainer', style={'display': 'flex','flex-direction':'column'})#last line don't touch
##################################################################################################
##############
##  connect ##
##############
#case_map
@app.callback(Output("case_map", "figure"),
            [Input("measure", "value"),
            Input("method","value")])
def display_case_map(measure, method):
    if method == "count":
        measure = measure
    elif method == "rate":
        measure = measure + "_rate"

    title_map={'total_cases':'Case (Count)', 'hospitalizations':'Hospitalization (Count)',
                'deaths':'Death (Count)', 'total_cases_rate': 'Cases (Rate per 100,000)',
                'hospitalizations_rate': 'Hospitalization (Rate per 100,000)',
                'deaths_rate': 'Death (Rate per 100,000)'}
    title = "COVID-19 in Virginia: " + str(title_map[measure])

    fig = px.choropleth(cases_map, geojson=counties,
                        locations='fips',
                        color=measure,
                        range_color=(0,cases_map[measure].max()*0.75),
                        color_continuous_scale="magenta",
                        scope='usa',
                        hover_name='locality',
                        hover_data=['total_cases',
                                    'hospitalizations',
                                    'deaths',
                                    'total_cases_rate',
                                    'hospitalizations_rate',
                                    'deaths_rate'])
    fig.update_geos(fitbounds="locations",visible=False)
    fig.update_layout(title_text=title,
                    margin={"r":0,"l":0,"b":0})
    return fig
#vax_map
@app.callback(Output("vax_map", "figure"),
            [Input("status", "value"),
            Input("method_vax","value")])
def display_vax_map(status, method_vax):
    if method_vax == "count":
        status = status
    elif method_vax == "rate":
        status = status + "_rate"

    title_map={'One_dose':'At Least One Dose (Count)','Fully_vaccinated':'Fully Vaccinated (Count)',
                'Total_doses': 'Total Doses(Count)',
                'One_dose_rate':'At Least One Dose (Rate per 100,000)',
                'Fully_vaccinated_rate':'Fully Vaccinated (Rate per 100,000)',
                'Total_doses_rate': 'Total Doses (Rate per 100,000)'}
    title = "Vaccination in Virginia: " + str(title_map[status])

    fig = px.choropleth(vax_map, geojson=counties,
                        locations='fips',
                        color=status,
                        range_color=(0,vax_map[status].max()* 0.90),
                        color_continuous_scale="mint",
                        scope='usa',
                        hover_name='locality',
                        hover_data=['Total_doses','One_dose','Fully_vaccinated',
                                    'Total_doses_rate','One_dose_rate','Fully_vaccinated_rate'])
    fig.update_geos(fitbounds="locations",visible=False)
    fig.update_layout(title_text=title,
                    margin={"r":0,"l":0,"b":0})
    return fig
#case plot
@app.callback(Output("case_plot", "figure"),
            [Input("slct_days", "value")])
def update_case_plot(slct_days):
    if slct_days == 0:
        df = cases_plot.copy()
        title_text = "All Reportings of Daily Cases in Virginia"
    else:
        df = cases_plot.copy()
        df = df.tail(slct_days)
        title_text = "Last " + str(slct_days) + " Days of Daily Cases in Virginia"

    return {
        'data': [go.Bar(
            x=df['report_date'],
            y=df['new_cases'],
            name='Daily Confirmed Cases',
            marker=dict(color='#5D6D7E'),
            hoverinfo='text',
            hovertext=
            '<b>Date</b>: ' + df['report_date'].astype(str) + '<br>' +
            '<b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in df['new_cases']] + '<br>'


        ),
            go.Scatter(
                x=df['report_date'],
                y=df['weekly_rolling_avg_cases'],
                mode='lines',
                name='Rolling Average of the last 7 days - daily confirmed cases',
                line=dict(width=3, color='#F7DC6F'),
                hoverinfo='text',
                hovertext=
                '<b>Date</b>: ' + df['report_date'].astype(str) + '<br>' +
                '<b>7 Days Rolling Average Cases</b>: ' + [f'{x:,.0f}' for x in df['weekly_rolling_avg_cases']] + '<br>'


            )],

        'layout': go.Layout(
            title={'text': title_text,
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'black',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='black',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#f2f4f7',
            plot_bgcolor='#f2f4f7',
            legend={'orientation': 'h',
                    'bgcolor': '#f2f4f7',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.2},
            # margin=dic(b=0),
            xaxis=dict(title='<b>Date</b>',
                       color = 'black',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='black',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='black',
                           size=12
                       )),
            yaxis=dict(title='<b>Daily Confirmed Cases</b>',
                       color='black',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='black',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='black',
                           size=12
                       ))


        )
    }

@app.callback(Output("vax_plot", "figure"),
            [Input("slct_days_vax", "value")])
def update_vax_plot(slct_days):
    if slct_days == 0:
        df = vax_plot.copy()
        title_text = "All Reportings of Vaccine Administered in Virginia"
    else:
        df = vax_plot.copy()
        df = df.tail(slct_days)
        title_text = "Last " + str(slct_days) + " Days of Vaccine Administered in Virginia"

    return {
        'data': [go.Bar(
            x=df['administration_date'],
            y=df['vaccine_doses_administered'],
            name='Daily Vaccine Administered',
            marker=dict(color='#5D6D7E'),
            hoverinfo='text',
            hovertext=
            '<b>Date</b>: ' + df['administration_date'].astype(str) + '<br>' +
            '<b>Daily Vaccine Administered</b>: ' + [f'{x:,.0f}' for x in df['vaccine_doses_administered']] + '<br>'


        ),
            go.Scatter(
                x=df['administration_date'],
                y=df['weekly_rolling_avg_dose'],
                mode='lines',
                name='Rolling Average of the last 7 days - daily vaccine administered',
                line=dict(width=3, color='#F7DC6F'),
                hoverinfo='text',
                hovertext=
                '<b>Date</b>: ' + df['administration_date'].astype(str) + '<br>' +
                '<b>7 Days Rolling Average Doses</b>: ' + [f'{x:,.0f}' for x in df['weekly_rolling_avg_dose']] + '<br>'


            )],

        'layout': go.Layout(
            title={'text': title_text,
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'black',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='black',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#f2f4f7',
            plot_bgcolor='#f2f4f7',
            legend={'orientation': 'h',
                    'bgcolor': '#f2f4f7',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.2},
            xaxis=dict(title='<b>Date</b>',
                       color = 'black',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='black',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='black',
                           size=12
                       )),
            yaxis=dict(title='<b>Daily Vaccine Administered</b>',
                       color='black',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='black',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='black',
                           size=12
                       ))
        )
    }
