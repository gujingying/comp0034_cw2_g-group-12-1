# Copied from the Dash tutorial documentation at https://dash.plotly.com/layout on 24/05/2021
# Import section modified 10/10/2021 to comply with changes in the Dash library.

# Run this app with `python dash.py` and visit http://127.0.0.1:8050/ in your web browser.
import math
from datetime import date
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from my_app.dash_app.airdata import AirQualityData
from my_app.dash_app.chart import AirQualityChart

# Prepare the data set
data = AirQualityData()
area = ''
start = '2021-1-1'
end = '2021-12-31'
data.process_data_for_area(area, start, end)

# Create the figures

# First map showing the location of cities (scatter mapbox)
df = pd.read_csv("data/min-max-avg.csv")

mapbox_token = "pk.eyJ1Ijoic3RlcGhhbmllMDYyNSIsImEiOiJja3plcDl3NTQwa2xoMzFtcXdtMGx4Z3U4In0.HJZkpBQj0blh5xUoXXR-VA"

fig_mapbox = go.Figure()

fig_mapbox.add_trace(
    go.Scattermapbox(lat=df["Latitude"], lon=df["Longitude"], text=df["Location"],
                     marker=go.scattermapbox.Marker(size=12, color='rgb(255, 0, 0)', opacity=0.7),
                     mode='markers+text', textposition="top center")),

fig_mapbox.add_trace(
    go.Scattermapbox(lat=df["Latitude"], lon=df["Longitude"],
                     marker=go.scattermapbox.Marker(size=6, color='rgb(242, 177, 172)', opacity=0.7),
                     mode='markers', hoverinfo=None)),

fig_mapbox.update_layout(
    width=570, height=425, margin=dict(l=140, r=0, t=35, b=0),
    hovermode='closest', showlegend=False,
    mapbox=dict(accesstoken=mapbox_token,
                center=dict(lat=53.479489, lon=-2.245115), zoom=4.5))

rc = AirQualityChart(data)
airtype_list = ['PM2.5', 'PM10']
airtype = 'PM2.5'
fig_rc = rc.create_chart(area, airtype)

external_stylesheets = [dbc.themes.MINTY]


