from flask import Flask
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.plotly as py
import plotly.figure_factory as ff
import plotly_express as px
from data.dataset import Dataset
import numpy as np

# starting flask server and connect dash server to flask
server = Flask("CHSI Dash App")
app = dash.Dash("Hello Dash World", server=server)

text_style = dict(color='#444', fontFamily='sans-serif', fontWeight=300)

cod = Dataset('./data/LEADINGCAUSESOFDEATH.csv')
cod.preproc()
test = cod.lookup('A', 'Wh', 'Comp').dropna()
test = test[test.FIPS.str.startswith("48")]
print(test.head())

def plot_choropleth(df):
	colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
    	"#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
    	"#08519c", "#0b4083", "#08306b"]

	fips = df.FIPS.tolist()
	values = df.A_Wh_Comp.tolist()
	endpts = list(np.linspace(1, 100, len(colorscale)-1))

	fig = ff.create_choropleth(
    	fips = fips, values = values, scope = ['Texas'],
    	binning_endpoints = endpts,
		colorscale = colorscale,
		simplify_county=0,
		simplify_state=0,
    	show_state_data = False,
    	show_hover = True, centroid_marker = {
        	'opacity': 0
    	},
    	asp = 2.9,
    	title = 'USA by A_Wh_Comp',
    	legend_title = 'A_Wh_Comp'
		)
	#py.iplot(fig, filename = 'choropleth_full_usa')
	return fig

choro_plot = plot_choropleth(test)

#plotly_figure = dict(data=[dict(x=[1,2,3], y=[2,4,8])])

app.layout = html.Div([
		html.H2("CHSI Data Visualization", style=text_style),
		html.P("No idea what this is", style=text_style),
		html.Label('Age Group'),
		dcc.Dropdown(
			options=[
            {'label': 'Under 1 Years Old', 'value': 'A'},
            {'label': '1 - 14 Years Old', 'value': 'B'},
            {'label': '15 - 24 Years Old', 'value': 'C'},
			{'label': '25 - 44 Years Old', 'value': 'D'},
			{'label': '44 - 64 Years Old', 'value': 'E'},
			{'label': '65+ Years Old', 'value': 'F'}
        	],
        	value='MTL'
    	),
		html.Label('Ethnic Group'),
		dcc.Dropdown(
			options=[
            {'label': 'White', 'value': 'Wh'},
            {'label': 'Black', 'value': 'Bl'},
            {'label': 'Hispanic', 'value': 'Hi'},
			{'label': 'Other', 'value': 'Ot'},
			],
        	value='MTL'
    	),
		html.Label('Age Group'),
		dcc.Dropdown(
			options=[
            {'label': 'Birth Complication', 'value': 'Comp'},
            {'label': 'Birth Defect', 'value': 'BirthDef'},
			{'label': 'Injury', 'value': 'Injury'},
            {'label': 'Cancer', 'value': 'Cancer'},
			{'label': 'Homocide', 'value': 'Homocide'},
			{'label': 'Heart Diseases', 'value': 'HeartDis'},
			{'label': 'HIV', 'value': 'HIV'}
        	],
        	value='MTL'
    	),
		dcc.Input(id='text1', placeholder='box', value=''),
		dcc.Graph(id='plot1', figure=choro_plot),
		])

#@app.callback(Output('plot1', 'figure'), [Input('text1', 'value')])
#def text_callback(text_input):
#    return {'data': [dict(x=[1,2,3], y=[2,4,8], type=text_input)]}


if __name__ == '__main__':
    app.server.run()
