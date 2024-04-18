import streamlit as st
import pandas as pd
from st_pages import Page, show_pages, add_page_title
import plotly.express as px



st.set_page_config(page_icon=':soccer:', layout="centered")


###sidebar section

st.sidebar.subheader('''''')

st.sidebar.info('''Hey! Want to connect? |  [**LinkedIn**](https://www.linkedin.com/in/christian-wl-gentry/)
                | [**Twitter**](https://twitter.com/_chocolatejuice?s=11)''')
#########################

df1 = pd.read_excel("season_games_all_teams23.xlsx")

df1['Season'] = pd.to_numeric(df1['Season'])
df1['GF'] = df1['GF'].astype(int)
df1['GA'] = df1['GA'].astype(int)


df2 = pd.read_excel("more_offense_stats.xlsx")


st.header("Head to Head")
st.write("Historical stats from 2021-present (last updated 4/2/24).")
col1, col2 = st.columns(2) 

with col1:
    selected_team_1 = st.selectbox("Select Team (Up the Gary's!)", options=[df1["Team"].iloc[0]], index=0)

with col2:
    selected_team_2 = st.selectbox("Opponent:", options=df1["Opponent"].unique(), index=2)


    
filtered_team_1 = df1[(df1['Team'] == selected_team_1) & (df1['Opponent'] == selected_team_2)]
filtered_team_2 = df1[(df1['Team'] == selected_team_2) & (df1['Opponent'] == selected_team_1)]

combined_teams = pd.concat([filtered_team_1, filtered_team_2])

st.subheader("Final Score Heatmap")

wins_df = combined_teams[combined_teams['Result'] == 'W']
draws_df = combined_teams[combined_teams['Result'] == 'D']
losses_df = combined_teams[combined_teams['Result'] == 'L']

num_wins = len(wins_df)
num_draws = len(draws_df)
num_losses = len(losses_df)

met1, met2, met3 = st.columns(3)
with met1:
    st.metric(label='Wins', value=num_wins)
with met2:
    st.metric(label='Draws', value=num_draws)
with met3:
    st.metric(label='Losses', value=num_losses)

heatmap = px.density_heatmap(combined_teams, x='GA', y='GF', nbinsx=8, nbinsy=8, color_continuous_scale=px.colors.diverging.Temps)
heatmap.update_yaxes(tickformat=".1f")
heatmap.update_yaxes(tickvals=filtered_team_1['GF'], ticktext=list(map(int, filtered_team_1['GF'])))
heatmap.update_xaxes(tickvals=filtered_team_1['GF'], ticktext=list(map(int, filtered_team_1['GF'])))
st.plotly_chart(heatmap, use_container_width=True)


#filtered2_team_1 = df2[(df2['Team'] == selected_team_1) | (df2['Opponent'] == selected_team_2)]
st.header("Team Success While On The Field")
st.write('''Team success +/- is goals scored minus goals allowed while each player was on the field.''')
position_select, season_select, team_select = st.columns(3)
if not df2.empty:
    
    all_positions_team = df2["Pos"].unique().tolist()

    with position_select:
        selected_position = st.multiselect("Positions", options=all_positions_team, default=["DF"])
        filtered_by_positions = df2[df2['Pos'].isin(selected_position)]
        all_seasons = filtered_by_positions["Season"].unique()

    with season_select:
        selected_season = st.selectbox("Season", options=all_seasons)
        filtered_by_season = filtered_by_positions[filtered_by_positions["Season"] == selected_season]

    with team_select:
        all_teams = filtered_by_season['Team'].unique().tolist()
        selected_teams = st.multiselect("Team(s)", options=all_teams, default=["FC Cincinnati"])
        filtered_team = filtered_by_season[filtered_by_season['Team'].isin(selected_teams)]



 
 
    scatter1 = px.scatter(filtered_team, x='Min', y='+/-', color='Team', size='PPM', hover_data='Player')

    
    st.plotly_chart(scatter1)

else:
    st.write("No data available for the selected team.")


