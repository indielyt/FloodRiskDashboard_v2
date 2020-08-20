import dash
from dash.dependencies import Input, State, Output, Event
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    html.P(id='target', children=''),
    dcc.Input(id='input', type='text', value=''),
    dcc.Input(id='input2', type='text', value=''),
    html.Button(id='submit', type='submit', children='ok'),
])


@app.callback(Output('target', 'children'), 
                [], 
                [State('input', 'value'),
                State('input2', 'value')], 
                [Event('submit', 'click')])
def callback(state, state2):
    return f"callback received value: {state}, {state2}"


# @app.callback(Output('target', 'children'),
#                 [Input('input', 'value')],
#                 [State('input', 'value'), 
#                 State('input2', 'value')],
#                 [Event('submit', 'click')])
# def callback(state):
#     return f"callback received value: {state}, {state}"

if __name__ == '__main__':
    app.run_server(debug=True)