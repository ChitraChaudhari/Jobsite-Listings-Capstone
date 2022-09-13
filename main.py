# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 11:26:38 2022

@author: chitra
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from plotly import graph_objects as go


app = dash.Dash(__name__)
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


##################### LOAD DATA FRAMES ####################

id_df = pd.read_csv('IndeedCleanedData.csv')
dice_df = pd.read_csv('DiceCleanedData.csv')
new_df = pd.read_csv('Cleaned_New_Data.csv')
old_df = pd.read_csv('Cleaned_Old_Data.csv')

###########################################################
###########################################################





##################### BUILD VISUALS ###########################

###### Indeed.com VISUALS ########

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

id_df['summary_income'] = id_df.salary_lower_range + id_df.salary_upper_range 
id_income_data = id_df[(id_df.salary_lower_range > 0) | (id_df.salary_upper_range > 0) 
                       & (id_df.summary_income != 0)]
lower_ranges = id_income_data[id_income_data['salary_upper_range'] == 0]
upper_ranges = id_income_data[id_income_data['salary_upper_range'] != 0]
id_income_data['avg_income'] = lower_ranges['salary_lower_range']
upper_ranges['avg_income'] = (upper_ranges['salary_lower_range'] + upper_ranges['salary_upper_range'])/2
id_income_data= pd.concat([lower_ranges,upper_ranges])
id_income_box = px.box(id_income_data, x="datadate", y="avg_income", color="job_type")



id_df_income_Scatter = px.box(id_income_data[((id_income_data['is_entrylevel'] != 0) & id_income_data['avg_income'] != 0)], x="experience_level", y="avg_income", points="all")


avg_income_by_state_scatter = px.scatter(id_income_data, 
                              x="state", y="avg_income",
                              color="job_type",
                              hover_name="title", size_max=15)
                              
                              
###### Dice.com VISUALS ########  

colors = px.colors.sequential.RdBu
dice_remote_job_count = go.Figure(data=[go.Pie(labels=['InPerson','Remote'], 
                                                values=dice_df['is_remote'].value_counts(), 
                                                textinfo='label+percent',
                                                pull=[0,0.1])])
dice_remote_job_count.update_traces(textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))


stateJobCount = pd.DataFrame(dice_df['state'].dropna(axis = 0)).value_counts()
stateJobCount = stateJobCount.to_frame()
stateJobCount = stateJobCount.reset_index()
stateJobCount.columns = ['state','totaljobs']
dice_job_count_map = px.choropleth(stateJobCount,locations='state', locationmode="USA-states", color='totaljobs', scope="usa", color_continuous_scale='PuRd')
dice_job_count_map.update_layout (title_text = 'Jobs count across state')


result = dice_df.groupby(['state','city']).size()
result = result.to_frame()
result = result.reset_index()
result.columns = ['state','city','job_count']
dice_jobs_across_USA = px.treemap(result, path=[px.Constant("USA"), 'state', 'city'], values='job_count')
dice_jobs_across_USA.update_traces(root_color="lightgrey")
dice_jobs_across_USA.update_layout(title_text='Treemap of Jobs available across USA', margin = dict(t=50, l=25, r=25, b=25))


mi_jobs = result.query("state == 'MI'")
dice_MI_jobs = px.treemap(mi_jobs, path=[px.Constant("Michigan"), 'city'], values='job_count')
dice_MI_jobs.update_traces(root_color="lightgrey")
dice_MI_jobs.update_layout(title_text='Jobs around Michigan on dice.com',margin = dict(t=50, l=25, r=25, b=25))


###### Total Jobs EDA VISUALS ########

remote_jobs = pd.DataFrame([['2021', old_df['is_remote'].value_counts(normalize=True)[1], 'Yes'],
                            ['2021', old_df['is_remote'].value_counts(normalize=True)[0], 'No'],
                            ['2022', new_df['is_remote'].value_counts(normalize=True)[1], 'Yes'],
                            ['2022', new_df['is_remote'].value_counts(normalize=True)[0], 'No']],
            columns=['Year','Average_Jobs','Remote'])
