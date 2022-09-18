# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                            options=[{'label': 'All Sites', 'value': 'All Sites'}] + [{'label': x, 'value':x} for x in spacex_df['Launch Site'].unique()],
                                            value='All Sites',
                                            placeholder="Select Launch Site: ",
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div([
                                    dcc.Graph(id='success-pie-chart', figure={})]),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='site-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(launch_site):
    filtered_df = spacex_df
    if launch_site == 'All Sites':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site',
        title='Total Success Launches by Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        count = spacex_df[spacex_df['Launch Site'] == launch_site]['class'].value_counts().reset_index(name='success')
        fig = px.pie(count, values='success',
        names='index', 
        title=f'Success Rate Launches in {launch_site}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
             [Input(component_id='site-slider', component_property='value'),
              Input(component_id='site-dropdown', component_property='value')])

def get_scatter_chart(slider_values, launch_site):
    min_value, max_value = slider_values
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(min_value, max_value)]
    if launch_site == 'All Sites':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
        hover_data=['Booster Version'],
        color='Booster Version Category',
        title='Correlation Between Payload and Success for all Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        selected_site = filtered_df[filtered_df['Launch Site'] == launch_site]
        fig = px.scatter(selected_site, x='Payload Mass (kg)', y='class',
        hover_data=['Booster Version'],
        color='Booster Version Category',
        title=f'Correlation Between Payload and Success in {launch_site}')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
