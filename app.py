# Helpful references

# adding multiple geolayers to mapbox layout  --  https://plot.ly/python/mapbox-county-choropleth/  
# mapbox background styles  --  https://www.mapbox.com/maps
# dash recipes from dash's creator -- https://github.com/plotly/dash-recipes  
# preserving state across callbacks  --  https://community.plot.ly/t/preserving-ui-state-like-zoom-in-dcc-graph/15793  
# using json .dump() and .dumps() for python  --  https://realpython.com/python-json/ 
# css and images in dash apps  --  https://dash.plot.ly/external-resources
# interactive color scale by Plotly  --  https://github.com/plotly/dash-colorscales/blob/master/README.md
# advice on color and visualizations  --  https://matplotlib.org/cmocean/#cmocean-available-elsewhere
# bootstrap  --  https://getbootstrap.com/docs/4.1/layout/grid/
# bootstrap and dash layouts  --  https://dash-bootstrap-components.opensource.asidatascience.com/l/components/layout
# example of bootstrap/dash boilderplate  --  https://github.com/ned2/slapdash
# video tutorial using boilerplate boostrap css  --  https://www.youtube.com/watch?v=f2qUWgq7fb8
# flexbox tutorial for sizing div items  --  https://css-tricks.com/snippets/css/a-guide-to-flexbox/
# ordering mapbox layers in dash app  --  https://community.plot.ly/t/solved-show-points-above-choropleth-layer/6552
# hiding divs with callbacks  --  https://stackoverflow.com/questions/50852743/plotly-figure-hide-and-display

# -*- coding: utf-8 -*-
import json
import pandas as pd
import geopandas as gpd
import requests
import time

import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import dash_colorscales
import plotly.graph_objs as go
import dash_daq as daq

from urllib.parse import quote
import urllib.request
import urllib, os



# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # from dash's tutorials
# external_stylesheets = ['https://bootswatch.com/4/cerulean/bootstrap.css']
# external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css'] # update from 2017
external_stylesheets = ['https://codepen.io/indielyt/pen/PVqKeq.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.config['suppress_callback_exceptions']=True

# Set mapbox public access token
mapbox_access_token = 'pk.eyJ1IjoiaW5kaWVseXQiLCJhIjoiY2pkcXZyMGZpMDB6NzJxbGw4aXdvb2w3bCJ9.sL_EzvrSj83Y0Hi1_6GT6A'

# Set google key
key = "&key=" + "AIzaSyDbo5FlMFzns5OzeuW1TA7dOikvEuF-eYI" #key

# Data sources
repo_url = 'https://raw.githubusercontent.com/indielyt/FloodRiskDashboard_v2'

custom_geometry_points = repo_url + '/master/S_CustomGeometries_centroids.csv'
structure_points = repo_url + '/master/S_Structure_centroids.csv'
geojson_structures = repo_url + '/master/jsons/S_Structure.json'
geojson_census = repo_url + '/master/jsons/S_CustomGeometries.json'
geojson_confidence = repo_url + '/master/jsons/S_Confidence.json'
geojson_100yr = repo_url + '/master/jsons/S_FHAD_100yr.json'
geojson_500yr = repo_url + '/master/jsons/S_FHAD_500yr.json'
narrative1_url = repo_url + '/master/assets/narrative1.txt'
narrative2_url = repo_url + '/master/assets/narrative2.txt'
structures_shp = ('shp/S_Structure.shp')

# Load Data 
df_cg = pd.read_csv(custom_geometry_points)
df_structures = pd.read_csv(structure_points)
narrative1 = (requests.get(narrative1_url)).text
narrative2 = (requests.get(narrative2_url)).text
struct_df = gpd.read_file(structures_shp)

# Define confidence interval steps for slider
steps = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]

# Define bins for structure based risk scoring viz
BINS = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', \
		'60-70', '70-80', '80-90', '90-100']

DEFAULT_COLORSCALE = ['rgb(253, 237, 176)', 'rgb(249, 198, 139)', 'rgb(244, 159, 109)', \
    'rgb(234, 120, 88)', 'rgb(218, 83, 82)', 'rgb(191, 54, 91)', 'rgb(158, 35, 98)', \
    'rgb(120, 26, 97)', 'rgb(83, 22, 84)', 'rgb(47, 15, 61)']

DEFAULT_COLORSCALE_2 = ['rgb(253, 253, 204)', 'rgb(195, 232, 175)', 'rgb(135, 212, 163)', \
    'rgb(92, 185, 163)', 'rgb(77, 156, 160)', 'rgb(67, 128, 154)', 'rgb(61, 99, 148)', \
    'rgb(65, 69, 130)', 'rgb(57, 46, 85)', 'rgb(39, 26, 44)']

