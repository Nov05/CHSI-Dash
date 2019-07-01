from flask import Flask
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


# starting flask server
server = Flask("CHSI Dash App")

# connecting dash to flask server
app = dash.Dash("Hello Dash World", server=server)

text_style = dict(color='#444', fontFamily='sans-serif', fontWeight=300)
plotly_figure = dict(data=[dict(x=[1,2,3], y=[2,4,8])])

app.layout = html.Div([
		html.H2("DASH APP", style=text_style),
		html.P("ASDFSDFSDJFKSL", style=text_style),
		dcc.Input(id='text1', placeholder='box', value=''),
		dcc.Graph(id='plot1', figure=plotly_figure),
		])

@app.callback(Output('plot1', 'figure'), [Input('text1', 'value')])
def text_callback(text_input):
    return {'data': [dict(x=[1,2,3], y=[2,4,8], type=text_input)]}


if __name__ == '__main__':
    app.server.run()
