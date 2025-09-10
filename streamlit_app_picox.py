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


today = datetime.date.today()
days_ahead = (today.weekday() - 0) % 7
last_monday_date = today - datetime.timedelta(days=days_ahead)  - datetime.timedelta(days=7)    
last_friday_date = last_monday_date + datetime.timedelta(days=4)
# Page config

st.set_page_config(page_title='The Usage Dashboard of Pico Queue for Pico X', layout='wide')
st.image('img/pico queue logo.png', width=300)
st.title('The Usage Dashboard of Pico Queue for Pico X')
st.markdown(f'You logged in at {datetime.datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d")}')
st.markdown(f'The default data shown in this page are from last {last_monday_date.strftime("%Y-%m-%d")} to {last_friday_date.strftime("%Y-%m-%d")}')
def update_data():
    subprocess.run(["C:/Users/qiany/anaconda3/envs/stenv/python.exe", "data_downloader_picox.py"])
    df = pd.read_csv('data/Pico_X_claim_data.csv', encoding='utf-8', sep = "|")
    st.session_state['last_update'] = df.Date.max()
    st.write('The data has been updated to {}'.format(st.session_state['last_update']))

st.button('🚀 Update the latest data', on_click=update_data)


df = pd.read_csv('data/Pico_X_claim_data.csv', encoding='utf-8', sep = "|")

st.html('''
<style>
div[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div {
    max-height: 30px !important; /* Fix the height */
    overflow: auto !important;
}
</style>
''')
st.sidebar.title('Filters')
date_range = st.sidebar.date_input('Select date range', 
    value=(last_monday_date, last_friday_date),
    min_value=pd.to_datetime(df['Date'].min()),
    max_value=pd.to_datetime(df['Date'].max())
    )
BU = st.sidebar.multiselect('Select BUs', df['BU'].unique(), default=df['BU'].unique())
Category = st.sidebar.multiselect('Select Categories', df['Category'].unique(), default=df['Category'].unique())
people = st.sidebar.multiselect('Select members', df['Analyst Name'].unique(), default=df['Analyst Name'].unique())



filtered_df = df[df['Analyst Name'].isin(people)&(df['Date']>=date_range[0].strftime("%Y-%m-%d"))&(df['Date']<=date_range[1].strftime("%Y-%m-%d"))&(df['BU'].isin(BU)&df['Category'].isin(Category))]
days_selected = (date_range[1] - date_range[0]).days + 1
compare_first_date = date_range[0] - datetime.timedelta(days=days_selected)
compare_last_date = date_range[1] - datetime.timedelta(days=days_selected)
compare_df = df[df['Analyst Name'].isin(people)&(df['Date']>=compare_first_date.strftime("%Y-%m-%d"))&(df['Date']<=compare_last_date.strftime("%Y-%m-%d"))&(df['BU'].isin(BU)&df['Category'].isin(Category))]
col1, col2, col3 ,col4, col5 = st.columns(5)
col1.metric("Total Hours", f"{filtered_df['Hours'].sum():.2f} Hr",delta=f"{(filtered_df['Hours'].sum() - compare_df['Hours'].sum()):.2f} Hr")
col2.metric("Average Hours per member", f"{filtered_df['Hours'].sum()/(len(people)):.2f} Hr", delta=f"{(filtered_df['Hours'].sum()/(len(people)) - compare_df['Hours'].sum()/(len(people))):.2f} Hr")
col3.metric("Average Hours per brief", f"{filtered_df['Hours'].sum()/(filtered_df['Brief Name'].nunique()):.2f} Hr", delta=f"{(filtered_df['Hours'].sum()/(filtered_df['Brief Name'].nunique()) - compare_df['Hours'].sum()/(compare_df['Brief Name'].nunique())):.2f} Hr")
col4.metric("Average Hours per BU", f"{filtered_df['Hours'].sum()/(filtered_df['BU'].nunique()):.2f} Hr",delta=f"{(filtered_df['Hours'].sum()/(filtered_df['BU'].nunique()) - compare_df['Hours'].sum()/(compare_df['BU'].nunique())):.2f} Hr")
col5.metric("Briefs", len(filtered_df),delta=f"{(len(filtered_df) - len(compare_df))} ")

col1, col2, col3 = st.columns(3)
fig1 = px.pie(filtered_df, values='Hours', names='Category', title='Pie Chart of Hours by Category')
col1.plotly_chart(fig1, use_container_width=True)
fig2 = px.pie(filtered_df, values='Hours', names='BU', title='Pie Chart of Hours by BU')
col2.plotly_chart(fig2, use_container_width=True)
fig3 = px.bar(filtered_df.groupby(['Analyst Name'])[['Hours']].sum().reset_index(), x='Analyst Name', y='Hours', title='Bar Chart of Hours of Analysts')
col3.plotly_chart(fig3, use_container_width=True)

st.write(filtered_df)


