
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import os

app = dash.Dash(__name__)
server = app.server.ipynb

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


##################### LOAD DATA FRAMES ####################
indeed_df = pd.read_csv('IndeedCleanedData.csv')

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


indeed_remote_bar = px.bar(id_df[(id_df['datadate']== 'Spring 2022')], x="job_type", y="is_remote",
             color='job_type',
             height=400)

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
    )
   
    html.Div(children='''
        Dash: Income Chart
    '''),
    
    dcc.Graph(
        id='example-graph2',
        figure=indeed_remote_bar
    )
    
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
    
##############################################################
##############################################################
