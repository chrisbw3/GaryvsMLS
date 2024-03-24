import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import requests
from PIL import Image
from io import BytesIO
import plotly.express as px
from st_pages import Page, show_pages, add_page_title

squad_logos = {
    'FC Cincinnati': 'https://images.mlssoccer.com/image/upload/t_q-best/v1620997960/assets/logos/CIN-Logo-480px.png',
    'Orlando City': 'https://images.mlssoccer.com/image/upload/t_q-best/v1614970757/assets/logos/6900-orlando-logo_tfcjmq.png',
    'Columbus Crew': 'https://images.mlssoccer.com/image/upload/v1623700105/assets/clb/logos/Crew_Crest_White_etrj73.png',
    'Philadelphia Union': 'https://images.mlssoccer.com/image/upload/w_128,h_128,c_pad/f_png/v1614970756/assets/logos/5513-philadelphia-logo_ea33hb.png',
    'New England Revolution': 'https://images.mlssoccer.com/image/upload/v1695757301/assets/ner/logos/NE_Logo_seal_480x480.png',
    'Atlanta United': 'https://images.mlssoccer.com/image/upload/w_128,h_128,c_pad/f_png/v1620997957/assets/logos/ATL-Logo-480px.png',
    'Nashville SC': 'https://images.mlssoccer.com/image/upload/w_128,h_128,c_pad/f_png/v1614970761/assets/logos/15154-nashville-logo_ldatso.png',
    'New York Red Bulls': 'https://images.mlssoccer.com/image/upload/w_128,h_128,c_pad/f_png/v1614970744/assets/logos/399-ny-red-bulls-logo_o6xw9r.png',
    'Charlotte FC' : 'https://images.mlssoccer.com/image/upload/w_128,h_128,c_pad/f_png/v1634242594/assets/logos/CLT_Logo_480x480v2.png',
    'CF Montréal' : 'https://images.mlssoccer.com/image/upload/w_128,h_128,c_pad/f_png/v1668018026/assets/mtl/logos/Montreal-Primary-480x480.png',
    'New York City FC' : 'https://images.mlssoccer.com/image/upload/w_128,h_128,c_pad/f_png/v1709593596/assets/logos/Primary-Club-Logo-480x480-cqrlan.png',
    'D.C. United' : 'https://images.mlssoccer.com/image/upload/w_128,h_128,c_pad/f_png/v1614970749/assets/logos/1326-dc-united-logo_pwc97q.png',
    'Chicago Fire' : 'https://images.mlssoccer.com/image/upload/w_128,h_128,c_pad/f_png/v1633358356/assets/logos/CHI_Logo_480x480-2021-v2.png',
    'Inter Miami' : 'https://images.mlssoccer.com/image/upload/w_128,h_128,c_pad/f_png/v1614970761/assets/logos/14880-miami-logo_m0n453.png',
    'Toronto FC': 'https://images.mlssoccer.com/image/upload/w_128,h_128,c_pad/f_png/v1614970755/assets/logos/2077-toronto-fc-logo_gx1gtb.png'
}

###initial config
st.set_page_config(page_icon=':soccer:', layout="wide")
st.title('Gary vs MLS: FC Cincinnati in Numbers :soccer:')
st.markdown(''' ''')


show_pages(
    [
        Page("1_🏠_Home.py", "Home", "🏠"),
        Page("pages/2_🤖_About_page.py", "About", "🤖"),
    ]
)

##load data and create dataframes
df1 = pd.read_excel("season_stats_all_teams23.xlsx")
df2 = pd.read_excel("individual_gsc23.xlsx")
df3 = pd.read_excel("goalkeeper_stats23.xlsx")
df4 = pd.read_excel("individual_player_stats_misc23.xlsx")


df2.drop(columns=['Nation', '90s', 'TO', 'Sh', 'Fld', 'Def', 'PassLive', 'PassDead', 'Age',
                  'PassLive.1', 'PassDead.1', 'TO.1', 'Sh.1', 'Fld.1', 'Def.1'], axis=1, inplace=True)
df3.drop(columns=['Nation'], axis=1, inplace=True)

df4.drop(columns=['Age', 'Starts', '90s', 'Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt', 'CrdY', 'CrdR', 'xG', 'npxG', 'xAG', 'npxG+xAG', 'PrgC', 'PrgP', 'PrgR', 'Gls', 'Ast', 'G+A', 'G-PK', 'G+A-PK', 'xG', 'xAG', 'xG+xAG', 'npxG', 'npxG+xAG'], axis=1, inplace=True)

df2['GCA'] = pd.to_numeric(df2['GCA'])
df2['SCA'] = pd.to_numeric(df2['SCA'])

###sidebar section
st.sidebar.write(''':orange[Note: Viewing the current season may not yield best results, as some 
                 stats have not been entered into the database or are missing.]
                 ''')
selected_season_df1 = st.sidebar.selectbox('Season (more seasons coming soon)',options=df1["Season"].unique(),index=0)

st.sidebar.subheader('''''')

st.sidebar.info('''Hey! Want to connect? |  [**LinkedIn**](https://www.linkedin.com/in/christian-wl-gentry/)
                | [**Twitter**](https://twitter.com/_chocolatejuice?s=11)''')
#########################


st.subheader('Overall Team Stats')

st.write('''Compare season-by-season how FCC stacks up with the rest of the east in goals/xg. Use the season selector on the sidebar.''')

filtered_df1_season = df1[df1['Season'] == selected_season_df1]

