import streamlit as st
import pandas as pd
import numpy as np
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
import re
import subprocess

# Page config
st.set_page_config(page_title='The Usage Dashboard of Pico Queue for Pico X', layout='wide')

def update_data():
    subprocess.run(["python", "data_downloader.py"])
    temp = pd.read_csv('data/Pico_X_claim_data.csv', encoding='utf-8', sep = "|")
    print(temp.Date.max())
    
st.button('Just do it!', on_click=update_data)


