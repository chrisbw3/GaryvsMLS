import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import requests
from PIL import Image
from io import BytesIO
import plotly.express as px

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
st.set_page_config(page_icon=':soccer:', layout="centered")
st.title('Gary vs MLS: FC Cincinnati in Numbers :soccer:')
st.markdown('''As a long time fan of FCC I felt the passion to blend my love for the club 
         with my ambitions working with data. Stats are compiled from
        [:orange[fbref.com]](https://fbref.com/en/). ''')

##load data and create dataframes
df1 = pd.read_excel("/Users/christiangentry/Documents/Data_projects/fcc_project/garyvsmls/season23/season_stats_all_teams23.xlsx")
df2 = pd.read_excel("/Users/christiangentry/Documents/Data_projects/fcc_project/garyvsmls/season23/individual_gsc23.xlsx")
df3 = pd.read_excel("/Users/christiangentry/Documents/Data_projects/fcc_project/garyvsmls/season23/goalkeeper_stats23.xlsx")
df4 = pd.read_excel("/Users/christiangentry/Documents/Data_projects/fcc_project/garyvsmls/season23/individual_player_stats_misc23.xlsx")


df2.drop(columns=['Nation', '90s', 'SCA', 'TO', 'Sh', 'Fld', 'Def', 'GCA','PassLive', 'PassDead', 'Age',
                  'PassLive.1', 'PassDead.1', 'TO.1', 'Sh.1', 'Fld.1', 'Def.1'], axis=1, inplace=True)
df3.drop(columns=['Nation'], axis=1, inplace=True)

df4.drop(columns=['Age', 'Starts', 'Min', '90s', 'Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt', 'CrdY', 'CrdR', 'xG', 'npxG', 'xAG', 'npxG+xAG', 'PrgC', 'PrgP', 'PrgR', 'Gls', 'Ast', 'G+A', 'G-PK', 'G+A-PK', 'xG', 'xAG', 'xG+xAG', 'npxG', 'npxG+xAG'], axis=1, inplace=True)

###sidebar section
st.sidebar.header('Parameters')
selected_year = st.sidebar.selectbox('Season (more seasons coming soon)',options=df2["Season"].unique(),index=0)

st.sidebar.info('''Hey! Want to connect? |  [**LinkedIn**](https://www.linkedin.com/in/christian-wl-gentry/)
                  ''')


st.subheader('Overall Team Stats')

st.dataframe(df1)
#########################################################

st.subheader('Overall Player Stats')

col1, col2, col3 = st.columns(3)  # Adjusted to remove the fourth column

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

combined_df_selected = combined_df[['Player', 'Team', 'Position', 'SCA90', 'GCA90', 'Season']] 
matches_played_selected = df4[['Player', 'MP']]  

combined_df = pd.merge(combined_df_selected, matches_played_selected, on='Player', how='left')

selected_metric = st.selectbox("Select Metric:", ['GCA90', 'SCA90'])



fig = px.scatter(combined_df, x='MP', y=selected_metric, color='Team', hover_data=['Player', 'Position'])
fig.update_traces(marker=dict(size=12,
                               line=dict(width=2,
                                         color='Coral')),
                  selector=dict(mode='markers'))

st.plotly_chart(fig)

st.dataframe(combined_df)

st.subheader('Overall Goalkeeper Stats')
st.dataframe(df3)
