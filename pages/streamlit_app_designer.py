import streamlit as st
import pandas as pd
import numpy as np
import datetime
import pytz
import time
from streamlit_date_picker import date_range_picker, date_picker, PickerType
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import re
import subprocess


# Page config
st.set_page_config(page_title='The Usage Dashboard of Pico Shanghai', page_icon='🎨',layout='wide')
today = datetime.date.today()
days_ahead = (today.weekday() - 0) % 7
last_monday_date = today - datetime.timedelta(days=days_ahead)  - datetime.timedelta(days=7)    
last_friday_date = last_monday_date + datetime.timedelta(days=4)



st.image('img/pico queue logo.png', width=300)
st.title('The Usage Dashboard of Pico Shanghai')
st.markdown(f'You logged in at {datetime.datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d")}')
# st.markdown(f'The default data shown in this page are from {last_monday_date.strftime("%Y-%m-%d")} to Friday {last_friday_date.strftime("%Y-%m-%d")}')
def update_data():
    subprocess.run(["C:/Users/qiany/anaconda3/envs/stenv/python.exe", "data_downloader_designers.py"])
    df_claim = pd.read_csv('data/designer_claim_data.csv', encoding='utf-8', sep = "|")
    df_Brief = pd.read_csv('data/designer_brief_data.csv', encoding='utf-8', sep = "|")
    st.session_state['last_update'] = df_Brief.BriefCreationTime.max()
    st.write('The data has been updated to {}'.format(st.session_state['last_update']))

st.button('🚀 Update the latest data', on_click=update_data)
st.sidebar.page_link("home.py", label="Home", icon="🏠")

df_claim = pd.read_csv('data/designer_claim_data.csv', encoding='utf-8', sep = "|")
df_Brief = pd.read_csv('data/designer_brief_data.csv', encoding='utf-8', sep = "|")

st.html('''
<style>
div[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div {
    max-height: 30px !important; /* Fix the height */
    overflow: auto !important;
}
</style>
''')
if pd.Timestamp(last_friday_date) > pd.Timestamp(pd.to_datetime(df_Brief['BriefCreationTime'].max())):
    last_friday_date = pd.to_datetime(df_Brief['BriefCreationTime'].max())

st.sidebar.title('Filters')
date_range = st.sidebar.date_input('Select date range', 
    value=(last_monday_date, last_friday_date),
    min_value=pd.to_datetime(df_Brief['BriefCreationTime'].min()),
    max_value=pd.to_datetime(df_Brief['BriefCreationTime'].max())
    )
ProjectStatus = st.sidebar.multiselect('Select Project Bidding Status', df_Brief['BidStatus'].unique(), default=df_Brief['BidStatus'].unique())
Team_Leader = st.sidebar.multiselect('Select Team Leaders', df_Brief['Team_Leader'].unique(), default=df_Brief['Team_Leader'].unique())
st.markdown(f'You selected date from {date_range[0].strftime("%Y-%m-%d")} to {date_range[1].strftime("%Y-%m-%d")}')
if Team_Leader == ['Max Liu']:
    Team = st.sidebar.multiselect('select Team', ['3D-B','3D-A','2D-C','Planner','CAD-Project'], default=['3D-B','3D-A','2D-C','Planner','CAD-Project'])
elif Team_Leader == ['Summer Xia']:
    Team = st.sidebar.multiselect('select Team', ['ST'], default=['ST'])
elif Team_Leader == ['大海']:
    Team = st.sidebar.multiselect('select Team', ['Hi-Studio'], default=['Hi-Studio'])
elif Team_Leader == ['Max Liu','Summer Xia']:
    Team = st.sidebar.multiselect('select Team', ['3D-B','3D-A','2D-C','Planner','CAD-Project','ST'], default=['3D-B','3D-A','2D-C','Planner','CAD-Project','ST'])
elif Team_Leader == ['Max Liu','大海']:
    Team = st.sidebar.multiselect('select Team', ['3D-B','3D-A','2D-C','Planner','CAD-Project','Hi-Studio'], default=['3D-B','3D-A','2D-C','Planner','CAD-Project','Hi-Studio'])
elif Team_Leader == ['Summer Xia','大海']:
    Team = st.sidebar.multiselect('select Team', ['ST','Hi-Studio'], default=['ST','Hi-Studio'])