def init_dashboard(flask_app):
    dash_app = dash.Dash(server=flask_app,
                         routes_pathname_prefix="/dash_app/",
                         external_stylesheets=external_stylesheets)

    # Create layout of the dashboard
    dash_app.layout = dbc.Container([
        html.Br(),
        # First row display the dashboard name
        dbc.Row(dbc.Col(children=[
            html.H1('Open Air Quality', style={'text-align': 'center'}),
            html.P('Particular matters monitoring dashboard',
                   className='lead', style={'text-align': 'center'})
        ])),

        # Insert multiple pages
        dcc.Tabs(children=[

            # First tab display the location of cities
            dcc.Tab(label='View Locations', children=[
                dbc.Row([

                    # This is for the first scatter mapbox
                    dbc.Col(width=6, children=[
                        html.Br(),
                        html.Br(),
                        html.H5('View air quality in various cities across UK:',
                                style={'text-align': 'center'}),
                        html.Br(),
                        html.P('London, Manchester, Cardiff, Edinburgh...',
                               style={'text-align': 'center'}),
                        dcc.Graph(id='scatter-map', figure=fig_mapbox),
                    ]),

                    # Add the second density heatmap here
                    dbc.Col(width=6, children=[
                        html.Br(),
                        html.Br(),

                        dbc.Row([
                            dbc.Col([
                                html.H5('Select date for the heatmap:', style={'text-align': 'center'}),
                                html.Br(),
                                html.P('view total pollutants amount in each city',
                                       style={'text-align': 'center'}),
                            ]),

                            dbc.Col([
                                dcc.DatePickerSingle(id='map-date-picker-single',
                                                     min_date_allowed=date(
                                                         2021, 1, 1),
                                                     max_date_allowed=date(
                                                         2021, 12, 31),
                                                     initial_visible_month=date(
                                                         2021, 1, 1),
                                                     date=date(2021, 1, 1)
                                                     ),
                            ]),
                            html.Div(
                                id='output-container-date-picker-single', children=[]),
                            html.Br(),
                            dcc.Graph(id='mapbox-heatmap', figure={}),
                        ]),
                    ]),
                ], className="mx-auto rounded", style={"position": "absolute"}),
            ]),

            # Second tab display the daily pollutant matters
            dcc.Tab(label='Daily Matters', children=[

                dbc.Row([dbc.Col(width=4, children=[
                    html.Br(),
                    html.H6('Select Date'),
                    dcc.DatePickerSingle(
                        id='my-date-picker-single',
                        min_date_allowed=date(2021, 1, 1),
                        max_date_allowed=date(2021, 12, 31),
                        initial_visible_month=date(2021, 1, 1),
                        date=date(2021, 1, 1)
                    ),
                    html.Br(),
                    html.Br(),
                    html.H6("Select Area"),
                    dcc.Dropdown(id="area-select_d",
                                 options=[{"label": x, "value": x}
                                          for x in data.area_list],
                                 value="London"),
                    html.Br(),
                    html.P("As suggested by WHO global air quality guidelines,"
                           "the 24-hour mean of PM2.5 below 12 micrograms is good ,"
                           "the 24-hour mean of PM10 below 45 micrograms is good.",
                           style={'text-align': 'center'}),
                    html.Div(id='comment', className="text-info", style={'text-align': 'center'}),
                ]),
                         dbc.Col(html.Div(id='card1')),
                         dbc.Col(html.Div(id='card2')),
                         # dbc.Col(html.Div("one of the three")),
                         ]),

                dbc.Row([
                    # Add the date/area pickers in the first column
                    dbc.Col(children=[
                        html.Br(),
                        html.Br(),

                        # Add the comment area under the pickers
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                    ]),
                ]),
            ]),

            # Third tab display the past data variation
            dcc.Tab(label='Past Data', children=[
                dbc.Row([

                    # Add the date picker
                    dbc.Col(children=[
                        html.Br(),
                        html.Br(),
                        html.H6('Select Period'),
                        dcc.DatePickerRange(
                            id='my-date-picker-range',
                            min_date_allowed=date(2021, 1, 1),
                            max_date_allowed=date(2021, 12, 31),
                            initial_visible_month=date(2021, 1, 1),
                            start_date=date(2021, 1, 1),
                            end_date=date(2021, 12, 31)
                        ),
                    ]),

                    # Add the area/pollutant picker
                    dbc.Col(children=[
                        html.Br(),
                        html.Br(),
                        html.H6("Select Area"),
                        dcc.Dropdown(id="area-select_p",
                                     options=[{"label": x, "value": x}
                                              for x in data.area_list],
                                     value=""),
                    ]),

                    dbc.Col(children=[
                        html.Br(),
                        html.Br(),
                        html.H6("Select Particular Matter"),
                        dcc.Dropdown(id="matter-select_p",
                                     options=[{"label": x, "value": x}
                                              for x in airtype_list],
                                     value="PM2.5"),
                    ]),

                    # Add the scatter chart
                ]),
                dbc.Row(
                    dbc.Col(children=[
                        dcc.Graph(id='recycle-chart', figure=fig_rc)
                    ])
                )
            ]),
        ]),
    ])

    init_callbacks(dash_app)

    return dash_app.server


