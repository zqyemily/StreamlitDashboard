import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import time
# from streamlit_date_picker import date_range_picker, date_picker, PickerType
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
import subprocess


# Page config
# st.set_page_config(page_title='The Usage Dashboard of Pico Queue for Pico X', layout='wide'/)
st.title('📑 The Usage Dashboard of Pico Queue for Pico X')
st.markdown(f'you are log in at {datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%A, %B %d, %Y")}')
def update_data():
    subprocess.run(["C:/Users/qiany/anaconda3/envs/stenv/python.exe", "data_downloader.py"])
    df = pd.read_csv('data/Pico_X_claim_data.csv', encoding='utf-8', sep = "|")
    st.session_state['last_update'] = df.Date.max()
    st.write('The data has been updated to {}'.format(st.session_state['last_update']))

st.button('🚀 Update the latest data', on_click=update_data)

df = pd.read_csv('data/Pico_X_claim_data.csv', encoding='utf-8', sep = "|")
st.sidebar.title('Filters')
people = st.sidebar.multiselect('Select member', df['Analyst Name'].unique(), default=df['Analyst Name'].unique())

# def find_monday_date():
#     today = datetime.date.today()
#     days_ahead = (today.weekday() - 0) % 7
#     monday_date = today - datetime.timedelta(days=days_ahead)    
#     return monday_date



filtered_df = df[df['Analyst Name'].isin(people)]
st.write(filtered_df)


