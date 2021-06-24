import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import pathlib
from app import app
##############
##   Data   ##
##############
# Load case data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
cases = pd.read_csv(DATA_PATH.joinpath('cases.csv'))
cases['report_date']=pd.to_datetime(cases.report_date)
county_list = sorted(cases.locality.unique())

# Load vax data
vax= pd.read_csv(DATA_PATH.joinpath("county_vax.csv"))
vax['administration_date']=pd.to_datetime(vax.administration_date)

##############
##  Layout  ##
##############

layout = html.Div([
    #county filter
    html.Div([
        dcc.Dropdown(
            id='county_dropdown',
            clearable=True,
            searchable=True,
            options = [{'label':x, 'value':x} for x in county_list],
            value='Virginia Beach',
            placeholder='Select a County',
            className='dcc_compon'
        )
    ], style={'textAlign':'center','marginTop':'-15px'},id='filter', className='dcc_compon'),
    #row 2
    html.Div([
        #col 1
        html.Div([
            html.P('As Of: ' ,
                   className='fix_label', style={'text-align': 'center', 'color': 'black'}),
            html.H6(str(cases['report_date'].iloc[-1].strftime('%B %d, %Y')),
                          className='fix_label', style={'text-align': 'center', 'color': 'black'}),
            dcc.Graph(id = 'confirmed', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}),
            dcc.Graph(id = 'hospital', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '15px'}),
            dcc.Graph(id = 'death', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '15px'}),
            html.H6('Vaccination Status: ',
                   className='fix_label', style={'text-align': 'center', 'color': '#1F618D'}),
            dcc.Graph(id = 'fullvax', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}),
            html.P('Fully Vaccinated',
                   className='fix_label', style={'text-align': 'center', 'color': 'black'}),
            dcc.Graph(id = 'onedose', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}),
            html.P('At Least One Dose',
                   className='fix_label', style={'text-align': 'center', 'color': 'black'}),
        ], className='create_container two columns'),
        #col 2
        html.Div([
            html.H5('How is the County Doing Compared to the Region Average?'),
            dcc.RadioItems(
                id='case_measure',
                options=[{'value':'cases_avg', 'label': 'Cases'},
                        {'value':'hosp_avg', 'label': 'Hospitalization'},
                        {'value':'deaths_avg', 'label': 'Deaths'}],
                value= 'cases_avg',
                labelStyle={'display':'inline-block'}
            ),
            dcc.Graph(id = 'case_plot2', config={'displayModeBar': 'hover'})
        ], className='create_container five columns'),
        #col 3
        html.Div([
            html.H5('Where and Which Vaccine are People Getting?'),
            dcc.RadioItems(
                id='dose_value',
                options=[{'value':1, 'label': 'First Dose'},
                        {'value':2, 'label': 'Second Dose'}],
                value= 1,
                labelStyle={'display':'inline-block'}
            ),
            dcc.Graph(id = 'dose_plot', config={'displayModeBar': 'hover'})
        ], className='create_container five columns')
    ],className='row flex-display'),

], id='countyContainer', style={'display': 'flex','flex-direction':'column'})

##############
##  connect ##
##############
@app.callback(Output("confirmed","figure"),
            [Input("county_dropdown","value")])
def update_confirmed(county_dropdown):
    df = cases[cases.locality == county_dropdown]
    value_confirmed = df.new_cases.iloc[-1].astype(int)
    delta_confirmed = df.new_cases.iloc[-2].astype(int)

    return {
        'data': [go.Indicator(
               mode='number+delta',
               value=value_confirmed,
               delta = {'reference': delta_confirmed,
                        'position': 'right',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 15},
                        'decreasing':{'color':'green'},
                        'increasing':{'color':'red'}},
               number={'valueformat': ',',
                       'font': {'size': 20}},
               domain={'y': [0, 1], 'x': [0, 1]}
        )],

        'layout': go.Layout(
            title={'text': 'New Confirmed',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='black'),
            paper_bgcolor='#FBFCFC',
            plot_bgcolor='#FBFCFC',
            height = 50,

        )
    }


@app.callback(Output("hospital","figure"),
            [Input("county_dropdown","value")])
def update_hospital(county_dropdown):
    df = cases[cases.locality == county_dropdown]
    value_hospital = df.new_hosp.iloc[-1].astype(int)
    delta_hospital = df.new_hosp.iloc[-2].astype(int)

    return {
        'data': [go.Indicator(
               mode='number+delta',
               value=value_hospital,
               delta = {'reference': delta_hospital,
                        'position': 'right',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 15},
                        'decreasing':{'color':'green'},
                        'increasing':{'color':'red'}},
               number={'valueformat': ',',
                       'font': {'size': 20}},
               domain={'y': [0, 1], 'x': [0, 1]}
        )],

        'layout': go.Layout(
            title={'text': 'New Hospitalization',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='orange'),
            paper_bgcolor='#FBFCFC',
            plot_bgcolor='#FBFCFC',
            height = 50,

        )
    }

@app.callback(Output("death","figure"),
            [Input("county_dropdown","value")])
def update_deaths(county_dropdown):
    df = cases[cases.locality == county_dropdown]
    value_death = df.new_deaths.iloc[-1].astype(int)
    delta_death = df.new_deaths.iloc[-2].astype(int)

    return {
        'data': [go.Indicator(
               mode='number+delta',
               value=value_death,
               delta = {'reference': delta_death,
                        'position': 'right',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 15},
                        'decreasing':{'color':'green'},
                        'increasing':{'color':'red'}},
               number={'valueformat': ',',
                       'font': {'size': 20}},
               domain={'y': [0, 1], 'x': [0, 1]}
        )],

        'layout': go.Layout(
            title={'text': 'New Deaths',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='#dd1e35'),
            paper_bgcolor='#FBFCFC',
            plot_bgcolor='#FBFCFC',
            height = 50,

        )
    }