# mapboxstyle = 'mapbox://styles/mapbox/satellite-streets-v9' #satellite streets
# mapboxstyle = 'mapbox://styles/mapbox/dark-v9' # dark
mapboxstyle = 'mapbox://styles/mapbox/light-v9' # light
# mapboxstyle = 'mapbox://styles/mapbox/outdoors-v9' # outdoors
# mapboxstyle = 'https://api.mapbox.com/styles/v1/indielyt/cjreghq012thv2ssdb6mbfguu.html?fresh=true&title=true&access_token=pk.eyJ1IjoiaW5kaWVseXQiLCJhIjoiY2pkcXZyMGZpMDB6NzJxbGw4aXdvb2w3bCJ9.sL_EzvrSj83Y0Hi1_6GT6A#10.0/42.362400/-71.020000/0'

# Define symbology for json layers
geo_index = [
    # 'S_Structure',         # structures index
    # 'S_CustomGeometries',  # census blocks index
    'S_Confidence',        # confidence index
    'S_100yr',             # 100yr index
    'S_500yr']             # 500yr index
sourcetype = [
    # 'geojson', # structures sourcetype
    # 'geojson', # census sourcetype
    'geojson', # confidence sourcetype
    'geojson', # 100yr sourcetype
    'geojson'] # 500yr sourcetype
color = [
    # '#D3D3D3', # structures color
    # '#484848', # census blocks color
    '#80b3ff', # confidence color
    '#013fa3', # 100yr color
    '#99ccff'] # 500yr color
opacity = [
    # 0.2,    # structures opacity
    # 0.4,  # census blocks opacity
    0,  # confidence opacity
    0.5,  # 100yr opacity
    0.7]  # 500yr opacity
symbology_type = [
    # 'fill',  # structures symbology
    # 'line',  # census block symbology
    'line',  # confidence symbology
    'fill',  # 100yr symbology
    'fill']  # 500yr symbology
json_file = [
    # 'S_Structure.json',         # structures json
    # 'S_CustomGeometries.json',  # census blocks json
    'S_Confidence.json',        # confidence json
    'S_FHAD_100yr.json',        # 100yr json
    'S_FHAD_500yr.json']        # 500yr json
# below_symbology = [
# before_layer = [    
#     'S_100yr',          # structures json
#     # 'S_500yr',        # census blocks json
#     'S_Structure',      # confidence json
#     'S_500yr',          # 100yr json
#     'water']            # 500yr json
before_layer = [    
    # 'S_Confidence',          # structures json
    # 'S_500yr',        # census blocks json
    'S_Structure',      # confidence json
    'S_100yr',          # 100yr json
    'water']            # 500yr json

# df_geolayer_info = pd.DataFrame(list(zip(sourcetype,color,opacity,symbology_type,json_file,below_symbology)),
#     columns=['sourcetype', 'color', 'opacity', 'symbology_type', 'json_file', 'below_symbology'])
df_geolayer_info = pd.DataFrame(list(zip(sourcetype,color,opacity,symbology_type,json_file,before_layer)),
    columns=['sourcetype', 'color', 'opacity', 'symbology_type', 'json_file', 'before_layer'])
df_geolayer_info.index = geo_index

# Styles for click-data 
styles = {
    'pre': {
        'border': 'none',
        'overflowX': 'visible'
    }
}

# Options for dropdown menu of structure based risk type
all_options=[
    {'label': 'Total Risk Score (R_SCORE)', 'value': 'R_SCORE'},
    {'label': 'Flood Risk Score (FR_TOT)', 'value': 'FR_TOT'},
    {'label': '100-Year Exceedance Probability (AEP_TOT)', 'value': 'AEP_TOT'},
    {'label': 'Flood Damage Potential (FDP_TOT)', 'value': 'FDP_TOT'},
    {'label': 'User Defined Risk Weighting', 'value': 'USER'}
]

no_options=[
    {'label': 'Total Risk Score (R_SCORE)', 'value': 'R_SCORE', 'disabled': True},
    {'label': 'Flood Risk Score (FR_TOT)', 'value': 'FR_TOT', 'disabled': True},
    {'label': '100-Year Exceedance Probability (AEP_TOT)', 'value': 'AEP_TOT', 'disabled': True},
    {'label': 'Flood Damage Potential (FDP_TOT)', 'value': 'FDP_TOT', 'disabled': True},
    {'label': 'User Defined Risk Weighting', 'value': 'USER', 'disabled': True}
]

customdatalist = [df_structures['R_SCORE'], df_structures['FR_TOT'], df_structures['AEP_TOT'], df_structures['FDP_TOT']]








'''
~~~~~~~~~~~~~~~~
~~ APP LAYOUT ~~
~~~~~~~~~~~~~~~~
'''







