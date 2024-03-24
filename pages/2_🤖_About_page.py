import streamlit as st
import pandas as pd
from st_pages import Page, show_pages, add_page_title


st.set_page_config(page_icon=':soccer:', layout="centered")
st.title('About the Project')

###sidebar section

st.sidebar.subheader('''''')

st.sidebar.info('''Hey! Want to connect? |  [**LinkedIn**](https://www.linkedin.com/in/christian-wl-gentry/)
                | [**Twitter**](https://twitter.com/_chocolatejuice?s=11)''')
#########################

col1, col2 = st.columns(2)

with col1:
    st.image('/Users/christiangentry/Documents/Data_projects/fcc_project/garyvsmls/IMG_0050.JPG', caption='Meeting my FCC hero, Emmanuel Ledesma')

with col2:
    st.write('''I went to my first FCC game in 2017, during the last visit from the Rochester Rhinos.
             That year is rich in history for long time fans of the club, and
             feeling pure energy and connection with the team made my dreams
             of supporting my local team a reality.''')
                                  
    st.write('''Through the ups and downs, this club
             has and will always be a part of me.
             I felt the passion to blend my love for the club 
         with my ambitions in working with data.''')
    st.write('''Cincy 'til I die!''')
    st.write('''[View the Github repository here](https://github.com/chrisbw3/GaryvsMLS). Stats are compiled from
        [:orange[fbref.com]](https://fbref.com/en/).''')