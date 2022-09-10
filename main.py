import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import os

app = dash.Dash(__name__)
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


##################### LOAD DATA FRAMES ####################
id_df = pd.read_csv('IndeedCleanedData.csv')

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})


###########################################################
###########################################################





##################### BUILD VISUALS ###########################
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

df2 = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

fig2 = px.scatter(df2, x="gdp per capita", y="life expectancy",
                 size="population", color="continent", hover_name="country",
                 log_x=True, size_max=60)



new_job_count = id_df[(id_df['datadate'] == 'Spring 2022')]
new_job_count = pd.DataFrame(new_job_count['state'].dropna(axis = 0)).value_counts()
new_job_count = new_job_count.to_frame()
new_job_count.reset_index(inplace=True)
new_job_count.columns = ['state','job_count']
indeed_job_count_map = px.choropleth(new_job_count,
                    locations='state', 
                    locationmode="USA-states", 
                    scope="usa",
                    color='job_count',
                    color_continuous_scale="PuRd")



indeed_remote_hist = px.histogram(id_df[(id_df['datadate'] == 'Spring 2022')], x="job_type", color="is_remote")

################################################################
################################################################









##################### LAND VISUALS IN WEB APP #####################
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    html.Div(children='''
        Dash: Another example for chart
    '''),

    dcc.Graph(
        id='example-graph2',
        figure=fig2
    ),
   
    html.Div(children='''
        Indeed.com: 
    '''),
    
    dcc.Graph(
        id='job_count_map_indeed',
        figure=indeed_job_count_map 
    ),

    
    dcc.Graph(
        id='Remote-Chart',
        figure=indeed_remote_hist
    )
    
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
    
##############################################################
##############################################################

