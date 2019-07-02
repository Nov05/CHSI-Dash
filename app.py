from flask import Flask
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly_express as px
from data.dataset import Dataset

# starting flask server and connect dash server to flask
server = Flask("CHSI Dash App")
app = dash.Dash("Hello Dash World", server=server)

text_style = dict(color='#444', fontFamily='sans-serif', fontWeight=300)

foo = Dataset('./data/LEADINGCAUSESOFDEATH.csv')
foo.preproc()
#print(foo.lookup('A', 'Wh', 'Comp'))

def choroplot():
	fig = ff.create_choropleth(
    	fips = fips, values = values, scope = ['usa'],
    	binning_endpoints = endpts, colorscale = colorscale,
    	show_state_data = False,
    	show_hover = True, centroid_marker = {
        	'opacity': 0
    	},
    	asp = 2.9,
    	title = 'USA by A_Wh_Comp',
    	legend_title = 'A_Wh_Comp'
		)
	py.iplot(fig, filename = 'choropleth_full_usa')
	return None


plotly_figure = dict(data=[dict(x=[1,2,3], y=[2,4,8])])

app.layout = html.Div([
		html.H2("CHSI Data Visualization", style=text_style),
		html.P("No idea what this is", style=text_style),
		html.Label('Age Group'),
		dcc.Dropdown(
			options=[
            {'label': 'New York City', 'value': 'A'},
            {'label': u'Montréal', 'value': 'B'},
            {'label': 'San Francisco', 'value': 'C'},
			{'label': 'San Francisco', 'value': 'D'},
			{'label': 'San Francisco', 'value': 'E'}
        	],
        	value='MTL'
    	),
		dcc.Input(id='text1', placeholder='box', value=''),
		dcc.Graph(id='plot1', figure=plotly_figure),
		])

@app.callback(Output('plot1', 'figure'), [Input('text1', 'value')])
def text_callback(text_input):
    return {'data': [dict(x=[1,2,3], y=[2,4,8], type=text_input)]}


if __name__ == '__main__':
    app.server.run()
