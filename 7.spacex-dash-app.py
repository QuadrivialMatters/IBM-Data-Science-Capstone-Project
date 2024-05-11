#on vertual cloud compluter first from the terminal run the next three commands
#python3.11 -m pip install pandas dash
#wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
#wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the spacex data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
#get sites list
site=list(set(spacex_df['Launch Site']))
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                html.P('Select a Launch Site to investigate or select \'All\''),
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options=[{'label': 'All Sites', 'value': 'ALL'},
                                    {'label': site[0], 'value': site[0]},
                                    {'label': site[1], 'value': site[1]},
                                    {'label': site[2], 'value': site[2]},
                                    {'label': site[3], 'value': site[3]},
                                    ],
                                    value='ALL',
                                    placeholder="Select a Launch Site",
                                    searchable=True
                                ),
                                #html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                # TASK 3: Add a slider to select payload range
                                html.P('Adjust the range of Payload Mass to display. The full range is displayed when \'All\' sites are selected.'),                
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0 kg', 2500: '2500 kg', 5000: '5000 kg', 7500: '7500 kg'},
                                    value=[min_payload, max_payload]
                                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):#local var: no name match to layout needed
    
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class']==1]
        data=filtered_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(data, 
            values='class', 
            names="Launch Site", 
            title='Total Successful Launches by Site'
            )
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df=spacex_df[spacex_df['Launch Site']==entered_site]
        data=filtered_df.groupby('class')['Launch Site'].count().reset_index()
        fig = px.pie(data,
            values='Launch Site', 
            names='class', 
            title='Total Sucessfull Launches for Site: {}'.format(entered_site)
            )
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload_slider_endpts):#local var: no name match to layout needed
    
    if entered_site == 'ALL':
        filtered_df = spacex_df
        data=filtered_df
        fig = px.scatter(data, 
            x='Payload Mass (kg)', 
            y='class',
            color="Booster Version Category", 
            title='Successful Launches by Payload colored by Booster version'
            )
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df=spacex_df[spacex_df['Launch Site']==entered_site]
        data=filtered_df[(filtered_df['Payload Mass (kg)']>=payload_slider_endpts[0])& 
                        (filtered_df['Payload Mass (kg)']<=payload_slider_endpts[1])
                        ]
        fig = px.scatter(data, 
            x='Payload Mass (kg)', 
            y='class',
            color="Booster Version Category", 
            title='Successful Launches at site: {} by Payload colored by Booster version'.format(entered_site)
            )
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
