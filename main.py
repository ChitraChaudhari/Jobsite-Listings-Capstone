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
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io
import base64
import numpy as np
from dash import Input, Output


app = dash.Dash(__name__)
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


##################### LOAD DATA FRAMES ####################

id_df = pd.read_csv('IndeedCleanedData.csv')
dice_df = pd.read_csv('DiceCleanedData.csv')
old_dice_df = pd.read_csv('Dice_Old_Data.csv')
new_df = pd.read_csv('Cleaned_New_Data.csv')
old_df = pd.read_csv('Cleaned_Old_Data.csv')
sh_df = pd.read_csv('SimplyHiredCleanData.csv')

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
                    color_continuous_scale="PuRd"
                    ,labels= {'job_count':'Job Count','state':'State'})



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


indeed_income_map_df = id_income_data[['state','avg_income']].groupby('state').mean('avg_income')
indeed_income_map_df = indeed_income_map_df.reset_index()
indeed_income_map = px.choropleth(indeed_income_map_df,
                    locations='state',
                    locationmode="USA-states", 
                    scope="usa",
                    color='avg_income',
                    color_continuous_scale="PuRd", 
                    labels= {'avg_income':'Average Income','state':'State'})



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
dice_remote_job_count.update_traces(textfont_size=15,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
dice_remote_job_count.update_layout (title_text = 'Average Remote Jobs Sep 2022')



old_dice_remote_job_count = go.Figure(data=[go.Pie(labels=['In Person','Remote'], 
                                                values=old_dice_df['is_remote'].value_counts(), 
                                                textinfo='label+percent',
                                                pull=[0,0.1])])
old_dice_remote_job_count.update_traces(textfont_size=15,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
old_dice_remote_job_count.update_layout (title_text = 'Average Remote Jobs March 2022')

dice_remote_hist = px.histogram(dice_df, x="job_type", color="is_remote")

stateJobCount = pd.DataFrame(dice_df['state'].dropna(axis = 0)).value_counts()
stateJobCount = stateJobCount.to_frame()
stateJobCount = stateJobCount.reset_index()
stateJobCount.columns = ['state','totaljobs']
dice_job_count_map = px.choropleth(stateJobCount,locations='state', locationmode="USA-states", color='totaljobs', scope="usa", color_continuous_scale='PuRd')
dice_job_count_map.update_layout (title_text = 'Jobs count across state')


###### Total Jobs EDA VISUALS ########

remote_jobs = pd.DataFrame([['2021', old_df['is_remote'].value_counts(normalize=True)[1], 'Yes'],
                            ['2021', old_df['is_remote'].value_counts(normalize=True)[0], 'No'],
                            ['2022', new_df['is_remote'].value_counts(normalize=True)[1], 'Yes'],
                            ['2022', new_df['is_remote'].value_counts(normalize=True)[0], 'No']],
            columns=['Year','Average_Jobs','Remote'])
remote_jobs_trend = px.bar(remote_jobs,x="Year", y="Average_Jobs", color="Remote", title='Average Jobs Per Year')

df = remote_jobs.query("Remote == 'Yes'")
remote_jobs_per_year =  px.line(df, x="Year", y="Average_Jobs", markers=True, title='Average Remote Jobs Per Year')


result = new_df.skills.str.split(',',expand=True).stack().value_counts().reset_index()
result.columns = ['Word','Frequency']
result = result[0:]

top_skills = px.funnel( x=result.Frequency.values[0:10], y=result.Word.values[0:10])

job_distribution_avg = px.pie( values=new_df.job_type.value_counts(), 
                          names=new_df.job_type.value_counts().index, 
                          title="Jobs available By Job Category")

result = new_df.groupby(['job_type']).size()
result = result.to_frame()
result = result.reset_index()
result.columns = ['job_type','job_count']

job_distribution_count = px.treemap(result, path=[px.Constant("Title"),'job_type'], values='job_count', color='job_count')
job_distribution_count.update_layout(margin = dict(t=50, l=25, r=25, b=25))

result = new_df.groupby(['state','city']).size()
result = result.to_frame()
result = result.reset_index()
result.columns = ['state','city','job_count']
jobs_by_state = px.treemap(result, path=[px.Constant("USA"), 'state', 'city'], values='job_count')
jobs_by_state.update_traces(root_color="lightgrey")
jobs_by_state.update_layout(margin = dict(t=50, l=25, r=25, b=25))

mi_jobs = result.query("state == 'MI'")
jobs_by_MI = px.treemap(mi_jobs, path=[px.Constant("Michigan"), 'city'], values='job_count')
jobs_by_MI.update_traces(root_color="lightgrey")
jobs_by_MI.update_layout(margin = dict(t=50, l=25, r=25, b=25))

md_jobs = result.query("state == 'MD'")
jobs_by_MD = px.treemap(md_jobs, path=[px.Constant("Maryland"), 'city'], values='job_count')
jobs_by_MD.update_traces(root_color="lightgrey")
jobs_by_MD.update_layout(margin = dict(t=50, l=25, r=25, b=25))
jobs_by_MD.show()


dice_df['website'] = 'dice'
id_df['website'] = 'indeed'
sh_df['website'] = 'simplyhired'
sh_result = sh_df.groupby(['website','company']).size()
sh_result = sh_result.to_frame()
sh_result = sh_result.reset_index()
sh_result.columns = ['website','company','job_count']
sh_result = sh_result.sort_values(by='job_count', ascending=False)
id_result = id_df.groupby(['website','company']).size()
id_result = id_result.to_frame()
id_result = id_result.reset_index()
id_result.columns = ['website','company','job_count']
id_result = id_result.sort_values(by='job_count', ascending=False)
dice_result = dice_df.groupby(['website','company']).size()
dice_result = dice_result.to_frame()
dice_result = dice_result.reset_index()
dice_result.columns = ['website','company','job_count']
dice_result = dice_result.sort_values(by='job_count', ascending=False)
result = pd.concat([sh_result[0:10],id_result[0:10],dice_result[0:10]], ignore_index=True)
Companies_by_website = px.sunburst(result, path=['website', 'company'], values='job_count')

############ SimplyHired Visuals ################################

sh_stateJobCount=pd.DataFrame(sh_df['state'].dropna(axis = 0)).value_counts()
sh_stateJobCount = sh_stateJobCount.to_frame()
sh_stateJobCount = sh_stateJobCount.reset_index()
sh_stateJobCount.columns = ['state','totaljobs']
sh_stateJobCount['state'] = sh_stateJobCount['state'].str.upper()
sh_stateJobCount['state'] = sh_stateJobCount['state'].str.strip()

sh_job_count_map = px.choropleth(sh_stateJobCount,locations='state', locationmode="USA-states", color='totaljobs', scope="usa", color_continuous_scale='PuRd')


wordcloud = WordCloud(width = 3000, height = 2000, colormap="Blues").generate(" ".join(sh_df.title))
buf = io.BytesIO() # in-memory files
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig(buf, format = "png", dpi=600, bbox_inches = 'tight', pad_inches = 0) # save to the above file object
data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements

sh_df['is_remote'] = np.where(sh_df['location'].str.contains('remote'),1,0)
colors = px.colors.sequential.RdBu
sh_remote_job_count = go.Figure(data=[go.Pie(labels=['InPerson','Remote'], 
                                                values=sh_df['is_remote'].value_counts(), 
                                                textinfo='label+percent',
                                                pull=[0,0.1])])
sh_remote_job_count.update_traces(textfont_size=15,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
sh_remote_job_count.update_layout (title_text = 'Average Remote Jobs')


who_is_hiring=sh_df.groupby(['company'])['title'].count()     
who_is_hiring=who_is_hiring.reset_index()
who_is_hiring=who_is_hiring.sort_values(['title'],ascending=False)
#who_is_hiring=who_is_hiring.head(15) 

#fig,a=plt.subplots(figsize=(10,6))             
sh_company_jobcount=px.bar(who_is_hiring[0:10],x="company", y="title", title='Companies Looking to Hiring')
#sns.barplot(x="company", y="title", data=who_is_hiring);    
#a.set_xticklabels(who_is_hiring['company'],rotation=90) 
#a.legend(loc='upper right')
#a.set_ylabel('Number of Jobs',fontsize=12,color='black')
#a.set_xlabel('Company Name',fontsize=12,color='black') 
#a.set_title("Companies Looking to Hiring",fontsize=16,color='black', fontweight='bold')
################################################################
################################################################



##################### LAND VISUALS IN WEB APP #####################
P_formating = {'textAlign' : 'middle','color' : '#3F92B7','font-size':'25px','margin':'40px'}
H1_formatting = {'textAlign' : 'center','color' : '#3F92B7','backgroundColor' : '#C9C7C7'}
H2_formating = {'textAlign' : 'left','color' : '#3F92B7','font-size' : '30px'}
Hr_small = {'color' : '#3F92B7','border-top' : '15px solid #C9C7C7'}
Hr_Large = {'color' : '#3F92B7','border-top' : '35px solid #C9C7C7'}




app.layout = html.Div(children=[
    
    html.H1(children="Welcom To Job DashBoard !!",
           style = H1_formatting
           ),
    ###############################################
    ############## Jobs by Title ##################
    ###############################################
    html.Hr(
        style = Hr_Large
    ),
    
    html.H2(children="Job Distribution: ",
            style = H2_formating
            ),
    
    html.P(''' Even though we are seeing different trend on different job sites, 
               when we combined all the data from different job sites we see that majority are titled Data Engineer. 
               And intrestingly almost 78% jobs are for Data Engineer and Data analyst !! '''    
               , style = P_formating),
    
    html.Div(
        dcc.Graph(
            id='job_distribution',
            figure=job_distribution_avg,
            style={'width': '800'}
        ), style={'display': 'inline-block'}),
    
    html.Div(
        dcc.Graph(
            id='job_distribution_count',
            figure=job_distribution_count,
            style={'width': '800'}
        ), style={'display': 'inline-block'}),
    
    ###############################################
    ################## Skills #####################
    ###############################################
    html.Hr(
        style = Hr_Large
    ),
                                                
    html.H1(children="Top 10 Skills: ",
            style = H2_formating
            ),
    
    dcc.Graph(
        
        id='Top_skills',
        figure = top_skills
    ),
    
    html.P('''The funnel chart shows the top 10 skills across all data from different job sites that we collected.  
               Can’t get away from those schemas and their infamous joining syntax yet! And we see that SQL being 
               top required skill here. Relational Database Management Systems (RDBMS) are key still to data discovery 
               and reporting no matter where they reside. Knowledge of terminology and familiarity with algorithms 
               remain an important part of the Data Engineers skillset. At minimum familiarity with Python’s libraries
               NumPy, SciPy, pandas, sci-kit learn and some actual experience with Notebooks (Jupyter or online cloud)
               is vital. Exploratory Data Analysis (EDA) appears again now as part of Data Engineers talents to ensure 
               ETL /ELT work mentioned earlier is successful. Data quality of the resultant data is crucial as the
               Data Engineers processes and visualizes datasets. No longer content to be tied to 
               single cloud vendors companies are opting to join the multi-cloud, instead of which cloud technology 
               to choose, many enterprises have already chosen a couple. A Data Engineer still needs to have a
               good understanding of the underlying technologies that make up cloud computing and in particular, 
               knowledge around IaaS, PaaS, and SaaS implementations. And we can see that as AWS and Azure making 
               into top-10 skills asked.'''    
               , style = P_formating),
    
    ###############################################
    ################## Salary #####################
    ###############################################
    html.Hr(
        style = Hr_Large
    ),
    
    html.Div(id = 'IncomeIncomeAnalysisResults', children=[
            
            html.H1('Income Analysis',
            style = H1_formatting),
    
            html.H2('Indeed.com: Income and Job Type by State',
                        style = H2_formating),
            
            html.P('''One major reason data careers are so attractive is the they offer great compensation. As inflation rises it is important to consider
                       what income ranges can be earned across the main disciplines of Data Analyst, Data Engineer, and Data Sceintist. Using some historical 
                       data pulled by the group we also want to compare and contrast how salaries have changed in recent months. '''    
                       , style = P_formating),
    
            dcc.Graph(
                    id='Indeed Income Analysis',
                    figure=id_income_box), 
                
            html.P('''Across the board all disciplines have seen an increase in salary from Fall of 2021 to Spring 2022. Addtionally, for both time periods 
                       Data Analyst has the lowest median salary of all disciplines listed ($75-$85k), while data engieering has the highest ($107k-$126k). 
                       Data Science on the other hand seems to be the middle ground between these two disciplines.  '''    
                       , style = P_formating),
     
            html.Hr(id='Indeed income small break 1',
                        style = Hr_small),
                        
            html.H2('Salaray and Job Type Scatter',
                    style = H2_formating),
            
                
            html.P('''Taking what we found so far, we wanted to build a tool that allowed us to visually search job listings by state 
                    and income amount to find the idea listings for our situations, and visually compare salary and job counts by state. '''    
                    , style = P_formating),

            dcc.Graph(
                    id='Indeed Income Entry Level Analysis',
                    figure=id_df_income_Scatter),
                
                
            html.P('''Interestingly it seems that the majority of listing have income below $150k which seems to be the upper end of the average
                       salary range across the board. There are also very few Analyst jobs with salaries in this range. Another point to note 
                       is that the highest paying analyst posistion is actually for a job not in the field of data. 
                       This indicates that Indeed's search engine may have some keyword search issues that could be affecting the raw data collected. '''    
                       , style = P_formating),
        
            html.Hr(id='Indeed income small break 2',
                    style = {
                    'color' : '#3F92B7',
                    'border-top' : '15px solid #C9C7C7'}),
    
    
    
           html.H2('Entry Level Income Aanlysis',
                       style = H2_formating),
    
    
           html.P('''Given that we will be looking into entry level posistions, we wanted to dive in to get a sense of what income ranges can be expected 
                      for folks that are new to this industry. To do this we searched by keyword to find all job listings that aligned with terms commonly used for entry-level jobs. '''    
                      , style = P_formating),
           
            dcc.Graph(
                    id='Indeed Sate Income Chart',
                    figure=avg_income_by_state_scatter), 
        
            
            html.P('''It seems the jobs using the key word entry-level have the lowest income of the keywords plotted, while jr and junior offer slightly higher income levels. 
                      Another keyword offering higher incomes is associate, however this may require more experience. When looking for first jobs on Indeed, it seems that junior/jr 
                      will yield higher paying job listings that those which explicitly mention "Entry Level".'''    
                      , style = P_formating),
            
            
            html.Hr(style=Hr_small),
            
            
            html.H2('Avg Income Per State',
                        style = H2_formating),
            
            html.P('''Previously in this analysis we examined how many job listings we're posted in each state. To take this one step 
                   further we wanted to see if there is any correlation between the count of jobs and the average income for each state. 
                   First, let's see how mapping the U.S. by average income compares to the map of job listing counts.'''    
                      , style = P_formating),
            
            dcc.Graph(
                    id='Indeed State Income Map',
                    figure=indeed_income_map),
            
            
            html.P('''Interestingly, despite the job count map having a handful of states which have the majority of jobs, the income 
                   map is much more evenly distributed. This is surprising considering the fact we expected that due to smaller population sizes, 
                   there would be more variance.'''    
                      , style = P_formating),
        
            ]),
    
    html.Hr(
        style = Hr_Large
    ),
    
    ###############################################
    ################# Company #####################
    ###############################################'=
                                     
    html.H1(children="Top 10 companies By Jobs: ",
         style = H2_formating
         ),
 
    dcc.Graph(     
        id='Companies_by_website',
        figure = Companies_by_website
        ),
 
    html.P(''' ADD TEXT HERE'''    
            , style = P_formating),
                                    
    
    ###############################################
    ############### Remote Jobs ###################
    ###############################################
    html.Hr(
        style = Hr_Large
    ),
    
    html.H2(children="Remote Jobs Trend: ",
            style = H2_formating
            ),
        
    html.Div(
       dcc.Graph(
           id='Remote_Jobs_Per_Year',
           figure=remote_jobs_per_year,
           style={'width': '800'}
       ), style={'display': 'inline-block'}),
    
    html.Div(
       dcc.Graph(
           id='Remote_Jobs_Trend',
           figure=remote_jobs_trend,
           style={'width': '800'}
       ), style={'display': 'inline-block'}),
   
    html.Div(
      dcc.Graph(
          id='dice_remote_count',
          figure= dice_remote_job_count,
          style={'width': '800'}
      ), style={'display': 'inline-block'}),
   
    html.Div(
      dcc.Graph(
          id='old_dice_remote_job_count',
          figure= old_dice_remote_job_count,
          style={'width': '800'}
      ), style={'display': 'inline-block'}),  
    
   html.P('''The outbreak of COVID-19 prompted many employers to shift to a remote work model for all employees 
              possible in a bid to limit the spread of the coronavirus.  Working remotely has traditionally held
              a bad reputation, but more and more companies are adopting work-from-home policies.
              Even though most of the companies started InPerson work we still see the remote work trend 
              keep on going due to felxibility it offers. From above charts we definately see the increase 
              in remote jobs between March 2022 and September 2022 by almost 13%. '''    
              , style = P_formating),
    
    html.H2('Indeed.com: Job Count and Proportion of Remote Jobs',
          style = H2_formating),

    html.P('''Over the past 3 years COVID19 has had a siginificant impact on how tech professionals live their lives. 
             In order to keep up with remote education for children and many other factors, many individuals may need to work 
             remote either part or full time. By extracting the keyword remote from the location and job title column,
             we will be able to determine the proportion of Data Analyst, 
             Data Scientist, and Data Engineer posisitons that offer the ability to work remotely.'''    
 
             , style = P_formating),

    dcc.Graph(
          id='Remote-Chart',
          figure=indeed_remote_hist),

    html.P('''57% of Data Analyst listings, and 58% of Data Engineer listings offer the ability to work remote according to the 
              Indeed.come data set. On the other hand, Data Scientist has a nearly exact 50/50 split. It is interesting to note that 
             Data Science also has a smaller number of job listings compared to the other two job titles, despite scraping the same 
             amount of raw data. This suggests that Data Science may have more specialized job titles which are not as clearly defined 
             as Analyst or Engineer.'''
             , style = P_formating),
    
    
    
    html.H2('Dice.com: Job Count and Proportion of Remote Jobs',
            style = H2_formating),
    
    dcc.Graph(
            id='Dice_Remote-Chart',
            figure=dice_remote_hist
            ),
    
    html.P(''' ADD TEXT HERE'''    
            , style = P_formating),
  
    
    ###############################################
    ############### Jobs by State #################
    ###############################################
     html.Hr(
         style = Hr_Large
     ),
                                                 
     html.H1(children="Job Distribution By States Across USA: ",
             style = H2_formating
             ),
     
    dcc.Graph(
         
         id='jobs_by_state',
         figure = jobs_by_state
     ),
     
    html.P(''' ADD TEXT HERE'''    
                , style = P_formating),
       
    
    html.Div([
        html.Label(['Choose a Website:'],style={'font-weight': 'bold'}),
        dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label': 'Indeed', 'value': 'graph1'},
                    {'label': 'Dice', 'value': 'graph2'},
                    {'label': 'SimplyHired', 'value': 'graph3'},
                    ],
                value='graph1',
                style={"width": "100%"}),
        
        html.Div(dcc.Graph(id='graph')),        
        ]),

    
    html.P(''' ADD TEXT HERE'''    
            , style = P_formating),
  
                                        
    html.H2(children="Job Distribution across Michigan: ",
            style = H2_formating
            ),
    
    dcc.Graph(
        
        id='jobs_by_MI',
        figure = jobs_by_MI
    ),
    
    html.P(''' ADD TEXT HERE'''    
               , style = P_formating),   

    html.H2(children="Job Distribution Across Maryland: ",
            style = H2_formating
            ),
    
    dcc.Graph(
        
        id='jobs_by_MD',
        figure = jobs_by_MD
    ),
    
    html.P(''' ADD TEXT HERE'''    
               , style = P_formating)  
    
])


@app.callback(
    Output('graph', 'figure'),
    [Input(component_id='dropdown', component_property='value')]
)

def select_graph(value):
    if value == 'graph1':
        fig1 = indeed_job_count_map 
        return fig1
    elif value == 'graph2':
        fig2 = dice_job_count_map 
        return fig2
    else:
        fig3 = sh_job_count_map
        return fig3

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
    
##############################################################
##############################################################


