# -*- coding: utf-8 -*-
"""

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
P_formating = {'textAlign' : 'middle','color' : '#3F92B7','font-size':'25px','margin':'40px'}
H1_formatting = {'textAlign' : 'center','color' : '#3F92B7','backgroundColor' : '#C9C7C7'}
H2_formating = {'textAlign' : 'left','color' : '#3F92B7','font-size' : '30px'}
Hr_small = {'color' : '#3F92B7','border-top' : '15px solid #C9C7C7'}
Hr_Large = {'color' : '#3F92B7','border-top' : '35px solid #C9C7C7'}




app.layout = html.Div(children=[
    
    html.H1(children="Welcom To Job DashBoard !!",
           style = H1_formatting
           ),
    
    
    html.Label(['Choose column:'],style={'font-weight': 'bold', "text-align": "center"}),
    
    dcc.Dropdown(id = 'my_dropdown',
                 options = ['indeed','dice','simplyhired'],
                 optionHeight=35,                    #height/space between dropdown options
                 value='Borough',                    #dropdown value selected automatically when page loads
                 disabled=False,                     #disable dropdown value selection
                 multi=False,                        #allow multiple dropdown values to be selected
                 searchable=True,                    #allow user-searching of dropdown values
                 search_value='',                    #remembers the value searched in dropdown
                 placeholder='Please select...',     #gray, default text shown when no option is selected
                 clearable=True,                     #allow user to removes the selected value
                 style={'width':"100%"},             #use dictionary to define CSS styles of your dropdown
                 # className='select_box',           #activate separate CSS document in assets folder
                 # persistence=True,                 #remembers dropdown value. Used with persistence_type
                 # persistence_type='memory'         #remembers dropdown value selected until...
            ),                                  #'memory': browser tab is refreshed
                                                #'session': browser tab is closed
                                                #'local': browser cookies are deleted
                
    
    #### Indeed.com ####
    
    html.H1(children="Indeed.com Analysis: ",
            style = Hr_Large
            ),
    
    
    dcc.Graph(
        id='job_count_map_indeed',
        figure=indeed_job_count_map 
    ),
    
    
    html.Hr(
        style = Hr_Large
    ),
    
    html.Div(id = 'IncomeIncomeAnalysisResults', children=[
    
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
            
            html.H1('Indeed.com: Income Analysis',
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
                        
            html.H2('Section Title Place Holder',
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
    
    
    
           html.H2('Section Title Place Holder',
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
            
            ]),
    
    html.Hr(
        style = Hr_Large
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
    ),
    
    ############ Total jobs trend ##################
    
    html.H2(children="Top 10 Skills: ",
            style = H2_formating
            ),
    
    dcc.Graph(
        
        id='Top_skills',
        figure = top_skills
    ),
    
   
    html.H2(children="Remote Jobs Trend: ",
            style = H2_formating
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
            style = H2_formating
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
    )
    
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
    
##############################################################
##############################################################