app.layout = html.Div(children=[

    html.Div([
        html.H4(children='Interactive Flood Hazard and Risk Viewer',
            className='nine columns'),

        html.A([
            html.Img(src='/assets/logo_white.png',
                className='three columns',
                style={
                    # 'height': '90%',
                    'width': '120px',
                    'float': 'right',
                    'position': 'relative',
                    'margin-top': '10px',
                    'margin-right': '10px'
                },
            ),
        ], href='http://www.mbakerintl.com/')
    ], className="header",
    style = {
        'border-radius': '3px'
    }
    ),

    # html.Div([
    #     html.P(
    #         narrative1
    #     )
    # ], className="row", style={
    # 'background-color':'white', 
    # 'padding':'5px', 
    # 'border-radius': '3px',
    # 'margin-top':'5px',
    # }),

    html.Div([
        dcc.Graph(
            id='risk-map',
            figure=dict(
                data = dict(
                    lat=df_structures['lat'],
                    lon=df_structures['lon'],
                    # hoverinfo = 'text', # for adding hover info to buildings
                    hoverinfo = 'none', # use this for testing, turns hover labels off
                    customdata=customdatalist,
                    text=df_structures['R_SCORE'],
                    type='scattermapbox',
                    marker=dict(
                        size=1
                    ),
                    opacity = 0,
                ),
                layout = dict(
                    # height = 600,
                    # height = 1500,
                    mapbox = dict(
                        layers = [],
                        accesstoken = mapbox_access_token,
                        style = mapboxstyle,
                        center=dict(
                            lat=39.7093,
                            lon=-105.05555           
                        ),
                        pitch=0,
                        zoom=14
                    )
                )
            ),
            style = {
                'height': '500',
                # 'border-radius' : '3px'
            }
        )
    ], className="row",
    style = { 
        'margin-top' : '5px',
        'border-radius' : '3px'
    }), 
    # html.Br(),

    # Flood hazard risk controls
    html.Div([
        html.Div([
            html.H5(children='Area Based Flood Hazards'), 
            html.Hr(),           
            dcc.Checklist(
                id = 'risk-checklist',
                options=[
                    # {'label': 'Display Structure Based Flood Risk', 'value': 'S_Structure'},
                    {'label': 'Display Probabilistic Floodplain Modeling', 'value': 'S_Confidence'},
                    # {'label': 'Display Sociovulnerability to Flood Hazards', 'value': 'S_CustomGeometries'},
                    {'label': 'Display 100yr Floodplain (FHAD in progress)', 'value': 'S_100yr'},
                    {'label': 'Display 500yr Floodplain (FHAD in progress)', 'value': 'S_500yr'}
                ],
                values=['S_Confidence'],
                # values=['S_100yr'],
                labelStyle={'display': 'block'}
            ),

            html.Br(),
            # html.P(id='slider-message'),

            html.Div(
                id='slider-container',
                children=[
                html.P(id='slider-message'),
                dcc.Slider(
                    id='confidence-slider',
                    min=min(steps),
                    max=max(steps),
                    step = 10,
                    value=50,
                    marks={step: {'label': str(step)} for step in steps},
                    updatemode = 'drag',
                )
            ], style={
                'width' : '90%',
                'padding': '10px'}), 

            html.Br(),
            html.Hr(),
            html.H5(children="Map Controls"),

            # Structures colormap
            html.Div([
                html.Div([
                    html.P(children='Structures Color Map',
                        style={
                            'font-size': '12px'}
                        )
                ], className='five columns', style={
                    'margin-top': '10px',
                }),
                html.Div([
                    dash_colorscales.DashColorscales(
                        id='colorscale-picker',
                        colorscale=DEFAULT_COLORSCALE,
                        nSwatches=10,
                        fixSwatches=True,
                    ),
                ]),
            ], className="row"),

            # Probablistic hexagon colormap
            html.Div([
                html.Div([
                    html.P(children='Probabilistic Floodplain Color Map',
                        style={
                            'font-size': '12px'}
                        )
                ], className='five columns', style={
                    'margin-top': '10px',
                }),
                html.Div([
                    dash_colorscales.DashColorscales(
                        id='colorscale-picker2',
                        colorscale=DEFAULT_COLORSCALE_2,
                        nSwatches=10,
                        fixSwatches=True,
                    ),
                ]),
            ], className="row"),

            html.Hr(),

            html.Div([
                html.P(
                    narrative1
                )
            ], className="row", style={
            'background-color':'white', 
            'padding':'5px', 
            'border-radius': '3px',
            'margin-top':'5px',
            }),


        ], className='five columns', 
        style={
            'background-color':'white',
            'margin-right': '0px', 
            # 'flex':1,
            'flex-basis': '40%',
            # 'display':'inline-block',
            # 'width':'100%',
            # 'position':'relative',
            'padding':'10px', 
            'border-radius': '3px',
            # 'margin-top':'25px'
        }
        ),

        # Structure based risk controls
        html.Div([
            html.H5(children='Structure Based Flood Risk'),
            html.Hr(), 
            # daq.BooleanSwitch(
            #     id='structures-switch',
            #     # label='Structure Based Flood Risk',
            #     # labelPosition = 'bottom',
            #     on=True
            # ),
            # html.P()

            dcc.Checklist(
                id = 'risk-checklist2',
                options=[
                    {'label': 'Display Structure Based Flood Risk', 'value': 'S_Structure'},
                ],
                values=['S_Structure'],
            ),

            html.Br(),

            html.Div([
                dcc.Dropdown(
                    id = 'structurebasedrisk_dropdown',
                    options = all_options,
                    value = "R_SCORE",
                    searchable = False,
                    # placeholder = 'choose one'
                ),
            ], style={'width' : '100%'}), 

            html.Br(),

            # html.Hr(),

            html.Div(
                id='userweights-container',
                children=[
                html.Hr(),
                html.Div([
                    html.H6(children='FR_TOT'),   
                    dcc.Input(
                        id = 'FRTOT-numericinput',
                        type = 'number',
                        size = '10',
                        placeholder = '0',
                        min = 0,
                        max = 100,
                        step = 5
                    ),
                ], style = {'display':'inline-block', 'flex-basis':'15%'}),
                html.Div([
                    html.H6(children='AEP_TOT'),  
                    dcc.Input(
                        id = 'AEPTOT-numericinput',
                        type = 'number',
                        size = '10',
                        placeholder = '0',
                        min = 0,
                        max = 100,
                        step = 5
                    ),
                ], style = {'display':'inline-block', 'flex-basis':'15%'}),
                html.Div([
                    html.H6(children='FDP_TOT'),  
                    dcc.Input(
                        id = 'FDPTOT-numericinput',
                        type = 'number',
                        size = '10',
                        placeholder = '0',
                        min = 0,
                        max = 100,
                        step = 5
                    ),
                ], style = {'display':'inline-block', 'flex-basis':'15%'}),
                html.Div([
                    html.H6(children='', id='user-message'), 
                    html.Button('Submit User Defined Weights', id='button')
                ], style={
                    'display':'inline-block', 
                    'flex-basis':'55%',
                    # 'margin-top':'0px',
                    'padding-left':'5%'}
                )
            ], style={'display':'flex', 'margin-bottom':'15px'}),

            html.Hr(), 

  
            # html.Pre(id='relayout-message', style=styles['pre']),

            # selected structure risk components
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='stackedbar',
                        config={'displayModeBar': False
                        }
                    ),
                ], className='two columns',
                style = {
                    'flex':1,
                }),
                html.Div([
                    html.Img(
                        id='image',
                        src=' ', 
                        height = '100px',
                        width = '100px'
                    ),
                ], className='two columns',
                style = {
                    # 'height': '100px',
                    # 'width': '100px',
                    'margin-top': '32px',
                    'display': 'flex',
                    # 'justify-content': 'right',
                    # 'flex':1,
                }),
                html.Div([
                    html.Pre(id='click-data', style=styles['pre'])
                ], className='four columns',
                style={
                    # 'float': 'right', 
                    'text-align': 'left',
                    'vertical-align':'bottom',
                    'position':'relative',
                    'margin-top': '40px',
                    'flex':1,
                })
            ], className='row',
            style = {
                'display': 'flex'
            }),

            # structures narrative
            html.Div([
                html.P(
                    narrative2
                )
            ], className="row", style={
            'background-color':'white', 
            'padding':'5px', 
            'border-radius': '3px',
            'margin-top':'5px',
            }),
        ], className='seven columns',
        style={
            'background-color':'white', 
            # 'display':'inline-block',
            'margin-left': '5px',
            # 'margin-right': '0px',
            # 'width':'100%',
            'padding':'10px', 
            'border-radius': '3px',
            # 'flex':1,
            'flex-basis': '60%',
            # 'width': '60.27%',
            # 'margin-top':'5px'
        }
        ),
    ], className='row',
    style={
        'background-color':'#d8d8d8', 
        # 'padding':'15px', 
        'margin-top':'5px',
        'margin-bottom':'5px',
        'display':'flex',
        'width':'100%'
    }
    ),

    # debugging text, comment out after testing
    # html.Pre(id='relayout-message', style=styles['pre']),
    # html.Img(src=' ', id='image'),
    
    # html.Div([
    #     dcc.Graph(
    #         id='risk-map',
    #         figure=dict(
    #             data = dict(
    #                 lat=df_structures['lat'],
    #                 lon=df_structures['lon'],
    #                 # hoverinfo = 'text', # for adding hover info to buildings
    #                 hoverinfo = 'none', # use this for testing, turns hover labels off
    #                 customdata=customdatalist,
    #                 text=df_structures['R_SCORE'],
    #                 type='scattermapbox',
    #                 marker=dict(
    #                     size=1
    #                 ),
    #                 opacity = 0,
    #             ),
    #             layout = dict(
    #                 # height = 600,
    #                 # height = 1500,
    #                 mapbox = dict(
    #                     layers = [],
    #                     accesstoken = mapbox_access_token,
    #                     style = mapboxstyle,
    #                     center=dict(
    #                         lat=39.7093,
    #                         lon=-105.05555           
    #                     ),
    #                     pitch=0,
    #                     zoom=12
    #                 )
    #             )
    #         ),
    #         style = {
    #             'height': '600',
    #         }
    #     )
    # ], className="row"),    
], className='ten columns offset-by-one')