elif Team_Leader == ['Max Liu','Summer Xia','大海']:
    Team = st.sidebar.multiselect('select Team', ['3D-B','3D-A','2D-C','Planner','CAD-Project','ST','Hi-Studio'], default=['3D-B','3D-A','2D-C','Planner','CAD-Project','ST','Hi-Studio'])
else:
    Team = st.sidebar.multiselect('select Team', df_Brief['TeamCode'].unique(), default=df_Brief['TeamCode'].unique())
   



filtered_df = df_Brief[df_Brief['Team_Leader'].isin(Team_Leader)&(df_Brief['TeamCode'].isin(Team))&(df_Brief['BriefCreationTime']>=date_range[0].strftime("%Y-%m-%d"))&(df_Brief['BriefCreationTime']<=date_range[1].strftime("%Y-%m-%d"))&(df_Brief['BidStatus'].isin(ProjectStatus))]
days_selected = (date_range[1] - date_range[0]).days + 1
compare_first_date = date_range[0] - datetime.timedelta(days=days_selected)
compare_last_date = date_range[1] - datetime.timedelta(days=days_selected)
compare_df = df_Brief[df_Brief['Team_Leader'].isin(Team_Leader)&(df_Brief['BriefCreationTime']>=compare_first_date.strftime("%Y-%m-%d"))&(df_Brief['BriefCreationTime']<=compare_last_date.strftime("%Y-%m-%d"))&(df_Brief['BidStatus'].isin(ProjectStatus))]
col1, col2, col3  = st.columns(3)
col1.metric("Total Briefs", f"{filtered_df['BriefID'].nunique():.2f}",delta=f"{(filtered_df['BriefID'].nunique() - compare_df['BriefID'].nunique()):.2f}")
col2.metric("Total Projects", f"{filtered_df['ProjectID'].nunique():.2f}", delta=f"{(filtered_df['ProjectID'].nunique() - compare_df['ProjectID'].nunique()):.2f}")
temp = filtered_df[['ProjectID','BidStatus','BidAmount']].drop_duplicates()
compare_temp = compare_df[['ProjectID','BidStatus','BidAmount']].drop_duplicates()
col3.metric("Total Projects Actual Receivable", f"{temp['BidAmount'].sum():,.2f} RMB",delta=f"{(temp['BidAmount'].sum() - compare_temp['BidAmount'].sum()):,.2f} RMB")

col1, col2, col3 = st.columns(3)
fig1 = px.pie(filtered_df.groupby(['BidStatus'])[['ProjectID']].nunique().reset_index(), values='ProjectID', names='BidStatus', title='Project Bidding Status')
fig1.update_layout(legend={'x':0,'y':0,'orientation':'h'}) 
col1.plotly_chart(fig1, use_container_width=True)
fig2 = px.pie(filtered_df.groupby(['ProjectNature'])[['ProjectID']].nunique().reset_index(), values='ProjectID', names='ProjectNature', title='Project Nature Distribution')
fig2.update_layout(legend={'x':0,'y':0,'orientation':'h'}) 
col2.plotly_chart(fig2, use_container_width=True)
fig3 = px.bar(filtered_df.groupby(['Team_Leader'])[['ProjectID']].nunique().reset_index(), x='Team_Leader', y='ProjectID', title='Bar Chart of Project counts by Team Leader')
col3.plotly_chart(fig3, use_container_width=True)

temp1 = filtered_df[['ProjectID','Customer','BidStatus','BidAmount']].drop_duplicates()
col1, col2 = st.columns(2)
temp1 = filtered_df.groupby(['Customer'])[['ProjectID','BidAmount']].agg({'ProjectID':'nunique','BidAmount':'sum'}).reset_index().sort_values(by='ProjectID', ascending=False).rename(columns={'ProjectID':'Project Counts'})
col1.write(temp1[['Customer', 'Project Counts']].head(10).reset_index(drop=True).style.set_caption('Top 10 Customers by Project Counts'))
col2.write(temp1[['Customer', 'BidAmount']].sort_values(by='BidAmount', ascending=False).head(10).reset_index(drop=True).style.format({'BidAmount':'{:,.2f} RMB'}).set_caption('Top 20 Customers by Project Actual Receivable Amounts'))
st.markdown('Brief Details')
st.write(filtered_df)

