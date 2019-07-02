import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.figure_factory as ff
import numpy as np
# importing Dataset wrapper class
from data.dataset import Dataset

# Set style basics
text_style = dict(color='#444', fontFamily='sans-serif', fontWeight=300)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9",
			  "#9ecae1", "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be",
			  "#2171b5", "#1361a9",	"#08519c", "#0b4083", "#08306b"]

# starting plotly Dash server
app = dash.Dash("CHSI Visualization")

# preload the dataset and preprocess it.
cod = Dataset('./data/LEADINGCAUSESOFDEATH.csv')
cod.preproc()

def plot_choropleth(df):
	"""
	This function generates and returns a choropleth from the input dataset.

	TODO: Add error checking.

	Parameters
	----------
	df: a pandas dataframe with two columns; first column is `FIPS` for FIPS
	    geoencoding. Second column is the features to be plotted, base on a
		combination of age, ethnicity, and cause of death.
	"""
	fips = df.FIPS.tolist()
	values = df.iloc[:,1].tolist()
	endpts = list(np.linspace(1, 100, len(colorscale)-1))

	fig = ff.create_choropleth(
    	fips = fips, values = values, scope = ['Texas'],
    	binning_endpoints = endpts, colorscale = colorscale,
		simplify_county=0, simplify_state=0, show_state_data = False,
    	show_hover = True, centroid_marker = {'opacity': 0},
    	asp = 2.9,
    	title = 'Everything Is Bigger In Texas',
    	legend_title = '% Death'
		)
	return fig

#choro_plot = plot_choropleth(test)
app.layout = html.Div(children=[
		html.H1("A Story of Life and Death", style=text_style),
		html.P("CHSI Cause of Death Visualization, 1996-2003", style=text_style),
		html.Div(children=[
			html.Label('Age Group', style=text_style),
			dcc.Dropdown(
				id='ages',
				options=[
	            {'label': 'Under 1 Years Old', 'value': 'A'},
	            {'label': '1 - 14 Years Old', 'value': 'B'},
	            {'label': '15 - 24 Years Old', 'value': 'C'},
				{'label': '25 - 44 Years Old', 'value': 'D'},
				{'label': '44 - 64 Years Old', 'value': 'E'},
				{'label': '65+ Years Old', 'value': 'F'}
	        	],
	        	value='D',
				style=text_style
	    	),
			html.Label('Ethnic Group', style=text_style),
			dcc.Dropdown(
				id='ethnicities',
				options=[
	            {'label': 'White', 'value': 'Wh'},
	            {'label': 'Black', 'value': 'Bl'},
	            {'label': 'Hispanic', 'value': 'Hi'},
				{'label': 'Other', 'value': 'Ot'},
				],
	        	value='Wh',
				style=text_style
	    	),
			html.Label('Age Group', style=text_style),
			dcc.Dropdown(
				id='cods',
				options=[
	            {'label': 'Birth Complication', 'value': 'Comp'},
	            {'label': 'Birth Defect', 'value': 'BirthDef'},
				{'label': 'Injury', 'value': 'Injury'},
	            {'label': 'Suicide', 'value': 'Suicide'},
	            {'label': 'Cancer', 'value': 'Cancer'},
				{'label': 'Homicide', 'value': 'Homicide'},
				{'label': 'Heart Diseases', 'value': 'HeartDis'},
				{'label': 'HIV', 'value': 'HIV'}
	        	],
	        	value='Homicide',
				style=text_style
	    	)], style={'columnCount': 3}),

		dcc.Graph(id='choropleth')
		])

@app.callback(Output('choropleth', 'figure'),
 			 [Input('ages', 'value'),
			  Input('ethnicities', 'value'),
			  Input('cods', 'value')])
def update_graph(age, ethnicities, cods):
	"""
	This is the callback function that dynamically adjusts the choropleth by
	taking inputs from the dropdown menus, calling the Dataset class to lookup
	the appropriate column, get the data slices with FIPS and feature column.
	It then returns a choropleth figure by calling plot_choropleth.

	TODO: add logics to prevent accessing unavailable combinations of age group,
	ethnicities, and causes of death. For example, age group B, C, D, E, F, has
	no cause of death from Comp (Birth Complication) or BirthDef (Birth Defect)

	Parameters
	----------
	age: age brackets
	ethnicities: ethnicities
	cods: causes of death
	"""
	slices = cod.lookup(age, ethnicities, cods)#.dropna()
	#print(slices.head())
	tx_slices = slices[slices.FIPS.str.startswith("48")]
	return plot_choropleth(tx_slices)


if __name__ == '__main__':
    app.run_server(debug=True)