'''
~~~~~~~~~~~~~~~~
~~ APP CALLBACKS ~~
~~~~~~~~~~~~~~~~
'''









# Update user defined weights div (show/hide)
@app.callback(
    Output('userweights-container', 'style'),
    [Input('structurebasedrisk_dropdown', 'value')])
def hide_slider(value):
    if value=='USER':
        return {'display': 'flex', 'margin-bottom':'15px'} 
    else:
        return {'display': 'none'} 



# User defined weights message
@app.callback(
    Output('user-message', 'children'),
    [Input('FRTOT-numericinput', 'value'),
    Input('AEPTOT-numericinput', 'value'),
    Input('FDPTOT-numericinput', 'value'),
    Input('structurebasedrisk_dropdown', 'value')])
def sum_user_weights(FRTOTval, AEPTOTval, FDPTOTval, dropdownvalue):
    if dropdownvalue == 'USER':
        if FRTOTval==None:# or AEPTOTval==None or FDPTOTval==None:
            message = f"Provide three weights"
        else:
            user_sum = FRTOTval + AEPTOTval + FDPTOTval
            if user_sum != 100:
                message = f"Sum = {user_sum}%. Must equal 100 %"
            else:
                message = f"Click submit to update map."    
    else: 
        message = " "
        
    return message