fig2 = px.bar(filtered_df1_season, x='Squad', y='Gls')
fig2.update_layout(title_text='Goals vs xG by Club', title_x=0.43)

line_trace = px.line(filtered_df1_season, x='Squad', y='xG').data[0]
line_trace.line.color = 'red'

fig2.add_trace(line_trace)


fig2.data[1].name = 'xG'


fig2.update_layout(xaxis_title='', yaxis_title='', legend_title='Metric')


st.plotly_chart(fig2, use_container_width=True)

st.dataframe(filtered_df1_season, hide_index=True)

def convert_df(filtered_df1_season):
   return filtered_df1_season.to_csv(index=False).encode('utf-8')


csv = convert_df(filtered_df1_season)

st.download_button(
   "Download CSV",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)
#########################################################

st.subheader('Overall Player Stats')

st.write('''Compare other Eastern Conference teams against the Orange and Blue with two insightful mertrics: 
         **shot & goal creating actions per 90 minutes**. You can also filter by positions, and
         see if they are above/below the mean.''')


col1, col2, col3 = st.columns(3) 

with col1:
    selected_team_1 = st.selectbox("Home Team (Up the Garys!):", options=[df2["Team"].iloc[0]], index=0)

with col2:
    selected_team_2 = st.selectbox("Opponent:", options=df2["Team"].unique(), index=2)

    filtered_df2_team_1 = df2[df2['Team'] == selected_team_1]
    filtered_df2_team_2 = df2[df2['Team'] == selected_team_2]
    
    all_positions_team_1 = filtered_df2_team_1["Position"].unique().tolist()
    all_positions_team_2 = filtered_df2_team_2["Position"].unique().tolist()
with col3:
    selected_position = st.multiselect("Positions:", options=list(set(all_positions_team_1) | set(all_positions_team_2)), default=all_positions_team_1)

if not isinstance(selected_position, list):
    selected_position = [selected_position]

df2_selection_team_1 = filtered_df2_team_1[(filtered_df2_team_1['Position'].isin(selected_position))]
df2_selection_team_2 = filtered_df2_team_2[(filtered_df2_team_2['Position'].isin(selected_position))]

combined_df = pd.concat([df2_selection_team_1, df2_selection_team_2])

combined_df_selected = combined_df[['Player', 'Team', 'Position', 'SCA', 'SCA90', 'GCA', 'GCA90', 'Season']] 
matches_played_selected = df4[['Player', 'Min']]  

combined_df = pd.merge(combined_df_selected, matches_played_selected, on='Player', how='left')

col1, col2 = st.columns(2)
with col1:
    st.write('**What is GCA and SCA?**')
    st.write('''Per [:orange[fbref.com]](https://fbref.com/en/), goal/shot creating actions
              are two offensive actions directly leading to goals/shots, such as: passes, 
             take-ons, and drawing fouls. Size of markers is based on how many total goal/
             shot creating actions each player had for the entire selected season.''')
with col2:
    selected_metric = st.selectbox("Select Metric:", ['GCA90', 'SCA90'])

filtered_df2_season = combined_df[combined_df['Season'] == selected_season_df1]

metric_to_size_column = {'GCA90': 'GCA', 'SCA90': 'SCA'}

size_column = metric_to_size_column[selected_metric]


fig = px.scatter(filtered_df2_season, x='Min', y=selected_metric, color='Team', size=size_column, hover_data=['Player', 'Position'])
fig.update_traces(marker=dict(
                               line=dict(width=2,
                                         color='Coral')),
                  selector=dict(mode='markers'))
fig.add_hline(y=combined_df[selected_metric].mean(), line_color="Red")
st.plotly_chart(fig, use_container_width=True)
st.dataframe(filtered_df2_season, hide_index=True)

def convert_df2(filtered_df2_season):
   return filtered_df2_season.to_csv(index=False).encode('utf-8')

csv = convert_df2(filtered_df2_season)

st.download_button(
   "Download CSV",
   csv,
   "file.csv",
   "text/csv",
   key='download2-csv'
)
#################################
#fig3 = px.density_heatmap(df3, x='PKatt', y='PKA', nbinsx=20, nbinsy=20, text_auto=True)

st.header('Overall Goalkeeper Stats')

filtered_df3_season = df3[df3['Season'] == selected_season_df1]


st.write('''Compare the save percentage over shots on target against, 
         where marker sizes are based on minutes played.''')
fig3 = px.scatter(filtered_df3_season, x='SoTA', y='Save%', color='Player', size='CS', hover_data=['Player', 'Team'])
fig3.add_hline(y=filtered_df3_season['Save%'].mean(), line_dash="dash", line_color="Red")
st.plotly_chart(fig3, use_container_width=True)

st.write('''***Post-shot expected goals - goals aginst*** is an intriguing look at a keeper's ability
         to stop shots based on shot-stopping probability, which includes penalty kicks
         but not penalty shootouts.''')
fig4 = px.bar(filtered_df3_season, x='Player', y='PSxG+/-', color='PSxG+/-', hover_data=['Team'])
st.plotly_chart(fig4, use_container_width=True)


st.dataframe(filtered_df3_season, hide_index=True)
def convert_df2(filtered_df3_season):
   return filtered_df3_season.to_csv(index=False).encode('utf-8')

csv = convert_df2(filtered_df3_season)

st.download_button(
   "Download CSV",
   csv,
   "file.csv",
   "text/csv",
   key='download3-csv'
)
