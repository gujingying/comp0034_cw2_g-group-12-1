from datetime import date
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
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
df = pd.read_csv("../my_app/dash_app/data/min-max-avg.csv")

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

layout = dbc.Container([
    # html.Div([
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