# streetview image text 
@app.callback(
    Output('relayout-message', 'children'),
    [Input('risk-map', 'clickData')])
def display_selected_data(clickData):
    if clickData==None:
        pass
        # return str((39,-105))
        # return json.dumps(relayoutData, indent=2)
    else: 
        # pass
        trace_lat = round(clickData['points'][0]['lat'],6)
        trace_lon = round(clickData['points'][0]['lon'],6)
        latlon = str(trace_lat) + ', ' + str(trace_lon)
        return latlon

# streetview image
@app.callback(
    Output('image','src'),
    [Input('risk-map', 'clickData')])
def update_image(clickData):
    if clickData==None:  
        src = 'assets/floodriskplaceholder.png'  
    else:
        saveLoc='assets'
        def GetStreet(Address):
            base = 'https://maps.googleapis.com/maps/api/streetview?size=1200x800&location='
            img_url = base + urllib.parse.quote(Address) + key #added url encoding
            img_name = 'gsvImg_' + Address + ".jpg"
            path_name = os.path.join(saveLoc,img_name)
            urllib.request.urlretrieve(img_url, path_name)
            # return img_url
            return path_name

        trace_lat = round(clickData['points'][0]['lat'], 6)
        trace_lon = round(clickData['points'][0]['lon'], 6)
        latlon = str(trace_lat) + ', ' + str(trace_lon)

        src=GetStreet(latlon)

        print(latlon)
        print(src)
    
    return src





# Structure based risk dropdown message
# @app.callback(
#     Output('dropdown-message', 'children'),
#     [Input('risk-checklist', 'values')
#     ])
# def update_dropdown_message(values):
#     if 'S_Structure' in values:
#         return 'Visualize scoring of structure based flood risk'
#     else:
#         return 'Turn on Structure Based Flood Risk to view on map'


# Update dropdown menu for structure based risk
@app.callback(
    Output('structurebasedrisk_dropdown', 'options'),
    # Output('structurebasedrisk_dropdown', 'disabled'),
    # Output('structurebasedrisk_dropdown', 'placeholder'),
    [Input('risk-checklist2', 'values')])
def update_risk_dropdown(values):
    if 'S_Structure' not in values:
        return no_options
        # return f"disabled"
    else:
        return all_options
        # return False
        # return f"enabled"





# Update probabilistic slider div (show/hide)
@app.callback(
    Output('slider-container', 'style'),
    [Input('risk-checklist', 'values')])
def hide_slider(values):
    if 'S_Confidence' in values:
        return {'display': 'block', 'width' : '90%', 'padding': '10px'} 
    else:
        return {'display': 'none'} 





# Update slider message - which  confidence level is displayed
@app.callback(
    Output('slider-message', 'children'),
    [Input('confidence-slider', 'value'),
    Input('risk-checklist', 'values')])
