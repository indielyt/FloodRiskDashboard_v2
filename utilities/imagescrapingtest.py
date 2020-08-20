
# base64 encoding in dash  --  https://github.com/plotly/dash/issues/71

import dash
import dash_html_components as html
import base64

from urllib.parse import quote
import urllib.request
import urllib, os

from flask import Flask
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import plotly.graph_objs as go


app = dash.Dash(__name__)
server = app.server

SaveLoc = 'assets' #location for images
key = "&key=" + "AIzaSyDbo5FlMFzns5OzeuW1TA7dOikvEuF-eYI" #key

# def GetStreet(Address,SaveLoc):
#     base = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="
#     MyUrl = base + urllib.parse.quote(Address) + key #added url encoding
#     fi = Address + ".jpg"
#     print(fi)
#     urllib.request.urlretrieve(MyUrl, os.path.join(SaveLoc,fi))
#     therequest = urllib.request.urlretrieve(MyUrl)
#     print(therequest)
#     return MyUrl

def GetStreet(Address):
    base = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="
    MyUrl = base + urllib.parse.quote(Address) + key #added url encoding
    return MyUrl


# LatLongTests = ['39.713229,-105.134735']
# LatLongTests = ['39.729898, -105.166717']


# image_URL = GetStreet(LatLongTests[0])

# Styles for click-data 
styles = {
    'pre': {
        'border': 'none',
        'overflowX': 'visible'
    }
}



app.layout = html.Div([
    # html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
    dcc.Dropdown(
            id = 'latlon_dropdown',
            options=[
                {'label': 'work', 'value': '39.713229,-105.134735'},
                {'label': 'dealership', 'value': '39.729898, -105.166717'},
                {'label':'new place', 'value': '39.667931, -105.095744'},
                {'label':'fourth place', 'value': '39.668626, -105.095589'}
            ],
        value='39.713229,-105.134735',
        searchable=False,
        # placeholder = 'choose one'
    ),
        html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe.png",
            style={
                'height': '100px',
                'float': 'right',
                'position': 'relative',
                'bottom': '40px',
                'left': '50px'
            },
        ),
        html.Br(),
        html.Img(id='simple_img', src=" ",
            style={
                'height':'200',
                'width':'200',
            #     'float':'left',
            #     'position': 'relative',
            #     'bottom': '40px',
            #     'left': '50px'
            }
        ),
        html.Br(),
        html.Pre(id='relayout-message', style=styles['pre']),
    ],style=dict(height='200', width="400"),
)


# update simple image
@app.callback(
    Output('simple_img', 'src'),
    [Input('latlon_dropdown', 'value')])
def update_image_src(value):
    # src=GetStreet(value, SaveLoc)
    src=GetStreet(value)
    return src



@app.callback(
    Output('relayout-message', 'children'),
    [Input('latlon_dropdown', 'value')])
def update_image_src(value):
    # src=GetStreet(value, SaveLoc)
    src=GetStreet(value)
    print(value)
    print(src)
    # print(src)
    return value



if __name__ == '__main__':
    app.run_server(debug=True)