def init_callbacks(dash_app):
    # Callback function of the density heat map
    @dash_app.callback(
        [Output('output-container-date-picker-single', 'children'),
         Output('mapbox-heatmap', 'figure')],
        [Input('map-date-picker-single', 'date')])
    def update_map(date_slctd):
        container = ''

        dff = df.copy()
        dff = dff[dff["utc"] == date_slctd]
        fig_heatmap = px.density_mapbox(
            data_frame=dff,
            lat='Latitude',
            lon='Longitude',
            z='Total (avg)',
            radius=20,
            range_color=[0, 55],
            center=dict(lat=53.479489, lon=-2.245115),
            zoom=4.5,
            mapbox_style='stamen-watercolor')
        fig_heatmap.update_layout(width=550, height=400,
                                  margin=dict(l=30, r=10, t=10, b=0), )
        return container, fig_heatmap

    # Callback function of the gauge charts
    @dash_app.callback(
        Output('card1', 'children'),
        Output('card2', 'children'),
        Input('my-date-picker-single', 'date'),
        Input("area-select_d", "value"),
    )
    def update_card(date_value_card, area_card):
        if date_value_card and area_card is not None:
            data.process_data_for_single_day(area_card, date_value_card)

            card1 = dbc.Card(className="card border-light mb-3", children=[
                dbc.CardBody([
                    dbc.Row([
                        html.H4(area_card, id="card-name", className="card-title"),
                        html.Br(),

                        # First PM2.5 gauge chart
                        dbc.Col(width=7, children=[
                            html.Br(),
                            daq.Gauge(id='chart1',
                                      color={"gradient": True, "ranges": {
                                          "green": [0, 12], "yellow": [12, 35], "red": [35, 60]}},
                                      value=data.day_data['PM2.5'].mean(),
                                      label='PM2.5',
                                      max=60,
                                      min=0,
                                      ),
                            # Display daily max/min/mean PM2.5
                            html.H6("Maximum PM2.5", className="card-title"),
                            html.H4(data.day_data['PM2.5'].max(),
                                    className="card-text text-dark"),
                            html.H6("Minimum PM2.5", className="card-title"),
                            html.H4(data.day_data['PM2.5'].min(),
                                    className="card-text text-dark"),
                            html.H6("Mean", className="card-title"),
                            html.H4("{:,.0f}".format(
                                data.day_data['PM2.5'].mean()), className="card-text text-dark"),
                        ]),
                    ]),
                ]),
            ])

            # Second PM10 gauge chart
            card2 = dbc.Card(className="card border-light mb-3", children=[
                dbc.CardBody([
                    dbc.Row([
                        html.Br(),

                        dbc.Col(width=7, children=[
                            html.Br(),
                            daq.Gauge(id='chart2',
                                      color={"gradient": True, "ranges": {
                                          "green": [0, 45], "yellow": [45, 60]}},
                                      value=data.day_data['PM10'].mean(),
                                      label='PM10',
                                      max=60,
                                      min=0,
                                      ),
                            # Display daily max/min/mean PM10
                            html.H6("Maximum PM10", className="card-title"),
                            html.H4(data.day_data['PM10'].max(),
                                    className="card-text text-dark"),
                            html.H6("Minimum PM10", className="card-title"),
                            html.H4(data.day_data['PM10'].min(),
                                    className="card-text text-dark"),
                            html.H6("Mean", className="card-title"),
                            html.H4("{:,.0f}".format(
                                data.day_data['PM10'].mean()), className="card-text text-dark"),
                        ]),
                    ]),
                ]),
            ])

        return card1, card2

        # Callback function of the comment for the gauge chart

    @dash_app.callback(
        Output('comment', 'children'),
        Input('my-date-picker-single', 'date'),
        Input("area-select_d", "value"),
    )
    def update_comment(date_value_comment, area_comment):
        if date_value_comment and area_comment is not None:
            data.process_data_for_single_day(area_comment, date_value_comment)

        if data.day_data['PM2.5'].mean() < 12 and data.day_data['PM10'].mean() < 45:
            comment = "Hurrah! The air is so good! Both pollutants amount are in the safe area. Let's take a fresh walk!~"

        elif data.day_data['PM2.5'].mean() < 12 and 45 <= data.day_data['PM10'].mean() < 100:
            comment = "Overall good air quality! The PM2.5 value in the safe area, " \
                      "although the PM10 value is slightly higher, don't worry about it! " \
                      "What about going outside? "

        elif 12 <= data.day_data['PM2.5'].mean() < 35 and data.day_data['PM10'].mean() < 45:
            comment = "Overall good air quality! The PM10 value in the safe area, " \
                      "although the PM2.5 value is slightly higher, don't worry about it! " \
                      "What about going outside? "

        elif 12 <= data.day_data['PM2.5'].mean() < 35 and 45 <= data.day_data['PM10'].mean() < 100:
            comment = "Ummm...moderate PM2.5 and PM10 amounts," \
                      "Seems there is some slight pollution in the air it won't damage your health!"

        elif math.isnan(data.day_data['PM2.5'].mean()) or math.isnan(data.day_data['PM10'].mean()):
            comment = "Sorry, there is no data about this day."

        else:
            comment = "Uh-oh, be careful about the pollution, you can wear a mask to protect yourself!"

        return comment

        # Callback function of the scatter chart

    @dash_app.callback(
        Output("recycle-chart", "figure"),
        Input('my-date-picker-range', 'start_date'),
        Input('my-date-picker-range', 'end_date'),
        Input("area-select_p", "value"),
        Input("matter-select_p", "value"),
    )
    def update_line_chart(start_date, end_date, area_select, matter_select):
        if start_date and area_select and matter_select is not None:
            data.process_data_for_area(
                area_select, start_date, end_date)
        fig_rc = rc.create_chart(area_select, matter_select)
        return fig_rc