def update_slider_message(value, values):
    if 'S_Confidence' in values:
        return 'Displaying the {} percent confidence boundary for the 100-year floodplain boundary'.format(value)
    else:
        return """Turn on Probabilistic Floodplain Modeling to view on map"""


# Update Structure Risk Click Data
@app.callback(
    Output('click-data', 'children'),
    [Input('risk-map', 'clickData')])
def display_click_data(clickData):
    if clickData==None:
        click_message = f"Total Risk Score: " + '\n' + \
            f"Flood Risk: " + '\n' +  \
            f"100-Year Exceedence Probability: " + '\n' + \
            f"Flood Damage Potential: "
        return click_message
    else:
        structFID = clickData['points'][0]['pointNumber'] # zero based index number assigned by app
        # pointnumber = clickData['points'][0]['pointNumber'] # zero based index number assigned by app
        # structFID = pointnumber+1  # 1 based index FID number from spatial data
        totalrisk = df_structures.loc[df_structures.FID == structFID, 'R_SCORE'].values[0]
        floodrisk = df_structures.loc[df_structures.FID == structFID, 'FR_TOT'].values[0]
        annualExceedence = df_structures.loc[df_structures.FID == structFID, 'AEP_TOT'].values[0]
        floodDamage = df_structures.loc[df_structures.FID == structFID, 'FDP_TOT'].values[0]
        click_message = f"Total Risk Score: {totalrisk}" + '\n' + \
            f"Flood Risk: {floodrisk}" + '\n' +  \
            f"Annual Exceedence Probability: {annualExceedence}" + '\n' + \
            f"Flood Damage Potential: {floodDamage}"
        return click_message
        # return json.dumps(clickData, indent=2)


# Update bar graph
@app.callback(
    Output('stackedbar', 'figure'),
    [Input('risk-map', 'clickData'),
    Input('risk-map', 'figure'),
    Input('colorscale-picker', 'colorscale')])
def update_bar_chart(clickData, riskmapfigure, colorscale):
    # cm = dict(zip(BINS, colorscale))

    if clickData==None:
        trace1 = go.Bar(x=['Total Risk'], y=[100],name='Total Risk',marker=dict(color=colorscale[9]))
        trace2 = go.Bar(x=['Risk Components'], y=[20],name='FR_TOT',marker=dict(color=colorscale[3]))
        trace3 = go.Bar(x=['Risk Components'], y=[40],name='AEP_TOT',marker=dict(color=colorscale[5]))
        trace4 = go.Bar(x=['Risk Components'], y=[40],name='FDP_TOT',marker=dict(color=colorscale[7]))

        figure=dict(
            data=[trace1, trace2, trace3, trace4],
            layout=go.Layout(
                barmode='stack',
                autosize=False,
                width=250,
                height=150,
                showlegend=False,
                title="Scoring Method",
                titlefont=dict(size=12),
                margin=go.layout.Margin(
                    l=30,
                    r=30,
                    b=30,
                    t=30,
                    pad=0
                ),
            )
        )
    else:
        structFID = clickData['points'][0]['pointNumber'] # zero based index number assigned by app
        # pointnumber = clickData['points'][0]['pointNumber'] # zero based index number assigned by app
        trace_lat = clickData['points'][0]['lat']
        trace_lon = clickData['points'][0]['lon']
        # structFID = pointnumber+1  # 1 based index FID number from spatial data
        totalrisk = df_structures.loc[df_structures.FID == structFID, 'R_SCORE'].values[0]
        floodrisk = df_structures.loc[df_structures.FID == structFID, 'FR_TOT'].values[0]
        annualExceedence = df_structures.loc[df_structures.FID == structFID, 'AEP_TOT'].values[0]
        floodDamage = df_structures.loc[df_structures.FID == structFID, 'FDP_TOT'].values[0]

        newtrace1 = go.Bar(x=['Total Risk'], y=[totalrisk], name='R_SCORE', marker=dict(color=colorscale[9]))
        newtrace2 = go.Bar(x=['Risk Components'], y=[0.2*floodrisk], name='FR_TOT', marker=dict(color=colorscale[3]))
        newtrace3 = go.Bar(x=['Risk Components'], y=[0.4*annualExceedence], name='AEP_TOT', marker=dict(color=colorscale[5]))
        newtrace4 = go.Bar(x=['Risk Components'], y=[0.4*floodDamage], name='FDP_TOT', marker=dict(color=colorscale[7]))

        figure=dict(
            data=[newtrace1, newtrace2, newtrace3, newtrace4],
            layout=go.Layout(
                barmode='stack',
                autosize=False,
                width=250,
                height=150,
                showlegend=False,
                # title=f"lat:{trace_lat} lon: {trace_lon}",
                title="Selected Structure Risk Scoring",
                titlefont=dict(size=12),
                yaxis=dict(range=[0, 100]),
                margin=go.layout.Margin(
                    l=30,
                    r=30,
                    b=30,
                    t=30,
                    pad=0
                ),
            )
        )
        # figure = dict(data=data,layout=layout)
    return figure