remote_jobs_trend = px.bar(remote_jobs,x="Year", y="Average_Jobs", color="Remote", title='Average Jobs Per Year')

df = remote_jobs.query("Remote == 'Yes'")
remote_jobs_per_year =  px.line(df, x="Year", y="Average_Jobs", markers=True)

result = new_df.skills.str.split(',',expand=True).stack().value_counts().reset_index()
result.columns = ['Word','Frequency']
result = result[0:]

top_skills = px.funnel( x=result.Frequency.values[0:10], y=result.Word.values[0:10])

#top_skills = go.Figure(go.Funnel(
#    y = result.Word.values[0:11],
#    x = result.Frequency.values[0:11],
#    textposition = "inside",
#    textinfo = "value+percent initial")
 #   )

job_distribution = px.pie( values=new_df.job_type.value_counts(), 
                          names=new_df.job_type.value_counts().index, 
                          title="Jobs available By Job Category")


################################################################
################################################################



##################### LAND VISUALS IN WEB APP #####################
app.layout = html.Div(children=[
    
    html.H1(children="Welcom To Job DashBoard !!",
           style = {
               'textAlign' : 'center',
               'color' : '#3F92B7'
               }
           ),
    
    html.H2(children="Top 10 Skills: ",
            style = {
               'textAlign' : 'left',
               'color' : '#3F92B7',
               'backgroundColor' : '#C9C7C7'
               }
            ),
    
    dcc.Graph(
        
        id='Top_skills',
        figure = top_skills
    ),
    
   
    html.H2(children="Remote Jobs Trend: ",
            style = {
               'textAlign' : 'left',
               'color' : '#3F92B7',
               'backgroundColor' : '#C9C7C7'
               }
            ),
    
    html.Div(children = "Average Remote Jobs Per Year:",
             style = {
                'textAlign' : 'left',
                'color' : '#3F92B7',
                }
            ),
    
    
    dcc.Graph(
        
        id='Remote_Jobs_Per_Year',
        figure=remote_jobs_per_year
    ),
    
    dcc.Graph(
        id='Remote_Jobs_Trend',
        figure=remote_jobs_trend 
    ),
    
    html.H2(children="Job Distribution: ",
            style = {
               'textAlign' : 'left',
               'color' : '#3F92B7',
               'backgroundColor' : '#C9C7C7'
               }
            ),
    
    html.Div(children = "Jobs By different Categotries:",
             style = {
                'textAlign' : 'left',
                'color' : '#3F92B7',
                }
            ),
    
    dcc.Graph(
        id='job_distribution',
        figure=job_distribution
    ),
    
    #### Indeed.com ####
    
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
    ),
    
    dcc.Graph(
        id='Indeed Sate Income Chart',
        figure=avg_income_by_state_scatter
    ), 
    
    dcc.Graph(
        id='Indeed Income Analysis',
        figure=id_income_box
    ), 
    
    
    dcc.Graph(
        id='Indeed Income Entry Level Analysis',
        figure=id_df_income_Scatter 
    ),
    
    ##### Dice.com ####
    html.Div(children = "Dice.com :",
            style = {
               'textAlign' : 'left',
               'color' : '#3F92B7',
               }
           ),
        
    dcc.Graph(
        id='dice_remote_count',
        figure= dice_remote_job_count
    ),
    
    dcc.Graph(
        id='job_count_map_dice',
        figure=dice_job_count_map 
    ),
    
    dcc.Graph(
        id='dice_jobs_across_USA',
        figure=dice_jobs_across_USA 
    ),
    
    dcc.Graph(
        id='dice_MI_jobs',
        figure=dice_MI_jobs 
    )
    
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
    
##############################################################
##############################################################