@app.callback(Output("fullvax","figure"),
            [Input("county_dropdown","value")])
def update_fullvax(county_dropdown):
    vax_df = vax[(vax.locality == county_dropdown)].reset_index()
    full_vax_perc = (round(vax_df[(vax_df.dose_number == 2) | ((vax_df.vaccine_manufacturer == "J&J")\
                    & (vax_df.dose_number ==2))].vaccine_doses_administered.sum() / vax_df.Population.iloc[-1] *100))

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = full_vax_perc,
        number = {'suffix':"%"},
        gauge={
            'axis' : {'visible':False, "range":(0,101)}},
        domain = {'x':[0,0], 'y':[0,0]}))
    fig.update_layout(
        height=80,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='#FBFCFC',
        plot_bgcolor='#FBFCFC',
    )
    return fig

@app.callback(Output("onedose","figure"),
            [Input("county_dropdown","value")])
def update_fullvax(county_dropdown):
    vax_df = vax[(vax.locality == county_dropdown)].reset_index()
    onedose_perc = (round(vax_df[vax_df.dose_number == 1].vaccine_doses_administered.sum() / vax_df.Population.iloc[-1] *100))

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = onedose_perc,
        number = {'suffix':"%"},
        gauge={
            'axis' : {'visible':False, "range":(0,101)}},
        domain = {'x':[0,0], 'y':[0,0]}))
    fig.update_layout(
        height=80,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='#FBFCFC',
        plot_bgcolor='#FBFCFC',
    )
    return fig

@app.callback(Output("case_plot2","figure"),
            [Input("county_dropdown","value"),
            Input("case_measure","value")])
def update_case_plot2(county_dropdown,case_measure):
    region = cases[cases.locality == county_dropdown].region.iloc[0]
    region_df = cases[cases.region == region].groupby(['report_date'])[['new_cases','new_hosp','new_deaths']].mean().reset_index()
    df = cases[cases.locality == county_dropdown].groupby(['report_date'])[['new_cases','new_hosp','new_deaths']].sum().reset_index()

    df['cases_avg'] = df['new_cases'].rolling(7).mean()
    df['hosp_avg'] = df['new_hosp'].rolling(7).mean()
    df['deaths_avg'] = df['new_deaths'].rolling(7).mean()
    region_df['cases_avg'] = region_df['new_cases'].rolling(7).mean()
    region_df['hosp_avg'] = region_df['new_hosp'].rolling(7).mean()
    region_df['deaths_avg'] = region_df['new_deaths'].rolling(7).mean()

    title_text = "Weekly Rolling Average Count of " + '<br>'+str(county_dropdown) + " County and " + str(region).title() + " Region"


    return {
        'data': [
            go.Scatter(
                x=df['report_date'],
                y=df[case_measure],
                mode='lines',
                name=str(county_dropdown),
                marker=dict(color='#F7DC6F'),
                hoverinfo='text',
                hovertext=
                '<b>Date</b>: ' + df['report_date'].astype(str) + '<br>' +
                '<b>7-Day Rolling Average Count</b>: ' + [f'{x:,.0f}' for x in df[case_measure]] + '<br>'


        ),
            go.Scatter(
                x=region_df["report_date"],
                y=region_df[case_measure],
                mode='lines',
                name='Region (' +str(region) +')',
                line=dict(width=3, color='#5D6D7E'),
                hoverinfo='text',
                hovertext=
                '<b>Date</b>: ' + region_df['report_date'].astype(str) + '<br>' +
                '<b>7 Days Rolling Average Count</b>: ' + [f'{x:,.0f}' for x in region_df[case_measure]] + '<br>'


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
                    'xanchor': 'center', 'yanchor':"bottom",'x': 0.5, 'y': 1},
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
            yaxis=dict(title='<b>7 Days Rolling Average Count</b>',
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



@app.callback(Output("dose_plot","figure"),
            [Input("county_dropdown","value"),
            Input("dose_value","value")])
def update_dose_plot(county_dropdown, dose_value):
    vax_df = vax[(vax.locality == county_dropdown)].reset_index()
    dose_df =vax_df[(vax_df.vaccine_manufacturer != 'Non-Specified')&(vax_df.dose_number == dose_value)].groupby(['facility_type','vaccine_manufacturer']).vaccine_doses_administered.sum().reset_index()
    dose_df = dose_df.pivot_table(index='facility_type', columns='vaccine_manufacturer', aggfunc='sum').fillna(0).reset_index()
    dose_df.columns = dose_df.columns.map(''.join)
    if dose_value == 1:
        dose_df.columns = ['facility_type', 'J&J', 'Moderna', 'Pfizer']
    elif dose_value == 2:
        dose_df.columns = ['facility_type','Moderna','Pfizer']
    dose_df.set_index('facility_type', inplace=True)

    colors = px.colors.qualitative.T10

    fig = px.bar(dose_df,
             x = dose_df.index,
             y = [c for c in dose_df.columns],
             template = 'plotly_white',
             color_discrete_sequence = colors,
             title = 'Types of Vaccine Administered at Different Facilities'
             )
    fig.update_layout(barmode='stack',
                    legend=dict(title=None, orientation="h",
                    y=1, yanchor="bottom", x=0.5, xanchor="center"),
                    xaxis=dict(title='<b>Facility Types</b>'),
                    yaxis=dict(title='<b>Vaccine Administered Count</b>'))

    return fig