# Update map figure  
@app.callback(
		Output('risk-map', 'figure'),
		[Input('risk-checklist', 'values'),
        Input('risk-checklist2', 'values'),
        Input('structurebasedrisk_dropdown','value'),
        Input('confidence-slider', 'value'),
        Input('colorscale-picker', 'colorscale'),
        Input('colorscale-picker2', 'colorscale')],
		[State('risk-map', 'relayoutData')])
# def display_map(values, dropdownvalue, value, colorscale, figure):
def display_map(values, checklist2values, dropdownvalue, value, colorscale, colorscale2, relayoutData):
    cm = dict(zip(BINS, colorscale)) # structures color dictionary
    cm2 = dict(zip(BINS, colorscale2)) # probabilistic floodplain color dictionary
    struct_dff = struct_df.copy()

    # Control of zoom and center for mapbox map
    try: # hold existing map extent constant during user interaction
        latInitial = (relayoutData['mapbox.center']['lat'])
        lonInitial = (relayoutData['mapbox.center']['lon'])
        zoom = (relayoutData['mapbox.zoom'])
    except: # incase of using checklist before changing map extent
        # latInitial=39.715
        # lonInitial=-105.065
        # zoom=12
        latInitial=39.718741
        lonInitial=-105.038733
        zoom=16
    
    # data = dict(
    #     # lat=df_structures['lat'],
    #     # lon=df_structures['lon'],
    #     lat=struct_dff['lat'],
    #     lon=struct_dff['lon'],
    #     customdata=customdatalist,
    #     hoverinfo = 'text', # for adding hover info to buildings
    #     # hoverinfo = 'none', # use this for testing, turns hover labels off
    #     # text=df_structures[dropdownvalue],
    #     text=struct_dff[[dropdownvalue],
    #     type='scattermapbox',
    #     marker=dict(
    #         size=10
    #     ),
    #     opacity = 0,
    # ),

    # define legend, title, and location
    title_dict = {'R_SCORE': 'Total Risk Score (R_SCORE)', 
        'FR_TOT': 'Flood Risk (FR_TOT)',
        'AEP_TOT': '100-Year Exceedence Probability (AEP_TOT)', 
        'FDP_TOT': 'Flood Damage Potential (FDP_TOT)',
        'USER': 'User Defined Weighting'}
    # legendtitle = '<b>' + title_dict[dropdownvalue] + '</b>'
    legendtitle = '<b>' + 'Structure Based Flood Risk' + '\n' + 'other' + '</b>'
    annotations = [dict(
        showarrow = False,
        align = 'left',
        text = legendtitle,
        x = 0.02, # legend title location (% from left)
        y = 0.98, # legend title location (% from bottom)
	)]

    for i, bin in enumerate(BINS):
        color = cm[bin]
        annotations.append(
			dict(
				arrowcolor = color,
				text = bin,
				x = 0.1,
				y = 0.9-(i/20),
				ax = -50,
				ay = 0,
				arrowwidth = 5,
				arrowhead = 0,
				# bgcolor = '#EFEFEE'
                bgcolor = '#ffffff'
			)
		)

    layout = dict(
        margin = dict(l = 0, r = 0, t = 0, b = 0),
        # plot_bgcolor="#191A1A",
        paper_bgcolor="#020202",
        mapbox = dict(
            layers = [],
            accesstoken = mapbox_access_token,
            style = mapboxstyle,
            center=dict(lat=latInitial, lon=lonInitial),
            zoom=zoom,
        ),
        annotations =  annotations,
    )

    # Define base urls for use in creating geolayers
    # base_layers = ['S_Structure', 'S_Confidence', 'S_CustomGeometries', 'S_100yr', 'S_500yr'] #v1
    base_layers = ['S_Confidence', 'S_100yr', 'S_500yr'] #v2
    # base_layers = ['S_100yr', 'S_500yr'] #v2

    base_url = repo_url + '/master/jsons/' #v2
    base_risk_url = repo_url + '/master/' #v2
    
    # Add flood hazard risk layers to map if selected
    for i in values:
        # Add base layers to layout if in checklist
        if i in base_layers:
            geo_layer = dict(
                sourcetype=df_geolayer_info['sourcetype'].loc[i],
                source = base_url + df_geolayer_info['json_file'].loc[i],
                type = df_geolayer_info['symbology_type'].loc[i],
                color = df_geolayer_info['color'].loc[i],
                opacity = df_geolayer_info['opacity'].loc[i]
            )
            layout['mapbox']['layers'].append(geo_layer)
            # print(layout)

            # Add selected confidence contour
            if i=='S_Confidence':
                # # Add selected risk contour from slider input
                # base_contourfilename = 'S_contour'
                # geo_layer = dict(
                #     sourcetype='geojson',
                #     source = base_url + base_contourfilename + str(value) +  '.json',
                #     type = 'line',
                #     color = '#000066',
                #     opacity = 0.5
                # )
                # layout['mapbox']['layers'].append(geo_layer)

            # Add risk hexagons
                for bin in BINS:
                    geo_layer = dict(
                        sourcetype = 'geojson',
                        source = base_risk_url + 'CONF' + '/' + bin +  '.geojson',
                        type ='fill',
                        fill = {'outlinecolor': cm2[bin]},
                        color = cm2[bin],
                        opacity = 0.5
                    )
                    layout['mapbox']['layers'].append(geo_layer)

                    geo_layer = dict(
                        sourcetype = 'geojson',
                        source = base_risk_url + 'CONF' + '/' + bin +  '.geojson',
                        type ='line',
                        # line = cm2[bin],
                        # color = cm2[bin],
                        color = 'white',
                        opacity = 0.15,
                    )
                    layout['mapbox']['layers'].append(geo_layer)
            
                # Add selected risk contour from slider input
                base_contourfilename = 'S_contour'
                geo_layer = dict(
                    sourcetype='geojson',
                    source = base_url + base_contourfilename + str(value) +  '.json',
                    type = 'line',
                    color = '#000066',
                    opacity = 0.5
                )
                layout['mapbox']['layers'].append(geo_layer)

                # # Add selected risk contour from slider input
                # base_contourfilename = 'S_contour'
                # geo_layer = dict(
                #     sourcetype='geojson',
                #     source = base_url + base_contourfilename + str(value) +  '.json',
                #     # beforeLayer = df_geolayer_info['before_layer'].loc[i],
                #     type = 'line',
                #     color = '#000066',
                #     opacity = 0.5
                # )
                # layout['mapbox']['layers'].append(geo_layer)

    # Add structure based risk to map if selected     
    for i in checklist2values:     
        # Add risk scoring type if selected in checkbox   
        if i=='S_Structure':
            # Calculate geolayer if user defined weighting is selected
            if dropdownvalue=='USER':
                pass

                # need to create 'USER' field in struct_dff and calc to that field (for annotations).


                # struct_dff = struct_df.copy()
                # struct_dff['USER'] = struct_df['R_SCORE']
                # for bin in BINS:
                # # Calculate geolayer if user defined weighting is selected
                #     low = int(bin.split('-')[0])
                #     high = int(bin.split('-')[1]) 

                #     # query the structure dataframe for values in each bin range by user's dropdown value
                #     bin_data = struct_dff[struct_dff[dropdownvalue].between(low,high,inclusive=False)]
                #     bin_json = json.loads(bin_data.to_json())

                #     geo_layer = dict(
                #             sourcetype = 'geojson',
                #             source = bin_json,
                #             type ='fill',
                #             # beforeLayer = df_geolayer_info['before_layer'].loc[i],
                #             # paint={
                #             #     # 'fill-color' : cm[bin],
                #             #     'fill-outline-color' : cm[bin],
                #             #     'fill-opacity' : 0.95
                #             # },
                #             color = cm[bin],
                #             opacity = 1
                #     )
                #     layout['mapbox']['layers'].append(geo_layer)

            # Serve prebuilt geolayer if not user defined weighting
            else:
                for bin in BINS:
                    geo_layer = dict(
                            sourcetype = 'geojson',
                            source = base_risk_url + dropdownvalue + '/' + bin +  '.geojson',
                            type ='fill',
                            # beforeLayer = df_geolayer_info['before_layer'].loc[i],
                            # paint=dict(
                            #     fill-color = cm[bin],
                            #     fill-outline-color = cm[bin],
                            #     fill-opacity = 0.95
                            # )
                            color = cm[bin],
                            opacity = 1
                    )

                    layout['mapbox']['layers'].append(geo_layer)

    data = dict(
        # lat=df_structures['lat'],
        # lon=df_structures['lon'],
        lat=struct_dff['lat'],
        lon=struct_dff['lon'],
        customdata=customdatalist,
        hoverinfo = 'text', # for adding hover info to buildings
        # hoverinfo = 'none', # use this for testing, turns hover labels off
        text=struct_dff[dropdownvalue],
        type='scattermapbox',
        marker=dict(
            size=10
        ),
        opacity = 0,
    ),

    figure = dict(data=data,layout=layout)
    # t5 = time.time()
    # print('prep map data Time: {:.2f} seconds'.format(round(t6 - t7, 2)))
    # print('render all geolayers Time: {:.2f} seconds'.format(round(t5 - t6, 2)))
    # print('TOTAL map callback Time: {:.2f} seconds'.format(round(t5 - t7, 2)))
    return figure



if __name__ == '__main__':
    app.run_server(debug=True)